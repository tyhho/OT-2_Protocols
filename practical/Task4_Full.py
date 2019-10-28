# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 16:08:36 2019

@author: Trevor Ho

Task description: 
    
    Using 0.1 mM HCl, perform titration of a NaOH sample pre-mixed with the pH indicator bromophenol blue.
    Create a series of tiration such that you observe the transition of bromophenol blue from blue to green and then yellow.
    See Figure 5 for the expected outcome.

    First, dilute the 0.1 mM HCl to concentrations of 0.1 mM, 0.09 mM, 0.08 mM, ..., 0.02 mM, 0.01 mM of 300 µL volume
    Then, distribute NaOH + pH indicator to different tubes, each receiving 150 µL.
    Finally, add 200 µL of diluted HCl, of different concentrations, to the distributed NaOH sample. 

You start with:
    Slot 2: 50 mL tube rack
        Well A1: 20 mL of water
        Well A2: 5 mL of sample (unknown pH) mixed with pH indicator
        Well A3: 5 mL of 0.1 mM HCl
    Slot 3: 1.5 mL tube rack
        Wells A1 to B3: Dilution series of HCl
        Wells A4 to B6: For mixing diluted HCl series with sample
        
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

# Phase 1: Dilute HCl to different concentratios
    # Step 1: Add water

p300s.pick_up_tip()
for i in range(0,10):
    water_vol = i * 30
    p300s.transfer(
            water_vol,
            deck_labware['2'].wells('A1'),
            deck_labware['3'].wells(i).top(-10),
            new_tip = 'never',
            blow_out = True
            )
p300s.drop_tip()

    # Step 2: Dilute the HCl into water
    # Must change tip every time to achieve accurate HCl concentration
    # TODO: Right now the same tip is used for all steps, correct the code such that tip is changed for every transfer & mix step

for i in range(0,10):
    p300s.pick_up_tip()
    acid_vol = 300 - i * 30
    p300s.transfer(
            acid_vol,
            deck_labware['2'].wells('A3'),
            deck_labware['3'].wells(i).top(-10),
            new_tip = 'never',
            blow_out = True
            )
    # Mix
    for _ in range(3):
        p300s.aspirate(200,deck_labware['3'].wells(i))
        p300s.dispense(200,deck_labware['3'].wells(i))
        p300s.move_to(deck_labware['3'].wells(i).top(-10))
        p300s.blow_out()
    p300s.drop_tip()

# Phase 2: Distribute the NaOH sample for mixing
p300s.pick_up_tip()
for i in range(0,10):
    p300s.transfer(150,
                 deck_labware['2'].wells('A2'),
                 deck_labware['3'].wells(i+12).top(-10),
                 new_tip = 'never',
                 blow_out=True
                 )
p300s.drop_tip()

# Phase 3: Add the diluted HCl to the NaOH sample and mix
# TODO: Copy and modify the codes from Phase 1 Step 2 (after modifications) above such that the robot adds 200 µL
# of diluted acid from tubes [A1, B1, ..., A3, B3] to [A4, B4, ..., A6, B6],
# followed by mixing of 3 times with 300 µL

for i in range(0,10):
    p300s.pick_up_tip()
    p300s.transfer(
            200,
            deck_labware['3'].wells(i),
            deck_labware['3'].wells(i+12).top(-10),
            new_tip = 'never',
            blow_out = True
            )
    # Mix
    for _ in range(3):
        p300s.aspirate(300,deck_labware['3'].wells(i+12))
        p300s.dispense(300,deck_labware['3'].wells(i+12))
        p300s.move_to(deck_labware['3'].wells(i+12).top(-10))
        p300s.blow_out()
    p300s.drop_tip()

#%% DO NOT EDIT ANYTHING BELOW
# Print out the commands step by step
for c in robot.commands():
    print(c)