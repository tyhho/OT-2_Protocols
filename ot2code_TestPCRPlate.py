# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 16:23:50 2019

@author: Trevor Ho

Test script for PCR plate
"""


# Import libraries for OT-2
from opentrons import labware, instruments,robot

# Reset for debugging
robot.clear_commands()
robot.reset()

# Put plates and racks onto the deck
slots_map = {
        '2':'nest_96_wellplate_100ul_pcr_full_skirt',
        }

deck_labware = {}
for slot, labware_item in slots_map.items():
    deck_labware.update({slot:labware.load(labware_item, slot)})

# Put tip boxes onto the deck

tip_slots_10 = ['1']
tip_racks_10 = []
for slot in tip_slots_10:
        tip_racks_10.append(labware.load('opentrons_96_tiprack_10ul', slot))

# Configure the pipettes

p10m = instruments.P10_Multi(
    mount='left',
    tip_racks=tip_racks_10
    )

# Set up the pipetting instruction

#%%    
## Execution of instructions

p10m.pick_up_tip()
for i in range(11):
    p10m.transfer(
        10,
        deck_labware['2'].cols(i),
        deck_labware['2'].cols(i+1),
        new_tip = 'never',
        blow_out = False)

p10m.drop_tip()
    
# Print out the commands step by step
for c in robot.commands():
    print(c)

# Clear the commands inside the robot
    # Otherwise the instructions will pile up when the script is executed again
robot.clear_commands()
    
# Reset the robot
robot.reset()