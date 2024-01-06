// bootstrap code
@256
D=A
@SP
M=D
// call Sys.init 0
@RETURN1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(RETURN1)
// function Sys.init 0
(Sys.init)
// push constant 4000
@4000
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@SP
M=M-1
A=M
D=M
@THIS
M=D
// push constant 5000
@5000
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@SP
M=M-1
A=M
D=M
@THAT
M=D
// call Sys.main 0
@RETURN2
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.main
0;JMP
(RETURN2)
// pop temp 1
@SP
M=M-1
@SP
A=M
D=M
@6
M=D
// label LOOP
(LOOP)
// goto LOOP
@LOOP
0;JMP
// function Sys.main 5
(Sys.main)
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1
// push constant 4001
@4001
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@SP
M=M-1
A=M
D=M
@THIS
M=D
// push constant 5001
@5001
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@SP
M=M-1
A=M
D=M
@THAT
M=D
// push constant 200
@200
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 1
@LCL
D=M
@1
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
// push constant 40
@40
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 2
@LCL
D=M
@2
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
// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 3
@LCL
D=M
@3
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
// push constant 123
@123
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Sys.add12 1
@RETURN3
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.add12
0;JMP
(RETURN3)
// pop temp 0
@SP
M=M-1
@SP
A=M
D=M
@5
M=D
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
// push local 1
@LCL
D=M
@1
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push local 2
@LCL
D=M
@2
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push local 3
@LCL
D=M
@3
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// push local 4
@LCL
D=M
@4
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
// add
@SP
M=M-1
A=M
D=M
@SP
A=M
A=A-1
M=M+D
// add
@SP
M=M-1
A=M
D=M
@SP
A=M
A=A-1
M=M+D
// add
@SP
M=M-1
A=M
D=M
@SP
A=M
A=A-1
M=M+D
// return
// endFrame = LCL
@LCL
D=M
@R13
M=D
// returnAddress = *(endFrame - 5)
@R13
D=M
@5
D=D-A
A=D
D=M
@R14
M=D
// *ARG = pop()
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
// SP = ARG + 1
@ARG
D=M+1
@SP
M=D
// THAT = *(endFrame - 1)
@R13
D=M-1
A=D
D=M
@THAT
M=D
// THIS = *(endFrame - 2)
@2
D=A
@R13
D=M-D
A=D
D=M
@THIS
M=D
// ARG = *(endFrame - 3)
@3
D=A
@R13
D=M-D
A=D
D=M
@ARG
M=D
// LCL = *(endFrame - 4)
@4
D=A
@R13
D=M-D
A=D
D=M
@LCL
M=D
// goto returnAddress
@R14
A=M
0;JMP
// function Sys.add12 0
(Sys.add12)
// push constant 4002
@4002
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@SP
M=M-1
A=M
D=M
@THIS
M=D
// push constant 5002
@5002
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@SP
M=M-1
A=M
D=M
@THAT
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
// push constant 12
@12
D=A
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
// return
// endFrame = LCL
@LCL
D=M
@R13
M=D
// returnAddress = *(endFrame - 5)
@R13
D=M
@5
D=D-A
A=D
D=M
@R14
M=D
// *ARG = pop()
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
// SP = ARG + 1
@ARG
D=M+1
@SP
M=D
// THAT = *(endFrame - 1)
@R13
D=M-1
A=D
D=M
@THAT
M=D
// THIS = *(endFrame - 2)
@2
D=A
@R13
D=M-D
A=D
D=M
@THIS
M=D
// ARG = *(endFrame - 3)
@3
D=A
@R13
D=M-D
A=D
D=M
@ARG
M=D
// LCL = *(endFrame - 4)
@4
D=A
@R13
D=M-D
A=D
D=M
@LCL
M=D
// goto returnAddress
@R14
A=M
0;JMP
// final loop
(FINALLOOP)
@FINALLOOP
0;JMP
