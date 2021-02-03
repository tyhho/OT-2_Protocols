"""
Combinatorial pipetting (alcohol)

This is a variant protocol on combinatorial pipetting,
with the pipette action customized for moving ethanol/isopropanol-
baesd solvents.

This protocol relies on instructions from InstructionWriter.py

When moving samples with high percentage of alcohol,
a common problem is that after dispensing, a visible amount
of sample still sticks to the tip wall, and they take
time to drip to the bottom of the tip. If the pipette
moves onto the next step, the dripping sample might drop into
other wells nearby and thus causing sample contamination around.

Pipette actions:
Starts with a simple transfer, but dispense with some distance
above the bottom of the receving tube. Then, pipette up and down
with air trying to clear as much alcohol as possible from the tip.

Doing so would not remove all bits of alcohol, but at least the
remaining sample volume will not be heavy enough to drip out of
the tip.

The example below comes from a previously executed protocol.
These pipette actions were used for cleaning up a 96-well PCR plate
of PCR products. In the lab we used NEB Monarch purification kit and the 
binding buffer is mostly isopropanol (determined from the smell of it). I would
add the binding buffer to the plate first using a multi-channel pipette,
and then use this protocol to move the samples into labelled tubes on
a 1.5 mL / 2 mL tube rack to proceed to the next step.
"""

from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Combinatorial Pipetting on samples with alcohol',
    'author': 'Trevor Y. H. Ho <trevor.ho@ed.ac.uk>',
    'description': 'A combinatorial pipetting protocol customized for alcohols transfers',
    'apiLevel': '2.9'
}

def run(protocol: protocol_api.ProtocolContext):
    
    slots_map = {
            '1':'starlabpcrplateonws_96_wellplate_350ul',
            '2':'opentrons_24_tuberack_generic_2ml_screwcap',
            '3':'opentrons_24_tuberack_generic_2ml_screwcap',
            '5':'opentrons_24_tuberack_generic_2ml_screwcap',
            '6':'opentrons_24_tuberack_generic_2ml_screwcap',
            }
    
    # Configure tip racks and pipette
    
    r_pipette_name = 'p300_single'
    r_tiprack_slots = ['4']
    # r_tiprack_name = 'opentrons_96_tiprack_300ul'
    r_tiprack_name = 'tipone_96_diytiprack_300ul'
    
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
        # '170$1_A1->2_A1',
        # '170$1_A2->2_A2',
        # '170$1_A3->2_A3',
        # '170$1_A4->2_A4',
        # '170$1_A5->2_A5',
        # '170$1_A6->2_A6',
        # '170$1_A7->2_B1',
        # '170$1_A8->2_B2',
        # '170$1_A9->2_B3',
        # '170$1_A10->2_B4',
        # '170$1_A11->2_B5',
        # '170$1_A12->2_B6',
        # '170$1_B1->2_C1',
        # '170$1_B2->2_C2',
        # '170$1_B3->2_C3',
        # '170$1_B4->2_C4',
        # '170$1_B5->2_C5',
        # '170$1_B6->2_C6',
        # '170$1_B7->2_D1',
        # '170$1_B8->2_D2',
        # '170$1_B9->2_D3',
        # '170$1_B10->2_D4',
        # '170$1_B11->2_D5',
        # '170$1_B12->2_D6',
        # '170$1_C1->3_A1',
        # '170$1_C2->3_A2',
        # '170$1_C3->3_A3',
        # '170$1_C4->3_A4',
        # '170$1_C5->3_A5',
        # '170$1_C6->3_A6',
        # '170$1_C7->3_B1',
        # '170$1_C8->3_B2',
        # '170$1_C9->3_B3',
        # '170$1_C10->3_B4',
        # '170$1_C11->3_B5',
        # '170$1_C12->3_B6',
        # '170$1_D1->3_C1',
        # '170$1_D2->3_C2',
        # '170$1_D3->3_C3',
        # '170$1_D4->3_C4',
        # '170$1_D5->3_C5',
        # '170$1_D6->3_C6',
        # '170$1_D7->3_D1',
        # '170$1_D8->3_D2',
        # '170$1_D9->3_D3',
        # '170$1_D10->3_D4',
        # '170$1_D11->3_D5',
        # '170$1_D12->3_D6',
        '170$1_E1->5_A1',
        '170$1_E2->5_A2',
        '170$1_E3->5_A3',
        '170$1_E4->5_A4',
        '170$1_E5->5_A5',
        '170$1_E6->5_A6',
        '170$1_E7->5_B1',
        '170$1_E8->5_B2',
        '170$1_E9->5_B3',
        '170$1_E10->5_B4',
        '170$1_E11->5_B5',
        '170$1_E12->5_B6',
        '170$1_F1->5_C1',
        '170$1_F2->5_C2',
        '170$1_F3->5_C3',
        '170$1_F4->5_C4',
        '170$1_F5->5_C5',
        '170$1_F6->5_C6',
        '170$1_F7->5_D1',
        '170$1_F8->5_D2',
        '170$1_F9->5_D3',
        '170$1_F10->5_D4',
        '170$1_F11->5_D5',
        '170$1_F12->5_D6',
        '170$1_G1->6_A1',
        '170$1_G2->6_A2',
        '170$1_G3->6_A3',
        '170$1_G4->6_A4',
        '170$1_G5->6_A5',
        '170$1_G6->6_A6',
        '170$1_G7->6_B1',
        '170$1_G8->6_B2',
        '170$1_G9->6_B3',
        '170$1_G10->6_B4',
        '170$1_G11->6_B5',
        '170$1_G12->6_B6',
        '170$1_H1->6_C1',
        '170$1_H2->6_C2',
        '170$1_H3->6_C3',
        '170$1_H4->6_C4',
        '170$1_H5->6_C5',
        '170$1_H6->6_C6',
        '170$1_H7->6_D1',
        '170$1_H8->6_D2',
        '170$1_H9->6_D3'
        ]
    
    for inst in inst_list:

        vol, path = inst.split('$')
        vol = int(vol)
        source, dest = path.split('->')
        source_slot, source_well = source.split('_')
        dest_slot, dest_well = dest.split('_')        
        
        r_pipette.pick_up_tip(r_tip_racks[0].wells_by_name()[source_well])
        r_pipette.aspirate(vol, labware_items[source_slot].wells_by_name()[source_well])
        r_pipette.dispense(vol, labware_items[dest_slot].wells_by_name()[dest_well].top(-2))
        r_pipette.aspirate(100)
        r_pipette.dispense(100)
        r_pipette.aspirate(100)
        r_pipette.dispense(100)
        r_pipette.blow_out()
        r_pipette.drop_tip()