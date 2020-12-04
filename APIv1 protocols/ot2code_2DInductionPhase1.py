# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 22:25:38 2019

@author: Trevor Ho
"""

from opentrons import labware, instruments, robot

#%% 

def distributeNoBlowOut(pipette,vol_out,source,dests,disposal_vol):
    '''Distribute function with disposal volume but without blow out'''
    
    # Converts the list of destination wells from :WellSeries: into a list to permit .pop() function
    dests_all = list(dests.items.values())
    
    pipette_max_vol = pipette.max_volume
    
    if (vol_out *2 + disposal_vol) <= pipette_max_vol:
    
    # Mode 1: 
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

    # Mode 2: 
    else:
        for dest in dests_all:    
            pipette.pick_up_tip()

            if vol_out > pipette_max_vol:
                vol_list = []
                vol_remaining = vol_out
                while vol_remaining > pipette_max_vol:
                    vol_list.append(pipette_max_vol)
                    vol_remaining -= pipette_max_vol
                vol_list.append(vol_remaining)
                
            else:
                vol_list = [vol_out]
                
            for vol in vol_list:
                pipette.transfer(
            	vol,
            	source,
            	dest,
                new_tip='never',
                blow_out=True
                )
            pipette.drop_tip()

#%% 

# Plate tracking
        # Plate 10, 11 = inducer aliquot plates
        # Tip slot = 1
        # Rack 2 = inducer to place
        


slots_map = {
        #'1':'96-flat',
        '2':'opentrons-tuberack-2ml-eppendorf',
        '10':'96-flat',
        '11':'96-flat'
        }

inducer_rack = '2'

inducer_y_map = {
        'A1':'H1',
        'A2':'G1',
        'A3':'F1',
        'A4':'E1',
        'A5':'D1',
        'A6':'C1',
        'B1':'B1',
        'B2':'A1'
        }

inducer_x_map = {'C1':'1',
                 'C2':'2',
                 'C3':'3',
                 'C4':'4',
                 'C5':'5',
                 'C6':'6',
                 'D1':'7',
                 'D2':'8',
                 'D3':'9',
                 'D4':'10',
                 'D5':'11',
                 'D6':'12'}

iap_y = '10'
iap_x = '11'

tip_slots = ['1']
tip_racks = [labware.load('tiprack-200ul', slot) for slot in tip_slots]

num_assay_plates = 3
inducer_x_vol = 2
inducer_x_disposal_vol = 1
iplate_x_dead_vol = 6

inducer_y_vol = 2
iplate_y_dead_vol = 6

labware_items = {}
for slot, labware_item in slots_map.items():
    labware_items.update({slot:labware.load(labware_item, slot)})

pipette = instruments.P300_Single(
    mount='left',
    tip_racks=tip_racks
    )

#%% Stage 1: Distribute y axis gradient

# total vol of y axis inducer needed for each well in aliquot plate
iy_total = inducer_y_vol * 12 * num_assay_plates + iplate_y_dead_vol

# Distribute the inducer for y axis
for source_well, dest_well in inducer_y_map.items():
    pipette.transfer(
        	iy_total,
        	labware_items[inducer_rack].wells(source_well),
        	labware_items[iap_y].wells(dest_well),
            new_tip='always',
            blow_out=True
            )

#%% Stage 2: Distribtue x axis gradient
    
ix_total = inducer_x_vol * num_assay_plates + iplate_x_dead_vol

for source_well, dest_col in inducer_x_map.items():
    distributeNoBlowOut(pipette,
                        ix_total,
                        labware_items[inducer_rack].wells(source_well),
                        labware_items[iap_x].cols(dest_col),
                        disposal_vol=3)
#
#for c in robot.commands():
#    print(c)
#
#robot.clear_commands()