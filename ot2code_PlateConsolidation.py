from opentrons import labware, instruments, robot


#%%

slots_map = {
        '1':'biorad_96_wellplate_200ul_pcr',
        '2':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
        '3':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
        '5':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
        '6':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap'
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
#    '2_A1->1_A1',
#    '2_A2->1_A2',
#    '2_A3->1_A3',
#    '2_A4->1_A4',
#    '2_A5->1_A5',
#    '2_A6->1_A6',
#    '2_B1->1_A7',
#    '2_B2->1_A8',
#    '2_B3->1_A9',
#    '2_B4->1_A10',
#    '2_B5->1_A11',
#    '2_B6->1_A12',
#    '2_C1->1_B1',
#    '2_C2->1_B2',
#    '2_C3->1_B3',
#    '2_C4->1_B4',
#    '2_C5->1_B5',
#    '2_C6->1_B6',
#    '2_D1->1_B7',
#    '2_D2->1_B8',
#    '2_D3->1_B9',
#    '2_D4->1_B10',
#    '2_D5->1_B11',
#    '2_D6->1_B12',
#    '3_A1->1_C1',
#    '3_A2->1_C2',
#    '3_A3->1_C3',
#    '3_A4->1_C4',
#    '3_A5->1_C5',
#    '3_A6->1_C6',
#    '3_B1->1_C7',
#    '3_B2->1_C8',
#    '3_B3->1_C9',
#    '3_B4->1_C10',
#    '3_B5->1_C11',
#    '3_B6->1_C12',
#    '3_C1->1_D1',
#    '3_C2->1_D2',
#    '3_C3->1_D3',
#    '3_C4->1_D4',
#    '3_C5->1_D5',
#    '3_C6->1_D6',
#    '3_D1->1_D7',
#    '3_D2->1_D8',
#    '3_D3->1_D9',
#    '3_D4->1_D10',
#    '3_D5->1_D11',
#    '3_D6->1_D12'
    '5_A1->1_E1',
    '5_A2->1_E2',
    '5_A3->1_E3',
    '5_A4->1_E4',
    '5_A5->1_E5',
    '5_A6->1_E6',
    '5_B1->1_E7',
    '5_B2->1_E8',
    '5_B3->1_E9',
    '5_B4->1_E10',
    '5_B5->1_E11',
    '5_B6->1_E12',
    '5_C1->1_F1',
    '5_C2->1_F2',
    '5_C3->1_F3',
    '5_C4->1_F4',
    '5_C5->1_F5',
    '5_C6->1_F6',
    '5_D1->1_F7',
    '5_D2->1_F8',
    '5_D3->1_F9',
    '5_D4->1_F10',
    '5_D5->1_F11',
    '5_D6->1_F12',
    '6_A1->1_G1',
    '6_A2->1_G2',
    '6_A3->1_G3',
    '6_A4->1_G4',
    '6_A5->1_G5',
    '6_A6->1_G6',
    '6_B1->1_G7',
    '6_B2->1_G8',
    '6_B3->1_G9',
    '6_B4->1_G10',
    '6_B5->1_G11',
    '6_B6->1_G12',
    '6_C1->1_H1',
    '6_C2->1_H2',
    '6_C3->1_H3',
    '6_C4->1_H4',
    '6_C5->1_H5',
    '6_C6->1_H6',
    '6_D1->1_H7',
    '6_D2->1_H8',
    '6_D3->1_H9',
    '6_D4->1_H10',
    '6_D5->1_H11',
    '6_D6->1_H12'
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
	labware_items[dest_slot].wells(dest_well),
    blow_out = True,
	new_tip='always')
    #robot.pause()
    
#%%
for c in robot.commands():
    print(c)