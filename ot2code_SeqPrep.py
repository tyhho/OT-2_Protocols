# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 20:14:35 2020

@author: Trevor Ho
"""

from opentrons import labware, instruments, robot

#%% Copy & Paste Arena
#transfer_vol = 2

 

slots_map = {
        '1':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
        '2':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
        '4':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
        '5':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
        '3':'opentrons_6_tuberack_falcon_50ml_conical'
        }

tip_slots_10 = ['7']
tip_racks_10 = [labware.load('geb_96_tiprack_10ul', slot) for slot in tip_slots_10]

inst_list = [
'5$1_A1->2_A1',
'5$1_A2->2_A2',
'5$1_A3->2_A3',
'5$1_A4->2_A4',
'5$1_A5->2_A5',
'5$1_A6->2_A6',
'5$1_B1->2_B1',
'5$1_B2->2_B2',
'5$1_B3->2_B3',
'5$1_B4->2_B4',
'5$1_B5->2_B5',
'5$1_B6->2_B6',
'5$1_C1->2_C1',
'5$1_C2->2_C2',
'5$1_C3->2_C3',
'5$1_C4->2_C4',
'5$1_C5->2_C5',
'5$1_C6->2_C6',
'5$1_D1->2_D1',
'5$1_D2->2_D2',
'5$1_D3->2_D3',
'5$1_D4->2_D4',
'5$1_D5->2_D5',
'5$1_D6->2_D6',
'5$4_A1->5_A1',
'5$4_A2->5_A2',
'5$4_A3->5_A3',
'5$4_A4->5_A4',
'5$4_A5->5_A5',
'5$4_A6->5_A6',
'5$4_B1->5_B1',
'5$4_B2->5_B2',
'5$4_B3->5_B3',
'5$4_B4->5_B4',
'5$4_B5->5_B5',
'5$4_B6->5_B6',
'5$4_C1->5_C1',
'5$4_C2->5_C2',
'5$4_C3->5_C3',
'5$4_C4->5_C4',
'5$4_C5->5_C5',
'5$4_C6->5_C6',
'5$4_D1->5_D1',
'5$4_D2->5_D2',
'5$4_D3->5_D3'
            ]

#%% Do not modify anything down here

labware_items = {}
for slot, labware_item in slots_map.items():
    labware_items.update({slot:labware.load(labware_item, slot)})

p10s = instruments.P10_Single(
    mount='left',
    tip_racks=tip_racks_10
    )


p10s.pick_up_tip()
for inst in inst_list:
    transfer_vol = 15
    source, dest = inst.split('$')[1].split('->')
    dest_slot, dest_well = dest.split('_')
    
    p10s.transfer(
	15,
	labware_items['3'].wells('A1'),
	labware_items[dest_slot].wells(dest_well),
	new_tip='never',
    blow_out=True)
p10s.drop_tip()


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
    #robot.pause()
    
    #%%
for c in robot.commands():
    print(c)