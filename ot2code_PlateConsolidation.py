from opentrons import labware, instruments, robot

#%%

slots_map = {
        '1':'corning_96_wellplate_360ul_flat',
        '2':'corning_96_wellplate_360ul_flat',
        '3':'corning_96_wellplate_360ul_flat',
        '4':'corning_96_wellplate_360ul_flat',
        '5':'corning_96_wellplate_360ul_flat',
        '6':'corning_96_wellplate_360ul_flat',
        '7':'corning_96_wellplate_360ul_flat',
        '8':'corning_96_wellplate_360ul_flat'
        }

labware_items = {}
for slot, labware_item in slots_map.items():
    labware_items.update({slot:labware.load(labware_item, slot)})

tip_slots = ['10','11']
#tip_racks = [labware.load('tiprack-10ul-custom', slot) for slot in tip_slots]
tip_racks = [labware.load('tiprack-200ul', slot) for slot in tip_slots]

pipette = instruments.P300_Single(
    mount='right',
    tip_racks=tip_racks
    )

inst_list = {
    '1_D9':'2_A1',
    '1_A9':'2_B1',
    '1_C9':'2_C1',
    '1_C10':'2_D1',
    '1_C8':'2_E1',
    '1_F9':'2_F1',
    '1_H8':'2_G1',
    '1_G10':'2_H1',
    '1_D10':'2_A2',
    '1_F10':'2_B2',
    '1_A6':'2_C2',
    '1_H4':'2_D2',
    '1_A5':'2_E2',
    '1_A3':'2_F2',
    '1_D5':'2_G2',
    '1_C6':'2_H2',
    '1_C2':'2_A3',
    '1_B4':'2_B3',
    '1_H3':'2_C3',
    '1_H1':'2_D3',
    '1_B6':'2_E3',
    '1_A4':'2_F3',
    '1_E5':'2_G3',
    '1_C3':'2_H3',
    '1_D3':'2_A4',
    '1_G4':'2_B4',
    '1_C4':'2_C4',
    '1_H2':'2_D4',
    '1_B5':'2_E4',
    '1_B3':'2_F4',
    '1_C5':'2_G4',
    '1_H5':'2_H4',
    '1_A2':'2_A5',
    '1_B1':'2_B5',
    '1_E3':'2_C5',
    '1_E4':'2_D5',
    '1_D4':'2_E5',
    '1_A1':'2_F5',
    '1_G2':'2_G5',
    '1_G1':'2_H5',
    '1_E6':'2_A6',
    '1_B2':'2_B6',
    '1_E2':'2_C6',
    '1_F5':'2_D6',
    '1_F4':'2_E6'
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