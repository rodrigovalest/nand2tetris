// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// Assumes that R0 >= 0, R1 >= 0, and R0 * R1 < 32768.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

//  while (counter != R1)
//      counter++
//      R2=R2+R0

@R2
M=0

@counter
M=0

(LOOP)
    @R1  // if (counter != R1) goto END
    D=M

    @counter
    D=D-M

    @END
    D;JEQ

    @counter  // counter++
    M=M+1

    @R0  // R2=R2+R0
    D=M

    @R2
    M=D+M

    @LOOP  // goto LOOP
    0;JMP

(END)
    @END
    0;JMP
