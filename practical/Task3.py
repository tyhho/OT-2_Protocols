# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 22:41:27 2019

@author: Trevor Ho

Task description: 
    
    The goal is to generate a checkered pattern of two colors on a 96-well PCR plate.
    For the final plate, each well should have 100 µL of 1X dye of eithr red or blue color.
    
    You will have to plan how to do this most efficiently.
    
You start with:
    A 1.5 mL tube rack in Slot '1':
        1.5 mL of 10X red dye in well A1
        1.5 mL of 10X blue dye in well A2
    An empty 96-well V-bottom PCR plate in Slot '2'
    A 96-well V-bottom PCR plate in Slot '3' (Final plate with checkered pattern!):
        All wells already have 90 µL of water inside

Your robot is equipped with:
    A P300 single channel pipette
    A P10 8-channel pipette

"""

# Import libraries for OT-2
from opentrons import labware, instruments,robot

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
        tip_racks_10.append(labware.load('opentrons_96_tiprack_300ul', slot))



# Configure the pipette
p300s = instruments.P300_Single(
    mount='right',
    tip_racks=tip_racks
    )

# Set up the pipetting instruction