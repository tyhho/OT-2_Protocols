# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 00:46:49 2020

@author: Trevor Ho
"""

from opentrons import protocol_api

#%%

# metadata
metadata = {
    'protocolName': 'Batch PCR',
    'author': 'Trevor Y. H. Ho <trevor.ho@ed.ac.uk>',
    'description': 'Mix and match primers and templates for setting up \
        bacth PCR reactions, depends on InstructionTranslator.py',
    'apiLevel': '2.5'
}

#%% 

def transfer_local_blow_out_no_change_tip(pipette, vol, source, dest):
    
    pipette.aspirate(vol, source)
    pipette.dispense(vol, dest)
    pipette.blow_out()
    

tube_height = -15

def run(protocol: protocol_api.ProtocolContext):

    slots_map = {
            '1':'starlabpcrwsstrips_96_wellplate_200ul',
            '2':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            '3':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            }
    
    # Configure tip racks and pipette
    
    # r_pipette_name = 'p300_single'
    # r_tiprack_slots = ['4']
    # r_tiprack_name = 'opentrons_96_tiprack_300ul'
    
    l_pipette_name = 'p10_single'
    l_tiprack_slots = ['4','5']
    l_tiprack_name = 'geb_96_tiprack_10ul'
    
    inst_list = [
        '1$3_D3->1_A1',
        '2.5$2_A6->1_A1',
        '2.5$2_B1->1_A1',
        '1$3_A1->1_A2',
        '2.5$2_B2->1_A2',
        '2.5$2_B3->1_A2',
        '1$3_A5->1_A3',
        '2.5$2_B2->1_A3',
        '2.5$2_B3->1_A3',
        '1$3_B1->1_A4',
        '2.5$2_B2->1_A4',
        '2.5$2_B3->1_A4',
        '1$3_B3->1_A5',
        '2.5$2_B2->1_A5',
        '2.5$2_B3->1_A5',
        '1$3_B5->1_A6',
        '2.5$2_B2->1_A6',
        '2.5$2_B3->1_A6',
        '1$3_A3->1_A7',
        '2.5$2_B2->1_A7',
        '2.5$2_B3->1_A7',
        '1$3_A2->1_A8',
        '2.5$2_B2->1_A8',
        '2.5$2_B3->1_A8',
        '1$3_A6->1_B1',
        '2.5$2_B2->1_B1',
        '2.5$2_B3->1_B1',
        '1$3_B2->1_B2',
        '2.5$2_B2->1_B2',
        '2.5$2_B3->1_B2',
        '1$3_B4->1_B3',
        '2.5$2_B2->1_B3',
        '2.5$2_B3->1_B3',
        '1$3_B6->1_B4',
        '2.5$2_B2->1_B4',
        '2.5$2_B3->1_B4',
        '1$3_A4->1_B5',
        '2.5$2_B2->1_B5',
        '2.5$2_B3->1_B5',
        '1$3_C1->1_B9',
        '2.5$2_A4->1_B9',
        '2.5$2_B4->1_B9',
        '1$3_A2->1_C1',
        '2.5$2_A5->1_C1',
        '2.5$2_A3->1_C1',
        '1$3_A6->1_C2',
        '2.5$2_A5->1_C2',
        '2.5$2_A3->1_C2',
        '1$3_B2->1_C3',
        '2.5$2_A5->1_C3',
        '2.5$2_A3->1_C3',
        '1$3_B4->1_C4',
        '2.5$2_A5->1_C4',
        '2.5$2_A3->1_C4',
        '1$3_B6->1_C5',
        '2.5$2_A5->1_C5',
        '2.5$2_A3->1_C5',
        '1$3_A4->1_C6',
        '2.5$2_A5->1_C6',
        '2.5$2_A3->1_C6',
        '1$3_C6->1_D1',
        '2.5$2_B5->1_D1',
        '2.5$2_B6->1_D1',
        '1$3_D1->1_D2',
        '2.5$2_B5->1_D2',
        '2.5$2_B6->1_D2',
        '1$3_D2->1_D3',
        '2.5$2_B5->1_D3',
        '2.5$2_B6->1_D3',
        '1$3_C6->1_D4',
        '2.5$2_B5->1_D4',
        '2.5$2_C1->1_D4',
        '1$3_D1->1_D5',
        '2.5$2_B5->1_D5',
        '2.5$2_C1->1_D5',
        '1$3_D2->1_D6',
        '2.5$2_B5->1_D6',
        '2.5$2_C1->1_D6',
        '1$3_C2->1_E1',
        '2.5$2_C2->1_E1',
        '2.5$2_C3->1_E1',
        '1$3_C3->1_E2',
        '2.5$2_C2->1_E2',
        '2.5$2_C3->1_E2',
        '1$3_C4->1_E3',
        '2.5$2_C2->1_E3',
        '2.5$2_C3->1_E3',
        '1$3_C5->1_E4',
        '2.5$2_C2->1_E4',
        '2.5$2_C3->1_E4',
        '1$3_C2->1_E5',
        '2.5$2_C2->1_E5',
        '2.5$2_A1->1_E5',
        '1$3_C3->1_E6',
        '2.5$2_C2->1_E6',
        '2.5$2_A1->1_E6',
        '1$3_C4->1_E7',
        '2.5$2_C2->1_E7',
        '2.5$2_A1->1_E7',
        '1$3_C5->1_E8',
        '2.5$2_C2->1_E8',
        '2.5$2_A1->1_E8',
        '1$3_C2->1_E9',
        '2.5$2_A2->1_E9',
        '2.5$2_C3->1_E9'
        ]
    
    labware_items = {}
    for slot, labware_item in slots_map.items():
        labware_items.update({slot:protocol.load_labware(labware_item, slot)})
    
    # r_tip_racks = [protocol.load_labware(r_tiprack_name, slot) for slot in r_tiprack_slots]
    l_tip_racks = [protocol.load_labware(l_tiprack_name, slot) for slot in l_tiprack_slots]
    
    # r_pipette = protocol.load_instrument(instrument_name = r_pipette_name,
    #     mount = 'right', tip_racks = r_tip_racks)
    l_pipette = protocol.load_instrument(instrument_name = l_pipette_name,
        mount = 'left', tip_racks = l_tip_racks)
    
    
    # First add 4 μL of water to each destination tube
#    l_pipette.pick_up_tip()
    
#    for inst in inst_list:
#        path = inst.split('$')[1]
#        dest = path.split('->')[1]
#        dest_slot, dest_well = dest.split('_')
        
#        transfer_local_blow_out_no_change_tip(l_pipette, # pipette
#                                              4, # vol
#                                              labware_items['3'].wells_by_name()['D6'], # water source
#                                              labware_items[dest_slot].wells_by_name()[dest_well].top(tube_height) # dest
#                                              )
 
#    l_pipette.drop_tip()
    
    # Then execute the addition of samples
    
    for inst in inst_list:

        vol, path = inst.split('$')
        vol = float(vol)
        source, dest = path.split('->')
        source_slot, source_well = source.split('_')
        dest_slot, dest_well = dest.split('_')        

        l_pipette.pick_up_tip()

        transfer_local_blow_out_no_change_tip(l_pipette, # pipette
                                              vol, # vol
                                              labware_items[source_slot].wells_by_name()[source_well], # source
                                              labware_items[dest_slot].wells_by_name()[dest_well].top(tube_height) # dest
                                              )
         
        l_pipette.drop_tip()
        
    return protocol.commands()

# The extra part: programmatically get a simulation ProtocolContext, so we can run this
# as a normal Python script and have everything in the run function get executed.
#
# This part should be removed or commented out before uploading to a real OT-2.

# import json
# extra_labware_list = [
#     'starlabpcrwsstrips_96_wellplate_200ul'
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