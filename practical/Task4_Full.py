# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 16:08:36 2019

@author: Trevor Ho

Task description: 
    
    Using 1 mM HCl, perform titration of a NaOH sample pre-mixed with the pH indicator bromophenol blue.
    Create a series of tiration such that you observe the transition of bromophenol blue from blue to green and then yellow.
    See Figure 5 for the expected outcome.

    First, dilute the 1 mM HCl to concentrations of 1 mM, 0.9 mM, 0.8 mM, ..., 0.2 mM, 0.1 mM of 300 µL volume
    Then, distribute NaOH + pH indicator to different tubes, each receiving 200 µL.
    Finally, add 200 µL of diluted HCl, of different concentrations, to the distributed NaOH sample. 

You start with:
    Slot 2: 50 mL tube rack
        Well A1: 20 mL of water
        Well A2: 10 mL of sample (unknown pH) mixed with pH indicator
        Well A3: 10 mL of 1 mM HCl
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
for i in range(0,10):
    water_vol = i * 30
    p300s.transfer(
            water_vol,
            deck_labware['2'].wells('A1'),
            deck_labware['3'].wells(i),
            mix_after=(3, 150),
            blow_out=True,
            new_tip = 'always'            
            )
    
# Alternatively,    
#p300s.distribute([0,30,60,90,120,150,180,210,240,270],
#                 deck_labware['2'].wells('A1'),
#                 deck_labware['3'].wells('A1', length=10),
#                 blow_out=True
#                 )
   
    # Step 2: Dilute the HCl into water
    # Must change tip every time to achieve accurate HCl concentration

for i in range(0,10):
    acid_vol = 300 - i * 30
    p300s.transfer(
            acid_vol,
            deck_labware['2'].wells('A3'),
            deck_labware['3'].wells(i),
            mix_after=(3, 150),
            blow_out=True,
            new_tip = 'always'            
            )    

# Alternatively,
#p300s.transfer(
#        [300,270,240,210,180,150,120,90,60,30],
#        deck_labware['2'].wells('A3'),
#        deck_labware['3'].wells('A1', length=10),
#        mix_after=(3, 150),
#        blow_out=True,
#        new_tip = 'always'
#        )

# Phase 2: Distribute the NaOH sample for mixing
p300s.distribute(200,
                 deck_labware['2'].wells('A2'),
                 deck_labware['3'].wells('A4', length=10),
                 blow_out=True
                 )

# Phase 3: Add the diluted HCl to the NaOH sample and mix

p300s.transfer(
        200,
        deck_labware['3'].wells('A1', length=10),
        deck_labware['3'].wells('A4', length=10),
        mix_after=(3, 150),
        blow_out=True,
        new_tip = 'always'
        )

#%% DO NOT EDIT ANYTHING BELOW
# Print out the commands step by step
for c in robot.commands():
    print(c)