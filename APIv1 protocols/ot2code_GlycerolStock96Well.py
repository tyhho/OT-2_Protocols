# -*- coding: utf-8 -*-
"""
Created on Tue May 14 17:46:57 2019

@author: Trevor Ho
"""

from opentrons import labware, instruments, robot

#%% Copy & Paste Arena
#transfer_vol = 2

 

slots_map = {
        '4':'usascientific_96_wellplate_2.4ml_deep',
        '5':'opentrons_6_tuberack_falcon_50ml_conical',
        '1':'opentrons-tuberack-1.5ml-eppendorf',
        '2':'opentrons-tuberack-1.5ml-eppendorf',
        '3':'opentrons-tuberack-1.5ml-eppendorf',
        }

tip_slots_10 = ['7']
tip_racks_10 = [labware.load('geb_96_tiprack_10ul', slot) for slot in tip_slots_10]

tip_slots_300 = ['8']
tip_racks_300 = [labware.load('tiprack-200ul', slot) for slot in tip_slots_300]

inst_list = [
'2$1_A1->4_A1',
'2$1_A2->4_A2',
'2$1_A3->4_A3',
'2$1_A4->4_A4',
'2$1_A5->4_A5',
'2$1_A6->4_A6',
'2$1_B1->4_A7',
'2$1_B2->4_A8',
'2$1_B3->4_A9',
'2$1_B4->4_A10',
'2$1_B5->4_A11',
'2$1_B6->4_A12',
'2$1_C1->4_B1',
'2$1_C2->4_B2',
'2$1_C3->4_B3',
'2$1_C4->4_B4',
'2$1_C5->4_B5',
'2$1_C6->4_B6',
'2$1_D1->4_B7',
'2$1_D2->4_B8',
'2$1_D3->4_B9',
'2$1_D4->4_B10',
'2$1_D5->4_B11',
'2$1_D6->4_B12',
'2$2_A1->4_C1',
'2$2_A2->4_C2',
#'2$2_A3->4_C3',
#'2$2_A4->4_C4',
'2$2_A5->4_C5',
'2$2_A6->4_C6',
'2$2_B1->4_C7',
'2$2_B2->4_C8',
'2$2_B3->4_C9',
'2$2_B4->4_C10',
'2$2_B5->4_C11',
'2$2_B6->4_C12',
'2$2_C1->4_D1',
'2$2_C2->4_D2',
'2$2_C3->4_D3',
'2$2_C4->4_D4',
'2$2_C5->4_D5',
'2$2_C6->4_D6',
'2$2_D1->4_D7',
'2$2_D2->4_D8',
'2$2_D3->4_D9',
'2$2_D4->4_D10',
'2$2_D5->4_D11',
'2$2_D6->4_D12',
'2$3_A1->4_E1',
'2$3_A2->4_E2',
'2$3_A3->4_E3',
'2$3_A4->4_E4',
'2$3_A5->4_E5'
            ]

#%% Do not modify anything down here

labware_items = {}
for slot, labware_item in slots_map.items():
    labware_items.update({slot:labware.load(labware_item, slot)})

p300s = instruments.P300_Single(
    mount='right',
    tip_racks=tip_racks_300
    )

p10s = instruments.P10_Single(
    mount='left',
    tip_racks=tip_racks_10
    )

medium_dict= {
        'A1':['A1', 'A2', 'A3', 'A4', 'A5', 'A7', 'A8', 'A9', 'A10', 'B7', 'C3', 'C4', 'E2', 'E3', 'E4', 'E5'],
        'A2':['C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12'],
        'A3':['B4', 'B8'],
        'B1':['A6', 'A11', 'A12', 'B1', 'B2', 'B3', 'B5', 'B6', 'B9', 'B10', 'B11', 'B12', 'C1', 'C2', 'E1']
        }


for med_source, dest_wells in medium_dict.items():
    p300s.pick_up_tip()
    for dest_well in dest_wells:
        p300s.transfer(
                400,
                labware_items['5'].wells(med_source),
                labware_items['4'].wells(dest_well).top(-10),
                new_tip = 'never',
                blow_out=True
                )
    p300s.drop_tip()
    

for inst in inst_list:
    transfer_vol = int(inst.split('$')[0])
    source, dest = inst.split('$')[1].split('->')
    source_slot, source_well = source.split('_')
    dest_slot, dest_well = dest.split('_')
    
    p10s.transfer(
	transfer_vol,
	labware_items[source_slot].wells(source_well),
	labware_items[dest_slot].wells(dest_well),
	new_tip='always',
    blow_out=True)


c = robot.commands()
for line in c:
    print(line)