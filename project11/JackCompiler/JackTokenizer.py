import re

class JackTokenizer:
    def __init__(self, jackfile):
        self.__file = jackfile
        self.__current_line = []
        self.__current_token = None

        self.__KEYWORDS = ("class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return")
        self.__SYMBOLS = ("{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "!", "~")
        
        self.__line_count = 0

    #####
    # API
        
    def has_more_lines(self):
        current_position = self.__file.tell()
        next_line = self.__file.readline()
        self.__file.seek(current_position)

        return bool(next_line)

    def has_more_tokens(self):
        if len(self.__current_line) > 0:
            return True
        else:
            return self.has_more_lines()
    

    def advance(self):
        while len(self.__current_line) < 3 and self.has_more_lines():
            line = self.__file.readline()
            self.__line_count += 1
            line = self.__sanitize(line)

            if line:
                self.__current_line.extend(line)
            
        if len(self.__current_line) != 0:
            self.__current_token = self.__current_line.pop(0)
        else:
            self.__current_token = None
            raise SystemExit("Error (EOF)")


    def token_type(self):
        if not self.__current_token:
            return None

        if self.__current_token in self.__KEYWORDS:
            return "KEYWORD"
        elif self.__current_token in self.__SYMBOLS:
            return "SYMBOL"
        elif self.__current_token.isdigit():
            return "INT_CONST"
        elif re.match(r'^"[^"\n]*"$|^\'[^\n\']*\'$', self.__current_token):
            return "STRING_CONST"
        elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', self.__current_token):
            return "IDENTIFIER"
        else:
            return None
    

    def keyword(self):
        if self.token_type() == "KEYWORD":
            return self.__current_token
        else:
            return None


    def symbol(self):
        if self.token_type() == "SYMBOL":
            return self.__current_token
        else:
            return None


    def identifier(self):
        if self.token_type() == "IDENTIFIER":
            return self.__current_token
        else:
            return None


    def int_val(self):
        if self.token_type() == "INT_CONST":
            return self.__current_token
        else:
            return None


    def string_val(self):
        if self.token_type() == "STRING_CONST":
            return self.__current_token[1:-1]
        else:
            return None
    

    # END API
    #########
    
    # Separate tokens
    def __sanitize(self, line):
        line = line.strip()

        line = re.sub(r'//.*', '', line)
        line = re.sub(r'/\*.*?\*/', '', line, flags=re.DOTALL)

        if not line:
            self.current_line = []
            self.current_token = None
            return None

        tokens = re.findall(r'".*?"|\b\w+\b|[^\w\s]', line)
        return tokens
    
    def get_current_token(self):
        return self.__current_token
    
    def get_next_token(self):
        if len(self.__current_line) > 0:
            return self.__current_line[0]
        else:
            return None
        
    def get_line_count(self):
        return self.__line_count
        