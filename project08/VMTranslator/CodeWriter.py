class CodeWriter:
    def __init__(self, filename):
        self.filename = filename.split('/')[-1].split('.')[0]
        self.file = open(filename, "w")
        self.label_count = 0

    # API
        
    def write_init(self):
        self.file.write("// bootstrap code\n")
        self.file.write("@256\n")
        self.file.write("D=A\n")
        self.file.write("@SP\n")
        self.file.write("M=D\n")

        self.write_call("Sys.init", 0)

        return
        
    def write_arithmetic(self, command):
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

    def write_push_pop(self, command, segment, index):
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
    
    def write_label(self, label):
        self.file.write(f"// label {label}\n")
        self.file.write(f"({label})\n")

        return
    
    def write_goto(self, label):
        self.file.write(f"// goto {label}\n")
        self.file.write(f"@{label}\n")
        self.file.write(f"0;JMP\n")

        return
    
    def write_if(self, label):
        self.file.write(f"// if-goto {label}\n")
        self.file.write("@SP\n")
        self.file.write("M=M-1\n")
        self.file.write("A=M\n")
        self.file.write("D=M\n")
        self.file.write(f"@{label}\n")
        self.file.write(f"D;JNE\n")

        return
    
    def write_function(self, function_name, num_vars):
        num_vars = int(num_vars)

        self.file.write(f"// function {function_name} {num_vars}\n")
        self.file.write(f"({function_name})\n")

        for i in range(num_vars):
            self.file.write("@SP\n")
            self.file.write("A=M\n")
            self.file.write("M=0\n")
            self.file.write("@SP\n")
            self.file.write("M=M+1\n")
        
        return
    
    def write_call(self, function_name, num_args):
        self.label_count += 1

        self.file.write(f"// call {function_name} {num_args}\n")
        self.file.write(f"@RETURN{self.label_count}\n")
        self.file.write("D=A\n")
        self.file.write("@SP\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")
        self.file.write("@SP\n")
        self.file.write("M=M+1\n")

        segments = ["LCL", "ARG", "THIS", "THAT"]
        for segment in segments:
            self.file.write(f"@{segment}\n")
            self.file.write("D=M\n")
            self.file.write("@SP\n")
            self.file.write("A=M\n")
            self.file.write("M=D\n")
            self.file.write("@SP\n")
            self.file.write("M=M+1\n")

        self.file.write("@SP\n")
        self.file.write("D=M\n")
        self.file.write("@5\n")
        self.file.write("D=D-A\n")
        self.file.write(f"@{num_args}\n")
        self.file.write("D=D-A\n")
        self.file.write("@ARG\n")
        self.file.write("M=D\n")

        self.file.write("@SP\n")
        self.file.write("D=M\n")
        self.file.write("@LCL\n")
        self.file.write("M=D\n")

        self.file.write(f"@{function_name}\n")
        self.file.write("0;JMP\n")

        self.file.write(f"(RETURN{self.label_count})\n")

        return
    
    def write_return(self):
        self.file.write("// return\n")
        
        self.file.write("// endFrame = LCL\n")
        self.file.write("@LCL\n")
        self.file.write("D=M\n")
        self.file.write("@R13\n")
        self.file.write("M=D\n")
        
        self.file.write("// returnAddress = *(endFrame - 5)\n")
        self.file.write("@R13\n")
        self.file.write("D=M\n")
        self.file.write("@5\n")
        self.file.write("D=D-A\n")
        self.file.write("A=D\n")
        self.file.write("D=M\n")
        self.file.write("@R14\n")
        self.file.write("M=D\n")

        self.file.write("// *ARG = pop()\n")
        self.file.write("@SP\n")
        self.file.write("M=M-1\n")
        self.file.write("A=M\n")
        self.file.write("D=M\n")
        self.file.write("@ARG\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")

        self.file.write("// SP = ARG + 1\n")
        self.file.write("@ARG\n")
        self.file.write("D=M+1\n")
        self.file.write("@SP\n")
        self.file.write("M=D\n")

        self.file.write("// THAT = *(endFrame - 1)\n")
        self.file.write("@R13\n")
        self.file.write("D=M-1\n")
        self.file.write("A=D\n")
        self.file.write("D=M\n")
        self.file.write("@THAT\n")
        self.file.write("M=D\n")

        self.file.write("// THIS = *(endFrame - 2)\n")
        self.file.write("@2\n")
        self.file.write("D=A\n")
        self.file.write("@R13\n")
        self.file.write("D=M-D\n")
        self.file.write("A=D\n")
        self.file.write("D=M\n")
        self.file.write("@THIS\n")
        self.file.write("M=D\n")

        self.file.write("// ARG = *(endFrame - 3)\n")
        self.file.write("@3\n")
        self.file.write("D=A\n")
        self.file.write("@R13\n")
        self.file.write("D=M-D\n")
        self.file.write("A=D\n")
        self.file.write("D=M\n")
        self.file.write("@ARG\n")
        self.file.write("M=D\n")

        self.file.write("// LCL = *(endFrame - 4)\n")
        self.file.write("@4\n")
        self.file.write("D=A\n")
        self.file.write("@R13\n")
        self.file.write("D=M-D\n")
        self.file.write("A=D\n")
        self.file.write("D=M\n")
        self.file.write("@LCL\n")
        self.file.write("M=D\n")

        self.file.write("// goto returnAddress\n")
        self.file.write("@R14\n")
        self.file.write("A=M\n")
        self.file.write("0;JMP\n")

        return

    def close(self):
        self.file.write("// final loop\n")
        self.file.write("(FINALLOOP)\n")
        self.file.write("@FINALLOOP\n")
        self.file.write("0;JMP\n")
        self.file.close()
        
        return
    
    # END API

    def set_register(self, register, value):
        self.file.write(f"@{value}\n")
        self.file.write("D=A\n")
        self.file.write(f"@{register}\n")
        self.file.write("M=D\n")
        
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
    