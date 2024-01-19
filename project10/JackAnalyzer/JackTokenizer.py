import re

class JackTokenizer:
    def __init__(self, jackfile):
        self.__file = jackfile
        self.__current_line = []
        self.__current_token = None

    #####
    # API

    def has_more_tokens(self):
        current_position = self.__file.tell()
        next_line = self.__file.readline()
        self.__file.seek(current_position)

        return bool(next_line)
    

    def advance(self):
        while len(self.__current_line) == 0:
            line = self.__file.readline()
            line = self.__sanitize(line)

            if line:
                self.__current_line = line
                break

        self.__current_token = self.__current_line.pop(0)


    def token_type(self):
        return
    

    def keyword(self):
        return


    def symbol(self):
        return


    def identifier(self):
        return


    def int_val(self):
        return


    def string_val(self):
        return
    

    # END API
    #########
    
    def __sanitize(self, line):
        line = line.strip()

        # Remove comments
        line = re.sub(r'//.*', '', line)
        line = re.sub(r'/\*.*?\*/', '', line, flags=re.DOTALL)

        if not line:
            self.current_line = []
            self.current_token = None
            return None

        # Regex to separate tokens
        tokens = re.findall(r'".*?"|\b\w+\b|[^\w\s]', line)
        return tokens
    
    def get_current_token(self):
        return self.__current_token
