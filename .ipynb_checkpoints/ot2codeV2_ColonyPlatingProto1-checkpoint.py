"""

"""

from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Colony Plating Plating',
    'author': 'Trevor Y. H. Ho <trevor.ho@ed.ac.uk>',
    'description': 'Transfer diluted bacteria from 96-well plate to an agar plate. \
        Prototype: Tip does not get changed when going 10-fold dilution up',
    'apiLevel': '2.9'
}

#%% 

def run(protocol: protocol_api.ProtocolContext):

    slots_map = {
            # '1':'corning_96_wellplate_360ul_flat',
            '4':'starlabpcrplateonws_96_wellplate_350ul', # no change tip
            # '5':'starlabpcrplateonws_96_wellplate_350ul', # change tip
            '1':'gbocellstaronewellagarplate_96_wellplate_10ul', # no change tip
            # '8':'gbocellstaronewellagarplate_96_wellplate_10ul' # change tip
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
    
    # 1 plate = 1 min 54 secs
    l_pipette.pick_up_tip()
    for i in reversed(range(12)):
        l_pipette.transfer(
            3, # transfer volume
            labware_items['4'].wells()[i * 8], # source
            labware_items['1'].wells()[i * 8], # dest
            new_tip='never'
            )
    l_pipette.drop_tip()
  