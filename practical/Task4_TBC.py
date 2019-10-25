# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 16:08:36 2019

@author: Trevor Ho

Task description: 
    
    Using 0.1 M HCl, perform titration of a NaOH sample pre-mixed with the pH indicator bromophenol blue.
    Create a series of tiration such that you observe the transition of bromophenol blue from blue to green and then yellow.
    See Figure 5 for the expected outcome.
    
    First, dilute the 0.1 M HCl to concentrations of 0.1 M, 0.09 M, 0.08 M, ..., 0.02 M, 0.01 M of 300 µL volume
    Then, distribute NaOH + pH indicator to different tubes, each receiving 200 µL.
    Finally, add 200 µL of diluted HCl, of different concentrations, to the distributed NaOH sample. 

You start with:
    Slot 2: 50 mL tube rack
        Well A1: 20 mL of water
        Well A2: 10 mL of sample (unknown pH) mixed with pH indicator
        Well A3: 10 mL of 0.1 M HCl
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
        '3':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
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
for i in 'X': # TODO: Replace 'X' by a range() function with the correct arguments to complete this for loop
    water_vol = i * 30
    p300s.transfer(
            water_vol,
            deck_labware['2'].wells('A1'),
            deck_labware['3'].wells(i),
            mix_after=(3, 150),
            blow_out=True,
            new_tip = 'always'            
            )
    
    # Step 2: Dilute the HCl into water
    
    # TODO: Insert a for loop and a transfer() function to add different amounts of HCl into different tubes
    # Must change tip every time to achieve accurate HCl concentration
    # Use the same mix_after and blow_out argument as the "Add water" step above










# Phase 2: Distribute the NaOH sample for mixing
    
# TODO: Insert a function to distribute 200 µL of NaOH mixed with pH indicator into wells A4 to B6 in slot '3'
    # This can be done using a for loop with the transfer() function, or just one distribute() function without using any for loops
    # Call the blow_out argument/function whenever possible/appropriate.








# Phase 3: Add the diluted HCl to the NaOH sample and mix

p300s.transfer(
        200,
        deck_labware['3'].wells(), # TODO: Complete the argument for .wells() of source wells without using a for loop
        deck_labware['3'].wells(), # TODO: Complete the argument for .wells() of destination wells without using a for loop
        mix_after=(3, 150),
        blow_out=True,
        new_tip = 'always'
        )

#%% DO NOT EDIT ANYTHING BELOW
# Print out the commands step by step
for c in robot.commands():
    print(c)