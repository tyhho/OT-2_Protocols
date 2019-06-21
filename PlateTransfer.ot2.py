'''Transfer 1 plate to another'''
from opentrons import robot, labware, instruments

robot.clear_commands()

# Copy contents of one plate into another

slot_map = {
        '1':'2'
            }

# TODO: optimize so that you only use 1 tiprack and can use an extra container,
# when you have 96 well source + dest (384 needs 2x tipracks, 96 needs just 1x)
tip_slots = ['3']

tip_racks = [labware.load('tiprack-200ul', slot) for slot in tip_slots]

# TODO: customizable pipette vol
p50multi = instruments.P50_Multi(
    mount='right',
    tip_racks=tip_racks)

container_choices = [
    '96-flat', '96-PCR-tall', '96-deep-well', '384-plate']

#
#def alternating_wells(plate, row_num):
#    """
#    Returns list of 2 WellSeries for the 2 possible positions of an
#    8-channel pipette for a row in a 384 well plate.
#    """
#    return [
#        plate.cols(row_num).wells(start_well, length=8, step=2)
#        for start_well in ['A', 'B']
#    ]


def plate_replica(
        transfer_volume: float=5,
        robot_model: 'StringSelection...'='not hood',
        source_container: 'StringSelection...'='96-flat',
        destination_container: 'StringSelection...'='96-flat',
        slot_map: 'StringSelection...'=slot_map):

    # Load labware
    
    for source_slot, dest_slot in slot_map.items():
        
        dest_plate = labware.load(destination_container, dest_slot)
        source_plate = labware.load(source_container, source_slot)
        
        col_count = len(source_plate.cols())
        
        for col_index in range(col_count):
            
            p50multi.transfer(
            transfer_volume,
            source_plate.cols(1),
            dest_plate.cols(1),
            new_tip='always' # always use new tips
            )


plate_replica(**{'transfer_volume': 5.0, 'robot_model': 'hood', 'source_container': '96-flat', 'destination_container': '96-flat', 'slot_map': slot_map})
