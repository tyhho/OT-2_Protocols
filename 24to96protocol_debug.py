# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 18:48:53 2020

@author: Jamie Auxillos
"""

from opentrons import labware, instruments, robot

metadata = {
    'protocolName': 'Transfer of cultures from a 24 well plate to a 96 well plate',
    'author': 'Jamie <jamie@auxillos.com>',
    'source': 'Custom Protocol'
}

# create custom labware
culture_plate_24_name = 'starlab_24_wellplate_10000ul'
if culture_plate_24_name not in labware.list():
    labware.create(
        culture_plate_24_name,
        grid=(6, 4),
        spacing=(18.2, 18.2),
        diameter=16.5,
        depth=42,
        volume=10000
    )


microtiter_clear_name = 'Corning-microtiter-96'
if microtiter_clear_name not in labware.list():
    labware.create(
        microtiter_clear_name,
        grid=(12, 8),
        spacing=(9, 9),
        diameter=6.86,
        depth=10.67,
        volume=360
    )

reservoir_name = 'Axygen-290ml-reservoir'
if reservoir_name not in labware.list():
    labware.create(
        reservoir_name,
        grid=(1, 1),
        spacing=(0, 0),
        diameter=8,
        depth=37,
        volume=290000
    )

# load labware
source_plate = labware.load(culture_plate_24_name, '1', 'source plate')
media_res = labware.load(reservoir_name, '2', 'media')

rep_plate = labware.load(
                microtiter_clear_name,
                '4',
                'clear microtiter plate'
            )
tips300 = labware.load('tiprack-200ul', '5')

# instruments
p300 = instruments.P300_Single(mount='right', tip_racks=[tips300])


#%%
# reagent setup
media = media_res.wells('A1')



# csv defaults
example1 = """,1,2,3,4,5,6
A,Media,Media,Media,Media,Media,Media
B,Media,Media,Media,Media,Media,Media
C,Media,Media,Media,Media,Media,Media
D,Media,Media,Media,Media,Media,Media
"""


example2 = """,1,2,3,4,5,6,7,8,9,10,11,12
A,Media,Media,Media,Media,Media,Media,Media,Media,Media,Media,Media,Media
B,Media,Media,Media,Media,Media,Media,Media,Media,Media,Media,Media,Media
C,Media,Media,Media,Media,Media,Media,Media,Media,Media,Media,Media,Media
D,Media,Media,Media,Media,Media,Media,Media,Media,Media,Media,Media,Media
E,Media,Media,Media,Media,Media,Media,Media,Media,Media,Media,Media,Media
F,Media,Media,Media,Media,Media,Media,Media,Media,Media,Media,Media,Media
G,Media,Media,Media,Media,Media,Media,Media,Media,Media,Media,Media,Media
H,Media,Media,Media,Media,Media,Media,Media,Media,Media,Media,Media,Media
"""


# def run_custom_protocol(
#         overnight_contents_in_24_well_plate_csv: 'FileInput' = example1,
#         destinations_for_96_well_plate_csv: 'FileInput' = example2,
# ):

# initialize data storage dictionary
all_data = {}
row_names = 'ABCDEFGH'

"""              start CSV parsing               """

# parse overnight contents CSV
overnight_data = [line.split(',')[1:] for line in example1.splitlines() if line][1:]

for r_ind, row in enumerate(overnight_data):
    for c_ind, culture in enumerate(row):
        if culture and culture != 'media':
            well_name = row_names[r_ind] + str(c_ind+1)
            well = source_plate.wells(well_name)
            all_data[culture.strip()] = [well]

# parse 96-well destinations CSV
dest_data = [line.split(',')[1:13] for line in example2.splitlines() if line][1:9]


#%%
# initialize well receiving only media
all_data['null'] = [media, []]
for r_ind, row in enumerate(dest_data):
    for c_ind, culture in enumerate(row):
        if (culture.strip() in all_data and
                culture.strip().split(' ')[0] != 'null'):
            well_name = row_names[r_ind] + str(c_ind+1)
            well = rep_plate.wells(well_name)
            if len(all_data[culture.strip()]) == 1:
                all_data[culture.strip()].append([well])
            else:
                all_data[culture.strip()][1].append(well)
        elif culture.strip().split(' ')[0] == 'null':
            well_name = row_names[r_ind] + str(c_ind+1)
            well = rep_plate.wells(well_name)
            all_data['null'][1].append(well)

"""              end CSV parsing                 """


#%%
# distribute overnight culture and media from 24- to 96-well plate
for key in all_data:
    dests = all_data[key][1]
    if key != 'null':
        source = all_data[key][0]
        #p10.transfer(20, source, dests)
        media_vol = 180
    else:
        media_vol = 200
    
    if dests:
        p300.distribute(
            media_vol,
            media,
            dests,
            disposal_vol=0
        )
    
# run_custom_protocol(**{'overnight_contents_in_24_well_plate_csv': ',1,2,3,4,5,6\r\nA,Strain1,,,,,\r\nB,,,,,,\r\nC,,,,,,\r\nD,,,,,,', 'destinations_for_96_well_plate_csv': ',1,2,3,4,5,6,7,8,9,10,11,12\r\nA,Strain1,,,,,,,,,,,\r\nB,,,,,,,,,,,,\r\nC,,,,,,,,,,,,\r\nD,,,,,,,,,,,,\r\nE,,,,,,,,,,,,\r\nF,,,,,,,,,,,,\r\nG,,,,,,,,,,,,\r\nH,,,,,,,,,,,,'})

#%%
for c in robot.commands():
    print(c)