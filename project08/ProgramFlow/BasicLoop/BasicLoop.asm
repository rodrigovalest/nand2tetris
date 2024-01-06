// instantiating default segments
@256
D=A
@SP
M=D
@300
D=A
@LCL
M=D
@400
D=A
@ARG
M=D
@3000
D=A
@THIS
M=D
@3010
D=A
@THAT
M=D
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 0
@LCL
D=M
@0
D=D+A
@2999
M=D
@SP
M=M-1
A=M
D=M
@2999
A=M
M=D
// label LOOP
(LOOP)
// push argument 0
@ARG
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push local 0
@LCL
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
M=M-1
A=M
D=M
@SP
A=M
A=A-1
M=M+D
// pop local 0
@LCL
D=M
@0
D=D+A
@2999
M=D
@SP
M=M-1
A=M
D=M
@2999
A=M
M=D
// push argument 0
@ARG
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
M=M-1
A=M
D=M
@SP
A=M
A=A-1
M=M-D
// pop argument 0
@ARG
D=M
@0
D=D+A
@2999
M=D
@SP
M=M-1
A=M
D=M
@2999
A=M
M=D
// push argument 0
@ARG
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// if-goto LOOP
@SP
M=M-1
A=M
D=M
@LOOP
D;JNE
// push local 0
@LCL
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// final loop
(FINALLOOP)
@FINALLOOP
0;JMP
