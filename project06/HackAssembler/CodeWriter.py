import Dicts

# Transform the instruction to the respective binary code
class CodeWriter:
    def to_binary(self, instruction):
        if instruction == None:
                return

        if instruction.startswith("@"):
            instruction = instruction.replace("@", "")

            if instruction.isdigit():
                binary_instruction = bin(int(instruction))[2:].zfill(15)
            else:
                binary_instruction = Dicts.symbol[instruction]
            
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

            dest_code = Dicts.dest.get(dest_part, "000")
            comp_code = Dicts.comp.get(comp_part)
            jump_code = Dicts.jump.get(jump_part, "000")

            if not comp_code:
                return None

            return "111" + comp_code + dest_code + jump_code
