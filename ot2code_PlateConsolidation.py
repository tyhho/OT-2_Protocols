from opentrons import labware, instruments, robot


#%%

slots_map = {
        '1':'96-flat',
        '2':'96-flat',
        '3':'96-flat'
        }

labware_items = {}
for slot, labware_item in slots_map.items():
    labware_items.update({slot:labware.load(labware_item, slot)})

tip_slots = ['4']
tip_racks = [labware.load('tiprack-10ul-custom', slot) for slot in tip_slots]

p10single = instruments.P10_Single(
    mount='left',
    tip_racks=tip_racks
    )

csv_dict = {
       '1_D12':'3_A1',
'1_B12':'3_B1',
'1_C11':'3_C1',
'1_B3':'3_D1',
'2_H2':'3_E1',
'1_G12':'3_F1',
'1_D5':'3_G1',
'2_B12':'3_H1',
'1_H5':'3_A2',
'2_E4':'3_B2',
'1_C3':'3_C2',
'2_G9':'3_D2',
'1_F10':'3_E2',
'1_D3':'3_F2',
'2_G10':'3_G2',
'2_D5':'3_H2',
'1_C6':'3_A3',
'2_F1':'3_B3',
'1_A11':'3_C3',
'1_C4':'3_D3',
'2_H11':'3_E3',
'1_F1':'3_F3',
'1_F4':'3_G3',
'1_H11':'3_H3',
'1_G5':'3_A4',
'2_B3':'3_B4',
'2_A12':'3_C4',
'2_E11':'3_D4',
'2_H1':'3_E4',
'2_D7':'3_F4',
'1_E7':'3_G4',
'1_G10':'3_H4',
'1_G6':'3_A5',
'2_G3':'3_B5',
'1_C9':'3_C5',
'1_C7':'3_D5',
'1_A5':'3_E5',
'2_F12':'3_F5',
'2_F2':'3_G5',
'2_A1':'3_H5',
'2_A8':'3_A6',
'1_D1':'3_B6',
'1_A3':'3_C6',
'1_E2':'3_D6',
'1_H7':'3_E6',
'2_E12':'3_F6',
'2_B5':'3_G6',
'2_H4':'3_H6'
            }

transfer_vol = 2
#%% Do not modify anything down here

for source, dest in csv_dict.items():
    
    source_plate, source_well = source.split('_')
    dest_plate, dest_well = dest.split('_')
    
    p10single.transfer(
	transfer_vol,
	labware_items[source_plate].wells(source_well),
	labware_items[dest_plate].wells(dest_well),
    blow_out = True,
	new_tip='always')
    #robot.pause()