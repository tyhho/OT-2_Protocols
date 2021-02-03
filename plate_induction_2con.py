"""
Plate Induction (2 conditions)

Dilute overnight cultures of 96 strains of bacteria into two
96-well plates, one without inducer and the other one with inducer,
to assay the performance of the strain/hosted construct under the 
2 conditions.

This protocol does not rely on the InstructionWriter.

Pipette actions:
Using a P10 8-channel
1. Aspirate 6 µL of overnight culture from slot 1 column 1,
2. Dispense 2 µL into slot 2 column 1 (This plate has no inducer)
3. Dispense 2 µL into slot 3 column 1 (This plate has inducer)
4. Dispense remaining liquids into waste plate slot 9 column 1
5. Repeat steps 1-4 for columns 2-12, but waste column is always
on slot 9 column 1

The example below was slightly modified from a previously executed
protocol for illustration.
"""

from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Plate Induction (2 Conditions)',
    'author': 'Trevor Y. H. Ho <trevor.ho@ed.ac.uk>',
    'description': 'Transfer bacteria from 96-well plate to 2 other plates \
        without changing tips',
    'apiLevel': '2.9'
}

def run(protocol: protocol_api.ProtocolContext):

    def distribute(pipette, vol_in, vol_out, source, dests, waste):
        pipette.pick_up_tip()
        pipette.aspirate(vol_in, source)
        for dest in dests:
            pipette.dispense(vol_out, dest)
        pipette.dispense(pipette.current_volume, waste)
        pipette.blow_out()
        pipette.drop_tip()

    slots_map = {
            '1':'corning_96_wellplate_360ul_flat',
            '2':'corning_96_wellplate_360ul_flat',
            '3':'corning_96_wellplate_360ul_flat',
            '9':'corning_96_wellplate_360ul_flat'
            }
    
    # Configure tip racks and pipette
    
    # r_pipette_name = 'p300_single'
    # r_tiprack_slots = ['4']
    # r_tiprack_name = 'opentrons_96_tiprack_300ul'
    
    l_pipette_name = 'p10_multi'
    l_tiprack_slots = ['4']
    l_tiprack_name = 'geb_96_tiprack_10ul'
    
    labware_items = {}
    for slot, labware_item in slots_map.items():
        labware_items.update({slot:protocol.load_labware(labware_item, slot)})
    
    # r_tip_racks = [protocol.load_labware(r_tiprack_name, slot) for slot in r_tiprack_slots]
    l_tip_racks = [protocol.load_labware(l_tiprack_name, slot) for slot in l_tiprack_slots]
    
    # r_pipette = protocol.load_instrument(instrument_name = r_pipette_name,
    #     mount = 'right', tip_racks = r_tip_racks)
    l_pipette = protocol.load_instrument(instrument_name = l_pipette_name,
        mount = 'left', tip_racks = l_tip_racks)
    
    for i in range(12):
        distribute(l_pipette,
                   6,
                   2,
                   labware_items['1'].wells()[i * 8],
                   [labware_items['2'].wells()[i * 8]],
                   labware_items['9'].wells()[0],
                   )