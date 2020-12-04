# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 19:15:09 2020

@author: s1635543
"""

from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'My Protocol',
    'author': 'Name <email@address.com>',
    'description': 'Simple protocol to get started using OT2',
    'apiLevel': '2.0'
}

# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
def run(protocol: protocol_api.ProtocolContext):

    # labware
    
    slots_map = {
            '1':'corning_96_wellplate_360ul_flat',
            '2':'corning_96_wellplate_360ul_flat'
            }

    labware_items = {}
    for slot, labware_item in slots_map.items():
        labware_items.update({slot:protocol.load_labware(labware_item, slot)})
        
    # plate = protocol.load_labware('corning_96_wellplate_360ul_flat', '2')

    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', '3')

    # pipettes
    left_pipette = protocol.load_instrument(
         'p300_single', 'left', tip_racks=[tiprack])

    # commands
    left_pipette.pick_up_tip()
    left_pipette.aspirate(100, labware_items['1'].wells_by_name()['A1'])
    left_pipette.dispense(100, labware_items['1'].wells_by_name()['B2'])
    left_pipette.drop_tip()