# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 18:30:15 2019

@author: s1635543
"""

'''Induction into medium with ON and OFF'''
from opentrons import labware, instruments,robot


robot.clear_commands()

# Distribute function without blowout
def distributeNoBlowOut(pipette,vol_in,vol_out,source,dests):
    pipette.pick_up_tip()
    pipette.aspirate(vol_in,source)
    for dest in dests:
        pipette.dispense(vol_out,dest)
    pipette.drop_tip()


# TODO: Load labwares
tip_slots = ['1','2']


plate_slots = ['4','5','7','8','10','11']

plates_dict = {}
for slot in plate_slots:
    plates_dict[slot] = labware.load('96-flat', slot)

tip_racks = [labware.load('tiprack-200ul', slot) for slot in tip_slots]

slot_map = {
        '4':['7','10']
#        '5':['8','11']
             }
p50multi = instruments.P50_Multi(
    mount='right',
    tip_racks=tip_racks)


for source_slot, dest_slots in slot_map.items():
        source_plate = plates_dict[source_slot]
        dest_plate1 = plates_dict[dest_slots[0]]
        dest_plate2 = plates_dict[dest_slots[1]]
        
        col_count = len(source_plate.cols())
        
        for col_index in range(col_count):
            distributeNoBlowOut(
                    p50multi,
                    8,
                    2,
                    source_plate.cols(col_index),
                    [dest_plate1.cols(col_index), dest_plate2.cols(col_index)])
            
#            p50multi.distribute(2, source_plate.cols(col_index), 
#                                [dest_plate1.cols(col_index), dest_plate2.cols(col_index)],
#                                disposal_vol=4,
#                                new_tip='always' # always use new tips
#                                )

for c in robot.commands():
    print(c)