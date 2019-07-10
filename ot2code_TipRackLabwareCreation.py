# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 19:12:06 2019

@author: s1635543
"""

from opentrons import labware, instruments, robot

#%% Create new tip rack for 10 uL custom
#
#tip_rack_name = 'tiprack-10ul-custom'
#if tip_rack_name not in labware.list():
#    custom_plate = labware.create(
#        tip_rack_name,                    # name of you labware
#        grid=(12, 9),                    # specify amount of (columns, rows)
#        spacing=(9, 9),               # distances (mm) between each (column, row)
#        diameter=3,                     # diameter (mm) of each well on the plate
#        depth=10,                       # depth (mm) of each well on the plate
#        volume=10
##        ,        offset=(14.3, 10.5, 65)
#        )

#%% Create new tip rack for 200 uL custom

#tip_rack_name = 'tiprack-200ul-custom'
#if tip_rack_name not in labware.list():
#    custom_plate = labware.create(
#        tip_rack_name,                    # name of you labware
#        grid=(12, 9),                    # specify amount of (columns, rows)
#        spacing=(9, 9),               # distances (mm) between each (column, row)
#        diameter=3,                     # diameter (mm) of each well on the plate
#        depth=10,                       # depth (mm) of each well on the plate
#        volume=10
##        ,        offset=(14.3, 10.5, 65)
#        )

#%% Create new tip rack for 300 uL custom
#
#tip_rack_name = 'tiprack-300ul-custom'
#if tip_rack_name not in labware.list():
#    custom_plate = labware.create(
#        tip_rack_name,                    # name of you labware
#        grid=(12, 9),                    # specify amount of (columns, rows)
#        spacing=(9, 9),               # distances (mm) between each (column, row)
#        diameter=3,                     # diameter (mm) of each well on the plate
#        depth=10,                       # depth (mm) of each well on the plate
#        volume=10
##        ,        offset=(14.3, 10.5, 65)
#        )

#%% Set up calibration for the tip boxes

# Environment set up
# Note: MUST PUT TIP BOXES in MIDDLE SLOTS: 2 / 5 / 8 / 11


slots_map = {
        #'1':'96-flat',
        '1':'96-flat'
        }

labware_items = {}
for slot, labware_item in slots_map.items():
    labware_items.update({slot:labware.load(labware_item, slot)})

tip_slots1 = ['2']
tip_racks1 = [labware.load('tiprack-200ul-custom', slot) for slot in tip_slots1]
tip_slots2 = ['5']
tip_racks2 = [labware.load('tiprack-10ul-custom', slot) for slot in tip_slots2]

p300s = instruments.P300_Single(
    mount='left',
    tip_racks=tip_racks1
    )

p10m = instruments.P10_Multi(
    mount='right',
    tip_racks=tip_racks2
    )

# Mock pipette for two times to test ability to pick up tips properly from custom tip boxes
for i in range(2):
    p300s.transfer(
            	300,
            	labware_items['1'].wells('A1'),
            	labware_items['1'].wells('A2'),
                new_tip = 'always'
                )
#    p10m.transfer(
#            	10,
#            	labware_items['1'].cols('1'),
#            	labware_items['1'].cols('2'),
#                new_tip = 'always'
#                )    
#%%

#from opentrons.data_storage import database
#if 'tiprack-10ul-custom1' in labware.list():
#    database.delete_container('tiprack-10ul-custom1')
#if 'tiprack-200ul-custom1' in labware.list():
#    database.delete_container('tiprack-200ul-custom1')
