# -*- coding: utf-8 -*-
"""
Created on Tue May 14 17:46:57 2019

@author: Trevor Ho
"""

from opentrons import labware, instruments, robot

#%% Copy & Paste Arena

slots_map = {
        '5':'opentrons-tuberack-15_50ml',
        '2':'opentrons-tuberack-2ml-eppendorf',
        '3':'opentrons-tuberack-2ml-eppendorf',
        '4':'opentrons-tuberack-2ml-eppendorf'
        }

tip_slots = ['1']
tip_racks = [labware.load('tiprack-200ul', slot) for slot in tip_slots]

inst_list = [
'5_A3->2_A1_280',
'5_A3->2_A2_303',
'5_A3->2_A3_297',
'5_A3->2_A4_351',
'5_A3->2_A5_325',
'5_A3->2_A6_278',
'5_A3->2_B1_295',
'5_A3->2_B2_316',
'5_A3->2_B3_275',
'5_A3->2_B4_299',
'5_A3->2_B5_315',
'5_A3->2_B6_294',
'5_A3->2_C1_289',
'5_A3->2_C2_335',
'5_A3->2_C3_300',
'5_A3->2_C4_331',
'5_A3->2_C5_274',
'5_A3->2_C6_274',
'5_A3->2_D1_361',
'5_A3->2_D2_316',
'5_A3->2_D3_275',
'5_A3->2_D4_255',
'5_A3->2_D5_245',
'5_A3->2_D6_252',
'5_A3->3_A1_266',
'5_A3->3_A2_293',
'5_A3->3_A3_241',
'5_A3->3_A4_249',
'5_A3->3_A5_271',
'5_A3->3_A6_285',
'5_A3->3_B1_250',
'5_A3->3_B2_306',
'5_A3->3_B3_310',
'5_A3->3_B4_272',
'5_A3->3_B5_268',
'5_A3->3_B6_216',
'5_A3->3_C1_244',
'5_A3->3_C2_230',
'5_A3->3_C3_310',
'5_A3->3_C4_245',
'5_A3->3_C5_290',
'5_A3->3_C6_246',
'5_A3->3_D1_261',
'5_A3->3_D2_278',
'5_A3->3_D3_256',
'5_A3->3_D4_270',
'5_A3->3_D5_269',
'5_A3->3_D6_214',
'5_A3->4_A1_241'
            ]

#%% Do not modify anything down here

labware_items = {}
for slot, labware_item in slots_map.items():
    labware_items.update({slot:labware.load(labware_item, slot)})

p300S = instruments.P300_Single(
    mount='right',
    tip_racks=tip_racks
    )

for inst in inst_list:
    source, dest = inst.split('->')
    source_slot, source_well = source.split('_')
    dest_slot, dest_well, dest_vol = dest.split('_')
    dest_vol = int(dest_vol)

    p300S.transfer(
	dest_vol,
	labware_items[source_slot].wells(source_well),
	labware_items[dest_slot].wells(dest_well),
	new_tip='always',
    blow_out=True)
    #robot.pause()