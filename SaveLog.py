"""
Write a simulated log file for checking and documenting an OT-2 protocol
"""

import sys
from opentrons.simulate import simulate, format_runlog

inputfile = ''

args = sys.argv

# Check the file

if len(args) != 2 or not args[1].lower().endswith('.py'):
    print('Input file or path should be an OT-2 protocol written in APIv2 ending with .py')
    sys.exit(2)

input_file = sys.argv[1]

# Simulation

protocol_file = open(input_file)
runlog = simulate(protocol_file, file_name='', custom_labware_paths=['./labware_def/'])
print(format_runlog(runlog[0])) # Line modified compared to Opentrons Doc

# Export simulated log file for documentation

simulated_log_filepath = "./protocol_log/" + input_file.split('.py')[0] + '_log.txt'
simulated_log = open(simulated_log_filepath, 'w+')
simulated_log.write(format_runlog(runlog[0]))
simulated_log.close()

print("Reminder: custom labware definitions in .json formats should be stored under ./labware_defs")
print("Log file created: " + simulated_log_filepath)