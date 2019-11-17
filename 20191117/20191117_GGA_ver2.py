# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 19:49:44 2019

@author: Trevor Ho
"""
from opentrons import labware, instruments, robot

#%% Copy & Paste Arena

slots_map = {
        '1':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
        '2':'biorad_96_wellplate_200ul_pcr',
        '3':'biorad_96_wellplate_200ul_pcr',
        }

tip_slots_10uL = ['4','5']
tip_racks_10uL = [labware.load('opentrons_96_tiprack_10ul', slot) for slot in tip_slots_10uL]

tip_slots_300uL = ['6']
tip_racks_300uL = [labware.load('opentrons_96_tiprack_300ul', slot) for slot in tip_slots_300uL]



# TODO: modify dest_rows according to the group
all_dest_wells = []
dest_cols = ['1','2','3']
dest_rows = [
        'A',
        'B',
        'C',
        'D',
        'E',
        'F',
        'G',
        'H'
        ]
for row in dest_rows:
    for col in dest_cols:
        well = row + col
        all_dest_wells.append(well)


# TODO: modify inst_list according to the group
inst_list = [
        
        # Group 1
        '1$2_B1->3_A1',
        '1$2_A1->3_A1',
        '1$2_A3->3_A1',
        '1$2_B2->3_A2',
        '1$2_A1->3_A2',
        '1$2_B5->3_A2',
        '1$2_D1->3_A3',
        '1$2_A1->3_A3',
        '1$2_A3->3_A3',
        
        # Group 2
        '1$2_B1->3_B1',
        '1$2_B3->3_B1',
        '1$2_B5->3_B1',
        '1$2_B2->3_B2',
        '1$2_B3->3_B2',
        '1$2_B5->3_B2',
        '1$2_B1->3_B3',
        '1$2_B3->3_B3',
        '1$2_A3->3_B3',
        
        # Group 3
        '1$2_B1->3_C1',
        '1$2_C1->3_C1',
        '1$2_A3->3_C1',
        '1$2_B2->3_C2',
        '1$2_C1->3_C2',
        '1$2_A3->3_C2',
        '1$2_F1->3_C3',
        '1$2_C1->3_C3',
        '1$2_F4->3_C3',
        
        # Group 4
        '1$2_D1->3_D1',
        '1$2_D3->3_D1',
        '1$2_A3->3_D1',
        '1$2_D2->3_D2',
        '1$2_D3->3_D2',
        '1$2_D5->3_D2',
        '1$2_E2->3_D3',
        '1$2_D3->3_D3',
        '1$2_E5->3_D3',
        
        # Group 5
        '1$2_E1->3_E1',
        '1$2_E3->3_E1',
        '1$2_G1->3_E1',
        '1$2_E2->3_E2',
        '1$2_E3->3_E2',
        '1$2_E5->3_E2',
        '1$2_B1->3_E3',
        '1$2_E3->3_E3',
        '1$2_E5->3_E3',
        
        # Group 6
        '1$2_F1->3_F1',
        '1$2_F2->3_F1',
        '1$2_F4->3_F1',
        '1$2_E2->3_F2',
        '1$2_F2->3_F2',
        '1$2_E5->3_F2',
        '1$2_E1->3_F3',
        '1$2_F2->3_F3',
        '1$2_G1->3_F3',
        
        # Group 7
        '1$2_B1->3_G1',
        '1$2_F2->3_G1',
        '1$2_G1->3_G1',
        '1$2_D2->3_G2',
        '1$2_F2->3_G2',
        '1$2_D5->3_G2',
        '1$2_E1->3_G3',
        '1$2_B3->3_G3',
        '1$2_G1->3_G3',
        
        # Group 8
        '1$2_D2->3_H1',
        '1$2_B3->3_H1',
        '1$2_D5->3_H1',
        '1$2_F1->3_H2',
        '1$2_B3->3_H2',
        '1$2_F4->3_H2',
        '1$2_B1->3_H3',
        '1$2_F2->3_H3',
        '1$2_E5->3_H3'
            ]

#%% Set up labware and pipettes

deck_labware = {}
for slot, labware_item in slots_map.items():
    deck_labware.update({slot:labware.load(labware_item, slot)})

p10s = instruments.P10_Single(
    mount='left',
    tip_racks=tip_racks_10uL
    )

p300s = instruments.P300_Single(
    mount='right',
    tip_racks=tip_racks_300uL
    )

#%% Distribute water to the wells

# TODO: Modify according to group
p300s.pick_up_tip()
p300s.distribute(
        7,
        deck_labware['1'].wells('A1'),
        deck_labware['3'].wells(all_dest_wells),
        new_tip='never'
        )
p300s.drop_tip()

#%% Carry out combinatorial pipetting
for inst in inst_list:
    transfer_vol = int(inst.split('$')[0])
    source, dest = inst.split('$')[1].split('->')
    source_slot, source_well = source.split('_')
    dest_slot, dest_well = dest.split('_')
    
    p10s.transfer(
	transfer_vol,
	deck_labware[source_slot].wells(source_well),
	deck_labware[dest_slot].wells(dest_well),
	new_tip='always',
    blow_out=True)
    #robot.pause()
    
#%%
cmd_list = robot.commands()
for c in cmd_list:
    print(c)