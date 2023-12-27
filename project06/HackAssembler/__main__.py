import sys
from Loader import Loader
from Parser import Parser
from CodeWriter import CodeWriter

filename = sys.argv[1]

loader = Loader()
parser = Parser()
codeWriter = CodeWriter()

# Load labels
with open(filename, "r") as asmfile: 
    count_line = 0
        
    for line in asmfile:
        label = parser.parse(line)
        new_line = loader.load_label(label, count_line)
        
        if new_line:
            count_line = count_line + 1

# Load variables
with open(filename, "r") as asmfile:
    variable_count = 16
        
    for line in asmfile:
        variable = parser.parse(line)
        new_variable = loader.load_variable(variable, variable_count)
            
        if new_variable:
            variable_count = variable_count + 1

# Transform and save
with open(filename, "r") as asmfile:
    filename = filename.replace(".asm", "")
    hackfile = open(filename + ".hack", "w")

    for line in asmfile:
        line = parser.parse(line)
        binary_instruction = codeWriter.to_binary(line)

        if binary_instruction:
            line = binary_instruction + "\n"
            hackfile.write(line)

    hackfile.close()
