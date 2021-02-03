"""
Primer Rehydration

Add water to oligonucleotide tubes from IDT,
where primers arrive in lypholized formats.
The amount of water each tube should receive differ and so
this protocol relies on instructions from InstructionWriter.py

Pipette actions:
Using a P300S, add X μL of water to the screw cap tube.
Tip does not change throughout the protocol. However, the water is dispensed
slowly at height 5 mm below the tube rim. This avoids contamination and splashing
of water.

This protocol expects user to vortex the capped microcentrifuge tubes afterwards,
and does not include mixing actions from pipettes.

The example below comes from a previously executed protocol.
"""

from opentrons import protocol_api
import math

# metadata
metadata = {
    'protocolName': 'Primer Rehydration',
    'author': 'Trevor Y. H. Ho <trevor.ho@ed.ac.uk>',
    'description': ' Add water to arrived IDT primer tubes, uses instructions from \
        InstructionWriter.py',
    'apiLevel': '2.9'
}

def run(protocol: protocol_api.ProtocolContext):

    slots_map = {
            '1':'opentrons_6_tuberack_falcon_50ml_conical', # water in 50 mL tube in well A1
            '2':'opentrons_24_tuberack_generic_2ml_screwcap',
            '3':'opentrons_24_tuberack_generic_2ml_screwcap'
            }
    
    # Configure tip racks and pipette
    
    pipette_name = 'p300_single'
    mount = 'right'
    tiprack_slots = ['4']
    tiprack_name = 'opentrons_96_tiprack_300ul' # or use 'tipone_96_diytiprack_300ul'
    
    inst_list = [
        '251$1_A1->2_A1',
        '204$1_A1->2_A2',
        '233$1_A1->2_A3',
        '218$1_A1->2_A4',
        '239$1_A1->2_A5',
        '309$1_A1->2_A6',
        '227$1_A1->2_B1',
        '234$1_A1->2_B2',
        '258$1_A1->2_B3',
        '234$1_A1->2_B4',
        '276$1_A1->2_B5',
        '249$1_A1->2_B6',
        '205$1_A1->2_C1',
        '290$1_A1->2_C2',
        '179$1_A1->2_C3',
        '172$1_A1->2_C4',
        '238$1_A1->2_C5',
        '199$1_A1->2_C6',
        '210$1_A1->2_D1',
        '249$1_A1->2_D2',
        '201$1_A1->2_D3',
        '294$1_A1->2_D4',
        '212$1_A1->2_D5',
        '235$1_A1->2_D6',
        '239$1_A1->3_A1',
        '243$1_A1->3_A2',
        '256$1_A1->3_A3',
        '274$1_A1->3_A4',
        '261$1_A1->3_A5'
        ]
    
    labware_items = {}
    for slot, labware_item in slots_map.items():
        labware_items.update({slot:protocol.load_labware(labware_item, slot)})
    
    tip_racks = [protocol.load_labware(tiprack_name, slot) for slot in tiprack_slots]
       
    pipette = protocol.load_instrument(
        instrument_name = pipette_name,
        mount = mount,
        tip_racks = tip_racks
        )
    
    pipette.pick_up_tip()
    
    for inst in inst_list:
        
        vol, path = inst.split('$')
        vol = int(vol)
        source, dest = path.split('->')
        source_slot, source_well = source.split('_')
        dest_slot, dest_well = dest.split('_')
        
        pipette_times = math.ceil(vol/pipette.max_volume)
        for i in range(pipette_times):
            pipette.aspirate( (vol/pipette_times), labware_items[source_slot].wells_by_name()[source_well])
            pipette.dispense( (vol/pipette_times), labware_items[dest_slot].wells_by_name()[dest_well].top(-5), rate=0.5)
            pipette.blow_out()
    pipette.drop_tip()