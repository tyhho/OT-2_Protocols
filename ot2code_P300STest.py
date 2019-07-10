# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 18:58:58 2019

@author: s1635543
"""

from opentrons import labware, instruments


#%%
def distributeNoBlowOut(pipette,vol_out,source,dests,disposal_vol=0,hover_over=-1):
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
                if hover_over >=0:
                    pipette.dispense(vol_out,dest.top(hover_over))
                else:
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
                if hover_over >=0:
                    pipette.transfer(
                    	vol,
                    	source,
                    	dest.top(hover_over),
                        new_tip='never',
                        blow_out=True
                        )
                else:
                    pipette.transfer(
                    	vol,
                    	source,
                    	dest,
                        new_tip='never',
                        blow_out=True
                        )
            pipette.drop_tip()

def distributeMixedInducer(pipette,mix_vol,vol,num_assay_plates,airgap_vol,source,dests):
    
    total_asp_vol = num_assay_plates * (airgap_vol + vol)
    
    if total_asp_vol >= pipette.max_volume:
        raise ValueError('Vol too large to handle in one aspiration')

    pipette.pick_up_tip()
    
    for x in range(3):
        pipette.aspirate(mix_vol,source)
        pipette.dispense(mix_vol,source)
        
    pipette.blow_out(source.top())

    pipette.air_gap(airgap_vol/2)
    for i in range(num_assay_plates):
        pipette.aspirate(vol,source)
        if i != num_assay_plates:
            pipette.air_gap(airgap_vol)
        else:
            pipette.air_gap(airgap_vol/2)
    
    dispense_vol = vol + airgap_vol
    for dest in dests:    
        pipette.dispense(dispense_vol,dest)
    pipette.drop_tip()

def calculateDispenseVol(vol,num_assay_plates):
    return vol * (num_assay_plates + 1)



#%%

tip_slots = ['1']

tip_racks = [labware.load('tiprack-200ul', slot) for slot in tip_slots]


slots_map = {
        #'1':'96-flat',
        '2':'opentrons-tuberack-2ml-eppendorf'
        }


labware_items = {}
for slot, labware_item in slots_map.items():
    labware_items.update({slot:labware.load(labware_item, slot)})

#dest_plate = labware.load('96-flat', slot='4')

p300s = instruments.P300_Single(
    mount='left',
    tip_racks=tip_racks
    )


p10s = instruments.P10_Single(
    mount='right',
    tip_racks=tip_racks
    )
#
#diluent_vol = 375
#
#distributeNoBlowOut(pipette,
#                    diluent_vol,
#                    labware_items['2'].wells('A6'),
#                    labware_items['2'].wells('A1','A2'),
#                    hover_over = 1
#                    )


p10s.transfer(6.7,
               labware_items['2'].wells('A6'),
               labware_items['2'].wells('A1'),
               blow_out = True,
               new_tip = 'always'
              )