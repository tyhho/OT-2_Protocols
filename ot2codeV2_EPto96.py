from opentrons import protocol_api

#%%

# metadata
metadata = {
    'protocolName': 'EP to 96',
    'author': 'Trevor Y. H. Ho <trevor.ho@ed.ac.uk>',
    'description': 'Transfer liquid from 1.5 mL centrifuge tubes to 96 well plate',
    'apiLevel': '2.7'
}

#%% Do not modify anything down here

def run(protocol: protocol_api.ProtocolContext):
    
    slots_map = {
            '1':'starlabpcrplateonws_96_wellplate_350ul',
            '2':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            '3':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            '5':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            '6':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            }
    
    # Configure tip racks and pipette
    
    r_pipette_name = 'p10_single'
    r_tiprack_slots = ['4']
    # r_tiprack_name = 'opentrons_96_tiprack_300ul'
    r_tiprack_name = 'tipone_96_diytiprack_10ul'
    
    # l_pipette_name = 'p10_multi'
    # l_tiprack_slots = ['2']
    # l_tiprack_name = 'geb_96_tiprack_10ul'
    
    labware_items = {}
    for slot, labware_item in slots_map.items():
        labware_items.update({slot:protocol.load_labware(labware_item, slot)})
    
    r_tip_racks = [protocol.load_labware(r_tiprack_name, slot) for slot in r_tiprack_slots]
    # l_tip_racks = [protocol.load_labware(l_tiprack_name, slot) for slot in l_tiprack_slots]
    
    r_pipette = protocol.load_instrument(instrument_name = r_pipette_name,
        mount = 'right', tip_racks = r_tip_racks)
    # l_pipette = protocol.load_instrument(instrument_name = l_pipette_name,
        # mount = 'left', tip_racks = l_tip_racks)
        
    inst_list = [
        # '5$2_A1->1_A1',
        # '5$2_A2->1_A2',
        # '5$2_A3->1_A3',
        # '5$2_A4->1_A4',
        # '5$2_A5->1_A5',
        # '5$2_A6->1_A6',
        # '5$2_B1->1_A7',
        # '5$2_B2->1_A8',
        # '5$2_B3->1_A9',
        '5$2_B4->1_A10',
        '5$2_B5->1_A11',
        '5$2_B6->1_A12',
        '5$2_C1->1_B1',
        '5$2_C2->1_B2',
        '5$2_C3->1_B3',
        '5$2_C4->1_B4',
        '5$2_C5->1_B5',
        '5$2_C6->1_B6',
        '5$2_D1->1_B7',
        '5$2_D2->1_B8',
        '5$2_D3->1_B9',
        '5$2_D4->1_B10',
        '5$2_D5->1_B11',
        '5$2_D6->1_B12',
        '5$3_A1->1_C1',
        '5$3_A2->1_C2',
        '5$3_A3->1_C3',
        '5$3_A4->1_C4',
        '5$3_A5->1_C5',
        '5$3_A6->1_C6',
        '5$3_B1->1_C7',
        '5$3_B2->1_C8',
        '5$3_B3->1_C9',
        '5$3_B4->1_C10',
        '5$3_B5->1_C11',
        '5$3_B6->1_C12',
        '5$3_C1->1_D1',
        '5$3_C2->1_D2',
        '5$3_C3->1_D3',
        '5$3_C4->1_D4',
        '5$3_C5->1_D5',
        '5$3_C6->1_D6',
        '5$3_D1->1_D7',
        '5$3_D2->1_D8',
        '5$3_D3->1_D9',
        '5$3_D4->1_D10',
        '5$3_D5->1_D11',
        '5$3_D6->1_D12',
        '5$5_A1->1_E1',
        '5$5_A2->1_E2',
        '5$5_A3->1_E3',
        '5$5_A4->1_E4',
        '5$5_A5->1_E5',
        '5$5_A6->1_E6',
        '5$5_B1->1_E7',
        '5$5_B2->1_E8',
        '5$5_B3->1_E9',
        '5$5_B4->1_E10',
        '5$5_B5->1_E11',
        '5$5_B6->1_E12',
        '5$5_C1->1_F1',
        '5$5_C2->1_F2',
        '5$5_C3->1_F3',
        '5$5_C4->1_F4',
        '5$5_C5->1_F5',
        '5$5_C6->1_F6',
        '5$5_D1->1_F7',
        '5$5_D2->1_F8',
        '5$5_D3->1_F9',
        '5$5_D4->1_F10',
        '5$5_D5->1_F11',
        '5$5_D6->1_F12',
        '5$6_A1->1_G1',
        '5$6_A2->1_G2',
        '5$6_A3->1_G3',
        '5$6_A4->1_G4',
        '5$6_A5->1_G5',
        '5$6_A6->1_G6',
        '5$6_B1->1_G7',
        '5$6_B2->1_G8',
        '5$6_B3->1_G9',
        '5$6_B4->1_G10',
        '5$6_B5->1_G11',
        '5$6_B6->1_G12',
        '5$6_C1->1_H1',
        '5$6_C2->1_H2',
        '5$6_C3->1_H3',
        '5$6_C4->1_H4',
        '5$6_C5->1_H5',
        '5$6_C6->1_H6',
        '5$6_D1->1_H7',
        '5$6_D2->1_H8',
        '5$6_D3->1_H9'
        ]
    
    for inst in inst_list:

        vol, path = inst.split('$')
        vol = int(vol)
        source, dest = path.split('->')
        source_slot, source_well = source.split('_')
        dest_slot, dest_well = dest.split('_')        
        
        r_pipette.pick_up_tip(r_tip_racks[0].wells_by_name()[dest_well])
        r_pipette.aspirate(vol, labware_items[source_slot].wells_by_name()[source_well])
        r_pipette.dispense(vol, labware_items[dest_slot].wells_by_name()[dest_well])
        r_pipette.blow_out()
        r_pipette.drop_tip()
   
    return protocol.commands()