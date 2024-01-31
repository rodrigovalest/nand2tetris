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
        vm_writer = VMWriter(filename.replace(".jack", ".vm"))
        parser = CompilationEngine(tokenizer, vm_writer, symbol_table)

        # tokenizer.advance()

        # symbol_table.define(
        #     name="teste",
        #     type="Teste",
        #     kind="VAR"
        # )

        # symbol_table.define(
        #     name="testando",
        #     type="Testando",
        #     kind="VAR"
        # )

        # symbol_table.define(
        #     name="game",
        #     type="PongGame",
        #     kind="VAR"
        # )

        parser.compile_class()


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 VMTranslator <vmfile.vm or directory>")
        return

    input_path = sys.argv[1]

    if os.path.isfile(input_path) and input_path.endswith(".jack"):
        single_jack(input_path)

if __name__ == "__main__":
    main()
