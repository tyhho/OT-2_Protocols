# -*- coding: utf-8 -*-
"""
@author: Trevor Ho
"""

# lines to comment out before actual run
# from opentrons import simulate
# protocol = simulate.get_protocol_api(version='2.2')

from opentrons import protocol_api

#%%
def distributeNoBlowOutLite(pipette,vol_in,vol_out,source,dests,trash):
    pipette.pick_up_tip()
    pipette.aspirate(vol_in,source)
    for dest in dests:
        pipette.dispense(vol_out,dest)
    pipette.dispense(pipette.current_volume,trash)
    pipette.blow_out()                                               
    pipette.drop_tip()

#%%

# metadata
metadata = {
    'protocolName': 'Multi-induction',
    'author': 'Trevor Y. H. Ho <trevor.ho@ed.ac.uk>',
    'description': 'Draw 2 uL * no_of_plate volumes from overnight culture \
    and dispense into plates with induction',
    'apiLevel': '2.2'
}
    
#%% Execution

def run(protocol: protocol_api.ProtocolContext):
    
    slots_map = {
            '1':'corning_96_wellplate_360ul_flat',
            '2':'corning_96_wellplate_360ul_flat',
            '3':'corning_96_wellplate_360ul_flat',
            '4':'corning_96_wellplate_360ul_flat',
            '5':'corning_96_wellplate_360ul_flat',
            '6':'corning_96_wellplate_360ul_flat',
            '7':'corning_96_wellplate_360ul_flat',
            '9':'corning_96_wellplate_360ul_flat',
            }
    
    # Configure tip racks and pipette
    
    pipette_name = 'p10_multi'
    mount = 'left'
    tiprack_slots = ['10','11']
    tiprack_name = 'geb_96_tiprack_10ul' # other options: 'opentrons_96_tiprack_10ul' / 'opentrons_96_tiprack_300ul'
    
    
    deck = {}
    for slot, labware_name in slots_map.items():
        deck.update({slot:protocol.load_labware(labware_name, slot)})
    
    tip_racks = [protocol.load_labware(tiprack_name, slot) for slot in tiprack_slots]
       
    pipette = protocol.load_instrument(
        instrument_name = pipette_name,
        mount = mount,
        tip_racks = tip_racks
        )
    
    #%%
    well_list =  [('A'+str(i)) for i in range(1,13) ]
    
    for well in well_list:
        distributeNoBlowOutLite(pipette,
                                8,
                                2,
                                deck['7'][well],
                                [deck[str(dest_slot)].wells_by_name()[well] for dest_slot in range(1,4)],
                                deck['9'].wells_by_name()[well]
                                )
        
        distributeNoBlowOutLite(pipette,
                                8,
                                2,
                                deck['7'][well],
                                [deck[str(dest_slot)].wells_by_name()[well] for dest_slot in range(4,7)],
                                deck['9'].wells_by_name()[well]
                                )
    
    #%%
    cmds = protocol.commands()
    for cmd in cmds:
        print(cmd)

# comment out the following line before actual run
# run(protocol)