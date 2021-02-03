"""
Primer dilution

Dilute 100 μM primers to 10 μM
This protocol relies on instructions from InstructionWriter.py

Pipette actions:
First, using P300S, add 180 μL of water to a microcentrifuge tube.
This is done for all destination tubes first without changing the tip.

Then, using P10S, add 20 μL of 100 μM primer to the different tubes.
Always changes the tip between each primer, but not between the two transfers
from stock primer to diluted primer.

This protocol expects user to vortex the capped microcentrifuge tubes afterwards,
and does not include mixing actions from pipettes.

The example below comes from a previously executed protocol.
"""

from opentrons import protocol_api
import math

# metadata
metadata = {
    'protocolName': 'Primer Dilution',
    'author': 'Trevor Y. H. Ho <trevor.ho@ed.ac.uk>',
    'description': ' Dilute 100 μM primers to 10 μM, uses instructions from \
        InstructionWriter.py',
    'apiLevel': '2.9'
}

def run(protocol: protocol_api.ProtocolContext):

    slots_map = {
            '2':'opentrons_24_tuberack_generic_2ml_screwcap',
            '3':'opentrons_24_tuberack_generic_2ml_screwcap',
            '5':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            '6':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',
            '7':'opentrons_6_tuberack_falcon_50ml_conical' # water in 50 mL tube in well A1
            }
    
    # Configure tip racks and pipette
    
    r_pipette_name = 'p300_single'
    r_tiprack_slots = ['4']
    r_tiprack_name = 'opentrons_96_tiprack_300ul'
    
    l_pipette_name = 'p10_single'
    l_tiprack_slots = ['1']
    l_tiprack_name = 'geb_96_tiprack_10ul'
    
    inst_list = [
        '20$2_A1->5_A1',
        '20$2_A2->5_A2',
        '20$2_A3->5_A3',
        '20$2_A4->5_A4',
        '20$2_A5->5_A5',
        '20$2_A6->5_A6',
        '20$2_B1->5_B1',
        '20$2_B2->5_B2',
        '20$2_B3->5_B3',
        '20$2_B4->5_B4',
        '20$2_B5->5_B5',
        '20$2_B6->5_B6',
        '20$2_C1->5_C1',
        '20$2_C2->5_C2',
        '20$2_C3->5_C3',
        '20$2_C4->5_C4',
        '20$2_C5->5_C5',
        '20$2_C6->5_C6',
        '20$2_D1->5_D1',
        '20$2_D2->5_D2',
        '20$2_D3->5_D3',
        '20$2_D4->5_D4',
        '20$2_D5->5_D5',
        '20$2_D6->5_D6',
        '20$3_A1->6_A1',
        '20$3_A2->6_A2',
        '20$3_A3->6_A3',
        '20$3_A4->6_A4',
        '20$3_A5->6_A5'
        ]
    
    labware_items = {}
    for slot, labware_item in slots_map.items():
        labware_items.update({slot:protocol.load_labware(labware_item, slot)})
    
    r_tip_racks = [protocol.load_labware(r_tiprack_name, slot) for slot in r_tiprack_slots]
    l_tip_racks = [protocol.load_labware(l_tiprack_name, slot) for slot in l_tiprack_slots]
    
    r_pipette = protocol.load_instrument(instrument_name = r_pipette_name,
        mount = 'right', tip_racks = r_tip_racks)
    l_pipette = protocol.load_instrument(instrument_name = l_pipette_name,
        mount = 'left', tip_racks = l_tip_racks)
    
    
    # First add 180 μL of water to each destination tube
    r_pipette.pick_up_tip()
    
    for inst in inst_list:
        path = inst.split('$')[1]
        dest = path.split('->')[1]
        dest_slot, dest_well = dest.split('_')
        
        r_pipette.aspirate(180, labware_items['7'].wells_by_name()['A1'])
        r_pipette.dispense(180, labware_items[dest_slot].wells_by_name()[dest_well].top(-5), rate=0.5)
        r_pipette.blow_out()
        
    r_pipette.drop_tip()
    
    # Then add the primer one by one
    
    for inst in inst_list:

        vol, path = inst.split('$')
        vol = float(vol)
        source, dest = path.split('->')
        source_slot, source_well = source.split('_')
        dest_slot, dest_well = dest.split('_')        
        
        # Code below assumes that P10 
        pipette_times = math.ceil(vol/l_pipette.max_volume)
        
        l_pipette.pick_up_tip()

        for i in range(pipette_times):
            l_pipette.aspirate( (vol/pipette_times), labware_items[source_slot].wells_by_name()[source_well])
            l_pipette.dispense( (vol/pipette_times), labware_items[dest_slot].wells_by_name()[dest_well])
            l_pipette.blow_out()
        
        l_pipette.drop_tip()