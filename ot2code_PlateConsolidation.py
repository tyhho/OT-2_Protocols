from opentrons import labware, instruments, robot


#%%

slots_map = {
        '1':'corning_96_wellplate_360ul_flat',
        '2':'usascientific_96_wellplate_2.4ml_deep'

        }

labware_items = {}
for slot, labware_item in slots_map.items():
    labware_items.update({slot:labware.load(labware_item, slot)})

tip_slots = ['4']
tip_racks = [labware.load('tiprack-10ul-custom', slot) for slot in tip_slots]
#tip_racks = [labware.load('opentrons_96_tiprack_10ul', slot) for slot in tip_slots]

p10s = instruments.P10_Single(
    mount='left',
    tip_racks=tip_racks
    )

inst_list = {
'1_C4->2_A1',
'1_H1->2_A2',
'1_B2->2_A3',
'1_E2->2_A4',
'1_A3->2_A5',
'1_E5->2_A6',
'1_C9->2_A7',
'1_F5->2_A8',
'1_D2->2_A9',
'1_D1->2_A10',
'1_C2->2_A11',
'1_E1->2_A12',
'1_F1->2_B1',
'1_C8->2_B2',
'1_B9->2_B3',
'1_F10->2_B4',
'1_A9->2_B5',
'1_B12->2_B6',
'1_H7->2_B7',
'1_C12->2_B8',
'1_E8->2_B9',
'1_A12->2_B10',
'1_E9->2_B11',
'1_D12->2_B12',
'1_C10->2_C1',
'1_G11->2_C2',
'1_E6->2_C3',
'1_F12->2_C4',
'1_F6->2_C5',
'1_H8->2_C6',
'1_A11->2_C7',
'1_B8->2_C8',
'1_A4->2_C9'
            }

transfer_vol = 4
#%% Do not modify anything down here

for inst in inst_list:
    
    source, dest = inst.split('->')
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
	labware_items[dest_slot].wells(dest_well).top(-30),
    blow_out = True,
	new_tip='always')
    #robot.pause()
    
#%%
for c in robot.commands():
    print(c)