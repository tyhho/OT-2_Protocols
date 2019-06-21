from opentrons import labware, instruments, robot


#%%

tip_slots = ['5']

tip_racks = [labware.load('tiprack-200ul', slot) for slot in tip_slots]

source_slots = ['1','2','3']
source_plates = [labware.load('96-flat', slot) for slot in source_slots]

dest_plate = labware.load('96-flat', slot='4')

p10single = instruments.P10_Single(
    mount='left',
    tip_racks=tip_racks
    )

csv_dict = {
        '1_A3':'4_A1',
'1_A4':'4_A2',
'1_B5':'4_A3',
'1_E4':'4_A4',
'1_E7':'4_A5',
'1_E12':'4_A6',
'1_F5':'4_A7',
'2_C8':'4_A8',
'3_A1':'4_A9',
'3_B1':'4_A10',
'3_C1':'4_A11',
'3_D1':'4_A12',
'3_E1':'4_B1',
'3_H1':'4_B2',
'3_A2':'4_B3',
'3_B2':'4_B4',
'2_F1':'4_B5'
            }

source_plate_type = '96-flat'

dest_plate_type = '96-flat'

transfer_vol = 2
#%% Do not modify anything down here

for source, dest in csv_dict.items():
    source_plate_name, source_well = source.split('_')
    dest_plate_name, dest_well = dest.split('_')
    source_plate = int(source_plate_name)-1
    p10single.transfer(
	transfer_vol,
	source_plates[source_plate].wells(source_well),
	dest_plate.wells(dest_well),
	new_tip='always')
    #robot.pause()