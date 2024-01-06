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
// function Class2.set 0
(Class2.set)
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
// pop static 0
@SP
M=M-1
A=M
D=M
@StaticsTest.0
M=D
// push argument 1
@ARG
D=M
@1
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop static 1
@SP
M=M-1
A=M
D=M
@StaticsTest.1
M=D
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
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
// function Class2.get 0
(Class2.get)
// push static 0
@StaticsTest.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// push static 1
@StaticsTest.1
D=M
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
// function Class1.set 0
(Class1.set)
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
// pop static 0
@SP
M=M-1
A=M
D=M
@StaticsTest.0
M=D
// push argument 1
@ARG
D=M
@1
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop static 1
@SP
M=M-1
A=M
D=M
@StaticsTest.1
M=D
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
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
// function Class1.get 0
(Class1.get)
// push static 0
@StaticsTest.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// push static 1
@StaticsTest.1
D=M
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
// function Sys.init 0
(Sys.init)
// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Class1.set 2
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
@2
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.set
0;JMP
(RETURN2)
// pop temp 0
@SP
M=M-1
@SP
A=M
D=M
@5
M=D
// push constant 23
@23
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 15
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Class2.set 2
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
@2
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.set
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
// call Class1.get 0
@RETURN4
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
@Class1.get
0;JMP
(RETURN4)
// call Class2.get 0
@RETURN5
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
@Class2.get
0;JMP
(RETURN5)
// label END
(END)
// goto END
@END
0;JMP
// final loop
(FINALLOOP)
@FINALLOOP
0;JMP
