"""
Combinatorial Pipetting

The simplest protocol designed to work with the InstructionWriter.

The example below is a mock protocol to illustrate how it works.
 
"""

from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Combinatorial Pipetting',
    'author': 'Trevor Y. H. Ho <trevor.ho@ed.ac.uk>',
    'description': 'Transfer samples based on instructions from InstructionWriter',
    'apiLevel': '2.9'
}

def run(protocol: protocol_api.ProtocolContext):
    
    # key: slot number in str
    # value: labware API name
    slots_map = {
            '1':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            '2':'starlabpcrplateonws_96_wellplate_350ul'
            }
    
    # Configure tip racks and pipette
    
    r_pipette_name = 'p10_single'
    r_tiprack_slots = ['3']
    r_tiprack_name = 'geb_96_tiprack_10ul'
    
    # l_pipette_name = 'p10_single'
    # l_tiprack_slots = ['1']
    # l_tiprack_name = 'geb_96_tiprack_10ul'
    
    inst_list = [
        '2$1_A2->2_A1',
        '1.0$1_B1->2_A1',
        '1$1_C2->2_A1',
        '3$1_A3->2_A2',
        '1.0$1_B1->2_A2',
        '1$1_C2->2_A2',
        '1$1_A1->2_A3',
        '1.5$1_B2->2_A3',
        '1$1_C2->2_A3',
        '2$1_A2->2_A4',
        '1.5$1_B2->2_A4',
        '1$1_C2->2_A4',
        '3$1_A3->2_A5',
        '1$1_C2->2_A5',
        '1$1_A1->2_A6',
        '2.0$1_B3->2_A6',
        '1$1_C2->2_A6',
        '2$1_A2->2_A7',
        '2.0$1_B3->2_A7',
        '1$1_C2->2_A7',
        '3$1_A3->2_A8',
        '2.0$1_B3->2_A8',
        '1$1_C2->2_A8'
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
        vol = float(vol)
        source, dest = path.split('->')
        source_slot, source_well = source.split('_')
        dest_slot, dest_well = dest.split('_')        

        r_pipette.transfer(vol,
                           labware_items[source_slot].wells_by_name()[source_well],
                           labware_items[dest_slot].wells_by_name()[dest_well],
                           new_tip='always'
                           )