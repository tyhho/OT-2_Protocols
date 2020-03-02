# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 20:27:10 2019

@author: s1635543
"""

from opentrons import labware, instruments,robot

#%%
def distributeNoBlowOutLite(pipette,vol_in,vol_out,source,dests):
    pipette.pick_up_tip()
    pipette.aspirate(vol_in,source)
    for dest in dests:
        pipette.dispense(vol_out,dest)
    pipette.drop_tip()

#%%
culture_vol = 2

slots_map = {
        '1':'corning_96_wellplate_360ul_flat',
        '2':'corning_96_wellplate_360ul_flat',
        '3':'corning_96_wellplate_360ul_flat',
        '5':'corning_96_wellplate_360ul_flat',
        '6':'corning_96_wellplate_360ul_flat'
        }

labware_items = {}
for slot, labware_item in slots_map.items():
    labware_items.update({slot:labware.load(labware_item, slot)})

tip_slots = ['7','8','10','11']
tip_racks = [labware.load('geb_96_tiprack_10ul', slot) for slot in tip_slots]

p10m = instruments.P10_Multi(
    mount='left',
    tip_racks=tip_racks
    )

#%%

for dest_slot in ['2','3','5','6']:
    for col_index in range(len(labware_items['1'].cols())):
        p10m.transfer(2,
                      labware_items['1'].cols(col_index),
                      labware_items[dest_slot].cols(col_index),
                      blow_out=True,
                      new_tip='always'
                      )
   
for c in robot.commands():
    print(c)