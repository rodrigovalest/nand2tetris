import sys

dest = {
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111",
}

comp = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101",
}

jump = {
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}

symbol = {
    "R0": "000000000000000",
    "R1": "000000000000001",
    "R2": "000000000000010",
    "R3": "000000000000011",
    "R4": "000000000000100",
    "R5": "000000000000101",
    "R6": "000000000000110",
    "R7": "000000000000111",
    "R8": "000000000001000",
    "R9": "000000000001001",
    "R10": "000000000001010",
    "R11": "000000000001011",
    "R12": "000000000001100",
    "R13": "000000000001101",
    "R14": "000000000001110",
    "R15": "000000000001111",
    "SCREEN": "100000000000000",
    "KBD": "110000000000000",
    "SP": "000000000000000",
    "LCL": "000000000000001",
    "ARG": "000000000000010",
    "THIS": "000000000000011",
    "THAT": "000000000000100",
}

def white_spaces(line):
    line = line.replace(" ", "")
    line = line.strip()

    if not line or line.startswith("//"):
        return None

    split = line.split("//", 1)
    line = split[0]

    return line

def parse_binary(instruction):
    instruction = white_spaces(instruction)

    if instruction == None:
        return

    if instruction.startswith("@"):
        instruction = instruction.replace("@", "")

        if instruction.isdigit():
            binary_instruction = bin(int(instruction))[2:].zfill(15)
        else:
            binary_instruction = symbol[instruction]
        
        return "0" + binary_instruction
    
    elif instruction.startswith("("):
        return None
    
    else:
        dest_part = ""
        comp_part = ""
        jump_part = ""

        if "=" in instruction:
            dest_part, instruction = instruction.split("=")

        if ";" in instruction:
            comp_part, jump_part = instruction.split(";")
        else:
            comp_part = instruction

        dest_code = dest.get(dest_part, "000")
        comp_code = comp.get(comp_part)
        jump_code = jump.get(jump_part, "000")

        if not comp_code:
            return None

        return "111" + comp_code + dest_code + jump_code

def load_label(label, count_line):
    label = white_spaces(label)

    if label == None:
        return False

    if label.startswith("("):
        label = label.replace("(", "")
        label = label.replace(")", "")

        label_code = symbol.get(label, None)

        if not label_code:
            count_line = bin(int(count_line))[2:].zfill(15)
            symbol[label] = count_line
        
        return False

    return True

def load_variable(variable, variable_count):
    variable = white_spaces(variable)

    if variable == None:
        return False

    if variable.startswith("@"):
        variable = variable.replace("@", "")

        if not variable.isdigit():
            variable_code = symbol.get(variable, None)

            if not variable_code:
                variable_count = bin(int(variable_count))[2:].zfill(15)
                symbol[variable] = variable_count

                return True

    return False


filename = sys.argv[1]

# Load labels
with open(filename, "r") as asmfile: 
    count_line = 0
        
    for line in asmfile:
        new_line = load_label(line, count_line)
        
        if new_line:
            count_line = count_line + 1

# Load variables
with open(filename, "r") as asmfile:
    variable_count = 16
        
    for line in asmfile:
        new_variable = load_variable(line, variable_count)
            
        if new_variable:
            variable_count = variable_count + 1

# Transform and save
with open(filename, "r") as asmfile:
    filename = filename.replace(".asm", "")
    hackfile = open(filename + ".hack", "w")

    for line in asmfile:
        binary_instruction = parse_binary(line)

        if binary_instruction:
            line = binary_instruction + "\n"
            hackfile.write(line)

    hackfile.close()
