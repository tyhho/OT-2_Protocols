# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 03:23:40 2020

@author: Trevor Ho
"""

from opentrons import protocol_api

#%%

# metadata
metadata = {
    'protocolName': '0.3mL TipRacK Test',
    'author': 'Trevor Y. H. Ho <trevor.ho@ed.ac.uk>',
    'description': 'Test the function of 3D printed 300 µL tip rack with P50 multi-channel',
    'apiLevel': '2.7'
}

#%% Do not modify anything down here

def run(protocol: protocol_api.ProtocolContext):
    
    slots_map = {
            '2':'corning_96_wellplate_360ul_flat',

            }
    
    # Configure tip racks and pipette
    
    r_pipette_name = 'p50_multi'
    r_tiprack_slots = ['3']
    # r_tiprack_name = 'opentrons_96_tiprack_300ul'
    r_tiprack_name = 'tipone_96_diytiprack_300ul'
    
    # l_pipette_name = 'p10_multi'
    # l_tiprack_slots = ['2']
    # l_tiprack_name = 'geb_96_tiprack_10ul'
    
    labware_items = {}
    for slot, labware_item in slots_map.items():
        labware_items.update({slot:protocol.load_labware(labware_item, slot)})
    
    r_tip_racks = [protocol.load_labware(r_tiprack_name, slot) for slot in r_tiprack_slots]
    # l_tip_racks = [protocol.load_labware(l_tiprack_name, slot) for slot in l_tiprack_slots]
    
    r_pipette = protocol.load_instrument(instrument_name = r_pipette_name,
        mount = 'right', tip_racks = r_tip_racks)
    # l_pipette = protocol.load_instrument(instrument_name = l_pipette_name,
        # mount = 'left', tip_racks = l_tip_racks)
    
    for i in range(12):
        
        r_pipette.pick_up_tip()
        r_pipette.aspirate(50, labware_items['2'].wells_by_name()['A1'])
        r_pipette.move_to(labware_items['2'].wells_by_name()['A1'].top())        
        protocol.delay(seconds=1)
        r_pipette.dispense(50, labware_items['2'].wells_by_name()['A1'])
        r_pipette.blow_out()
        protocol.delay(seconds=0.5)
        r_pipette.drop_tip()
        
    return protocol.commands()