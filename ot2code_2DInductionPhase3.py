# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 23:06:12 2019

@author: Trevor Ho

This code distributes the bacterial culture from the overnight culture plate to the 96-well plates.

Currently, the script is designed to handle 3 * 96-well plates.

In this current script, the overnight culture plate is in slot 6,
 cultures for plate in slot 7 = cols(5), slot 8 = cols(8), slot 9 = cols(11)

"""

from opentrons import labware, instruments, robot

#%%  Setup

slots_map = {
        #'1':'96-flat',
        '6':'96-flat',
        '7':'96-flat',
        '8':'96-flat',
        '9':'96-flat'
        }

tip_slots = ['1','2','3']

culture_vol = 2

source_plate = '6'
culture_map = {
        '5':'7',
        '8':'8',
        '11':'9',
               }

#%%  Do not reload this section

tip_racks = [labware.load('tiprack-200ul', slot) for slot in tip_slots]

labware_items = {}
for slot, labware_item in slots_map.items():
    labware_items.update({slot:labware.load(labware_item, slot)})

pipette = instruments.P10_Multi(
    mount='right',
    tip_racks=tip_racks)

#%%
    
for source_col, dest_plate in culture_map.items():
    
    col_count = len(labware_items[dest_plate].cols())
    
    for col_index in range(col_count):
        # Add x axis inducer
        pipette.transfer(
        	culture_vol,
        	labware_items[source_plate].cols(source_col),
        	labware_items[dest_plate].cols(col_index),
        	new_tip='always',
            blow_out=True)
#%%

for c in robot.commands():
    print(c)

robot.clear_commands()