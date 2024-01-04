class Parser:   
    def __init__(self, file):
        self.file = file
        self.commands = self.commands_dict()
        self.current_line = None

    # API

    def hasMoreCommands(self):
        current_position = self.file.tell()
        next_line = self.file.readline()
        self.file.seek(current_position)

        if next_line:
            return True
        else:
            return False


    def advance(self):
        line = self.file.readline() 
        self.current_line = self.parse(line)

        if not self.current_line:
            self.advance()

        return


    def commandType(self):
        return self.commands.get(self.current_line[0])


    def arg1(self):
        if self.commandType() == "C_ARITHMETIC":
            return self.current_line[0]
        elif self.commandType() == "C_RETURN":  
            return
        else:
            return self.current_line[1]


    def arg2(self):
        permitedTypes = ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]

        if self.commandType() in permitedTypes:
            return self.current_line[2]
        
        return

    # END API

    def parse(self, line):
        line = line.strip()

        if not line or line.startswith("//"):
            return None

        line = line.split("//", 1)[0]
        parts = line.split()

        return parts


    def commands_dict(self):
        return {
            "add": "C_ARITHMETIC",
            "sub": "C_ARITHMETIC",
            "eq": "C_ARITHMETIC",
            "gt": "C_ARITHMETIC",
            "lt": "C_ARITHMETIC",
            "and": "C_ARITHMETIC",
            "or": "C_ARITHMETIC",
            "not": "C_ARITHMETIC",
            "neg": "C_ARITHMETIC",
            "push": "C_PUSH",
            "pop": "C_POP",
            "label": "C_LABEL",
            "goto": "C_GOTO",
            "if-goto": "C_IF",
            "function": "C_FUNCTION",
            "return": "C_RETURN",
            "call": "C_CALL",
        }
