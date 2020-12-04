from opentrons import protocol_api

#%%

# metadata
metadata = {
    'protocolName': 'Cherry Picking',
    'author': 'Trevor Y. H. Ho <trevor.ho@ed.ac.uk>',
    'description': 'Consolidate  screened candidate strains from different plates \
        onto a new plate. Experiment: IBM_BM012',
    'apiLevel': '2.7'
}

#%% 

def run(protocol: protocol_api.ProtocolContext):

    slots_map = {
            '1':'corning_96_wellplate_360ul_flat',
            '2':'corning_96_wellplate_360ul_flat',
            '3':'corning_96_wellplate_360ul_flat',
            '4':'corning_96_wellplate_360ul_flat',
            }
    
    # Configure tip racks and pipette
    
    r_pipette_name = 'p300_single'
    r_tiprack_slots = ['5']
    r_tiprack_name = 'tipone_96_diytiprack_200ul'
    
    # l_pipette_name = 'p10_single'
    # l_tiprack_slots = ['1']
    # l_tiprack_name = 'geb_96_tiprack_10ul'
    
    inst_list = [
       '200$2_A7->4_A1',
        '200$2_D12->4_A2',
        '200$1_C7->4_A3',
        '200$1_E1->4_A4',
        '200$2_D7->4_A5',
        '200$1_A3->4_A6',
        '200$1_D7->4_A7',
        '200$1_G6->4_A8',
        '200$2_A9->4_A9',
        '200$1_C6->4_A10',
        '200$1_A8->4_A11',
        '200$2_G7->4_A12',
        '200$2_C10->4_B1',
        '200$1_E11->4_B2',
        '200$1_A11->4_B3',
        '200$1_A9->4_B4',
        '200$2_E11->4_B5',
        '200$2_B9->4_B6',
        '200$2_A12->4_B7',
        '200$2_A11->4_B8',
        '200$2_H8->4_B9',
        '200$1_D3->4_B10',
        '200$1_F5->4_B11',
        '200$1_D1->4_B12',
        '200$2_D1->4_C1',
        '200$1_C10->4_C2',
        '200$1_G7->4_C3',
        '200$2_E12->4_C4',
        '200$1_D9->4_C5',
        '200$1_B12->4_C6',
        '200$1_B9->4_C7',
        '200$3_H11->4_C8',
        '200$2_B7->4_C9',
        '200$2_G9->4_C10',
        '200$2_C11->4_C11',
        '200$1_H6->4_C12',
        '200$1_C8->4_D1',
        '200$1_A12->4_D2',
        '200$1_E7->4_D3',
        '200$2_G11->4_D4',
        '200$2_E4->4_D5',
        '200$2_F7->4_D6',
        '200$1_B2->4_D7',
        '200$1_E4->4_D8',
        '200$2_C7->4_D9',
        '200$2_H10->4_D10',
        '200$2_C8->4_D11',
        '200$2_C1->4_D12',
        '200$2_B11->4_E1',
        '200$2_C9->4_E2',
        '200$2_C4->4_E3',
        '200$2_D2->4_E4',
        '200$2_B6->4_E5',
        '200$2_B2->4_E6',
        '200$2_A10->4_E7',
        '200$2_B10->4_E8',
        '200$2_E9->4_E9',
        '200$3_D9->4_E10',
        '200$3_E8->4_E11',
        '200$2_D3->4_E12',
        '200$3_F10->4_F1',
        '200$2_G6->4_F2',
        '200$3_H3->4_F3',
        '200$3_F9->4_F4',
        '200$2_C3->4_F5',
        '200$1_B10->4_F6',
        '200$2_F5->4_F7',
        '200$2_F2->4_F8',
        '200$2_E8->4_F9',
        '200$2_B5->4_F10',
        '200$2_B3->4_F11',
        '200$3_E12->4_F12',
        '200$2_H5->4_G1',
        '200$3_B2->4_G2',
        '200$3_B10->4_G3',
        '200$2_C6->4_G4',
        '200$3_E11->4_G5',
        '200$2_B8->4_G6',
        '200$2_C2->4_G7',
        '200$1_E12->4_G8',
        '200$2_A6->4_G9',
        '200$3_H8->4_G10',
        '200$2_D9->4_G11',
        '200$2_E10->4_G12',
        '200$1_F2->4_H1',
        '200$3_E9->4_H2',
        '200$2_F3->4_H3',
        '200$1_F10->4_H4',
        '200$2_G2->4_H5',
        '200$2_F11->4_H6',
        '200$1_A2->4_H7',
        '200$1_C3->4_H8',
        '200$1_C2->4_H9',

        ]
    
    labware_items = {}
    for slot, labware_item in slots_map.items():
        labware_items.update({slot:protocol.load_labware(labware_item, slot)})
    
    r_tip_racks = [protocol.load_labware(r_tiprack_name, slot) for slot in r_tiprack_slots]
    # l_tip_racks = [protocol.load_labware(l_tiprack_name, slot) for slot in l_tiprack_slots]
    
    r_pipette = protocol.load_instrument(instrument_name = r_pipette_name,
        mount = 'right', tip_racks = r_tip_racks)
    # l_pipette = protocol.load_instrument(instrument_name = l_pipette_name,
    #     mount = 'left', tip_racks = l_tip_racks)
    

    for inst in inst_list:

        vol, path = inst.split('$')
        vol = int(vol)
        source, dest = path.split('->')
        source_slot, source_well = source.split('_')
        dest_slot, dest_well = dest.split('_')        

        r_pipette.transfer(vol,
                           labware_items[source_slot].wells_by_name()[source_well],
                           labware_items[dest_slot].wells_by_name()[dest_well],
                           new_tip='always'
                           )
   
    return protocol.commands()

# The extra part: programmatically get a simulation ProtocolContext, so we can run this
# as a normal Python script and have everything in the run function get executed.

# This part should be removed or commented out before uploading to a real OT-2.

# import json
# extra_labware_list = [
#     'starlabpcrplateonws_96_wellplate_350ul',
#     'gbocellstaronewellagarplate_96_wellplate_10ul',
#     'tipone_96_diytiprack_200ul'
#     ]

# extra_labware = {}
# for labware_name in extra_labware_list:
#     labware_json_fn = labware_name + '.json'
#     with open(labware_json_fn) as f: labware_data = json.load(f)
#     extra_labware.update({labware_name:labware_data})

# from opentrons.simulate import get_protocol_api
# protocol = get_protocol_api(version=metadata['apiLevel'], extra_labware=extra_labware)
# commands = run(protocol)

# for c in commands:
#     print(c)