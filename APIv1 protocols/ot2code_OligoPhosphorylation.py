# -*- coding: utf-8 -*-
"""
Created on Tue May 28 18:34:58 2019

@author: s1635543
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 14 17:46:57 2019

@author: Trevor Ho
"""

from opentrons import labware, instruments, robot

#%% Copy & Paste Arena

slots_map = {
        '1':'PCR-strip-tall',
        '2':'opentrons-tuberack-2ml-screwcap',
        '3':'opentrons-tuberack-2ml-screwcap',
        '4':'opentrons-tuberack-2ml-eppendorf'
        }

tip_slots = ['5']
tip_racks = [labware.load('tiprack-200ul', slot) for slot in tip_slots]

inst_list = [
'4_A1->1_A1$9',
'2_A1->1_A1$1',
'4_A1->1_A2$9',
'2_A2->1_A2$1',
'4_A1->1_A3$9',
'2_A3->1_A3$1',
'4_A1->1_A4$9',
'2_A4->1_A4$1',
'4_A1->1_A5$9',
'2_A5->1_A5$1',
'4_A1->1_A6$9',
'2_A6->1_A6$1',
'4_A1->1_A7$9',
'2_B1->1_A7$1',
'4_A1->1_A8$9',
'2_B2->1_A8$1',
'4_A1->1_B1$9',
'2_B3->1_B1$1',
'4_A1->1_B2$9',
'2_B4->1_B2$1',
'4_A1->1_B3$9',
'2_B5->1_B3$1',
'4_A1->1_B4$9',
'2_B6->1_B4$1',
'4_A1->1_B5$9',
'2_C1->1_B5$1',
'4_A1->1_B6$9',
'2_C2->1_B6$1',
'4_A1->1_B7$9',
'2_C3->1_B7$1',
'4_A1->1_B8$9',
'2_C4->1_B8$1',
'4_A1->1_C1$9',
'2_C5->1_C1$1',
'4_A1->1_C2$9',
'2_C6->1_C2$1',
'4_A1->1_C3$9',
'2_D1->1_C3$1',
'4_A1->1_C4$9',
'2_D2->1_C4$1',
'4_A1->1_C5$9',
'2_D3->1_C5$1',
'4_A1->1_C6$9',
'2_D4->1_C6$1',
'4_A1->1_C7$9',
'2_D5->1_C7$1',
'4_A1->1_C8$9',
'2_D6->1_C8$1',
'4_A1->1_D1$9',
'3_A1->1_D1$1',
'4_A1->1_D2$9',
'3_A2->1_D2$1',
'4_A1->1_D3$9',
'3_A3->1_D3$1',
'4_A1->1_D4$9',
'3_A4->1_D4$1',
'4_A1->1_D5$9',
'3_A5->1_D5$1',
'4_A1->1_D6$9',
'3_A6->1_D6$1',
'4_A1->1_D7$9',
'3_B1->1_D7$1',
'4_A1->1_D8$9',
'3_B2->1_D8$1'
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
    transfer_vol = int(inst.split('$')[1])
    source, dest = inst.split('$')[0].split('->')
    source_slot, source_well = source.split('_')
    dest_slot, dest_well = dest.split('_')
    
    p10single.transfer(
	transfer_vol,
	labware_items[source_slot].wells(source_well),
	labware_items[dest_slot].wells(dest_well),
	new_tip='always',
    blow_out=True)
    #robot.pause()