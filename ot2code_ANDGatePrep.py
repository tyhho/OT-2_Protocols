# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 16:00:17 2020

@author: Trevor Ho
"""

# from opentrons import protocol_api

from opentrons.simulate import get_protocol_api
protocol = get_protocol_api(version='2.2')

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

# def run(protocol: protocol_api.ProtocolContext):
    
slots_map = {
        '1':'corning_96_wellplate_360ul_flat',
        '2':'corning_96_wellplate_360ul_flat',
        '3':'corning_96_wellplate_360ul_flat',
        '6':'opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap'
        }

# Configure tip racks and pipette

r_pipette_name = 'p300_single'
r_tiprack_name = 'opentrons_96_tiprack_300ul'
r_tiprack_slots = ['7']
    
l_pipette_name = 'p10_multi'
l_tiprack_name = 'geb_96_tiprack_10ul'
l_tiprack_slots = ['8']

#%%
deck = {}
for slot, labware_name in slots_map.items():
    deck.update({slot:protocol.load_labware(labware_name, slot)})

l_tip_racks = [protocol.load_labware(l_tiprack_name, slot) for slot in l_tiprack_slots]
r_tip_racks = [protocol.load_labware(r_tiprack_name, slot) for slot in r_tiprack_slots]

l_pipette = protocol.load_instrument(
    instrument_name = l_pipette_name,
    mount = 'left',
    tip_racks = l_tip_racks
    )

r_pipette = protocol.load_instrument(
    instrument_name = r_pipette_name,
    mount = 'right',
    tip_racks = r_tip_racks
    )
#%%
# Produce range of wells for a single grid
single_grid_well_list = list(range(0,4)) + list(range(8,12)) + list(range(16,20)) + list(range(32,36))


wells_medium = []

for well_index in single_grid_well_list:
    
    for medium_slot in [2,3]:
        wells_medium += [
            deck[medium_slot].wells(well_index),
            deck[medium_slot].wells(well_index+4),
            deck[medium_slot].wells(well_index+32),
            deck[medium_slot].wells(well_index+36)]

def pipette_medium(pipette, source, dests, )

#%%
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

# from opentrons.simulate import get_protocol_api
# protocol = get_protocol_api(version=metadata['apiLevel'])
# run(protocol)