# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 20:42:09 2019

@author: Trevor Ho

Task description: 
    
    Generate a pattern of "EDI" on a 96-well flat bottom plate by pipetting dyes from source to destination wells.
    Each letter will have a different color, i.e. you have to keep pipetting colored liquid from one source to different destination wells.
    See Figure 1 for the expected final pattern.

You start with:
    Slot 2: 50 mL tube rack
        Well A1: 20 mL of yellow dye, for constructing the letter "E"
        Well A2: 20 mL of blue dye, for constructing the letter "D"
        Well A3: 20 mL of red dye, for constructing the letter "I"
    Slot 3: Empty 96-well flat bottom plate
    
Your robot is equipped with:
    Right mount: P300 single channel pipette
        
"""

# Import libraries for OT-2
from opentrons import labware, instruments,robot

# Put plates and racks onto the deck
slots_map = {
        '2':'opentrons_6_tuberack_falcon_50ml_conical',
        '3':'corning_96_wellplate_360ul_flat'
        }

deck_labware = {}
for slot, labware_item in slots_map.items():
    deck_labware.update({slot:labware.load(labware_item, slot)})

# Put tip boxes onto the deck
tip_slots = ['1']
tip_racks=[]
for slot in tip_slots:
        tip_racks.append(labware.load('opentrons_96_tiprack_300ul', slot))

# Configure the pipette
p300s = instruments.P300_Single(
    mount='right',
    tip_racks=tip_racks
    )

# Set up the pipetting instruction

# pattern_info dictionary maps the source to the destinations
# key = source well
# value (list) = destination wells that belong to the same source well

pattern_info = {
        'A1':['B1','B2','B3','C1','D1','D2','D3','E1','F1','F2','F3'],
        'A2': ['B5', 'B6', 'B7', 'C5', 'C8', 'D5', 'D8', 'E5','E8', 'F5','F6','F7'], 
        'A3': ['B10', 'B11', 'B12', 'C11', 'D11', 'E11', 'F10', 'F11', 'F12'],
        }

# Define the volume to be transferred
transfer_volume = 200

# Instruct the robot to use information in "pattern_info" and perform the pipetting steps

for source_well, dest_wells_list in pattern_info.items():
    
    # For each color, begin by instructing the pipette to pick up a tip
    # TODO: Insert the function that tells the P300 single channel pipette to pick up a tip
    
    p300s.pick_up_tip()
    
    for dest_well in dest_wells_list:
        p300s.transfer(
                transfer_volume,       # volume
                deck_labware['2'].wells(source_well),      # source
                deck_labware['3'].wells(dest_well),    # destination
                new_tip='never',       # do not change tip for the same color
                blow_out=True   # blow out all residual liquid in the tip to ensure that 0.2 mL is fully transferred
                )
        
    p300s.drop_tip()        
        
    
    # When pipetting for one color is done, instruct the pipette to drop the used tip
    # TODO: Insert the function that tells the P300 single channel pipette to drop the used tip

#%% DO NOT EDIT ANYTHING BELOW
# Print out the commands step by step
for c in robot.commands():
    print(c)