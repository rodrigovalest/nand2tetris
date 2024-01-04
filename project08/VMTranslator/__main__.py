import sys
from Parser import Parser
from CodeWriter import CodeWriter

full_vmfilename = sys.argv[1]

if not full_vmfilename or not ".vm" in full_vmfilename:
    print("Usage: python3 VMTranslator <vmfile.vm>")

full_asmfilename = full_vmfilename.replace(".vm", ".asm")

with open(full_vmfilename, "r") as vmfile:
    parser = Parser(vmfile)
    codeWriter = CodeWriter(full_asmfilename)

    codeWriter.initialize_default_segments()

    while parser.hasMoreCommands():
        parser.advance()

        if parser.commandType() == "C_ARITHMETIC":
            codeWriter.writeArithmetic(parser.arg1())
        elif parser.commandType() == "C_PUSH" or parser.commandType() == "C_POP":
            codeWriter.writePushPop(parser.commandType(), parser.arg1(), parser.arg2())

    codeWriter.final_loop()
    codeWriter.close()
