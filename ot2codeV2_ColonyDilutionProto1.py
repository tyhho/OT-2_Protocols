# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 23:28:44 2020

@author: s1635543
"""

from opentrons import protocol_api

#%%

# metadata
metadata = {
    'protocolName': 'Colony Dilution Prototype',
    'author': 'Trevor Y. H. Ho <trevor.ho@ed.ac.uk>',
    'description': 'Serially dilute transformed bacteria on 96-well plate \
        Prototype: Test change tip between each transfer and no change of tip',
    'apiLevel': '2.6'
}

#%% 

def transfer_n_mix(protocol, pipette, vol, source, dest, mix_vol, change_tip=False):
    
    if change_tip == True:
        pipette.pick_up_tip()
    
    pipette.aspirate(vol, source)
    # pipette.move_to(source.top())
    # protocol.pause()
    pipette.dispense(vol, dest)
    pipette.move_to(dest.top())
    # pipette.aspirate(mix_vol, dest.top())
    # pipette.dispense(mix_vol, dest.top())
    protocol.delay(seconds=1)
    
    for i in range(3):
        pipette.aspirate(mix_vol, dest)
        pipette.dispense(mix_vol, dest)
        
    if change_tip == True:
        pipette.drop_tip()
    else:
        pipette.move_to(dest.top(-2))
        protocol.delay(seconds=1)
        
def run(protocol: protocol_api.ProtocolContext):

    slots_map = {
            '1':'corning_96_wellplate_360ul_flat',
            '4':'starlabpcrplateonws_96_wellplate_350ul', # no change tip
            # '5':'starlabpcrplateonws_96_wellplate_350ul', # change tip
            # '7':'gbocellstaronewellagarplate_96_wellplate_10ul',
            }
    
    # Configure tip racks and pipette
    
    # r_pipette_name = 'p50_multi'
    # r_tiprack_slots = ['2']
    # r_tiprack_name = 'opentrons_96_tiprack_300ul'
    
    l_pipette_name = 'p10_multi'
    l_tiprack_slots = ['2']
    l_tiprack_name = 'geb_96_tiprack_10ul'
    
    labware_items = {}
    for slot, labware_item in slots_map.items():
        labware_items.update({slot:protocol.load_labware(labware_item, slot)})
    
    # r_tip_racks = [protocol.load_labware(r_tiprack_name, slot) for slot in r_tiprack_slots]
    l_tip_racks = [protocol.load_labware(l_tiprack_name, slot) for slot in l_tiprack_slots]
    
    # r_pipette = protocol.load_instrument(instrument_name = r_pipette_name,
        # mount = 'right', tip_racks = r_tip_racks)
    l_pipette = protocol.load_instrument(instrument_name = l_pipette_name,
        mount = 'left', tip_racks = l_tip_racks)
    
    
    # Serial dilution part
    
    #%% mode 1: plate 4: no change tip (1 min 19 secs per plate)
    
    # first dilution
    l_pipette.pick_up_tip()
    transfer_n_mix(protocol,
                    l_pipette,
                    2, # transfer volume
                    labware_items['1'].wells()[40], # source
                    labware_items['4'].wells()[0], # dest
                    10, # mix volume
                    False
                    )
    
    # subsequent dilution
    
    for i in range(11):
        transfer_n_mix(protocol,
                        l_pipette,
                        2, # transfer volume
                        labware_items['4'].wells()[i * 8], # source
                        labware_items['4'].wells()[(i + 1) * 8], # dest
                        10, # mix volume
                        False
                        )
    l_pipette.drop_tip()
    
    #%% mode 2: plate 5: change tip (8 min 19 secs)
    
    # # first dilution
    # transfer_n_mix(protocol,
    #                l_pipette,
    #             2, # transfer volume
    #             labware_items['1'].wells()[0], # source
    #             labware_items['4'].wells()[0], # dest
    #             10, # mix volume
    #             True
    #             )
    
    # # subsequent dilution
    
    # for i in range(11):
    #     transfer_n_mix(protocol,
    #                    l_pipette,
    #                     2, # transfer volume
    #                     labware_items['4'].wells()[i * 8], # source
    #                     labware_items['4 '].wells()[(i + 1) * 8], # dest
    #                     10, # mix volume
    #                     True
    #                     )
    
#%%    
        
    return protocol.commands()

# The extra part: programmatically get a simulation ProtocolContext, so we can run this
# as a normal Python script and have everything in the run function get executed.
#
# This part should be removed or commented out before uploading to a real OT-2.

# import json
# extra_labware_list = [
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