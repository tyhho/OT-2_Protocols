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

tip_slots = ['4','5']
tip_racks = [labware.load('opentrons_96_tiprack_10ul', slot) for slot in tip_slots]

inst_list = [

# Group 1
'11$1_A1->3_A1',
'2$1_A2->3_A1',
'1$2_H12->3_A1',
'1$2_B1->3_A1',
'1$2_A1->3_A1',
'1$2_B4->3_A1',
'1$2_A3->3_A1',
'11$1_A1->3_A2',
'2$1_A2->3_A2',
'1$2_H12->3_A2',
'1$2_B2->3_A2',
'1$2_A1->3_A2',
'1$2_B4->3_A2',
'1$2_B5->3_A2',
'11$1_A1->3_A3',
'2$1_A2->3_A3',
'1$2_H12->3_A3',
'1$2_D1->3_A3',
'1$2_A1->3_A3',
'1$2_B4->3_A3',
'1$2_A3->3_A3',

# Group 2
'11$1_A1->3_B1',
'2$1_A2->3_B1',
'1$2_H12->3_B1',
'1$2_B1->3_B1',
'1$2_B3->3_B1',
'1$2_B4->3_B1',
'1$2_B5->3_B1',
'11$1_A1->3_B2',
'2$1_A2->3_B2',
'1$2_H12->3_B2',
'1$2_B2->3_B2',
'1$2_B3->3_B2',
'1$2_B4->3_B2',
'1$2_B5->3_B2',
'11$1_A1->3_B3',
'2$1_A2->3_B3',
'1$2_H12->3_B3',
'1$2_B1->3_B3',
'1$2_B3->3_B3',
'1$2_B4->3_B3',
'1$2_A3->3_B3',

# Group 3
'11$1_A1->3_C1',
'2$1_A2->3_C1',
'1$2_H12->3_C1',
'1$2_B1->3_C1',
'1$2_C1->3_C1',
'1$2_B4->3_C1',
'1$2_A3->3_C1',
'11$1_A1->3_C2',
'2$1_A2->3_C2',
'1$2_H12->3_C2',
'1$2_B2->3_C2',
'1$2_C1->3_C2',
'1$2_B4->3_C2',
'1$2_A3->3_C2',
'11$1_A1->3_C3',
'2$1_A2->3_C3',
'1$2_H12->3_C3',
'1$2_F1->3_C3',
'1$2_C1->3_C3',
'1$2_B4->3_C3',
'1$2_F4->3_C3',

# Group 4
'11$1_A1->3_D1',
'2$1_A2->3_D1',
'1$2_H12->3_D1',
'1$2_D1->3_D1',
'1$2_D3->3_D1',
'1$2_B4->3_D1',
'1$2_A3->3_D1',
'11$1_A1->3_D2',
'2$1_A2->3_D2',
'1$2_H12->3_D2',
'1$2_D2->3_D2',
'1$2_D3->3_D2',
'1$2_B4->3_D2',
'1$2_D5->3_D2',
'11$1_A1->3_D3',
'2$1_A2->3_D3',
'1$2_H12->3_D3',
'1$2_E2->3_D3',
'1$2_D3->3_D3',
'1$2_B4->3_D3',
'1$2_E5->3_D3',

# Group 5
'11$1_A1->3_E1',
'2$1_A2->3_E1',
'1$2_H12->3_E1',
'1$2_E1->3_E1',
'1$2_E3->3_E1',
'1$2_B4->3_E1',
'1$2_G1->3_E1',
'11$1_A1->3_E2',
'2$1_A2->3_E2',
'1$2_H12->3_E2',
'1$2_E2->3_E2',
'1$2_E3->3_E2',
'1$2_B4->3_E2',
'1$2_E5->3_E2',
'11$1_A1->3_E3',
'2$1_A2->3_E3',
'1$2_H12->3_E3',
'1$2_B1->3_E3',
'1$2_E3->3_E3',
'1$2_B4->3_E3',
'1$2_E5->3_E3',

# Group 6
'11$1_A1->3_F1',
'2$1_A2->3_F1',
'1$2_H12->3_F1',
'1$2_F1->3_F1',
'1$2_F2->3_F1',
'1$2_B4->3_F1',
'1$2_F4->3_F1',
'11$1_A1->3_F2',
'2$1_A2->3_F2',
'1$2_H12->3_F2',
'1$2_E2->3_F2',
'1$2_F2->3_F2',
'1$2_B4->3_F2',
'1$2_E5->3_F2',
'11$1_A1->3_F3',
'2$1_A2->3_F3',
'1$2_H12->3_F3',
'1$2_E1->3_F3',
'1$2_F2->3_F3',
'1$2_B4->3_F3',
'1$2_G1->3_F3',

# Group 7
'11$1_A1->3_G1',
'2$1_A2->3_G1',
'1$2_H12->3_G1',
'1$2_B1->3_G1',
'1$2_F2->3_G1',
'1$2_B4->3_G1',
'1$2_G1->3_G1',
'11$1_A1->3_G2',
'2$1_A2->3_G2',
'1$2_H12->3_G2',
'1$2_D2->3_G2',
'1$2_F2->3_G2',
'1$2_B4->3_G2',
'1$2_D5->3_G2',
'11$1_A1->3_G3',
'2$1_A2->3_G3',
'1$2_H12->3_G3',
'1$2_E1->3_G3',
'1$2_B3->3_G3',
'1$2_B4->3_G3',
'1$2_G1->3_G3',

# Group 8
'11$1_A1->3_H1',
'2$1_A2->3_H1',
'1$2_H12->3_H1',
'1$2_D2->3_H1',
'1$2_B3->3_H1',
'1$2_B4->3_H1',
'1$2_D5->3_H1',
'11$1_A1->3_H2',
'2$1_A2->3_H2',
'1$2_H12->3_H2',
'1$2_F1->3_H2',
'1$2_B3->3_H2',
'1$2_B4->3_H2',
'1$2_F4->3_H2',
'11$1_A1->3_H3',
'2$1_A2->3_H3',
'1$2_H12->3_H3',
'1$2_B1->3_H3',
'1$2_F2->3_H3',
'1$2_B4->3_H3',
'1$2_E5->3_H3'
            ]

#%% Do not modify anything down here

deck_labware = {}
for slot, labware_item in slots_map.items():
    deck_labware.update({slot:labware.load(labware_item, slot)})

p10single = instruments.P10_Single(
    mount='left',
    tip_racks=tip_racks
    )

for inst in inst_list:
    transfer_vol = int(inst.split('$')[0])
    source, dest = inst.split('$')[1].split('->')
    source_slot, source_well = source.split('_')
    dest_slot, dest_well = dest.split('_')
    
    p10single.transfer(
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