# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 19:20:11 2020

@author: Trevor Ho
"""

from opentrons import protocol_api

#%%

# metadata
metadata = {
    'protocolName': 'Plate Consolidation',
    'author': 'Trevor Y. H. Ho <trevor.ho@ed.ac.uk>',
    'description': 'Select specific wells from different plates and consolidate \
    their contents onto a new plate in a user-defined order',
    'apiLevel': '2.0'
}
    

#%% Do not modify anything down here

def run(protocol: protocol_api.ProtocolContext):
    
    slots_map = {
            '1':'corning_96_wellplate_360ul_flat',
            '2':'corning_96_wellplate_360ul_flat',
            '3':'corning_96_wellplate_360ul_flat',
            '4':'corning_96_wellplate_360ul_flat',
            '5':'corning_96_wellplate_360ul_flat',
            '6':'corning_96_wellplate_360ul_flat',
            '7':'corning_96_wellplate_360ul_flat',
            '8':'corning_96_wellplate_360ul_flat'
            }
    
    # Configure tip racks and pipette
    
    pipette_name = 'p300_single'
    mount = 'right'
    tiprack_slots = ['10']
    tiprack_name = 'opentrons_96_tiprack_300ul' # other options: 'tiprack-10ul' / 'opentrons_96_tiprack_10ul' / 'opentrons_96_tiprack_300ul'
    
    transfer_vol = 150
    
    inst_list = {
        '2_H7':'8_A1',
        # '1_C2':'8_B1',
        # '2_G3':'8_C1',
        # '2_B1':'8_D1',
        # '2_A7':'8_E1',
        # '1_G6':'8_F1',
        # '2_A6':'8_G1',
        # '2_C9':'8_H1',
        # '1_D1':'8_A2',
        # '2_F5':'8_B2',
        # '2_B5':'8_C2',
        # '2_G11':'8_D2',
        # '1_F4':'8_E2',
        # '2_G1':'8_F2',
        # '2_H6':'8_G2',
        # '2_E12':'8_H2',
        # '2_H3':'8_A3',
        # '2_H5':'8_B3',
        # '2_H4':'8_C3',
        # '2_H11':'8_D3',
        # '2_D6':'8_E3',
        # '3_C10':'8_F3',
        # '3_H2':'8_G3',
        # '3_E10':'8_H3',
        # '4_E3':'8_A4',
        # '3_F4':'8_B4',
        # '4_C6':'8_C4',
        # '3_G1':'8_D4',
        # '4_C9':'8_E4',
        # '3_G4':'8_F4',
        # '4_F12':'8_G4',
        # '3_H5':'8_H4',
        # '4_E4':'8_A5',
        # '4_H7':'8_B5',
        # '4_B4':'8_C5',
        # '4_F11':'8_D5',
        # '4_D11':'8_E5',
        # '3_G8':'8_F5',
        # '3_A3':'8_G5',
        # '3_F7':'8_H5',
        # '3_B5':'8_A6',
        # '4_C7':'8_B6',
        # '4_E6':'8_C6',
        # '3_H3':'8_D6',
        # '4_C3':'8_E6',
        # '3_G12':'8_F6',
        # '3_D6':'8_G6',
        # '3_A11':'8_H6',
        # '3_E7':'8_A7',
        # '4_G8':'8_B7',
        # '4_A3':'8_C7',
        # '4_A5':'8_D7',
        # '6_D5':'8_E7',
        # '5_H10':'8_F7',
        # '5_G8':'8_G7',
        # '5_E3':'8_H7',
        # '5_F6':'8_A8',
        # '6_B8':'8_B8',
        # '6_G5':'8_C8',
        # '6_A9':'8_D8',
        # '5_E8':'8_E8',
        # '5_G12':'8_F8',
        # '5_G9':'8_G8',
        # '6_H1':'8_H8',
        # '6_F7':'8_A9',
        # '6_F9':'8_B9',
        # '6_C1':'8_C9',
        # '6_C2':'8_D9',
        # '7_B10':'8_E9',
        # '5_B12':'8_F9',
        # '5_C5':'8_G9',
        # '5_E1':'8_H9',
        # '6_A4':'8_A10',
        # '6_D4':'8_B10',
        # '7_B11':'8_C10',
        # '7_B4':'8_D10',
        # '6_B5':'8_E10',
        # '5_B3':'8_F10',
        # '6_D10':'8_G10',
        # '7_C1':'8_H10',
        # '5_B6':'8_A11',
        # '6_E10':'8_B11',
        # '5_B9':'8_C11',
        # '6_A6':'8_D11',
        # '5_C6':'8_E11',
        # '5_A5':'8_F11',
        # '6_C8':'8_G11',
        # '5_A7':'8_H11',
        # '6_A2':'8_A12'
                    }
    labware_items = {}
    for slot, labware_item in slots_map.items():
        labware_items.update({slot:protocol.load_labware(labware_item, slot)})

    tip_racks = [protocol.load_labware(tiprack_name, slot) for slot in tiprack_slots]
       
    pipette = protocol.load_instrument(
        instrument_name = pipette_name,
        mount = mount,
        tip_racks = tip_racks
        )

    for source, dest in inst_list.items():
    
        source_slot, source_well = source.split('_')
        dest_slot, dest_well = dest.split('_')
        
        pipette.transfer(
         	transfer_vol,
         	labware_items[source_slot].wells(source_well),
         	labware_items[dest_slot].wells(dest_well),
            blow_out = True,
         	new_tip='always')
        
        # pipette.pick_up_tip()
        # pipette.aspirate(transfer_vol, labware_items[source_slot].wells_by_name()[source_well])
        # pipette.dispense(transfer_vol, labware_items[dest_slot].wells_by_name()[dest_well])
        # pipette.blow_out()
        # pipette.drop_tip()
        
    print(*protocol.commands(), sep = '\n')

# The extra part: programmatically get a simulation ProtocolContext, so we can run this
# as a normal Python script and have everything in the run function get executed.
#
# This part should be removed or commented out before uploading to a real OT-2.

from opentrons.simulate import get_protocol_api
protocol = get_protocol_api(version=metadata['apiLevel'])
run(protocol)