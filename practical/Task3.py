# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 22:41:27 2019

@author: Trevor Ho

Task description: 
    
    Generate a checkered pattern of two colors on a 96-well PCR plate.
    For the final plate, each well should have 100 µL of 1X dye of eithr red or blue color.
        
You start with:
    Slot 1: 1.5 mL tube rack
        Well A1: 1.5 mL of 10X red dye
        Well A2: 1.5 mL of 10X blue dye
    Slot 2: 96-well V-bottom PCR plate
    Slot 3: 96-well V-bottom PCR plate (Final plate with checkered pattern!):
        Wells A1 - H12: prefilled with 90 µL of water

Your robot is equipped with:
    Right mount: P300 single channel pipette
    Left mount: P10 8-channel pipette

"""

# Import libraries for OT-2
from opentrons import labware, instruments,robot

# Reset for debugging
robot.clear_commands()
robot.reset()

# Put plates and racks onto the deck
slots_map = {
        '1':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
        '2':'nest_96_wellplate_100ul_pcr_full_skirt',
        '3':'nest_96_wellplate_100ul_pcr_full_skirt'
        }

deck_labware = {}
for slot, labware_item in slots_map.items():
    deck_labware.update({slot:labware.load(labware_item, slot)})

# Put tip boxes onto the deck
tip_slots_300 = ['4']
tip_racks_300 = []
for slot in tip_slots_300:
        tip_racks_300.append(labware.load('opentrons_96_tiprack_300ul', slot))

tip_slots_10 = ['5']
tip_racks_10 = []
for slot in tip_slots_10:
        tip_racks_10.append(labware.load('opentrons_96_tiprack_10ul', slot))

# Configure the pipettes
p300s = instruments.P300_Single(
    mount='right',
    tip_racks=tip_racks_300
    )

p10m = instruments.P10_Multi(
    mount='left',
    tip_racks=tip_racks_10
    )

# Set up the pipetting instruction

# Phase 1: Create an intermediate source where dyes would be distributed from
# The final checkered pattern is in essence a concatentation of two alternating patterns
# So, the most efficient way is to set up two columns of alternating colors

master_pattern_info = {
        'A1':['A1','C1','E1','G1','B2','D2','F2','H2'],
        'A2':['B1','D1','F1','H1','A2','C2','E2','G2']
        }

for source_well, dest_wells_list in master_pattern_info.items():
    p300s.distribute(67,
                     deck_labware['1'].wells(source_well),
                     deck_labware['2'].wells(dest_wells_list)
                     )

# Phase 2: Transfer the patterned dye from the intermediate plate in slot 2
# into every other column on the final plate in slot 3


# Version 1:
final_pattern_info = {
        '1':['1','3','5','7','9','11'],
        '2':['2','4','6','8','10','12']
        }

for source_col, dest_cols_list in final_pattern_info.items():
    p10m.transfer(
            10,
            deck_labware['2'].cols(source_col),
            deck_labware['3'].cols(dest_cols_list),
            new_tip = 'always',
            blow_out = True)

# Version 2: the same can be achieved by fewer codes if you use the "slice" function 
#for start_col in [0,1]:
#    p10m.transfer(
#            10,
#            deck_labware['2'].cols(start_col),
#            deck_labware['3'].cols[start_col:12:2],
#            new_tip = 'always',
#            blow_out = True)

# Print out the commands step by step
for c in robot.commands():
    print(c)

# Clear the commands inside the robot
    # Otherwise the instructions will pile up when the script is executed again
robot.clear_commands()
    
# Reset the robot
robot.reset()