# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 21:33:49 2019

@author: Trevor Ho
"""

from opentrons import labware, instruments, robot

#%%

def horiz_well_generator(first_well,length,rack_format='opentrons-tuberack-2ml-eppendorf'):
    '''Generate a list of wells given a defined first well and total number of wells across a plate or rack'''
    
    rack_formats = ['96-flat','opentrons-tuberack-2ml-eppendorf','opentrons-tuberack-2ml-screwcap']
    
    if rack_format not in rack_formats:
        raise ValueError('Invalid rack format. Expected one of: %s' % rack_formats)
    
    if rack_format == 'opentrons-tuberack-2ml-eppendorf' or rack_format == 'opentrons-tuberack-2ml-screwcap':
        last_col = 6
        col_list = ['A','B','C','D']
        
    elif rack_format == '96-flat':
        last_col = 12
        col_list = ['A','B','C','D','E','F','G','H']    
    
    # Check if init_well is within range
    if rack_format != '96-flat' and (first_well[0] in ['E','F','G','H'] or int(first_well[1:]) > 6):
        raise ValueError('First well out of range. Consider switching rack format to 96-flat')
    elif first_well[0] not in col_list or int(first_well[1:]) > last_col:
        raise ValueError('First well out of range')
    
    # Generate well list    
    well_list = [first_well]
    counter = length - 1
    last_well = first_well
    
    while counter > 0:
        
        last_well_row = last_well[0]
        last_well_col = int(last_well[1:])
        
        if last_well_col == last_col:
            next_well_col = 1
            next_well_row = chr(ord(last_well_row)+1)
            if next_well_row not in col_list:
                raise ValueError('Requested list exceeds range of rack or plate')
        else:
            next_well_row = last_well_row
            next_well_col = last_well_col + 1        
        
        next_well = next_well_row + str(next_well_col)
        last_well = next_well
        well_list.append(next_well)
                
        counter -= 1
    return well_list

def distributeNoBlowOut(pipette,vol_out,source,dests,disposal_vol):
    '''Distribute function with disposal volume but without blow out'''
    
    # Converts the list of destination wells from :WellSeries: into a list to permit .pop() function
    dests_all = list(dests.items.values())
    
    pipette_max_vol = pipette.max_volume
    
    # Full description: So long as there are wells that have not received dispensed liquid (item still in dests_all), the function will try to calculate how many dispenses can be fit into one aspiration volume (one_trans_aspir_vol), and then perform the sub-distribution step. To keep track of the wells to be dispensed, the function pops a :Well: from dests_all and then add it to the list of one_trans_dests. The function stops tracking when there is no more :Well: in the dests_all list
    
    # The function changes tip for each sub-distribution step
    
    while dests_all:
        pipette.pick_up_tip()
    
        one_trans_aspir_vol = disposal_vol
        one_trans_dests = []
        
        # Calculate the maximum distributions that one aspiration can take
        while one_trans_aspir_vol + vol_out < pipette_max_vol:
            one_trans_dests.append(dests_all.pop(0))
            one_trans_aspir_vol = one_trans_aspir_vol + vol_out
            if not dests_all: break
            
        # Performs the actual distribution sub-step
        pipette.aspirate(one_trans_aspir_vol,source)
        for dest in one_trans_dests:
            pipette.dispense(vol_out,dest)
            
        pipette.drop_tip()

#%%
#transfer_vol = 2
#
    
slots_map = {
        #'1':'96-flat',
        '1':'opentrons-tuberack-2ml-eppendorf'
        }

tip_slots = ['2']

# TODO: Provide the information of the location of diluent and stock to be diluted

active_slot = '1'
diluent_source = 'D6'
stock_source = 'A1'

target_vol = 100
fold_dilution = 4 # Note: value of 2 = 1:1 dilution, 4 = 4-fold dilution, etc.

no_dils = 12 # Note: stock is included in this number

#%% Do not re-load this part
labware_items = {}
for slot, labware_item in slots_map.items():
    labware_items.update({slot:labware.load(labware_item, slot)})

tip_racks = [labware.load('tiprack-200ul', slot) for slot in tip_slots]

pipette = instruments.P300_Single(
    mount='left',
    tip_racks=tip_racks
    )

#%%

# Generate well lists according to requirement
well_list = horiz_well_generator(stock_source,no_dils,slots_map[active_slot])
diluent_dest_list = well_list[1:]
serial_source_list = well_list[:-1]

# Calculate volumes to dispense and mix

mix_vol = int(target_vol * 0.75)
sample_vol = int(target_vol / fold_dilution)
diluent_vol = target_vol - sample_vol

#%%

# Distribute the diluent across the eppendorf tubes
distributeNoBlowOut(pipette,
                    diluent_vol,
                    labware_items[active_slot].wells(diluent_source),
                    labware_items[active_slot].wells(diluent_dest_list),
                    disposal_vol=5)

# Perform the serial transfer and mixing
for i in range(0,len(serial_source_list)):
    last_well = serial_source_list[i]
    next_well = diluent_dest_list[i]

    pipette.transfer(
    	sample_vol,
    	labware_items[active_slot].wells(last_well),
    	labware_items[active_slot].wells(next_well),
    	mix_after=(3, mix_vol),
        new_tip='always',
        blow_out=True
        )
    
for c in robot.commands():
    print(c)

robot.clear_commands()
#robot.reset()