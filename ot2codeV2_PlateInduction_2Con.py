# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 17:15:31 2020

@author: Trevor Ho
"""

from opentrons import protocol_api

#%%

# metadata
metadata = {
    'protocolName': 'Plate Induction (2 Conditions)',
    'author': 'Trevor Y. H. Ho <trevor.ho@ed.ac.uk>',
    'description': 'Transfer bacteria from 96-well plate to 2 other plates \
        without changing tips',
    'apiLevel': '2.6'
}

#%% 

def run(protocol: protocol_api.ProtocolContext):

    def distributeNoBlowOutLite(pipette,vol_in,vol_out,source,dests):
        pipette.pick_up_tip()
        pipette.aspirate(vol_in,source)
        for dest in dests:
            pipette.dispense(vol_out,dest)
        pipette.drop_tip()

    slots_map = {
            '1':'corning_96_wellplate_360ul_flat',
            '2':'corning_96_wellplate_360ul_flat',
            '3':'corning_96_wellplate_360ul_flat',
            '4':'corning_96_wellplate_360ul_flat',
            '5':'corning_96_wellplate_360ul_flat',
            '6':'corning_96_wellplate_360ul_flat'
            }
    
    # Configure tip racks and pipette
    
    # r_pipette_name = 'p300_single'
    # r_tiprack_slots = ['4']
    # r_tiprack_name = 'opentrons_96_tiprack_300ul'
    
    l_pipette_name = 'p10_multi'
    l_tiprack_slots = ['7', '8']
    l_tiprack_name = 'geb_96_tiprack_10ul'
    
    labware_items = {}
    for slot, labware_item in slots_map.items():
        labware_items.update({slot:protocol.load_labware(labware_item, slot)})
    
    # r_tip_racks = [protocol.load_labware(r_tiprack_name, slot) for slot in r_tiprack_slots]
    l_tip_racks = [protocol.load_labware(l_tiprack_name, slot) for slot in l_tiprack_slots]
    
    # r_pipette = protocol.load_instrument(instrument_name = r_pipette_name,
    #     mount = 'right', tip_racks = r_tip_racks)
    l_pipette = protocol.load_instrument(instrument_name = l_pipette_name,
        mount = 'left', tip_racks = l_tip_racks)
    
    for i in range(9):
        distributeNoBlowOutLite(l_pipette,6,
                                2,
                                labware_items['1'].wells()[i * 8],
                                [labware_items['2'].wells()[i * 8], labware_items['3'].wells()[i * 8]]
                                )
        
    for i in range(9):
        distributeNoBlowOutLite(l_pipette,6,
                                2,
                                labware_items['4'].wells()[i * 8],
                                [labware_items['5'].wells()[i * 8], labware_items['6'].wells()[i * 8]]
                                )

    return protocol.commands()

# The extra part: programmatically get a simulation ProtocolContext, so we can run this
# as a normal Python script and have everything in the run function get executed.
#
# This part should be removed or commented out before uploading to a real OT-2.

# import json
# extra_labware_list = [
#     'starlabpcrplateonws_96_wellplate_350ul',
#     'gbocellstaronewellagarplate_96_wellplate_10ul'
#     ]

# extra_labware = {}
# for labware_name in extra_labware_list:
#     labware_json_fn = labware_name + '.json'
#     with open(labware_json_fn) as f: labware_data = json.load(f)
#     extra_labware.update({labware_name:labware_data})

# from opentrons.simulate import get_protocol_api
# protocol = get_protocol_api(version=metadata['apiLevel'], extra_labware=extra_labware)
# commands = run(protocol)

# for c in commands:
#     print(c)