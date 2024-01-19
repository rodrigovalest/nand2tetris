#################
# Jack Analyzer #
#################

import os
import sys
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

def single_jack(filename):
    with open(filename, "r") as jackfile:
        tokenizer = JackTokenizer(jackfile)

        xmlfilename = filename.replace()
        parser = CompilationEngine(tokenizer, )

        while(tokenizer.has_more_tokens()):
            tokenizer.advance()
            print(tokenizer.get_current_token())
            
            type = tokenizer.token_type()
            
            if (type == "IDENTIFIER"):
                print(tokenizer.identifier())
            elif (type == "INT_CONST"):
                print(tokenizer.int_val())
            elif (type == "KEYWORD"):
                print(tokenizer.keyword())
            elif (type == "STRING_CONST"):
                print(tokenizer.string_val())
            elif (type == "SYMBOL"):
                print(tokenizer.symbol())

            print("\n")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 VMTranslator <vmfile.vm or directory>")
        return

    input_path = sys.argv[1]

    if os.path.isfile(input_path) and input_path.endswith(".jack"):
        single_jack(input_path)

if __name__ == "__main__":
    main()
