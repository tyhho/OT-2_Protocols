# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 21:12:39 2019

@author: Trevor Ho

Task description: 
    
    The goal is to perform serial dilution of a dye, initially at 4096X, into a graident of:
        2048X, 1024X, ... , 4X, 2X, 1X
    using water as the diluent.
    
    You should end up with a total of 12 tubes, each with 120 µL of diluted dye
    (except the last tube, which should have 240 µL of diluted dye).
    
    After each pipette step, you should instruct the robot to mix the diluted dye
    to ensure a homogenous solution is achieved before you move on
    
You start with:
    A 1.5 mL tube rack in Slot '2':
        1 mL of 4096X dye in well A1
        Empty 1.5 mL tubes are in wells A4 to D6 (these tubes should hold the serially diluted dyes)
    A 50 mL tube rack in Slot '3':
        20 mL of water in well A1
        
Your robot is equipped with:
    A P300 single channel pipette (Right Mount)
        
"""

# Import libraries for OT-2
from opentrons import labware, instruments,robot

# Put plates and racks onto the deck
slots_map = {
        '2':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
        '3':'opentrons_6_tuberack_falcon_50ml_conical',
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

# Phase 1: Distribute the diluent into the empty tubes
p300s.distribute(120,
                 deck_labware['3'].wells('A1'),
                 deck_labware['2'].cols('4', length=3)
                 )

# Phase 2: Perform the serial dilution

# Do not change the tip throughout the dilution process
p300s.pick_up_tip()

for well_num in range(12,23):
    p300s.transfer(
            120,
            deck_labware['2'].wells(well_num),
            deck_labware['2'].wells(well_num+1),
            new_tip = 'never',
            mix_after=(3, 200)
            )
    p300s.blow_out()
    
p300s.drop_tip()

## Option 2: The mix_after command has been known to caues all subsequent pipetting steps to slow down
#       Not sure if that has been fixed yet, but if not, the following scripts will replace the dilution processes above
#
#p300s.pick_up_tip()
#
#for well_num in range(12,22):
#    p300s.transfer(
#            120,
#            deck_labware['2'].wells(well_num),
#            deck_labware['2'].wells(well_num+1),
#            new_tip = 'never',
#            )
#    for _ in range(3):
#        p300s.aspirate(200,deck_labware['2'].wells(well_num+1))
#        p300s.dispense(200,deck_labware['2'].wells(well_num+1))
#    p300s.blow_out()    
#p300s.drop_tip()

# Print out the commands step by step
for c in robot.commands():
    print(c)

# Clear the commands inside the robot
    # Otherwise the instructions will pile up when the script is executed again
robot.clear_commands()
    
# Reset the robot
robot.reset()