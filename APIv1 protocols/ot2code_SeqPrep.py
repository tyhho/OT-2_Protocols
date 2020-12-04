# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 20:14:35 2020

@author: Trevor Ho
"""

from opentrons import labware, instruments,robot

robot.reset()
#%%
slots_map = {
        '1':'biorad_96_wellplate_200ul_pcr',
        '2':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
        '3':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
        '5':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
        '6':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap'
        }

tip_slots_10 = ['7']
tip_racks_10 = [labware.load('geb_96_tiprack_10ul', slot) for slot in tip_slots_10]

inst_list = [
    '$1_A1->2_A1',
    '$1_B1->2_A2',
    # '$1_C1->2_A3',
    '$1_D1->2_A4',
    '$1_E1->2_A5',
    '$1_F1->2_A6',
    '$1_G1->2_B1',
    '$1_H1->2_B2',
    '$1_A2->2_B3',
    '$1_B2->2_B4',
    '$1_C2->2_B5',
    '$1_D2->2_B6',
    '$1_E2->2_C1',
    '$1_F2->2_C2',
    '$1_G2->2_C3',
    '$1_H2->2_C4',
    '$1_A3->2_C5',
    '$1_B3->2_C6',
    '$1_C3->2_D1',
    '$1_D3->2_D2',
    '$1_E3->2_D3',
    '$1_F3->2_D4',
    '$1_G3->2_D5',
    '$1_H3->2_D6',
    '$1_A4->3_A1',
    '$1_B4->3_A2',
    '$1_C4->3_A3',
    '$1_D4->3_A4',
    '$1_E4->3_A5',
    '$1_F4->3_A6',
    '$1_G4->3_B1',
    '$1_H4->3_B2',
    '$1_A5->3_B3',
    '$1_B5->3_B4',
    '$1_C5->3_B5',
    '$1_D5->3_B6',
    '$1_E5->3_C1',
    '$1_F5->3_C2',
    '$1_G5->3_C3',
    '$1_H5->3_C4',
    '$1_A6->3_C5',
    '$1_B6->3_C6',
    '$1_C6->3_D1',
    '$1_D6->3_D2',
    '$1_E6->3_D3',
    '$1_F6->3_D4',
    '$1_G6->3_D5',
    '$1_H6->3_D6',
    '$1_A7->5_A1',
    '$1_B7->5_A2',
    '$1_C7->5_A3',
    '$1_D7->5_A4',
    '$1_E7->5_A5',
    '$1_F7->5_A6',
    '$1_G7->5_B1',
    '$1_H7->5_B2',
    '$1_A8->5_B3',
    '$1_B8->5_B4',
    '$1_C8->5_B5',
    '$1_D8->5_B6',
    '$1_E8->5_C1',
    '$1_F8->5_C2',
    '$1_G8->5_C3',
    '$1_H8->5_C4',
    '$1_A9->5_C5',
    '$1_B9->5_C6',
    '$1_C9->5_D1',
    '$1_D9->5_D2',
    '$1_E9->5_D3',
    '$1_F9->5_D4',
    '$1_G9->5_D5',
    '$1_H9->5_D6',
    '$1_A10->6_A1',
    '$1_B10->6_A2',
    '$1_C10->6_A3',
    '$1_D10->6_A4',
    '$1_E10->6_A5',
    '$1_F10->6_A6',
    '$1_G10->6_B1',
    '$1_H10->6_B2',
    '$1_A11->6_B3',
    '$1_B11->6_B4',
    '$1_C11->6_B5',
    '$1_D11->6_B6',
    '$1_E11->6_C1',
    '$1_F11->6_C2',
    '$1_G11->6_C3',
    '$1_H11->6_C4',
    '$1_A12->6_C5',
    '$1_B12->6_C6',
    '$1_C12->6_D1',
    '$1_D12->6_D2',
    '$1_E12->6_D3',
    '$1_F12->6_D4',
    '$1_G12->6_D5',
    '$1_H12->6_D6'
    ]


#%% Do not modify anything down here

labware_items = {}
for slot, labware_item in slots_map.items():
    labware_items.update({slot:labware.load(labware_item, slot)})

pipette = instruments.P10_Single(
    mount='right',
    tip_racks=tip_racks_10
    )


for inst in inst_list:
    inst = inst.split('$')[1]
    dest, source = inst.split('->')
    source_slot, source_well = source.split('_')
    dest_slot, dest_well = dest.split('_')
    
    pipette.transfer(10,
                     labware_items[source_slot].wells(source_well),
                     labware_items[dest_slot].wells(dest_well),
                     blow_out=True,
                     new_tip='always'
                     )
    #%%
for c in robot.commands():
    print(c)