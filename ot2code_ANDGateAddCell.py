# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 00:20:58 2020

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
            '1':'biorad_96_wellplate_200ul_pcr',
            '2':'corning_96_wellplate_360ul_flat',
            '3':'corning_96_wellplate_360ul_flat',
            '6':'corning_96_wellplate_360ul_flat'
             }
    
    # Configure tip racks and pipette
    
    # r_pipette_name = 'p300_single'
    # r_tiprack_name = 'opentrons_96_tiprack_300ul'
    # r_tiprack_slots = ['7']
        
    l_pipette_name = 'p10_multi'
    l_tiprack_name = 'geb_96_tiprack_10ul'
    l_tiprack_slots = ['8']
    
    #%%
    deck = {}
    for slot, labware_name in slots_map.items():
        deck.update({slot:protocol.load_labware(labware_name, slot)})
    
    l_tip_racks = [protocol.load_labware(l_tiprack_name, slot) for slot in l_tiprack_slots]
    # r_tip_racks = [protocol.load_labware(r_tiprack_name, slot) for slot in r_tiprack_slots]
    
    l_pipette = protocol.load_instrument(
        instrument_name = l_pipette_name,
        mount = 'left',
        tip_racks = l_tip_racks
        )
    
    # r_pipette = protocol.load_instrument(
    #     instrument_name = r_pipette_name,
    #     mount = 'right',
    #     tip_racks = r_tip_racks
    #     )
    #%%
        
    def distributeCell(pipette,vol,source,dests,waste):
        pipette.pick_up_tip()
        pipette.aspirate((vol*4 + 2), source)
        for dest in dests:
            pipette.dispense(vol, dest)
        pipette.dispense(2, waste)
        pipette.blow_out()
        pipette.drop_tip()
    
    #%%
    
    # Mapper
    cell_mapper  = {
        'A1':['A4','A3','A2','A1'],
        'A3':['A8','A7','A6','A5'],
        'A5':['A4','A3','A2','A1'],
        'A7':['A8','A7','A6','A5']
        }
    
    waste = deck['6'].wells_by_name()['A1']
    
    for source_well_name, dest_wells_names in cell_mapper.items():
        
        source = deck['1'].wells_by_name()[source_well_name]
        
        if source_well_name == 'A1' or source_well_name == 'A3':
            dest_slot = '2'
        elif source_well_name == 'A5' or source_well_name == 'A7':
            dest_slot = '3'
        
        dest_wells = []
        for dest_well_name in dest_wells_names:
            dest_wells.append(
                deck[dest_slot].wells_by_name()[dest_well_name]
                )
        
        distributeCell(l_pipette,2,
                       source,
                       dest_wells,
                       waste)

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