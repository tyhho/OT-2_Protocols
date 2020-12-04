# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 18:41:16 2020

@author: Trevor Ho

"""


from opentrons import protocol_api

#%%

# metadata
metadata = {
    'protocolName': 'Batch Transformation Preparation',
    'author': 'Trevor Y. H. Ho <trevor.ho@ed.ac.uk>',
    'description': 'Mix and match plasmids for batch transformation. \
        Experiment IBM_FC038. \
        Requires InstructionWriter.py.',
    'apiLevel': '2.6'
}

#%% 

def transfer_local_blow_out(pipette, vol, source, dest):
    
    pipette.pick_up_tip()
    pipette.aspirate(vol, source)
    pipette.dispense(vol, dest)
    pipette.blow_out()
    pipette.drop_tip()
    
def run(protocol: protocol_api.ProtocolContext):

    slots_map = {
            '1':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            '2':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            '3':'starlabpcrwsstrips_96_wellplate_200ul',
            }
    
    # Configure tip racks and pipette
    
    r_pipette_name = 'p10_single'
    r_tiprack_slots = ['4']
    r_tiprack_name = 'geb_96_tiprack_10ul'
    
    # l_pipette_name = 'p10_single'
    # l_tiprack_slots = ['4']
    # l_tiprack_name = 'opentrons_96_tiprack_300ul'
    
    inst_list = [
        '1$2_A3->3_A1',
        '1$2_A4->3_A1',
        '1$2_A3->3_B1',
        '1$2_A4->3_B1',
        '1$2_A3->3_C1',
        '1$2_A5->3_C1',
        '1$1_A1->3_D1',
        '1$2_A4->3_D1',
        '1$1_A2->3_E1',
        '1$2_A4->3_E1',
        '1$1_A3->3_F1',
        '1$2_A4->3_F1',
        '1$1_A4->3_G1',
        '1$2_A4->3_G1',
        '1$1_A5->3_H1',
        '1$2_A4->3_H1',
        '1$1_A6->3_A2',
        '1$2_A4->3_A2',
        '1$1_B1->3_B2',
        '1$2_A4->3_B2',
        '1$1_B2->3_C2',
        '1$2_A4->3_C2',
        '1$1_B3->3_D2',
        '1$2_A4->3_D2',
        '1$1_B4->3_E2',
        '1$2_A4->3_E2',
        '1$1_B5->3_F2',
        '1$2_A4->3_F2',
        '1$1_B6->3_G2',
        '1$2_A4->3_G2',
        '1$1_C1->3_H2',
        '1$2_A4->3_H2',
        '1$2_A3->3_A3',
        '1$1_C2->3_A3',
        '1$2_A3->3_B3',
        '1$1_C3->3_B3',
        '1$2_A3->3_C3',
        '1$1_C4->3_C3',
        '1$2_A3->3_D3',
        '1$1_C5->3_D3',
        '1$2_A3->3_E3',
        '1$1_C6->3_E3',
        '1$2_A3->3_F3',
        '1$1_D1->3_F3',
        '1$2_A3->3_G3',
        '1$1_D2->3_G3',
        '1$2_A3->3_H3',
        '1$1_D3->3_H3',
        '1$2_A3->3_A4',
        '1$1_D4->3_A4',
        '1$2_A3->3_B4',
        '1$1_D5->3_B4',
        '1$2_A3->3_C4',
        '1$1_D6->3_C4',
        '1$2_A3->3_D4',
        '1$2_A1->3_D4',
        '1$2_A3->3_E4',
        '1$2_A2->3_E4',
        '1$1_A1->3_F4',
        '1$1_C2->3_F4',
        '1$1_A2->3_G4',
        '1$1_C3->3_G4',
        '1$1_A3->3_H4',
        '1$1_C4->3_H4',
        '1$1_A4->3_A5',
        '1$1_C5->3_A5',
        '1$1_A5->3_B5',
        '1$1_C6->3_B5',
        '1$1_A6->3_C5',
        '1$1_D1->3_C5',
        '1$1_B1->3_D5',
        '1$1_D2->3_D5',
        '1$1_B2->3_E5',
        '1$1_D3->3_E5',
        '1$1_B3->3_F5',
        '1$1_D4->3_F5',
        '1$1_B4->3_G5',
        '1$1_D5->3_G5',
        '1$1_B5->3_H5',
        '1$1_D6->3_H5',
        '1$1_B6->3_A6',
        '1$2_A1->3_A6',
        '1$1_C1->3_B6',
        '1$2_A2->3_B6'
        ]
    
    labware_items = {}
    for slot, labware_item in slots_map.items():
        labware_items.update({slot:protocol.load_labware(labware_item, slot)})
    
    r_tip_racks = [protocol.load_labware(r_tiprack_name, slot) for slot in r_tiprack_slots]
    # l_tip_racks = [protocol.load_labware(l_tiprack_name, slot) for slot in l_tiprack_slots]
    
    r_pipette = protocol.load_instrument(instrument_name = r_pipette_name,
        mount = 'right', tip_racks = r_tip_racks)
    # l_pipette = protocol.load_instrument(instrument_name = l_pipette_name,
        # mount = 'left', tip_racks = l_tip_racks)

    for inst in inst_list:

        vol, path = inst.split('$')
        vol = float(vol)
        source, dest = path.split('->')
        source_slot, source_well = source.split('_')
        dest_slot, dest_well = dest.split('_')        

        transfer_local_blow_out(r_pipette, # pipette
                                vol, # vol
                                labware_items[source_slot].wells_by_name()[source_well], # source
                                labware_items[dest_slot].wells_by_name()[dest_well] # dest
                                )

    return protocol.commands()

# The extra part: programmatically get a simulation ProtocolContext, so we can run this
# as a normal Python script and have everything in the run function get executed.
#
# This part should be removed or commented out before uploading to a real OT-2.

# import json
# extra_labware_list = [
#     'starlabpcrwsstrips_96_wellplate_200ul',
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