# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 16:00:17 2020

@author: Trevor Ho
"""

from opentrons import protocol_api

# from opentrons.simulate import get_protocol_api
# protocol = get_protocol_api(version='2.2')

#%%

# metadata
metadata = {
    'protocolName': 'AND gate preparation',
    'author': 'Trevor Y. H. Ho <trevor.ho@ed.ac.uk>',
    'description': 'Select specific wells from different plates and consolidate \
    their contents onto a new plate in a user-defined order',
    'apiLevel': '2.2'
}
    

#%% Do not modify anything down here

def run(protocol: protocol_api.ProtocolContext):
    
    slots_map = {
            # '1':'biorad_96_wellplate_200ul_pcr',
            '2':'corning_96_wellplate_360ul_flat',
            '3':'corning_96_wellplate_360ul_flat',
            '6':'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap'
            }
    
    # Configure tip racks and pipette
    
    r_pipette_name = 'p300_single'
    r_tiprack_name = 'opentrons_96_tiprack_300ul'
    r_tiprack_slots = ['7']
        
    # l_pipette_name = 'p10_multi'
    # l_tiprack_name = 'geb_96_tiprack_10ul'
    # l_tiprack_slots = ['8']
    
    #%%
    deck = {}
    for slot, labware_name in slots_map.items():
        deck.update({slot:protocol.load_labware(labware_name, slot)})
    
    # l_tip_racks = [protocol.load_labware(l_tiprack_name, slot) for slot in l_tiprack_slots]
    r_tip_racks = [protocol.load_labware(r_tiprack_name, slot) for slot in r_tiprack_slots]
    
    # l_pipette = protocol.load_instrument(
    #     instrument_name = l_pipette_name,
    #     mount = 'left',
    #     tip_racks = l_tip_racks
#     )
    
    r_pipette = protocol.load_instrument(
        instrument_name = r_pipette_name,
        mount = 'right',
        tip_racks = r_tip_racks
        )
    #%%
    
    def pipette_medium(pipette, vol, source, dests):
        pipette.pick_up_tip()
        pipette.aspirate((vol + 50), source)
        
        for dest in dests:
            pipette.dispense(vol, dest)
            if dest != dests[-1]:
                pipette.aspirate(vol, source)
        
        pipette.dispense(100, source)
        pipette.blow_out()
        pipette.drop_tip()
    
    #%%
    
    # Produce range of wells for a single grid
    single_grid_well_list = list(range(0,4)) + list(range(8,12)) + list(range(16,20)) + list(range(24,28))
    medium_source_list = list(range(0,16))
    medium_mapper = dict(zip(medium_source_list,single_grid_well_list))
    
    
    # Dispense media for induction grid
    for medium_source_index, well_index in medium_mapper.items():
        
        medium_source = deck['6'].wells()[medium_source_index]
        
        wells_medium = []
        
        for dest_plate_slot in ['2','3']:
            wells_medium += [
                deck[dest_plate_slot].wells()[well_index],
                deck[dest_plate_slot].wells()[well_index+4],
                deck[dest_plate_slot].wells()[well_index+32],
                deck[dest_plate_slot].wells()[well_index+36]]
            
        pipette_medium(r_pipette, 198,  medium_source, wells_medium)
    
    # Dispense media for positive controls
    
    ctrl_medium_mapper = {
        20:64,
        21:72,
        22:80,
        23:88,
        }
    
    for medium_source_index, well_index in ctrl_medium_mapper.items():
        
        medium_source = deck['6'].wells()[medium_source_index]
        
        wells_medium = []
        
        for dest_plate_slot in ['2','3']:
            wells_medium += [
                deck[dest_plate_slot].wells()[well_index],
                deck[dest_plate_slot].wells()[well_index+1],
                deck[dest_plate_slot].wells()[well_index+2],
                deck[dest_plate_slot].wells()[well_index+3]]
            
        pipette_medium(r_pipette, 198,  medium_source, wells_medium)
    
    # Dispense media for autofluorescence controls
    
    medium_source = deck['6'].wells()[19]
    
    wells_medium = []
    
    for well_index in [67, 75]:
        for dest_plate_slot in ['2','3']:
            wells_medium += [deck[dest_plate_slot].wells()[well_index]]
            
    pipette_medium(r_pipette, 198,  medium_source, wells_medium)
    
    # Dispense media for autofluorescence controls
    
    wells_medium = []
    
    for well_index in [83, 91]:
        for dest_plate_slot in ['2','3']:
            wells_medium += [deck[dest_plate_slot].wells()[well_index]]
            
    pipette_medium(r_pipette, 200,  medium_source, wells_medium)

    return protocol.commands()
#%%
    
# print(*protocol.commands(), sep = '\n')

# The extra part: programmatically get a simulation ProtocolContext, so we can run this
# as a normal Python script and have everything in the run function get executed.
#
# This part should be removed or commented out before uploading to a real OT-2.

# from opentrons.simulate import get_protocol_api
# protocol = get_protocol_api(version=metadata['apiLevel'])
# cmds = run(protocol)
# print(*cmds, sep = '\n')