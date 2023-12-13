// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen
// by writing 'black' in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen by writing
// 'white' in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(INFINITELOOP)
    // if KDB != 0 goto PRINTSCREEN
    @KBD
    D=M

    @PRINTSCREEN
    D;JNE

    // goto INFINITELOOP
    @INFINITELOOP
    0;JMP

    (PRINTSCREEN)
        // counter = 0
        @counter
        M=0

        @SCREEN
        D=M

        @ONSCREEN
        D;JEQ

            (OFFSCREEN)
                @counter
                D=M

                // screen = screen + counter
                @SCREEN
                A=A+D        
                M=0

                // counter++
                @counter
                M=M+1

                // if (counter != 8191) goto OFFSCREEN
                @screensize
                D=M

                @counter
                D=M-D

                @OFFSCREEN
                D;JLT

                // goto INFINITELOOP
                @INFINITELOOP
                0;JMP

            (ONSCREEN)
                @counter
                D=M

                // screen = screen + counter
                @SCREEN
                A=A+D        
                M=1

                // counter++
                @counter
                M=M+1

                // if (counter != 8191) goto ONSCREEN
                @screensize
                D=M

                @counter
                D=M-D
                
                @ONSCREEN
                D;JLT

                // goto INFINITELOOP
                @INFINITELOOP
                0;JMP
