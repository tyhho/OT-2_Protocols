# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 21:25:40 2020

@author: s1635543
"""

# The normal part: write the protocol as if it were being uploaded to the Opentrons App.

from opentrons import protocol_api

metadata = {
    'protocolName': 'My Protocol',
    'author': 'Name <email@address.com>',
    'description': 'Simple protocol to get started using OT2',
    'apiLevel': '2.0'
}

def run(protocol: protocol_api.ProtocolContext):
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', '2')
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', '1')
    
    left_pipette = protocol.load_instrument(
         'p300_single', 'left', tip_racks=[tiprack])

    left_pipette.pick_up_tip()
    left_pipette.aspirate(100, plate['A1'])
    left_pipette.dispense(100, plate['B2'])
    left_pipette.drop_tip()


# The extra part: programmatically get a simulation ProtocolContext, so we can run this
# as a normal Python script and have everything in the run function get executed.
#
# This part should be removed or commented out before uploading to a real OT-2.
from opentrons.simulate import get_protocol_api
protocol = get_protocol_api(version=metadata["apiLevel"])
run(protocol)