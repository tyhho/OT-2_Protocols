# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 18:54:06 2020

@author: Trevor Ho

Simulates an OT-2 protocol
"""


from opentrons.simulate import simulate, format_runlog
protocol_file = open('ot2code_PlateConsolidation_v2.py')
# protocol_file = open('ot2code_test.py')
runlog = simulate(protocol_file, file_name='')
print(format_runlog(runlog[0]))
