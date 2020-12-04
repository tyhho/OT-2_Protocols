# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 18:14:33 2020

@author: s1635543
"""

from opentrons import protocol_api
import json
with open(r'C:\Users\s1635543\.opentrons\labware\v2\custom_definitions\Custom 96 Well Plate 350 µL.json') as labware_file:
    labware_def = json.load(labware_file)


#%%
metadata = {
    'protocolName': 'Test',
    'author': 'Trevor Ho',
    'source': 'Somewhere',
    'apiLevel': '2.2'
}

# import opentrons.execute
# protocol = opentrons.execute.get_protocol_api(version='2.2')
# well_plate = protocol.load_labware_from_definition(labware_def, 1)


#%%
def run(protocol: protocol_api.ProtocolContext):
    # tiprack =[protocol.load_labware('opentrons_96_tiprack_300ul', '1')]
    tiprack =[protocol.load_labware_from_definition(labware_def, location= '2')]

    
    print(tiprack)
    
    return(tiprack)
    
from opentrons.simulate import get_protocol_api
protocol = get_protocol_api(version=metadata["apiLevel"])
tiprack = run(protocol)

