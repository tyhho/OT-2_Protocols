# Author : Group 2
'''
Task description: 
    
    Perform serial dilution of a dye, initially at 4096X, into a gradient of:
        2048X, 1024X, ... , 4X, 2X, 1X
    using water as the diluent.
    See Figure 2 for the expected final pattern.

    You should end up with a total of 12 tubes, each with 120 µL of diluted dye
    (except the last tube, which should have 240 µL of diluted dye).
    
    After each pipette step, you should instruct the robot to mix the diluted dye
    to ensure a homogenous solution is achieved before you move on
    
You start with:
    Slot 2: 50 mL tube rack
        Well A1: 20 mL of water
    Slot 3: 1.5 mL tube rack
        Well A1: 1 mL of 4096X dye
        Well A4 - D6: Empty 1.5 mL tubes (these tubes should hold the serially diluted dyes)
        
Your robot is equipped with:
    Right mount: P300 single channel pipette
        
'''
# Import libraries for OT-2
from opentrons import labware, instruments,robot


# Put plates and racks onto the deck
slots_map = {
        '2':'opentrons_6_tuberack_falcon_50ml_conical',
        '3':'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap'
        }

deck_labware = {}
for slot, labware_item in slots_map.items():
    deck_labware.update({slot:labware.load(labware_item, slot)})

# Put tip boxes onto the deck
tip_slots = ['1']
tip_racks=[]
for slot in tip_slots:
        tip_racks.append(labware.load('opentrons_96_tiprack_300ul', slot))

# Configure the pipette
p300s = instruments.P300_Single(
    mount='right',
    tip_racks=tip_racks
    )


'''
**************** Code above is the OG code and was left unchanged, everything below was coded
 from scratch since it was easier than understanding what the OG author wanted
'''

# Function for distribution of water into specified wells
def distribution(pipette, origin, wells_n_amounts, target_labware):
	# check and prepare tip
	if pipette.has_tip : pipette.return_tip()
	pipette.pick_up_tip()
	pipette.blow_out()
	
	
	#loops for dispensing
	not_finished = True
	n = 0
	while not_finished:		
		#Aspirating liquid
		vol_in = pipette.max_volume - pipette.current_volume
		pipette.aspirate(vol_in, origin)
		
		#Dispensing the liquid into wells until it runs out
		while vol_in > pipette.min_volume and vol_in >= wells_n_amounts[n][1] :
			pipette.dispense(wells_n_amounts[n][1], target_labware.wells(wells_n_amounts[n][0]))
			vol_in -= wells_n_amounts[n][1]
			n += 1
			if n > len(wells_n_amounts)-1: 
				not_finished = False
				break
		#idk if this check is necesarry, would have to see it in action		
		if vol_in == 0: 
			pipette.move_to(origin.top(-20))
			pipette.blow_out()
	#Returning any unused liquid		
	if not vol_in == 0: pipette.dispense(vol_in, origin)
	pipette.move_to(origin.top(-20))
	pipette.blow_out()

# Function for mixing insides of a well
def mix_and_blow(pipette, place):
	pipette.aspirate(200, place)
	pipette.dispense(200, place)	
	pipette.aspirate(200, place)
	pipette.dispense(200, place)
	pipette.move_to(place.top(-20))
	pipette.blow_out()

# Function for diluting dye into cells
def dilution(pipette, dye_place, wells_n_amounts, target_labware):
	# check and prepare tip
	if pipette.has_tip : pipette.return_tip()
	pipette.pick_up_tip()
	pipette.blow_out()
	
	#loop for mixing
	n = 0
	pipette.aspirate(wells_n_amounts[n][1], dye_place) #First aspiration of dye
	while n < len(wells_n_amounts):	
		pipette.dispense(wells_n_amounts[n][1], target_labware.wells(wells_n_amounts[n][0]))
		mix_and_blow(pipette, target_labware.wells(wells_n_amounts[n][0]))
		n += 1
		
		#Check so that the liquid is not aspirated in the last well
		if not n >= len(wells_n_amounts):
			pipette.aspirate(wells_n_amounts[n][1], target_labware.wells(wells_n_amounts[n-1][0]))
		else:
			pipette.return_tip()
		
		
#Creation of list of lists for wells and their required volumes
letters = ['A', 'B', 'C', 'D']
numbers = [4, 5, 6]
wells_n_amounts = []
for num in numbers : 
	for letter in letters: 	
		wells_n_amounts.append([letter+str(num), 120])
		
		
#Executing the 2 functions 
distribution(p300s, deck_labware['2'].wells('A1'), wells_n_amounts, deck_labware['3'])
dilution(p300s, deck_labware['3'].wells('A1'), wells_n_amounts, deck_labware['3'])
	
	
	
# Print out the commands step by step
for c in robot.commands():
    print(c)
































