import sys
from Parser import Parser
from CodeWriter import CodeWriter

full_filename = sys.argv[1]

if not full_filename:
    print("Usage: python3 VMTranslator <input_file.vm>")
    sys.exit(1)

filename = full_filename.split("/")[-1].replace(".vm", "")

parser = Parser()
codeWriter = CodeWriter(filename)

with open(full_filename, "r") as vmfile:
    full_filename = full_filename.replace(".vm", "")

    with open(full_filename + ".asm", "w") as asmfile:
        default_segments_code = codeWriter.initialize_segments()
        asmfile.write("// instantiating default segments\n")

        for code in default_segments_code:
            asmfile.write(code + "\n")

        for line in vmfile:
            line = parser.parse(line)

            if line:
                codes = codeWriter.code(line)

                if codes:                
                    for code in codes:
                        asmfile.write(code + "\n")

        final_loop_code = codeWriter.final_loop()

        for code in final_loop_code:
            asmfile.write(code + "\n")
