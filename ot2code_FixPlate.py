# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 23:08:32 2019

@author: s1635543
"""


from opentrons import labware, instruments,robot

#%%
def smallVoltransfer(pipette,vol_in,vol_out,source,dest):
    pipette.pick_up_tip()
    pipette.aspirate(vol_in,source)
    pipette.dispense(vol_out,dest)
    pipette.dispense(pipette.current_volume,source)
    pipette.blow_out()
    pipette.drop_tip()

#%%

slots_map = {
        '2':'corning_96_wellplate_360ul_flat',
        '3':'corning_96_wellplate_360ul_flat',
        '5':'corning_96_wellplate_360ul_flat',
        '6':'corning_96_wellplate_360ul_flat',
        '8':'corning_96_wellplate_360ul_flat',
        '9':'corning_96_wellplate_360ul_flat'
        }

labware_items = {}
for slot, labware_item in slots_map.items():
    labware_items.update({slot:labware.load(labware_item, slot)})

tip_slots = ['1','4','7']
tip_racks = [labware.load('geb_96_tiprack_10ul', slot) for slot in tip_slots]

p10m = instruments.P10_Multi(
    mount='left',
    tip_racks=tip_racks
    )

#%%

transfer_dict= {
        2:3,
        5:6,
        8:9        
        }

for source_plate, dest_plate in transfer_dict.items():
    for col_index in range(12):
        smallVoltransfer(
                p10m,
                3,
                0.5,
                labware_items[str(source_plate)].cols(col_index),
                labware_items[str(dest_plate)].cols(col_index)
                )

for c in robot.commands():
    print(c)