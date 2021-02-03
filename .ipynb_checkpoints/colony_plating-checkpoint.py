"""
Colony Plating

Plate out of transformed bacteria onto
a rectangular agar plate using the P10 8-channel pipette.

The idea is to treat an agar plate, which has no boundries,
as a 96-well plate with 1 mm well height. Then, it is merely
a single transfer function that handles liquid moving.

This protocol does not rely on the InstructionWriter.

This protocol requires a custom labware definition:
"gbocellstaronewellagarplate_96_wellplate_10ul"
for the one-well agar plate.

During calibration, make sure the tips poke into the agar,
this ensures enough contact surfaces for the dispensed
liquid (bacteria in LB) to adhere to the agar.

Typically, < 4 µL of liquid will dry in 10-15 mins,
if you wedge the lid open and place the plate up right 
in a 37 °C incubator.

I had so far not experienced immediate contamination from
air-borne microbes, at least not until the plates were
left in cold room for over 2 months.

The example below comes from a previously executed protocol.
It assumes you have 4 columns of transformed E. coli,
on columns 1-4, that are already recovered after
transformation, and that they have been diluted to a concentration
that will yield single colonies when plated out. the protocol then
plate bacteria from column 1 in source plate to columns 1-3 on
destination agar plate, from column 2 in source to columns 4-6 on
agar plate, etc. Plating the same sample 3 times increases the chance
of having well separated single colonies from a plate.

As to how many times the naive transformed, recovered cells need to be
diluted, it depends on the conditions of transformation and competencies.
As a rule of thumb, prepare 2-3 plates of 10-fold serially diluted cells
to increase the chance of obtaining single colonies on plates.

This protocol can be adopted for plate spotting assays with slight modifications.
However, extra care is needed because when plating cells, the volume dispensed
on agar plates might not be exactly 4 µL.
"""

from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Colony Plating',
    'author': 'Trevor Y. H. Ho <trevor.ho@ed.ac.uk>',
    'description': 'Transfer bacteria from 96-well plate to a 1-well agar plate',
    'apiLevel': '2.9'
}

def run(protocol: protocol_api.ProtocolContext):

    slots_map = {
            '4':'corning_96_wellplate_360ul_flat',
            '1':'gbocellstaronewellagarplate_96_wellplate_10ul',

            }
    
    # Configure tip racks and pipette
    
    # r_pipette_name = 'p300_single'
    # r_tiprack_slots = ['4']
    # r_tiprack_name = 'opentrons_96_tiprack_300ul'
    
    l_pipette_name = 'p10_multi'
    l_tiprack_slots = ['2']
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
    
    transfer_inst = {
        'A1':['A1','A2','A3'],
        'A2':['A4','A5','A6'],
        'A3':['A7','A8','A9'],
        'A4':['A10','A11','A12']
        }
    
    for source_well, dest_wells in transfer_inst.items():
        l_pipette.transfer(
                4,
                labware_items['4'].wells_by_name()[source_well],
                [labware_items['1'].wells_by_name()[dest_well] for dest_well in dest_wells], 
                new_tip='always'
                )