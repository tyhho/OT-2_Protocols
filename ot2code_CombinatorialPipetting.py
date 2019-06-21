# -*- coding: utf-8 -*-
"""
Created on Tue May 14 17:46:57 2019

@author: Trevor Ho
"""

from opentrons import labware, instruments, robot

#%% Copy & Paste Arena
#transfer_vol = 2

 

slots_map = {
        #'1':'96-flat',
        '1':'opentrons-tuberack-2ml-eppendorf',
        '2':'opentrons-tuberack-2ml-eppendorf',
        '3':'opentrons-tuberack-2ml-eppendorf',
        '4':'opentrons-tuberack-2ml-eppendorf'
        }

tip_slots = ['5']
tip_racks = [labware.load('tiprack-200ul', slot) for slot in tip_slots]

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
'5$3_A1->4_A1',
'5$3_A2->4_A2',
'5$3_A3->4_A3',
'5$3_A4->4_A4',
'5$3_A5->4_A5',
'5$3_A6->4_A6',
'5$3_B1->4_B1',
'5$3_B2->4_B2',
'5$3_B3->4_B3',
'5$3_B4->4_B4',
'5$3_B5->4_B5',
'5$3_B6->4_B6',
'5$3_C1->4_C1',
'5$3_C2->4_C2',
'5$3_C3->4_C3',
'5$3_C4->4_C4'
            ]

#%% Do not modify anything down here

labware_items = {}
for slot, labware_item in slots_map.items():
    labware_items.update({slot:labware.load(labware_item, slot)})

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
	labware_items[source_slot].wells(source_well),
	labware_items[dest_slot].wells(dest_well),
	new_tip='always',
    blow_out=True)
    #robot.pause()