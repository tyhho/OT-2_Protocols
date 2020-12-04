# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 00:45:56 2020

@author: Trevor Ho
"""

# FIXME: check


# Import libraries for OT-2
from opentrons import labware, instruments,robot

# Put plates and racks onto the deck
slots_map = {
        '1':'corning_96_wellplate_360ul_flat',
        }

dlw = {}
for slot, labware_item in slots_map.items():
    dlw.update({slot:labware.load(labware_item, slot)})

# Put tip boxes onto the deck

tip_slots = ['2']
tip_racks = []
for slot in tip_slots:
        tip_racks.append(labware.load('tiprack-200ul', slot))

# Configure the pipettes

pipette = instruments.P50_Multi(
    mount='right',
    tip_racks=tip_racks
    )

# Set up the pipetting instruction
 
#%%    
## Execution of instructions
vol = 50

for well in ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12']:
    pipette.pick_up_tip()
    pipette.aspirate(vol, dlw['1'].wells(well))
    pipette.move_to(dlw['1'].wells(well).top(10))
    pipette.dispense(vol,dlw['1'].wells(well))
    pipette.blow_out()
    pipette.drop_tip()

# Print out the commands step by step
for c in robot.commands():
    print(c)
