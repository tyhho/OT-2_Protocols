from opentrons import labware, instruments, robot

#%%

slots_map = {
        '1':'corning_96_wellplate_360ul_flat',
        '2':'corning_96_wellplate_360ul_flat',
        '3':'corning_96_wellplate_360ul_flat',
        '4':'corning_96_wellplate_360ul_flat',
        '5':'corning_96_wellplate_360ul_flat'
        }

labware_items = {}
for slot, labware_item in slots_map.items():
    labware_items.update({slot:labware.load(labware_item, slot)})

tip_slots = ['6']
#tip_racks = [labware.load('tiprack-10ul-custom', slot) for slot in tip_slots]
tip_racks = [labware.load('opentrons_96_tiprack_10ul', slot) for slot in tip_slots]

p10s = instruments.P10_Single(
    mount='left',
    tip_racks=tip_racks
    )

inst_list = {
'3_B5':'5_A1',
'3_F10':'5_B1',
'3_F11':'5_C1',
'3_F6':'5_D1',
'3_D8':'5_E1',
'3_E11':'5_F1',
'3_B11':'5_G1',
'3_B9':'5_H1',
'3_B2':'5_A2',
'2_A10':'5_B2',
'4_B9':'5_C2',
'4_A12':'5_D2',
'2_F7':'5_E2',
'4_D3':'5_F2',
'3_H2':'5_G2',
'2_B6':'5_H2',
'3_H4':'5_A3',
'3_G3':'5_B3',
'1_D7':'5_C3',
'2_D9':'5_D3',
'2_A7':'5_E3',
'2_A11':'5_F3',
'2_E11':'5_G3',
'2_D7':'5_H3',
'2_H8':'5_A4',
'1_G11':'5_B4',
'2_A9':'5_C4',
'2_D11':'5_D4',
'2_F6':'5_E4',
'2_C3':'5_F4',
'2_F8':'5_G4',
'1_E1':'5_H4',
'2_G11':'5_A5',
'1_B7':'5_B5',
'1_G2':'5_C5',
'3_D2':'5_D5',
'2_H4':'5_E5',
'1_A11':'5_F5',
'1_A9':'5_G5',
'2_A12':'5_H5',
'2_H5':'5_A6',
'2_H11':'5_B6',
'1_A6':'5_C6',
'1_A3':'5_D6',
'2_F3':'5_E6',
'2_G9':'5_F6'
            }

transfer_vol = 10
#%% Do not modify anything down here

for source, dest in inst_list.items():

#for inst in inst_list:
    
#    source, dest = inst.split('->')
    source_slot, source_well = source.split('_')
    dest_slot, dest_well = dest.split('_')
    
#    p10s.pick_up_tip(location=tip_racks[0].wells(dest_well))
#    p10s.aspirate(4,labware_items[source_slot].wells(source_well) )
#    p10s.dispense(4,labware_items[dest_slot].wells(dest_well) )
#    p10s.blow_out()
#    p10s.drop_tip()
    
    p10s.transfer(
    	transfer_vol,
    	labware_items[source_slot].wells(source_well),
    	labware_items[dest_slot].wells(dest_well),
        blow_out = True,
    	new_tip='always')
    #robot.pause()
    
#%%
for c in robot.commands():
    print(c)