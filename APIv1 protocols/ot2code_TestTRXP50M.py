# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 16:23:50 2019

@author: Trevor Ho

Test script for testing if TipRackExterior works with P50M reliably
"""


# Import libraries for OT-2
from opentrons import labware, instruments,robot

# Put plates and racks onto the deck
slots_map = {
        '2':'corning_96_wellplate_360ul_flat',
        }

deck_labware = {}
for slot, labware_item in slots_map.items():
    deck_labware.update({slot:labware.load(labware_item, slot)})

# Put tip boxes onto the deck

tip_slots = ['1']
tip_racks = []
for slot in tip_slots:
        tip_racks.append(labware.load('tiprack-200ul', slot))

# Configure the pipettes

p50m = instruments.P50_Multi(
    mount='right',
    tip_racks=tip_racks
    )

# Set up the pipetting instruction

#%%    
## Execution of instructions

for i in range(12):
    p50m.pick_up_tip()
    p50m.aspirate(
        50,
        deck_labware['2'].cols(i)
        )  
    p50m.dispense(50,
                  deck_labware['2'].cols(i)
                  )
    p50m.blow_out()
    p50m.drop_tip()
    
# Print out the commands step by step
for c in robot.commands():
    print(c)
