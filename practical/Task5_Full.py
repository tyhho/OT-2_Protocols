# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 17:25:08 2019

@author: Trevor Ho

Task description: 
    
    A 96-well PCR plate with randomized concentration (between 100X to 300X) of a dye (100 µL) is given.
    Dilute and standardize the concentrations (1X) and volumes (100 µL) of all dye on a new 96-well PCR plate.
    See Figure 6 for the expected outcome.
    
    Note: mixing can be omitted from the final transfer step
          
You start with:
    Slot 1: 96-well V-bottom PCR plate (Starting material)
        Wells A1 - H12: Dye at randomized but known concentrations in each well
    Slot 2: Empty 96-well V-bottom PCR plate (Intermediate plate)
    Slot 3: Empty 96-well V-bottom PCR plate (Final product)
    Slot 6: 50 mL tube rack
        Well A1: 20 mL of water
        Well A2: 20 mL of water

Your robot is equipped with:
    Right mount: P300 single channel pipette
    Left mount: P10 8-channel pipette
    
"""

# Import libraries for OT-2
from opentrons import labware, instruments,robot
import math

# Put plates and racks onto the deck
slots_map = {
        '1':'biorad_96_wellplate_200ul_pcr',
        '2':'biorad_96_wellplate_200ul_pcr',
        '3':'biorad_96_wellplate_200ul_pcr',
        '6':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap'
        }

deck_labware = {}
for slot, labware_item in slots_map.items():
    deck_labware.update({slot:labware.load(labware_item, slot)})

# Put tip boxes onto the deck
tip_slots_300 = ['4']
tip_racks_300 = []
for slot in tip_slots_300:
        tip_racks_300.append(labware.load('opentrons_96_tiprack_300ul', slot))

tip_slots_10 = ['5','8']
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

inter_conc_factor = 10    # desired concentration for samples on the intermediate plate
inter_sample_vol_from_source = 5   # volume of sample to be transferred from source plate to intermediate plate (user-defined, fixed for all samples since using P10 8-channel)
final_vol_water_to_add = 90 
final_sample_vol_from_int = 10

inter_dict_of_vol_water_to_add = {}
inter_dict_of_mix_vol = {}

# Calculate the volume of water to be added to each well of the intermediate plate

for well, init_sample_conc in dye_conc.items():
    # init_sample_conc = initial sample concentration    
    inter_vol_water_to_add = (init_sample_conc - inter_conc_factor) * inter_sample_vol_from_source / inter_conc_factor
    mix_vol = math.ceil((inter_sample_vol_from_source + inter_vol_water_to_add) * 0.7) # mixing volume for intermediate step, before being diluted to final plate
    inter_dict_of_vol_water_to_add.update({well:inter_vol_water_to_add})
    inter_dict_of_mix_vol.update({well: mix_vol})

# Checking: the maximum volume that can be held in a 96-well PCR plate is 200 µL.
    # This section checks if the total volume of liquid for every well exceeds that limit
for vol in inter_dict_of_vol_water_to_add.values():
    if vol + inter_sample_vol_from_source > 200:
        raise ValueError('Volume to pipette exceeds maximum volume of PCR plate ')

#%%    
## Execution of instructions
    
# Phase 1: Standardize concentration
    # Step 1: Transfer water into the intermediate plate. Volumes to be determined by initial sample concentration
    
p300s.pick_up_tip()
for well, water_to_add_vol in inter_dict_of_vol_water_to_add.items():
    p300s.transfer(water_to_add_vol,
                 deck_labware['6'].wells('A1'),
                 deck_labware['2'].wells(well),
                 blow_out=True,
                 new_tip = 'never'
                 )
p300s.drop_tip()


    # Step 2: Dilute samples of random concentration from source plate to intermediate plate
p10m.transfer(
    inter_sample_vol_from_source,
    deck_labware['1'].cols('1',length=12),
    deck_labware['2'].cols('1',length=12),
    new_tip = 'always',
    blow_out = True)

    # Step 3: Mix the samples to ensure homogenity before the final dilution
    # Since all samples should now be at similar concentrations, it is acceptable to use a single tip for all mixes
p300s.pick_up_tip()
for well, mix_vol in inter_dict_of_mix_vol.items():
    for _ in range(2):
        p300s.aspirate(mix_vol,deck_labware['2'].wells(well))
        p300s.dispense(mix_vol,deck_labware['2'].wells(well))
    p300s.blow_out()
p300s.drop_tip()

# Phase 2: Standardize volume
    # Step 1: Distribute water into the final plate
p300s.distribute(final_vol_water_to_add,
                 deck_labware['6'].wells('A2'),
                 deck_labware['3'].wells('A1', length=96),
                 blow_out=True
                 )

    # Step 2: Dilute samples of standardized concentration from intermediate plate to final plate
    # by adding 10 µL of sample to 90 µL of water

p10m.transfer(
        final_sample_vol_from_int,
        deck_labware['2'].cols('1',length=12),
        deck_labware['3'].cols('1',length=12),
        new_tip = 'always',
        blow_out = True)

#Alternatively,
#for i in range(0,12):
#    p10m.transfer(
#            final_sample_vol_from_int,
#            deck_labware['2'].cols(i),
#            deck_labware['3'].cols(i),
#            new_tip = 'always',
#            blow_out = True)

#%% DO NOT EDIT ANYTHING BELOW
# Print out the commands step by step
for c in robot.commands():
    print(c)