#################
# Jack Compiler #
#################

import os
import sys
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
from SymbolTable import SymbolTable
from VMWriter import VMWriter


def single_jack(filename):
    with open(filename, "r") as jackfile:
        tokenizer = JackTokenizer(jackfile)
        symbol_table = SymbolTable()
        generator = VMWriter(filename.replace(".jack", ".vm"))
        parser = CompilationEngine(tokenizer, generator, symbol_table)
        parser.compile_class()
        generator.close()


def process_directory(directory):
    jack_files = [f for f in os.listdir(directory) if f.endswith(".jack")]
    for jack_file in jack_files:
        jack_path = os.path.join(directory, jack_file)
        single_jack(jack_path)


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 VMTranslator <jackfile.jack or directory>")
        return

    input_path = sys.argv[1]

    if os.path.isfile(input_path) and input_path.endswith(".jack"):
        single_jack(input_path)
    elif os.path.isdir(input_path):
        process_directory(input_path)
    else:
        print("Invalid input. Provide a .jack file or a directory containing .jack files.")


if __name__ == "__main__":
    main()

