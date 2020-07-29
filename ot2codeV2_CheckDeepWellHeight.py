# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 19:49:04 2020

@author: s1635543
"""

from opentrons import protocol_api

#%%

# metadata
metadata = {
    'protocolName': 'Check 96 well plate height',
    'author': 'Trevor Y. H. Ho <trevor.ho@ed.ac.uk>',
    'description': 'Select specific wells from different plates and consolidate \
    their contents onto a new plate in a user-defined order',
    'apiLevel': '2.5'
}

#%% Do not modify anything down here

def run(protocol: protocol_api.ProtocolContext):
    
    slots_map = {
            '3':'nest_96_wellplate_2ml_deep'
            }
    
    # Configure tip racks and pipette
    
    pipette_name = 'p10_single'
    mount = 'left'
    tiprack_slots = ['4']
    tiprack_name = 'geb_96_tiprack_10ul'
    
    labware_items = {}
    for slot, labware_item in slots_map.items():
        labware_items.update({slot:protocol.load_labware(labware_item, slot)})

    tip_racks = [protocol.load_labware(tiprack_name, slot) for slot in tiprack_slots]
       
    pipette = protocol.load_instrument(
        instrument_name = pipette_name,
        mount = mount,
        tip_racks = tip_racks
        )
    
    pipette.move_to(labware_items['3'].wells_by_name()['H12'].top(-15))
    protocol.pause('Check level')
    pipette.transfer(10,
                     labware_items['3'].wells_by_name()['H12'].top(-15),
                     labware_items['3'].wells_by_name()['H12'].top(-15)        
        )

    
    return protocol.commands()

# The extra part: programmatically get a simulation ProtocolContext, so we can run this
# as a normal Python script and have everything in the run function get executed.
#
# This part should be removed or commented out before uploading to a real OT-2.

# from opentrons.simulate import get_protocol_api
# protocol = get_protocol_api(version=metadata['apiLevel'])
# commands = run(protocol)

# for c in commands:
#     print(c)
