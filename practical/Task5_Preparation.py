# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 18:14:24 2019

@author: Trevor Ho

Creates the plate for Task 5

You start with:
    Slot 1: 96-well V-bottom PCR plate
    Slot 6: 50 mL tube rack
        Well A1: 20 mL of water
        Well A2: 20 mL of dye

Your robot is equipped with:
    Right mount: P300 single channel pipette    

"""

# Import libraries for OT-2
from opentrons import labware, instruments,robot

# Put plates and racks onto the deck
slots_map = {
        '1':'biorad_96_wellplate_200ul_pcr',
        '2':'opentrons_6_tuberack_falcon_50ml_conical'
        }

deck_labware = {}
for slot, labware_item in slots_map.items():
    deck_labware.update({slot:labware.load(labware_item, slot)})

# Put tip boxes onto the deck
tip_slots_300 = ['4','5']
tip_racks_300 = []
for slot in tip_slots_300:
        tip_racks_300.append(labware.load('opentrons_96_tiprack_300ul', slot))

# Configure the pipettes
p300s = instruments.P300_Single(
    mount='right',
    tip_racks=tip_racks_300
    )

# Set up the pipetting instruction

#%%
## Preparation

# Known concentrations of dyes
# Key = well position on source plate
# Value = dye concentration, in value of X, e.g. A1 dye was in concentration of 248X
dye_conc = {
        "A1":248,
        "A2":102,
        "A3":180,
        "A4":143,
        "A5":179,
        "A6":120,
        "A7":268,
        "A8":286,
        "A9":191,
        "A10":296,
        "A11":145,
        "A12":253,
        "B1":190,
        "B2":108,
        "B3":291,
        "B4":139,
        "B5":202,
        "B6":230,
        "B7":222,
        "B8":144,
        "B9":146,
        "B10":268,
        "B11":104,
        "B12":274,
        "C1":229,
        "C2":162,
        "C3":138,
        "C4":201,
        "C5":139,
        "C6":147,
        "C7":163,
        "C8":280,
        "C9":138,
        "C10":229,
        "C11":161,
        "C12":214,
        "D1":214,
        "D2":155,
        "D3":104,
        "D4":208,
        "D5":187,
        "D6":142,
        "D7":155,
        "D8":196,
        "D9":152,
        "D10":190,
        "D11":248,
        "D12":278,
        "E1":162,
        "E2":289,
        "E3":126,
        "E4":105,
        "E5":190,
        "E6":192,
        "E7":104,
        "E8":239,
        "E9":248,
        "E10":180,
        "E11":143,
        "E12":196,
        "F1":251,
        "F2":106,
        "F3":280,
        "F4":180,
        "F5":254,
        "F6":151,
        "F7":184,
        "F8":231,
        "F9":249,
        "F10":253,
        "F11":137,
        "F12":101,
        "G1":282,
        "G2":200,
        "G3":128,
        "G4":118,
        "G5":136,
        "G6":136,
        "G7":238,
        "G8":168,
        "G9":188,
        "G10":116,
        "G11":224,
        "G12":190,
        "H1":126,
        "H2":155,
        "H3":164,
        "H4":285,
        "H5":229,
        "H6":136,
        "H7":193,
        "H8":147,
        "H9":147,
        "H10":245,
        "H11":130,
        "H12":270
        }

water_dict = {}

for well, init_sample_conc in dye_conc.items():
    # Calculate the volume of water to be added to each well of the intermediate plate
    water_vol = 150 - (init_sample_conc / 10)
    water_dict.update({well: water_vol})

#%%    
## Execution of instructions
    
# Step 1: Transfer water into the plate
        
# Use the same tip for transfers
#p300s.pick_up_tip()
#for well, water_to_add_vol in water_dict.items():
#    
#    p300s.transfer(water_to_add_vol,
#                 deck_labware['2'].wells('A1'),
#                 deck_labware['1'].wells(well).top(-5),
#                 blow_out=True,
#                 new_tip = 'never'
#                 )
#
#p300s.drop_tip()

mix_vol = 100

for well, sample_vol in dye_conc.items():
    p300s.pick_up_tip()

    p300s.transfer((sample_vol/10),
                 deck_labware['2'].wells('A2'),
                 deck_labware['1'].wells(well),
                 new_tip = 'never'
                 )
    p300s.blow_out(deck_labware['1'].wells(well).top(-2))
    
    for _ in range(2):
        p300s.aspirate(mix_vol,deck_labware['1'].wells(well))
        p300s.dispense(mix_vol,deck_labware['1'].wells(well))
        p300s.blow_out(deck_labware['1'].wells(well).top(-2))

    p300s.drop_tip()

#%% DO NOT EDIT ANYTHING BELOW
# Print out the commands step by step
for c in robot.commands():
    print(c)
