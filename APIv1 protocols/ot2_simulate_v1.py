# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 14:48:13 2020

@author: Trevor Ho
"""

# imports
from opentrons import labware, instruments, robot

# metadata
metadata = {
    'protocolName': 'My Protocol',
    'author': 'Name <email@address.com>',
    'description': 'Simple protocol to get started using OT2',
}

# labware
plate = labware.load('96-flat', '2')
tiprack = labware.load('opentrons_96_tiprack_300ul', '1')

# pipettes
pipette = instruments.P300_Single(mount='left', tip_racks=[tiprack])

# commands
pipette.transfer(100, plate.wells('A1'), plate.wells('B2'))

for c in robot.commands():
    print(c)