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
        '1':'96-flat',
        '2':'96-flat',
        '3':'96-flat'
        }

labware_items = {}
for slot, labware_item in slots_map.items():
    labware_items.update({slot:labware.load(labware_item, slot)})

tip_slots = ['4']
tip_racks = [labware.load('tiprack-10ul', slot) for slot in tip_slots]

p10m = instruments.P10_Multi(
    mount='right',
    tip_racks=tip_racks
    )

#%%

for col_index in range(6):
    distributeNoBlowOutLite(p10m,
                            (culture_vol*2+2),
                            culture_vol,
                            labware_items['1'].cols(col_index),
                            [labware_items['2'].cols(col_index),labware_items['2'].cols(col_index+6)]
                            )
for col_index in range(6):
    distributeNoBlowOutLite(p10m,
                            (culture_vol*2+2),
                            culture_vol,
                            labware_items['1'].cols(col_index),
                            [labware_items['3'].cols(col_index),labware_items['3'].cols(col_index+6)]
                            )
for c in robot.commands():
    print(c)