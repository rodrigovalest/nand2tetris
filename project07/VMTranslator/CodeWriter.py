class CodeWriter:
    def __init__(self, filename):
        self.filename = filename.split('/')[-1].split('.')[0]
        self.file = open(filename, "w")
        self.label_count = 0

    # API
        
    def writeArithmetic(self, command):
        self.file.write(f"// {command}\n")

        if command == "add":
            self.file.write("@SP\n")
            self.file.write("M=M-1\n")
            self.file.write("A=M\n")
            self.file.write("D=M\n")
            self.file.write("@SP\n")
            self.file.write("A=M\n")
            self.file.write("A=A-1\n")
            self.file.write("M=M+D\n")
        elif command == "sub":
            self.file.write("@SP\n")
            self.file.write("M=M-1\n")
            self.file.write("A=M\n")
            self.file.write("D=M\n")
            self.file.write("@SP\n")
            self.file.write("A=M\n")
            self.file.write("A=A-1\n")
            self.file.write("M=M-D\n")
        elif command == "and":
            self.file.write("@SP\n")
            self.file.write("M=M-1\n")
            self.file.write("A=M\n")
            self.file.write("D=M\n")
            self.file.write("A=A-1\n")
            self.file.write("M=D&M\n")
        elif command == "or":
            self.file.write("@SP\n")
            self.file.write("M=M-1\n")
            self.file.write("A=M\n")
            self.file.write("D=M\n")
            self.file.write("A=A-1\n")
            self.file.write("M=D|M\n")
        elif command == "not":
            self.file.write("@SP\n")
            self.file.write("A=M\n")
            self.file.write("A=A-1\n")
            self.file.write("M=!M\n")
        elif command == "neg":
            self.file.write("@SP\n")
            self.file.write("A=M\n")
            self.file.write("A=A-1\n")
            self.file.write("M=-M\n")
        elif command == "eq":
            self.conditional_command("JEQ")
        elif command == "gt":
            self.conditional_command("JGT")
        elif command == "lt":
            self.conditional_command("JLT")

        return

    def writePushPop(self, command, segment, index):
        index = int(index)
        
        if command == "C_PUSH":
            self.file.write(f"// push {segment} {index}\n")

            if segment == "constant":
                self.file.write(f"@{index}\n")
                self.file.write("D=A\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")
            elif segment == "temp":
                self.file.write(f"@{5 + index}\n")
                self.file.write("D=M\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")
            elif segment == "static":
                self.file.write(f"@{self.filename}.{index}\n")
                self.file.write("D=M\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")
            elif segment == "pointer":
                this_or_that = "THIS" if index == 0 else "THAT"

                self.file.write(f"@{this_or_that}\n")
                self.file.write("D=M\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")
            elif segment == "local":
                self.push_segment("LCL", index)
            elif segment == "argument":
                self.push_segment("ARG", index)
            elif segment == "this":
                self.push_segment("THIS", index)
            elif segment == "that":
                self.push_segment("THAT", index)

        elif command == "C_POP":
            self.file.write(f"// pop {segment} {index}\n")

            if segment == "temp":
                self.file.write("@SP\n")
                self.file.write("M=M-1\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("D=M\n")
                self.file.write(f"@{5 + index}\n")
                self.file.write("M=D\n")
            elif segment == "static":
                self.file.write("@SP\n")
                self.file.write("M=M-1\n")
                self.file.write("A=M\n")
                self.file.write("D=M\n")
                self.file.write(f"@{self.filename}.{index}\n")
                self.file.write("M=D\n")
            elif segment == "pointer":
                this_or_that = "THIS" if index == 0 else "THAT"

                self.file.write("@SP\n")
                self.file.write("M=M-1\n")
                self.file.write("A=M\n")
                self.file.write("D=M\n")
                self.file.write(f"@{this_or_that}\n")
                self.file.write("M=D\n")
            elif segment == "local":
                self.pop_segment("LCL", index)
            elif segment == "argument":
                self.pop_segment("ARG", index)
            elif segment == "this":
                self.pop_segment("THIS", index)
            elif segment == "that":
                self.pop_segment("THAT", index)

        return

    def close(self):
        self.file.close()
        return
    
    # END API

    def set_register(self, register, value):
        self.file.write(f"@{value}\n")
        self.file.write("D=A\n")
        self.file.write(f"@{register}\n")
        self.file.write("M=D\n")
        
        return

    def initialize_default_segments(self):
        self.file.write("// instantiating default segments\n")

        self.set_register("SP", 256)
        self.set_register("LCL", 300)
        self.set_register("ARG", 400)
        self.set_register("THIS", 3000)
        self.set_register("THAT", 3010)

        return
    
    def final_loop(self):
        self.file.write("// final loop\n")
        self.file.write("(FINALLOOP)\n")
        self.file.write("@FINALLOOP\n")
        self.file.write("0;JMP\n")
        
        return
    
    def push_segment(self, segment, index):
        self.file.write(f"@{segment}\n")
        self.file.write("D=M\n")
        self.file.write(f"@{index}\n")
        self.file.write("A=A+D\n")
        self.file.write("D=M\n")
        self.file.write("@SP\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")
        self.file.write("@SP\n")
        self.file.write("M=M+1\n")

        return
    
    def pop_segment(self, segment, index):
        RANDOM = 2999
        
        self.file.write(f"@{segment}\n")
        self.file.write("D=M\n")
        self.file.write(f"@{index}\n")
        self.file.write("D=D+A\n")
        self.file.write(f"@{RANDOM}\n")
        self.file.write("M=D\n")
        self.file.write("@SP\n")
        self.file.write("M=M-1\n")
        self.file.write("A=M\n")
        self.file.write("D=M\n")
        self.file.write(f"@{RANDOM}\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")
        
        return
    
    def conditional_command(self, condition):
        self.label_count += 1
        self.file.write(f"@SP\n")
        self.file.write("M=M-1\n")
        self.file.write("A=M\n")
        self.file.write("D=M\n")
        self.file.write("A=A-1\n")
        self.file.write("D=M-D\n")
        self.file.write(f"@CONDITIONALLABEL{self.label_count}\n")
        self.file.write(f"D;{condition}\n")
        self.file.write("@SP\n")
        self.file.write("A=M-1\n")
        self.file.write("M=0\n")
        self.file.write(f"@ENDCONDITIONALLABEL{self.label_count}\n")
        self.file.write("0;JMP\n")
        self.file.write(f"(CONDITIONALLABEL{self.label_count})\n")
        self.file.write("@SP\n")
        self.file.write("A=M-1\n")
        self.file.write("M=-1\n")
        self.file.write(f"(ENDCONDITIONALLABEL{self.label_count})\n")

        return
    