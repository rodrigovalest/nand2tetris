class CodeWriter:
    eq = 0
    lt = 0
    get = 0

    def __init__(self, filename):
        self.filename = filename

    def set_register(self, register, value):
        return [
            f"@{value}",
            "D=A",
            f"@{register}",
            "M=D"
        ]

    def initialize_segments(self):
        segments = []  

        segments.extend(self.set_register("SP", 256))
        segments.extend(self.set_register("LCL", 300))
        segments.extend(self.set_register("ARG", 400))
        segments.extend(self.set_register("THIS", 3000))
        segments.extend(self.set_register("THAT", 3010))

        return segments
    
    def final_loop(self):
        return [
            "(LOOP)",
            "@LOOP",
            "0;JMP"
        ]
    
    def push_segment(self, segment, address):
        return [
            f"// push {segment} {address}",
            f"@{segment}",
            "D=M",
            f"@{address}",
            "A=A+D",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ]
    
    def pop_segment(self, segment, address):
        RANDOM = 2999

        return [
            f"// pop {segment} {address}",
            f"@{segment}",
            "D=M",
            f"@{address}",
            "D=D+A",
            f"@{RANDOM}",
            "M=D",
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            f"@{RANDOM}",
            "A=M",
            "M=D"
        ]
    
    def memory_acess_command(self, line):
        if line[0] == "push":
            if line[1] == "constant":
                return [
                    f"// {line[0]} {line[1]} {line[2]}",
                    f"@{line[2]}",
                    "D=A",
                    "@SP",
                    "A=M",
                    "M=D",
                    "@SP",
                    "M=M+1"
                ]
            elif line[1] == "temp":
                return [
                    f"// push temp {line[2]}",
                    f"@{5 + int(line[2])}",
                    "D=M",
                    "@SP",
                    "A=M",
                    "M=D",
                    "@SP",
                    "M=M+1"
                ]
            elif line[1] == "static":
                return [
                    f"// push static {line[2]}",
                    f"@{self.filename}.{line[2]}",
                    "D=M",
                    "@SP",
                    "A=M",
                    "M=D",
                    "@SP",
                    "M=M+1"
                ]
            elif line[1] == "pointer":
                this_or_that = "THAT"

                if line[2] == "0":
                    this_or_that = "THIS"
                
                return [
                    f"// push pointer {line[2]}",
                    f"@{this_or_that}",
                    "D=M",
                    "@SP",
                    "A=M",
                    "M=D",
                    "@SP",
                    "M=M+1"
                ]
            elif line[1] == "local":
                return self.push_segment("LCL", line[2])
            elif line[1] == "argument":
                return self.push_segment("ARG", line[2])
            elif line[1] == "this":
                return self.push_segment("THIS", line[2])
            elif line[1] == "that":
                return self.push_segment("THAT", line[2])
    
        elif line[0] == "pop":
            if line[1] == "temp":
                return [
                    f"// pop temp {line[2]}",
                    "@SP",
                    "M=M-1",
                    "@SP",
                    "A=M",
                    "D=M",
                    f"@{5 + int(line[2])}",
                    "M=D"
                ]
            elif line[1] == "static":
                return [
                    f"// pop static {line[2]}",
                    "@SP",
                    "M=M-1",
                    "A=M",
                    "D=M",
                    f"@{self.filename}.{line[2]}",
                    "M=D"
                ]
            elif line[1] == "pointer":
                this_or_that = "THAT"

                if line[2] == "0":
                    this_or_that = "THIS"
                
                return [
                    f"// pop pointer {line[2]}",                    
                    "@SP",
                    "M=M-1",
                    "A=M",
                    "D=M",
                    f"@{this_or_that}",
                    "M=D"
                ]
            elif line[1] == "local":
                return self.pop_segment("LCL", line[2])
            elif line[1] == "argument":
                return self.pop_segment("ARG", line[2])
            elif line[1] == "this":
                return self.pop_segment("THIS", line[2])
            elif line[1] == "that":
                return self.pop_segment("THAT", line[2])
            
    def arithmetic_logical_command(self, line):
        if line[0] == "add":
            return [
                f"// {line[0]}",
                "@SP",
                "M=M-1",
                "A=M",
                "D=M",
                "@SP",
                "A=M",
                "A=A-1",
                "M=M+D"
            ]
        elif line[0] == "sub":
            return [
                f"// {line[0]}",
                "@SP",
                "M=M-1",
                "A=M",
                "D=M",
                "@SP",
                "A=M",
                "A=A-1",
                "M=M-D"
            ]
        elif line[0] == "neg":
            return [
                f"// {line[0]}",
                "@SP",
                "A=A-1",
                "M=-M"
            ]
        elif line[0] == "not":
            return [
                f"// {line[0]}",
                "@SP",
                "A=A-1",
                "M=!M"
            ]
        elif line[0] == "and":
            return [
                f"// {line[0]}",
                "@SP",
                "M=M-1",
                "A=M",
                "D=M",
                "A=A-1",
                "M=D&M"
            ]
        elif line[0] == "or":
            return [
                f"// {line[0]}",
                "@SP",
                "M=M-1",
                "A=M",
                "D=M",
                "A=A-1",
                "M=D|M"
            ]
        elif line[0] == "eq":
            self.eq += 1

            return [
                f"// eq",
                "@SP",
                "M=M-1",
                "A=M",
                "D=M",
                "A=A-1",
                "D=M-D",
                f"@EQUAL{self.eq}",
                "D;JEQ",
                "@SP",
                "A=M-1",
                "M=0",
                f"@ENDEQ{self.eq}",
                "0;JMP",
                f"(EQUAL{self.eq})",
                "@SP",
                "A=M-1",
                "M=-1",
                f"(ENDEQ{self.eq})"
            ]
        elif line[0] == "get":
            self.get += 1

            return [
                f"// gt",
                "@SP",
                "M=M-1",
                "A=M",
                "D=M",
                "A=A-1",
                "D=M-D",
                f"@GREATER{self.gt}",
                "D;JGT",
                "@SP",
                "A=M-1",
                "M=0",
                f"@ENDGREATER{self.gt}",
                "0;JMP",
                f"(GREATER{self.gt})",
                "@SP",
                "A=M-1",
                "M=-1",
                f"(ENDGREATER{self.gt})"
            ]
        elif line[0] == "lt":
            self.lt += 1

            return [
                f"// lt",
                "@SP",
                "M=M-1",
                "A=M",
                "D=M",
                "A=A-1",
                "D=M-D",
                f"@LESS{self.lt}",
                "D;JLT",
                "@SP",
                "A=M-1",
                "M=0",
                f"@ENDLESS{self.lt}",
                "0;JMP",
                f"(LESS{self.lt})",
                "@SP",
                "A=M-1",
                "M=-1",
                f"(ENDLESS{self.lt})"
            ]
    
    def code(self, line):
        if len(line) == 1:
            return self.arithmetic_logical_command(line)         
        if len(line) == 3:
            return self.memory_acess_command(line)
