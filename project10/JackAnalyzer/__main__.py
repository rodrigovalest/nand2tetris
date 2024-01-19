#################
# Jack Analyzer #
#################

import os
import sys
from JackTokenizer import JackTokenizer


def single_jack(filename):
    with open(filename, "r") as jackfile:
        jackTokenizer = JackTokenizer(jackfile)

        while(jackTokenizer.has_more_tokens()):
            jackTokenizer.advance()
            print(jackTokenizer.get_current_token())


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 VMTranslator <vmfile.vm or directory>")
        return

    input_path = sys.argv[1]

    if os.path.isfile(input_path) and input_path.endswith(".jack"):
        single_jack(input_path)

if __name__ == "__main__":
    main()
