"""
For use with OT-2 customizable protocols, convert transfer paths and
volumes stored in a specifically formatted .xlsx file into
protocol parsable lines.
"""

import InstructionWriter
import sys

inputfile = ''

args = sys.argv

if len(args) != 2 or not args[1].lower().endswith('.xlsx'):
    print('Input file or path should be one Excel file ending with .xlsx')
    sys.exit(2)

input_file = sys.argv[1]

instructions = InstructionWriter.main(input_file)

output_file = input_file.split(".xlsx")[0] + "_instructions.txt"
f = open(output_file, "w+")
f.write(instructions)
f.close()

print("Output file successfully created: " + output_file)