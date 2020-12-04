# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 22:36:20 2019

@author: Trevor Ho

This code distributes the inducers from 2 inducer aliquot plates to 96-well plates.

Currently, the script is designed to handle 3 * 96-well plates.
"""

from opentrons import labware, instruments, robot

#%%  Setup

slots_map = {
        #'1':'96-flat',
        '7':'96-flat',
        '8':'96-flat',
        '9':'96-flat',
        '10':'96-flat',
        '11':'96-flat'
        }

tip_slots = ['1','2','3','4','5','6']

plates = ['7','8','9']

inducer_x_vol = 2
inducer_y_vol = 2

iap_x = '11'
iap_y = '10'

#%%  Do not reload this section

tip_racks = [labware.load('tiprack-200ul', slot) for slot in tip_slots]

labware_items = {}
for slot, labware_item in slots_map.items():
    labware_items.update({slot:labware.load(labware_item, slot)})

pipette = instruments.P10_Multi(
    mount='right',
    tip_racks=tip_racks)

#%%
    
for plate in plates:
    
    col_count = len(labware_items[plate].cols())
    
    for col_index in range(col_count):
        
        # Add y axis inducer
        pipette.transfer(
        	inducer_y_vol,
        	labware_items[iap_y].cols('1'),
        	labware_items[plate].cols(col_index),
        	new_tip='always',
            blow_out=True)
    
        # Add x axis inducer
        pipette.transfer(
        	inducer_y_vol,
        	labware_items[iap_x].cols(col_index),
        	labware_items[plate].cols(col_index),
        	new_tip='always',
            blow_out=True)
#%%
#
#for c in robot.commands():
#    print(c)
#
#robot.clear_commands()