# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 23:28:44 2020

@author: s1635543
"""

from opentrons import protocol_api

#%%

# metadata
metadata = {
    'protocolName': 'Colony Plating',
    'author': 'Trevor Y. H. Ho <trevor.ho@ed.ac.uk>',
    'description': 'Serially dilute transformed bacteria and plate \
        onto LB agar on single well plate',
    'apiLevel': '2.6'
}

#%% 

def transfer_n_mix(pipette, vol, source, dest, mix_vol):
    
    pipette.aspirate(vol, source)
    pipette.dispense(vol, dest)
    pipette.blow_out()
    pipette.move_to(dest.top(-13))
    
    for i in range(3):
        pipette.aspirate(mix_vol, dest)
        pipette.move_to(dest.top(-13))
        pipette.dispense(mix_vol, dest)
        pipette.blow_out()
        
    pipette.move_to(dest.top())


def run(protocol: protocol_api.ProtocolContext):

    slots_map = {
            '2':'corning_96_wellplate_360ul_flat',
            '4':'starlabpcrplateonws_96_wellplate_350ul',
            '7':'gbocellstaronewellagarplate_96_wellplate_10ul',
            }
    
    # Configure tip racks and pipette
    
    # r_pipette_name = 'p300_single'
    # r_tiprack_slots = ['4']
    # r_tiprack_name = 'opentrons_96_tiprack_300ul'
    
    l_pipette_name = 'p10_multi'
    l_tiprack_slots = ['11']
    l_tiprack_name = 'geb_96_tiprack_10ul'
    
    labware_items = {}
    for slot, labware_item in slots_map.items():
        labware_items.update({slot:protocol.load_labware(labware_item, slot)})
    
    # r_tip_racks = [protocol.load_labware(r_tiprack_name, slot) for slot in r_tiprack_slots]
    l_tip_racks = [protocol.load_labware(l_tiprack_name, slot) for slot in l_tiprack_slots]
    
    # r_pipette = protocol.load_instrument(instrument_name = r_pipette_name,
    #     mount = 'right', tip_racks = r_tip_racks)
    l_pipette = protocol.load_instrument(instrument_name = l_pipette_name,
        mount = 'left', tip_racks = l_tip_racks)
    
    #%% Serial dilution part
    
    # first dilution
    
    l_pipette.pick_up_tip()
    # transfer_n_mix(l_pipette,
    #                2, # transfer volume
    #                labware_items['2'].wells()[0], # source
    #                labware_items['4'].wells()[0], # dest
    #                10 # mix volume
    #                )
    
    # # subsequent dilution
    
    # for i in range(5):
    #     transfer_n_mix(l_pipette,
    #                     2, # transfer volume
    #                     labware_items['4'].wells()[i * 8], # source
    #                     labware_items['4'].wells()[(i + 1) * 8], # dest
    #                     10 # mix volume
    #                     )
    
    #%% Plating part

    for i in reversed(range(1,6)):
        l_pipette.transfer(2,
                           labware_items['4'].wells()[i * 8],
                           labware_items['7'].wells()[i * 8],
                           new_tip='never'
                           )
    
    l_pipette.drop_tip()
    
    
    #%%
    # Then execute the addition of samples
    
    # for inst in inst_list:

    #     vol, path = inst.split('$')
    #     vol = float(vol)
    #     source, dest = path.split('->')
    #     source_slot, source_well = source.split('_')
    #     dest_slot, dest_well = dest.split('_')        

    #     l_pipette.pick_up_tip()

    #     transfer_local_blow_out_no_change_tip(l_pipette, # pipette
    #                                           vol, # vol
    #                                           labware_items[source_slot].wells_by_name()[source_well], # source
    #                                           labware_items[dest_slot].wells_by_name()[dest_well].top(tube_height) # dest
    #                                           )
         
    #     l_pipette.drop_tip()
        
    return protocol.commands()

# The extra part: programmatically get a simulation ProtocolContext, so we can run this
# as a normal Python script and have everything in the run function get executed.
#
# This part should be removed or commented out before uploading to a real OT-2.

import json
extra_labware_list = [
    'starlabpcrplateonws_96_wellplate_350ul',
    'gbocellstaronewellagarplate_96_wellplate_10ul'
    ]

extra_labware = {}
for labware_name in extra_labware_list:
    labware_json_fn = labware_name + '.json'
    with open(labware_json_fn) as f: labware_data = json.load(f)
    extra_labware.update({labware_name:labware_data})

from opentrons.simulate import get_protocol_api
protocol = get_protocol_api(version=metadata['apiLevel'], extra_labware=extra_labware)
commands = run(protocol)

for c in commands:
    print(c)