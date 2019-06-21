from opentrons import labware, instruments


#%%

tip_slots = ['3']

tip_racks = [labware.load('tiprack-200ul', slot) for slot in tip_slots]

tube_rack_slots = ['1']
tube_racks = [labware.load('opentrons-tuberack-2ml-eppendorf', slot) for slot in tube_rack_slots]

#dest_plate = labware.load('96-flat', slot='4')

p10single = instruments.P10_Single(
    mount='left',
    tip_racks=tip_racks
    )

csv_dict = {
       
            }

transfer_vol = 10

for source, dest in csv_dict.items():
    source_plate_name, source_well = source.split('_')
    dest_plate_name, dest_well = dest.split('_')
    source_plate = int(source_plate_name)-1
    p10single.transfer(
	transfer_vol,
	tube_racks[source_plate].wells(source_well),
	tube_racks[source_plate].wells(dest_well),
	new_tip='always')
