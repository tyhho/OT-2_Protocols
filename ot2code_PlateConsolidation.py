from opentrons import labware, instruments, robot

#%%

slots_map = {
        '1':'corning_96_wellplate_360ul_flat',
        '2':'corning_96_wellplate_360ul_flat',
        '3':'corning_96_wellplate_360ul_flat',
        # '4':'corning_96_wellplate_360ul_flat',
        # '5':'corning_96_wellplate_360ul_flat',
        # '6':'corning_96_wellplate_360ul_flat',
        # '7':'corning_96_wellplate_360ul_flat',
        # '8':'corning_96_wellplate_360ul_flat'
        }

labware_items = {}
for slot, labware_item in slots_map.items():
    labware_items.update({slot:labware.load(labware_item, slot)})

tip_slots = ['4']
#tip_racks = [labware.load('tiprack-10ul-custom', slot) for slot in tip_slots]
tip_racks = [labware.load('tiprack-200ul', slot) for slot in tip_slots]

pipette = instruments.P300_Single(
    mount='right',
    tip_racks=tip_racks
    )

inst_list = {
'2_B8':'3_A1',
'2_G9':'3_B1',
'2_H8':'3_C1',
'2_A3':'3_D1',
'2_C3':'3_E1',
'2_A12':'3_F1',
'2_D3':'3_G1',
'2_A11':'3_H1',
'1_E11':'3_A2',
'1_H1':'3_B2',
'2_C11':'3_C2',
'1_C11':'3_D2',
'2_D11':'3_E2',
'2_F9':'3_F2',
'1_H3':'3_G2',
'2_D7':'3_H2',
'1_H2':'3_A3',
'1_G4':'3_B3',
'2_B9':'3_C3',
'2_D12':'3_D3',
'1_G1':'3_E3',
'2_F4':'3_F3',
'1_H11':'3_G3',
'2_E3':'3_H3',
'2_D5':'3_A4',
'2_C5':'3_B4',
'1_H8':'3_C4',
'1_F8':'3_D4',
'1_H9':'3_E4',
'2_A5':'3_F4',
'1_A12':'3_G4',
'1_A11':'3_H4',
'1_F11':'3_A5',
'2_H7':'3_B5',
'1_F7':'3_C5',
'1_E4':'3_D5',
'1_A4':'3_E5',
'2_G1':'3_F5',
'1_A10':'3_G5',
'2_B3':'3_H5',
'2_F11':'3_A6',
'2_H2':'3_B6',
'2_C7':'3_C6',
'1_H10':'3_D6',
'1_C4':'3_E6',
'1_F9':'3_F6',
'1_E6':'3_G6',
'1_D2':'3_H6',
'1_A5':'3_A7',
'1_A8':'3_B7',
'2_H6':'3_C7',
'1_D6':'3_D7',
'1_A3':'3_E7',
'1_A6':'3_F7',
'1_D5':'3_G7',
'1_B9':'3_H7',
'2_A8':'3_A8',
'1_F3':'3_B8',
'2_F1':'3_C8',
'1_F4':'3_D8',
'1_A9':'3_E8',
'1_D12':'3_F8',
'1_F12':'3_G8',
'2_F12':'3_H8',
'2_G7':'3_A9',
'1_F2':'3_B9',
'2_B6':'3_C9',
'1_C6':'3_D9',
'1_G12':'3_E9',
'2_G12':'3_F9',
'1_G6':'3_G9',
'1_C1':'3_H9',
'1_D8':'3_A10',
'2_D6':'3_B10',
'2_B11':'3_C10',
'1_G5':'3_D10',
'1_G9':'3_E10',
'2_G4':'3_F10',
'1_C12':'3_G10',
'2_F2':'3_H10',
'2_H10':'3_A11',
'2_G8':'3_B11',
'1_H5':'3_C11',
'2_B5':'3_D11',
'2_B2':'3_E11',
'1_H4':'3_F11',
'2_A6':'3_G11',
'2_B7':'3_H11',
'2_F5':'3_A12',
'2_B12':'3_B12',
'1_C8':'3_C12',
'2_C1':'3_D12',
'1_B8':'3_E12',
'1_C9':'3_F12',
'1_F5':'3_G12',
'2_H12':'3_H12'
            }

transfer_vol = 150
#%% Do not modify anything down here

for source, dest in inst_list.items():

#for inst in inst_list:
    
#    source, dest = inst.split('->')
    source_slot, source_well = source.split('_')
    dest_slot, dest_well = dest.split('_')
    
    pipette.transfer(
    	transfer_vol,
    	labware_items[source_slot].wells(source_well),
    	labware_items[dest_slot].wells(dest_well),
        blow_out = True,
    	new_tip='always')
    
#%%
for c in robot.commands():
    print(c)