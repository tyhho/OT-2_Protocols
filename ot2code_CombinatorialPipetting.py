# -*- coding: utf-8 -*-
"""
Created on Tue May 14 17:46:57 2019

@author: Trevor Ho
"""

from opentrons import labware, instruments, robot

#%% Copy & Paste Arena
#transfer_vol = 2

 

slots_map = {
        '1':'96-flat',
        '2':'opentrons-tuberack-1.5ml-eppendorf',
        }

tip_slots = ['5']
tip_racks = [labware.load('tiprack-200ul', slot) for slot in tip_slots]

inst_list = [
'2$2_A1->1_E3',
'2$2_A1->1_E4',
'2$2_A2->1_E5',
'2$2_A2->1_E6',
'2$2_A3->1_E7',
'2$2_A3->1_E8',
'2$2_A4->1_E9',
'2$2_A4->1_E10',
'2$2_A1->1_F3',
'2$2_A1->1_F4',
'2$2_A2->1_F5',
'2$2_A2->1_F6',
'2$2_A3->1_F7',
'2$2_A3->1_F8',
'2$2_A4->1_F9',
'2$2_A4->1_F10',
'2$2_A1->1_G3',
'2$2_A1->1_G4',
'2$2_A2->1_G5',
'2$2_A2->1_G6',
'2$2_A3->1_G7',
'2$2_A3->1_G8',
'2$2_A4->1_G9',
'2$2_A4->1_G10'
            ]

#%% Do not modify anything down here

labware_items = {}
for slot, labware_item in slots_map.items():
    labware_items.update({slot:labware.load(labware_item, slot)})

p10single = instruments.P10_Single(
    mount='right',
    tip_racks=tip_racks
    )

for inst in inst_list:
    transfer_vol = int(inst.split('$')[0])
    source, dest = inst.split('$')[1].split('->')
    source_slot, source_well = source.split('_')
    dest_slot, dest_well = dest.split('_')
    
    p10single.transfer(
	transfer_vol,
	labware_items[source_slot].wells(source_well),
	labware_items[dest_slot].wells(dest_well),
	new_tip='always',
    blow_out=True)
    #robot.pause()