# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 19:13:03 2020

@author: s1635543
"""

from opentrons import protocol_api

#%%

# metadata
metadata = {
    'protocolName': 'Glycerol stocks preparation',
    'author': 'Trevor Y. H. Ho <trevor.ho@ed.ac.uk>',
    'description': 'Select specific wells from different plates and consolidate \
    their contents onto a new plate in a user-defined order',
    'apiLevel': '2.5'
}

#%% Do not modify anything down here

def run(protocol: protocol_api.ProtocolContext):
    
    slots_map = {
            '1':'corning_96_wellplate_360ul_flat',
            '2':'corning_96_wellplate_360ul_flat',
            '3':'nest_96_wellplate_2ml_deep'
            }
    
    # Configure tip racks and pipette
    
    pipette_name = 'p10_single'
    mount = 'left'
    tiprack_slots = ['4']
    tiprack_name = 'geb_96_tiprack_10ul'
    
    inst_list = [
        '2$1_C4->3_A1',
        '2$1_E9->3_A2',
        '2$1_C10->3_A3',
        '2$1_G3->3_A4',
        '2$1_D1->3_A5',
        '2$1_H9->3_A6',
        '2$1_F7->3_A7',
        '2$1_C1->3_A8',
        '2$1_G6->3_A9',
        '2$1_H6->3_A10',
        '2$1_F3->3_A11',
        '2$1_B4->3_A12',
        '2$1_H1->3_B1',
        '2$1_F8->3_B2',
        '2$1_A1->3_B3',
        '2$1_D2->3_B4',
        '2$1_B1->3_B5',
        '2$1_G2->3_B6',
        '2$1_C3->3_B7',
        '2$1_F11->3_B8',
        '2$1_B3->3_B9',
        '2$1_C7->3_B10',
        '2$2_B9->3_B11',
        '2$2_C9->3_B12',
        '2$2_A12->3_C1',
        '2$2_A8->3_C2',
        '2$2_A2->3_C3',
        '2$2_A6->3_C4',
        '2$2_B8->3_C5',
        '2$2_B11->3_C6',
        '2$2_A1->3_C7',
        '2$2_A11->3_C8',
        '2$2_B2->3_C9',
        '2$2_C1->3_C10',
        '2$2_B4->3_C11'
                    ]
    
    labware_items = {}
    for slot, labware_item in slots_map.items():
        labware_items.update({slot:protocol.load_labware(labware_item, slot)})

    tip_racks = [protocol.load_labware(tiprack_name, slot) for slot in tiprack_slots]
       
    pipette = protocol.load_instrument(
        instrument_name = pipette_name,
        mount = mount,
        tip_racks = tip_racks
        )

    for inst in inst_list:
        
        vol, path = inst.split('$')
        vol = int(vol)
        source, dest = path.split('->')
        source_slot, source_well = source.split('_')
        dest_slot, dest_well = dest.split('_')
        
        pipette.transfer(
         	vol,
         	labware_items[source_slot].wells_by_name()[source_well],
         	labware_items[dest_slot].wells_by_name()[dest_well].top(-30),
         	new_tip='always')
        
        # pipette.pick_up_tip()
        # pipette.aspirate(transfer_vol, labware_items[source_slot].wells_by_name()[source_well])
        # pipette.dispense(transfer_vol, labware_items[dest_slot].wells_by_name()[dest_well])
        # pipette.blow_out()
        # pipette.drop_tip()
        
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