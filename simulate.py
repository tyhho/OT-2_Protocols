# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 15:51:36 2019

@author: s1635543
"""

from opentrons import labware, instruments

import opentrons.simulate
protocol_file = open('ot2inst_SerialDilution.py')
runlog = opentrons.simulate.simulate(protocol_file)
print(opentrons.simulate.format_runlog(runlog))