# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 07:22:53 2020

@author: User
"""

from opentrons import simulate
protocol = simulate.get_protocol_api('2.2')

#%%
# from opentrons.protocols import types
# api_version = types.APIVersion(2,0)
# from opentrons import protocol_api
# protocol = protocol_api.ProtocolContext(api_version=api_version)
#%%



# metadata
metadata = {
    'protocolName': 'Plate Consolidation',
    'author': 'Trevor Y. H. Ho <trevor.ho@ed.ac.uk>',
    'description': 'Select specific wells from different plates and consolidate \
    their contents onto a new plate in a user-defined order',
    'apiLevel': '2.0'
}
    
#%%

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
    '1_C2':'8_B1',
    '2_G3':'8_C1',
    '2_B1':'8_D1',
    '2_A7':'8_E1'
                }
labware_items = {}
for slot, labware_item in slots_map.items():
    labware_items.update({slot:protocol.load_labware(labware_item, slot)})


#%%
tip_racks = [protocol.load_labware(tiprack_name, slot) for slot in tiprack_slots]
   
pipette = protocol.load_instrument(
    instrument_name = pipette_name,
    mount = mount,
    tip_racks = tip_racks
    )

for source, dest in inst_list.items():

    source_slot, source_well = source.split('_')
    dest_slot, dest_well = dest.split('_')
    
    # pipette.transfer(
    #  	transfer_vol,
    #  	labware_items[source_slot].wells(source_well),
    #  	labware_items[dest_slot].wells(dest_well),
    #     blow_out = True,
    #  	new_tip='always')
    
    pipette.pick_up_tip()
    pipette.aspirate(transfer_vol, labware_items[source_slot].wells_by_name()[source_well])
    pipette.dispense(transfer_vol, labware_items[dest_slot].wells_by_name()[dest_well])
    pipette.blow_out()
    pipette.drop_tip()

print(*protocol.commands(), sep = '\n')