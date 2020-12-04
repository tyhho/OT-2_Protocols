# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 17:48:33 2020

@author: Trevor Ho
"""

from opentrons import protocol_api

#%%

# metadata
metadata = {
    'protocolName': 'Cell Mass Transfer',
    'author': 'Trevor Y. H. Ho <trevor.ho@ed.ac.uk>',
    'description': 'Transfer cells from 96-well deep well plate into Epp tubes, diff vol to standardize cell mass',
    'apiLevel': '2.6'
}

#%% Do not modify anything down here

def run(protocol: protocol_api.ProtocolContext):
    
    slots_map = {
            '4':'nest_96_wellplate_2ml_deep',
            '1':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            '2':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            '3':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap'
            }
    
    # Configure tip racks and pipette
    
    r_pipette_name = 'p300_single'
    r_tiprack_slots = ['5']
    r_tiprack_name = 'opentrons_96_tiprack_300ul'
    
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
    
    inst_list = [
    # '435$4_A1->1_A1',
    '533$4_B1->1_A2',
    '451$4_C1->1_A3',
    '446$4_D1->1_A4',
    '435$4_E1->1_A5',
    '471$4_F1->1_A6',
    '536$4_G1->1_B1',
    '509$4_H1->1_B2',
    # '423$4_A4->1_B3',
    '466$4_B4->1_B4',
    '453$4_C4->1_B5',
    '484$4_D4->1_B6',
    '484$4_E4->1_C1',
    '425$4_F4->1_C2',
    # '1361$4_G4->1_C3',
    '508$4_H4->1_C4',
    '452$4_A2->2_A1',
    '539$4_B2->2_A2',
    '453$4_C2->2_A3',
    '460$4_D2->2_A4',
    '433$4_E2->2_A5',
    '476$4_F2->2_A6',
    '466$4_G2->2_B1',
    '498$4_H2->2_B2',
    '415$4_A5->2_B3',
    '444$4_B5->2_B4',
    '423$4_C5->2_B5',
    '458$4_D5->2_B6',
    '445$4_E5->2_C1',
    '435$4_F5->2_C2',
    '462$4_G5->2_C3',
    '484$4_H5->2_C4',
    '417$4_A3->3_A1',
    '546$4_B3->3_A2',
    '453$4_C3->3_A3',
    '451$4_D3->3_A4',
    '447$4_E3->3_A5',
    '457$4_F3->3_A6',
    '437$4_G3->3_B1',
    '498$4_H3->3_B2',
    '424$4_A6->3_B3',
    '458$4_B6->3_B4',
    '432$4_C6->3_B5',
    '465$4_D6->3_B6',
    '416$4_E6->3_C1',
    '429$4_F6->3_C2',
    '466$4_G6->3_C3',
    '477$4_H6->3_C4'
                    ]

    for inst in inst_list:
        
        vol, path = inst.split('$')
        vol = float(vol)
        source, dest = path.split('->')
        source_slot, source_well = source.split('_')
        dest_slot, dest_well = dest.split('_')
        
        r_pipette.transfer(
         	vol,
         	labware_items[source_slot].wells_by_name()[source_well].top(-38),
         	labware_items[dest_slot].wells_by_name()[dest_well],
         	new_tip='once')
        
    return protocol.commands()

# The extra part: programmatically get a simulation ProtocolContext, so we can run this
# as a normal Python script and have everything in the run function get executed.

# This part should be removed or commented out before uploading to a real OT-2.

# from opentrons.simulate import get_protocol_api
# protocol = get_protocol_api(version=metadata['apiLevel'])
# commands = run(protocol)

# for c in commands:
#     print(c)