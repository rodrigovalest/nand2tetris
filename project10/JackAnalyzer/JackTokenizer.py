class JackTokenizer:
    def __init__(self, jackfile):
        self.file = jackfile
        self.current_line = None
        self.current_tokens = []
        self.current_token = None



    def has_more_tokens(self):
        current_position = self.file.tell()
        next_line = self.file.readline()
        self.file.seek(current_position)

        return bool(next_line)
    

    def advance(self):
        if len(self.current_tokens) > 0:
            self.current_token = self.current_tokens[0]
            del self.current_tokens[0]
        else:
            while True:
                line = self.file.readline()
                if not line:
                    return
                self.sanitize(line)
                if self.current_tokens:
                    self.current_token = self.current_tokens.pop(0)
                    break


    # KEYWORD, SYMBOL, INT_CONST, STRING_CONST, IDENTIFIER
    def token_type(self):
        KEYWORDS = ["class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"]
        SYMBOLS = ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]

        if self.current_token in KEYWORDS:
            return "KEYWORD"
        
        elif self.current_token in SYMBOLS:
            return "SYMBOL"
        
        elif self.current_token.isdigit() and 0 <= int(self.current_token) <= 32767:
            return "INT_CONST"
        
        elif (self.current_token.startswith('"') and self.current_token.endswith('"')) or (self.current_token.startswith("'") and self.current_token.endswith("'")):
            return "STRING_CONST"
        
        else:
            return "IDENTIFIER"
    

    # CLASS, METHOD, FUNCTION, CONSTRUCTOR, INT, BOOLEAN, CHAR, VOID, VAR, STATIC, FIELD, LET, DO, IF, ELSE, WHILE, RETURN, TRUE, FALSE, NULL, THIS
    def keyword(self):
        KEYWORDS = {
            "class": "CLASS",
            "constructor": "CONSTRUCTOR",
            "function": "FUNCTION",
            "method": "METHOD",
            "field": "FIELD",
            "static": "STATIC",
            "var": "VAR",
            "int": "INT",
            "char": "CHAR",
            "boolean": "BOOLEAN",
            "void": "VOID",
            "true": "TRUE",
            "false": "FALSE",
            "null": "NULL",
            "this": "THIS",
            "let": "LET",
            "do": "DO",
            "if": "IF",
            "else": "ELSE",
            "while": "WHILE",
            "return": "RETURN"
        }
        
        return KEYWORDS.get(self.current_token)


    def symbol(self):
        return "<symbol> " + self.current_token + " </symbol>"


    def identifier(self):
        return "<identifier> " + self.current_token + " </identifier>"


    def int_val(self):
        return "<integerConstant> " + self.current_token + " </integerConstant>"


    def string_val(self):
        return "<stringConstant> " + self.current_token + " </stringConstant>"
    

    # END API

    def sanitize(self, line):
        line = line.strip()
        if not line or line.startswith("//"):
            self.current_line = None
            self.current_tokens = []
            self.current_token = None
            return None

        line = line.split("//", 1)[0]
        self.current_line = line

        tokens = []
        token = ""
        inside_string = False
        string_delimiter = ''

        for char in line:
            if char.isalnum() or char in ['_', '"', "'"]:
                token += char
                if char in ['"', "'"]:
                    if not inside_string:
                        inside_string = True
                        string_delimiter = char
                    elif char == string_delimiter:
                        inside_string = False
            elif char.isspace() and inside_string:
                token += char
            else:
                if token:
                    tokens.append(token)
                    token = ""
                if char.strip():
                    tokens.append(char)

        if token:
            tokens.append(token)

        self.current_tokens = tokens
        self.current_token = self.current_tokens[0]
