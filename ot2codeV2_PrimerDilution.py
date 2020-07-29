# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 18:39:16 2020

@author: Trevor Ho
"""

from opentrons import protocol_api
import math

#%%

# metadata
metadata = {
    'protocolName': 'Primer Rehydration',
    'author': 'Trevor Y. H. Ho <trevor.ho@ed.ac.uk>',
    'description': ' Dilute 100 μM primers to 10 cM, uses instructions from \
        InstructionTranslator.py',
    'apiLevel': '2.5'
}

#%% 

def run(protocol: protocol_api.ProtocolContext):

    slots_map = {
            '2':'opentrons_24_tuberack_generic_2ml_screwcap',
            '3':'opentrons_24_tuberack_generic_2ml_screwcap',
            '5':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            '6':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            '7':'opentrons_6_tuberack_falcon_50ml_conical'
            }
    
    # Configure tip racks and pipette
    
    r_pipette_name = 'p300_single'
    r_tiprack_slots = ['4']
    r_tiprack_name = 'opentrons_96_tiprack_300ul'
    
    l_pipette_name = 'p10_single'
    l_tiprack_slots = ['1']
    l_tiprack_name = 'geb_96_tiprack_10ul'
    
    inst_list = [
        '20$2_A1->5_A1',
        '20$2_A2->5_A2',
        '20$2_A3->5_A3',
        '20$2_A4->5_A4',
        '20$2_A5->5_A5',
        '20$2_A6->5_A6',
        '20$2_B1->5_B1',
        '20$2_B2->5_B2',
        '20$2_B3->5_B3',
        '20$2_B4->5_B4',
        '20$2_B5->5_B5',
        '20$2_B6->5_B6',
        '20$2_C1->5_C1',
        '20$2_C2->5_C2',
        '20$2_C3->5_C3',
        '20$2_C4->5_C4',
        '20$2_C5->5_C5',
        '20$2_C6->5_C6',
        '20$2_D1->5_D1',
        '20$2_D2->5_D2',
        '20$2_D3->5_D3',
        '20$2_D4->5_D4',
        '20$2_D5->5_D5',
        '20$2_D6->5_D6',
        '20$3_A1->6_A1',
        '20$3_A2->6_A2',
        '20$3_A3->6_A3',
        '20$3_A4->6_A4',
        '20$3_A5->6_A5'
        ]
    
    labware_items = {}
    for slot, labware_item in slots_map.items():
        labware_items.update({slot:protocol.load_labware(labware_item, slot)})
    
    r_tip_racks = [protocol.load_labware(r_tiprack_name, slot) for slot in r_tiprack_slots]
    l_tip_racks = [protocol.load_labware(l_tiprack_name, slot) for slot in l_tiprack_slots]
    
    r_pipette = protocol.load_instrument(instrument_name = r_pipette_name,
        mount = 'right', tip_racks = r_tip_racks)
    l_pipette = protocol.load_instrument(instrument_name = l_pipette_name,
        mount = 'left', tip_racks = l_tip_racks)
    
    
    # First add 180 μL of water to each destination tube
    r_pipette.pick_up_tip()
    
    for inst in inst_list:
        path = inst.split('$')[1]
        dest = path.split('->')[1]
        dest_slot, dest_well = dest.split('_')
        
        r_pipette.aspirate(180, labware_items['7'].wells_by_name()['A1'])
        r_pipette.dispense(180, labware_items[dest_slot].wells_by_name()[dest_well].top(-5), rate=0.5)
        r_pipette.blow_out()
        
    r_pipette.drop_tip()
    
    # Then add the primer one by one
    
    for inst in inst_list:

        vol, path = inst.split('$')
        vol = int(vol)
        source, dest = path.split('->')
        source_slot, source_well = source.split('_')
        dest_slot, dest_well = dest.split('_')        

        pipette_times = math.ceil(vol/l_pipette.max_volume)
        
        l_pipette.pick_up_tip()

        for i in range(pipette_times):
            l_pipette.aspirate( (vol/pipette_times), labware_items[source_slot].wells_by_name()[source_well])
            l_pipette.dispense( (vol/pipette_times), labware_items[dest_slot].wells_by_name()[dest_well])
            l_pipette.blow_out()
        
        l_pipette.drop_tip()
   
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