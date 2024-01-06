import os
import sys
from Parser import Parser
from CodeWriter import CodeWriter

def translate_single_vm(vm_filename):
    full_asmfilename = vm_filename.replace(".vm", ".asm")

    with open(vm_filename, "r") as vmfile:
        parser = Parser(vmfile)
        codeWriter = CodeWriter(full_asmfilename)

        codeWriter.write_init()

        while parser.has_more_commands():
            parser.advance()

            if parser.command_type() == "C_ARITHMETIC":
                codeWriter.write_arithmetic(parser.arg1())
            elif parser.command_type() == "C_PUSH" or parser.command_type() == "C_POP":
                codeWriter.write_push_pop(parser.command_type(), parser.arg1(), parser.arg2())
            elif parser.command_type() == "C_LABEL":
                codeWriter.write_label(parser.arg1())
            elif parser.command_type() == "C_GOTO":
                codeWriter.write_goto(parser.arg1())
            elif parser.command_type() == "C_IF":
                codeWriter.write_if(parser.arg1())
            elif parser.command_type() == "C_FUNCTION":
                codeWriter.write_function(parser.arg1(), parser.arg2())
            elif parser.command_type() == "C_CALL":
                codeWriter.write_call(parser.arg1(), parser.arg2())
            elif parser.command_type() == "C_RETURN":
                codeWriter.write_return()

        codeWriter.close()

def translate_vm_files(directory):
    asm_filename = os.path.join(directory, os.path.basename(directory.rstrip('/')) + ".asm")

    with open(asm_filename, "w") as asmfile:
        codeWriter = CodeWriter(asm_filename)
        codeWriter.write_init()

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".vm"):
                    vm_filename = os.path.join(root, file)
                    with open(vm_filename, "r") as vmfile:
                        parser = Parser(vmfile)

                        while parser.has_more_commands():
                            parser.advance()

                            if parser.command_type() == "C_ARITHMETIC":
                                codeWriter.write_arithmetic(parser.arg1())
                            elif parser.command_type() == "C_PUSH" or parser.command_type() == "C_POP":
                                codeWriter.write_push_pop(parser.command_type(), parser.arg1(), parser.arg2())
                            elif parser.command_type() == "C_LABEL":
                                codeWriter.write_label(parser.arg1())
                            elif parser.command_type() == "C_GOTO":
                                codeWriter.write_goto(parser.arg1())
                            elif parser.command_type() == "C_IF":
                                codeWriter.write_if(parser.arg1())
                            elif parser.command_type() == "C_FUNCTION":
                                codeWriter.write_function(parser.arg1(), parser.arg2())
                            elif parser.command_type() == "C_CALL":
                                codeWriter.write_call(parser.arg1(), parser.arg2())
                            elif parser.command_type() == "C_RETURN":
                                codeWriter.write_return()

        codeWriter.close()

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 VMTranslator <vmfile.vm or directory>")
        return

    input_path = sys.argv[1]

    if os.path.isfile(input_path) and input_path.endswith(".vm"):
        translate_single_vm(input_path)
    elif os.path.isdir(input_path):
        translate_vm_files(input_path)
    else:
        print("Invalid input. Please provide a .vm file or a directory containing .vm files.")

if __name__ == "__main__":
    main()
