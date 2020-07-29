# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 22:28:34 2020

@author: s1635543
"""

from opentrons import protocol_api


#%%

# metadata
metadata = {
    'protocolName': 'CLONE095_SrpR',
    'author': 'Trevor Y. H. Ho <trevor.ho@ed.ac.uk>',
    'description': 'Cherry pick SrpR constructs from glycerol stock plate',
    'apiLevel': '2.5'
}

#%% 

def run(protocol: protocol_api.ProtocolContext):

    slots_map = {
            '2':'corning_96_wellplate_360ul_flat',
            '3':'nest_96_wellplate_100ul_pcr_full_skirt'
            }
    
    # Configure tip racks and pipette
    
    pipette_name = 'p10_single'
    mount = 'left'
    tiprack_slots = ['1']
    tiprack_name = 'geb_96_tiprack_10ul'
    
    source_wells = [
        'B9',
        'C9',
        'A12',
        'A8',
        'A2',
        'A6',
        'B8',
        'B11',
        'A1',
        'A11',
        'B2',
        'C1',
        'B4',
        ]
    
    labware_items = {}
    for slot, labware_item in slots_map.items():
        labware_items.update({slot:protocol.load_labware(labware_item, slot)})
    
    tip_racks = [protocol.load_labware(tiprack_name, slot) for slot in tiprack_slots]
       
    pipette = protocol.load_instrument(
        instrument_name = pipette_name,
        mount = mount,
        tip_racks = tip_racks
        )
        
    for i, source_well in enumerate(source_wells):
        
        pipette.transfer(10,
                         labware_items['2'].wells_by_name()[source_well],
                         labware_items['3'].wells()[i].top(-15),
                         new_tip='always'
            )
       
    return protocol.commands()

# The extra part: programmatically get a simulation ProtocolContext, so we can run this
# as a normal Python script and have everything in the run function get executed.
#
# This part should be removed or commented out before uploading to a real OT-2.

#from opentrons.simulate import get_protocol_api
#protocol = get_protocol_api(version=metadata['apiLevel'])
#commands = run(protocol)
#
#for c in commands:
#    print(c)