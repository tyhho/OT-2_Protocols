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
    '2_H8':'3_A7',
    '2_F4':'3_B7',
    '2_H5':'3_C7',
    '2_A6':'3_D7',
    '1_E12':'3_E7',
    '2_H7':'3_F7',
    '1_C12':'3_G7',
    '2_H12':'3_H7',
    '1_E1':'3_A8',
    '1_F2':'3_B8',
    '2_H3':'3_C8',
    '2_C5':'3_D8',
    '1_G3':'3_E8',
    '2_E2':'3_F8',
    '2_H10':'3_G8',
    '1_D7':'3_H9',
    '1_B4':'3_A9',
    '1_G1':'3_B9',
    '2_D11':'3_C9',
    '2_H6':'3_D9',
    '1_D11':'3_E9',
    '1_G7':'3_F9',
    '1_F9':'3_G9',
    '2_G1':'3_H9',
    '1_B7':'3_A10',
    '1_G9':'3_B10',
    '2_D9':'3_C10',
    '1_E11':'3_D10',
    '2_G11':'3_E10',
    '2_H9':'3_F10',
    '2_C7':'3_G10',
    '1_B8':'3_H10',
    '2_G2':'3_A11',
    '2_E9':'3_B11',
    '2_C10':'3_C11',
    '1_G8':'3_D11',
    '2_C3':'3_E11',
    '2_A11':'3_F11',
    '2_B6':'3_G11',
    '1_D9':'3_H11',
    '1_F12':'3_A12',
    '1_C1':'3_B12',
    '1_G11':'3_C12',
    '2_C12':'3_D12',
    '1_G4':'3_E12',
    '2_F8':'3_F12',
    '1_A12':'3_G12',
    '1_F6':'3_H12'
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