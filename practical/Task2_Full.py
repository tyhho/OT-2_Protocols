# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 21:12:39 2019

@author: Trevor Ho

Task description: 
    
    Perform serial dilution of a dye, initially at 4096X, into a gradient of:
        2048X, 1024X, ... , 4X, 2X, 1X
    using water as the diluent.
    See Figure 2 for the expected final pattern.

    You should end up with a total of 12 tubes, each with 120 µL of diluted dye
    (except the last tube, which should have 240 µL of diluted dye).
    
    After each pipette step, you should instruct the robot to mix the diluted dye
    to ensure a homogenous solution is achieved before you move on
    
You start with:
    Slot 2: 50 mL tube rack
        Well A1: 20 mL of water
    Slot 3: 1.5 mL tube rack
        Well A1: 1 mL of 4096X dye
        Well A4 - D6: Empty 1.5 mL tubes (these tubes should hold the serially diluted dyes)
        
Your robot is equipped with:
    Right mount: P300 single channel pipette
        
"""

# Import libraries for OT-2
from opentrons import labware, instruments,robot

# Put plates and racks onto the deck
slots_map = {
        '2':'opentrons_6_tuberack_falcon_50ml_conical',
        '3':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap'
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
                 deck_labware['2'].wells('A1'),
                 # TODO: Insert here the argument of destination wells (A1, B1, C1, ... , B3, C3, D3 (total of 12)
                 deck_labware['3'].wells('A4', to='D6')
                 )

# Phase 2: Perform the serial dilution

# TODO: Use the same tip for all transfer and mixing processes
# Insert the missing functions for picking up and dropping tip

p300s.pick_up_tip()

p300s.transfer(
            120,
            deck_labware['3'].wells('A1'),
            deck_labware['3'].wells('A4').top(-20),
            new_tip = 'never'
            )

# For-loop for mixing
for _ in range(3):
        p300s.aspirate(200,deck_labware['3'].wells('A4'))
        p300s.dispense(200,deck_labware['3'].wells('A4'))
        p300s.move_to(deck_labware['3'].wells('A4').top(-20))
        p300s.blow_out()

for well_num in range(12,23):

    # TODO: Copy and modify the transfer function from above to complete this for-loop for serial dilution
    # Beware of the new_tip argument
    
    p300s.transfer(
            120,
            deck_labware['3'].wells(well_num),
            deck_labware['3'].wells(well_num+1).top(-20),
            new_tip = 'never'
            )
    
    # TODO: Copy and modify the for-loop for mixing above such that
    # the robot performs a mixing on each well right after transfer
    
    for _ in range(3):
        p300s.aspirate(200,deck_labware['3'].wells(well_num+1))
        p300s.dispense(200,deck_labware['3'].wells(well_num+1))
        p300s.move_to(deck_labware['3'].wells(well_num+1).top(-20))
        p300s.blow_out()    

p300s.drop_tip()

#%% DO NOT EDIT ANYTHING BELOW
# Print out the commands step by step
for c in robot.commands():
    print(c)