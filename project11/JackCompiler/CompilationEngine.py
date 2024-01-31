from JackTokenizer import JackTokenizer
from VMWriter import VMWriter
from SymbolTable import SymbolTable

class CompilationEngine:
    def __init__(self, tokenizer: JackTokenizer, vmwriter: VMWriter, symbol_table: SymbolTable):
        self.__tokenizer = tokenizer
        self.__vm_writer = vmwriter
        self.__symbol_table = symbol_table
        self.__label_count = 0
        self.__ASCII_TABLE = { 
            "\x00": 0, "\x01": 1, "\x02": 2, "\x03": 3, "\x04": 4, "\x05": 5, "\x06": 6, "\x07": 7, "\x08": 8, "\t": 9, "\n": 10, "\x0b": 11, "\x0c": 12, "\r": 13, "\x0e": 14, "\x0f": 15, "\x10": 16, "\x11": 17, "\x12": 18, "\x13": 19, "\x14": 20, "\x15": 21, "\x16": 22, "\x17": 23, "\x18": 24, "\x19": 25, "\x1a": 26, "\x1b": 27, "\x1c": 28, "\x1d": 29, "\x1e": 30, "\x1f": 31, " ": 32, "!": 33, "\"": 34, "#": 35, "$": 36, "%": 37, "&": 38, "'": 39, "(": 40, ")": 41, "*": 42, "+": 43, ",": 44, "-": 45, ".": 46, "/": 47, "0": 48, "1": 49, "2": 50, "3": 51, "4": 52, "5": 53, "6": 54, "7": 55, "8": 56, "9": 57, ":": 58, ";": 59, "<": 60, "=": 61, ">": 62, "?": 63, "@": 64, "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73, "J": 74, "K": 75, "L": 76, "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84, "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90, "[": 91, "\\": 92, "]": 93, "^": 94, "_": 95, "`": 96, "a": 97, "b": 98, "c": 99, "d": 100, "e": 101, "f": 102, "g": 103, "h": 104, "i": 105, "j": 106, "k": 107, "l": 108, "m": 109, "n": 110, "o": 111, "p": 112, "q": 113, "r": 114, "s": 115, "t": 116, "u": 117, "v": 118, "w": 119, "x": 120, "y": 121, "z": 122, "{": 123, "|": 124, "}": 125, "~": 126, "\x7f": 127 
        }
        self.__classname = None

    #####
    # API

    ## program structure

    # 'class' className '{' classVarDec* subroutineDec* '}'
    def compile_class(self):

        # 'class'
        self.__tokenizer.advance()
        if self.__tokenizer.token_type() == "KEYWORD" and self.__tokenizer.get_current_token() == "class":

            # className
            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "IDENTIFIER":

                self.__classname = self.__tokenizer.get_current_token()

                # '{'
                self.__tokenizer.advance()
                if self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() == "{":

                    # classVarDec*
                    self.__tokenizer.advance()
                    while self.__tokenizer.token_type() == "KEYWORD" and self.__tokenizer.get_current_token() in ["static", "field"]:
                        self.compile_class_var_dec()
                        self.__tokenizer.advance()

                    # subroutineDec*
                    while self.__tokenizer.token_type() == "KEYWORD" and self.__tokenizer.get_current_token() in ["function", "method", "constructor"]:
                        # print(self.__tokenizer.get_current_token())
                        self.compile_subroutine_dec()
                        self.__tokenizer.advance()
                        self.__tokenizer.advance()
                        # print(self.__tokenizer.get_current_token())

                    if self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() == "}":
                        return

        raise SystemExit("ERROR: class")


    # ('static' | 'field') type varName (',' varName)* ';'
    def compile_class_var_dec(self):
        vartype = None
        varnames = []

        # ('static' | 'field')
        if self.__tokenizer.token_type() == "KEYWORD" and self.__tokenizer.get_current_token() in ["static", "field"]:
            varkind = self.__tokenizer.get_current_token()

            # type
            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "IDENTIFIER" or self.__tokenizer.get_current_token() in ["int", "char", "boolean"]:
                vartype = self.__tokenizer.get_current_token()

                # varName
                self.__tokenizer.advance()
                if self.__tokenizer.token_type() == "IDENTIFIER":
                    varnames.append(self.__tokenizer.get_current_token())

                    # (',' varName)*
                    self.__tokenizer.advance()
                    while self.__tokenizer.get_current_token() == ",":
                        self.__tokenizer.advance()
                        if self.__tokenizer.token_type() == "IDENTIFIER": 
                            varnames.append(self.__tokenizer.get_current_token())
                            self.__tokenizer.advance()
                        else:
                            raise SystemExit("ERROR: class var dec")

                    # ';'
                    if self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() == ";":
                        for varname in varnames:
                            self.__symbol_table.define(
                                name=varname,
                                type=vartype,
                                kind=varkind.upper()
                            )

                        return                  

        raise SystemExit("ERROR: class var dec")


    # ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
    def compile_subroutine_dec(self):
        # ('constructor' | 'function' | 'method')
        if self.__tokenizer.token_type() == "KEYWORD" and self.__tokenizer.get_current_token() in ["function", "method", "constructor"]:
            subroutine_type = self.__tokenizer.get_current_token()

            # ('void' | type)
            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "IDENTIFIER" or self.__tokenizer.get_current_token() in ["int", "char", "boolean", "void"]:              
                return_type = self.__tokenizer.get_current_token()

                # subroutineName
                self.__tokenizer.advance()
                if self.__tokenizer.token_type() == "IDENTIFIER":

                    subroutine_name = self.__tokenizer.get_current_token()

                    # '('
                    self.__tokenizer.advance()
                    if self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() == "(":

                        # parameterList
                        self.__symbol_table.start_subroutine()

                        self.__tokenizer.advance()
                        argcount = self.compile_parameter_list()

                        self.__vm_writer.write_function(f"{self.__classname}.{subroutine_name}", (argcount + 1))

                        if subroutine_type == "constructor":
                            self.__vm_writer.write_push("CONST", argcount)
                            self.__vm_writer.write_call("Memory.alloc", 1)
                        else:
                            self.__vm_writer.write_push("ARG", 0)

                        self.__vm_writer.write_pop("POINTER", 0)

                        # ')'
                        if self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() == ")":
                            
                            # subroutineBody
                            self.__tokenizer.advance()
                            self.compile_subroutine_body()
                            
                            return

        raise SystemExit("ERROR: subroutine dec")


    # (type varName) (',' type varName)*
    def compile_parameter_list(self):
        vartype = None
        varname = None
        argcount = 0

        if self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() == ")":
            return 0

        # type
        if self.__tokenizer.token_type() == "IDENTIFIER" or self.__tokenizer.get_current_token() in ["int", "char", "boolean"]:
            vartype = self.__tokenizer.get_current_token()
        
            # varName
            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "IDENTIFIER":
                varname = self.__tokenizer.get_current_token()

                self.__symbol_table.define(
                    name=varname,
                    type=vartype,
                    kind="ARG"
                )
                argcount += 1

                # (',' type varName)*
                self.__tokenizer.advance()
                while self.__tokenizer.get_current_token() == ",":
                    self.__tokenizer.advance()
                    if self.__tokenizer.token_type() == "IDENTIFIER" or self.__tokenizer.get_current_token() in ["int", "char", "boolean"]:
                        vartype = self.__tokenizer.get_current_token()
                    
                        self.__tokenizer.advance()
                        if self.__tokenizer.token_type() == "IDENTIFIER":
                            varname = self.__tokenizer.get_current_token()
                            self.__symbol_table.define(
                                name=varname,
                                type=vartype,
                                kind="ARG"
                            )
                            argcount += 1
                            self.__tokenizer.advance()
                            continue

                    raise SystemExit("ERROR: parameter list")

                # '('
                if self.__tokenizer.get_current_token() == ")":
                    return argcount

        raise SystemExit("ERROR: parameter list")
    

    # '{' varDec* statements '}'
    def compile_subroutine_body(self):
        # '{'
        if self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() == "{":
            # varDec*
            if self.__tokenizer.get_next_token() == "var":
                while self.__tokenizer.get_next_token() == "var":
                    self.__tokenizer.advance()
                    self.compile_var_dec()

            # statements
            if self.__tokenizer.get_next_token() != "}":
                self.compile_statements()
                return

            # '}'
            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() == "}":
                return

        raise SystemExit("ERROR: subroutine body")


    # 'var' type varName (',' varName)* ';'
    def compile_var_dec(self):
        vartype = None
        varnames = []

        # 'var'
        if self.__tokenizer.get_current_token() == "var":
            
            # type
            self.__tokenizer.advance()
            if (
                self.__tokenizer.token_type() == "IDENTIFIER" 
                or (self.__tokenizer.token_type() == "KEYWORD" and self.__tokenizer.get_current_token() in ["int", "char", "boolean"])
            ):
                vartype = self.__tokenizer.get_current_token()
                
                # varName
                self.__tokenizer.advance()
                if self.__tokenizer.token_type() == "IDENTIFIER":
                    varnames.append(self.__tokenizer.get_current_token())

                    # (',' varName)*
                    self.__tokenizer.advance()
                    while self.__tokenizer.get_current_token() == ",":
                        self.__tokenizer.advance()
                        
                        if self.__tokenizer.token_type() == "IDENTIFIER":
                            varnames.append(self.__tokenizer.get_current_token())
                            self.__tokenizer.advance()
                        else:
                            raise SystemExit("ERROR: var_dec")
                    
                    # ';'
                    if self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() == ";":
                        for varname in varnames:
                            self.__symbol_table.define(
                                name=varname,
                                type=vartype,
                                kind="VAR"
                            )
                        
                        return

        raise SystemExit("ERROR: var_dec")


    ## statements

    # statement*
    def compile_statements(self):
        while self.__tokenizer.get_next_token() != "}":
            self.__tokenizer.advance()
            if self.__tokenizer.get_current_token() == "let":
                self.compile_let()
            elif self.__tokenizer.get_current_token() == "if":
                self.compile_if()
            elif self.__tokenizer.get_current_token() == "while":
                self.compile_while()
            elif self.__tokenizer.get_current_token() == "do":
                self.compile_do()
            elif self.__tokenizer.get_current_token() == "return":
                self.compile_return()
            else:
                raise SystemExit("ERROR: statements")


    # 'let' varName ('[' expression ']')? '=' expression ';'
    def compile_let(self):

        # 'let'
        if self.__tokenizer.get_current_token() == "let":
            
            # 'varName'
            self.__tokenizer.advance() 
            if self.__tokenizer.token_type() == "IDENTIFIER":
                varname = self.__tokenizer.get_current_token()

                type = self.__symbol_table.type_of(varname)
                index = self.__symbol_table.index_of(varname)
                kind = self.__symbol_table.kind_of(varname)
                segment = {"ARG": "ARG", "VAR": "LOCAL", "STATIC": "STATIC", "FIELD": "THIS"}.get(kind, None)

                if type is None or index is None or kind is None:
                    raise SystemExit("ERROR: let")

                self.__vm_writer.write_pop(
                    segment=segment,
                    index=index
                )

                # ('[' expression ']')?
                self.__tokenizer.advance()
                if self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() == "[":
                    return
                
                # '='
                if self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() == "=":

                    # expression
                    self.__tokenizer.advance()
                    expression_type = self.compile_expression()

                    if (
                        expression_type == "integer_expression" and type not in ["int", "boolean"]
                        or expression_type == "string_expression" and type != "char"
                    ):
                        raise SystemExit("ERROR: let type don't match")

                    # ';'
                    if self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() == ";":
                        return                 

        raise SystemExit("ERROR: let")            
        

    # if '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
    def compile_if(self):
        label_else = f"L{self.__label_count}"
        label_endif = f"L{self.__label_count + 1}"
        self.__label_count += 2

        # 'if'
        if self.__tokenizer.get_current_token() == "if":
            
            # '('
            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() == "(":
                
                # expression
                self.__tokenizer.advance()
                self.compile_expression()
                self.__vm_writer.write_arithmetic("not")
                self.__vm_writer.write_if(label_else)

                # ')'
                if self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() == ")":

                    # '{'
                    self.__tokenizer.advance()
                    if self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() == "{":
                       
                        # statements
                        if self.__tokenizer.get_next_token() != "}":
                            self.compile_statements()
                    
                        # '}'
                        self.__tokenizer.advance()
                        if self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() == "}":
                            self.__vm_writer.write_goto(label_endif)
                            self.__vm_writer.write_label(label_else)

                            # ('else' '{' statements '}')?
                            if self.__tokenizer.has_more_tokens() and self.__tokenizer.get_next_token() == "else":
                                self.__tokenizer.advance()

                                # '{'
                                self.__tokenizer.advance()
                                if self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() == "{":
                                    
                                    # statements
                                    if self.__tokenizer.get_next_token() != "}":
                                        self.compile_statements()

                                    # '}'
                                    self.__tokenizer.advance()
                                    if self.__tokenizer.token_type() != "SYMBOL" or self.__tokenizer.get_current_token() != "}":
                                        raise SystemExit("ERROR: else")
                                else:
                                    raise SystemExit("ERROR: else") 

                            self.__vm_writer.write_label(label_endif)
                            return
            
        raise SystemExit("ERROR: if") 


    # 'while' '(' expression ')' '{' statements '}'
    def compile_while(self):
        label_initloop = f"L{self.__label_count}"
        label_endloop = f"L{self.__label_count + 1}"
        self.__label_count += 2

        # 'while'
        if self.__tokenizer.get_current_token() == "while":
            self.__vm_writer.write_label(label_initloop)
            
            # '('
            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() == "(":
                
                # expression
                self.__tokenizer.advance()
                self.compile_expression()
                self.__vm_writer.write_arithmetic("not")
                self.__vm_writer.write_if(label_endloop)

                # ')'
                if self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() == ")":

                    # '{'
                    self.__tokenizer.advance()
                    if self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() == "{":

                        # statements
                        if self.__tokenizer.get_next_token() != "}":
                            self.compile_statements()

                        # '}'
                        self.__tokenizer.advance()
                        if self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() == "}":
                            self.__vm_writer.write_goto(label_initloop)
                            self.__vm_writer.write_label(label_endloop)
                            return
            
        raise SystemExit("ERROR: while")


    # 'do' subroutineCall ';'
    # 'do' expression ';'
    # expression = object expression
    def compile_do(self):
        
        # 'do'
        if self.__tokenizer.get_current_token() == "do":
            
            # expression?
            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "IDENTIFIER":
                expression_type = self.compile_expression()

                # ';'
                if expression_type == "object_expression" and self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() == ";":
                    return

        raise SystemExit("ERROR: do")


    # 'return' expression? ';'
    def compile_return(self):

        # 'return'
        if self.__tokenizer.get_current_token() == "return":
            
            # expression?
            self.__tokenizer.advance()
            if self.__tokenizer.get_current_token() != ";":
                self.compile_expression()

                # ';'
                if self.__tokenizer.get_current_token() == ";":
                    self.__vm_writer.write_return()
                    return

            # ';'
            else:
                self.__vm_writer.write_push("CONST", 0)
                self.__vm_writer.write_return()
                return                

        raise SystemExit("ERROR: return")
            

    ## expressions

    # (expression (',' expression)*)?
    def compile_expression_list(self, expression_tokens):
        count = 0

        if expression_tokens is None:
            self.compile_expression()
            count += 1

            while self.__tokenizer.get_current_token() == ",":
                self.__tokenizer.advance()
                self.compile_expression()
                count += 1
        else:
            current_expression_tokens = []
            parentheses_depth = 0

            for expression_token in expression_tokens:
                current_expression_tokens.append(expression_token)

                if expression_token["token"] == "(":
                    parentheses_depth += 1
                elif expression_token["token"] == ")":
                    parentheses_depth -= 1

                if parentheses_depth == 0 and expression_token["token"] == ",":
                    self.compile_expression(current_expression_tokens[:-1])
                    count += 1
                    current_expression_tokens = []

            if current_expression_tokens:
                self.compile_expression(current_expression_tokens)
                count += 1

            return count


    # term (op term)*
    def compile_expression(self, expression_tokens=None):
        if expression_tokens is None:
            first_token_type = self.__tokenizer.token_type()
            first_token = self.__tokenizer.get_current_token()
        else:
            first_token_type = expression_tokens[0]["type"]
            first_token = expression_tokens[0]["token"]

        expression_type = None

        # first token type determine the expression type
        if (
            first_token_type == "INT_CONST" 
            or (first_token_type == "KEYWORD" and first_token in ["true", "false", "null"]) 
            or (first_token_type == "SYMBOL" and first_token in ["~", "-"])
        ):
            expression_type = "int"
        
        elif first_token_type == "STRING_CONST":
            expression_type = "string"
        
        elif first_token_type == "IDENTIFIER":
            var_type = self.__symbol_table.type_of(first_token)

            if var_type in ["int", "boolean"]:
                expression_type = "int"
            elif var_type == "string":
                expression_type = "string"
            else:
                expression_type = "object"

        if expression_type == "int":
            if expression_tokens is None: expression_tokens = self.__get_expression_tokens()
            self.handle_integer_expression(expression_tokens)
            return "integer_expression"
        elif expression_type == "string":
            if expression_tokens is None: expression_tokens = self.__get_expression_tokens()
            self.handle_string_expression(expression_tokens)
            return "string_expression"
        elif expression_type == "object":
            if expression_tokens is None: expression_tokens = self.__get_expression_tokens(expression_type)
            self.handle_object_expression(expression_tokens)
            return "object_expression"

        raise SystemExit("ERROR: invalid token in expression")


    # integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | '(' expression ')' | unaryOp term
    def compile_term(self, token, token_type):
        if token_type in ["INT_CONST", "KEYWORD"]:
            self.__vm_writer.write_push("CONST", token)

        elif token_type == "SYMBOL":
            commands = {"+": "add", "-": "sub", "*": "mult", "/": "div", "&": "and", "|": "or", "<": "lt", ">": "gt", "=": "eq", "-": "neg", "~": "not"}
            
            command = commands.get(token, None)
            if command: 
                self.__vm_writer.write_arithmetic(command)

        elif token_type == "STRING_CONST":
            return
        
        elif token_type == "IDENTIFIER":
            kind = self.__symbol_table.kind_of(token)
            index = self.__symbol_table.index_of(token)
            segment = {"ARG": "ARG", "VAR": "LOCAL", "STATIC": "STATIC", "FIELD": "THIS"}.get(kind, None)
            
            if segment is not None and index is not None:
                self.__vm_writer.write_push(segment, index)
        else:
            raise SystemExit("ERROR: term")
        
    
    # END API
    #########

    def handle_integer_expression(self, expression_tokens):
        for expression_token in expression_tokens:
            token_type = expression_token["type"]
            token = expression_token["token"]
            
            if token_type == "STRING_CONST":
                raise SystemExit("ERROR: invalid token in integer expression")
            
            elif token_type == "IDENTIFIER":
                var_type = self.__symbol_table.type_of(token)
                
                if not var_type or not var_type in ["int", "boolean"]:
                    raise SystemExit("ERROR: invalid token in integer expression")

            elif token_type == "KEYWORD":
                if token in ["false", "null"]:
                    expression_token["token"] = 0
                elif token == "true":
                    expression_token["token"] = 1
                else:
                    raise SystemExit("ERROR: invalid token in integer expression")

            elif token_type == "SYMBOL" and not token in ["+", "-", "*", "/", "&", "|", "<", ">", "(", ")", "~", "="]:
                raise SystemExit("ERROR: invalid token in integer expression")

        # shuting yard algorithm
        queue = []
        stack = []
        priority = { "~": 3, "-": 3, "*": 2, "/": 2, "+": 1, "-": 1, "&": 0, "|": 0, "<": 0, ">": 0, "=": 0 }

        for expression_token in expression_tokens:
            token_type = expression_token["type"]
            token = expression_token["token"]

            if token_type in ["KEYWORD", "INT_CONST"]:
                queue.append(expression_token)

            elif token_type == "IDENTIFIER" and self.__symbol_table.type_of(token) == "int":
                queue.append(expression_token)

            elif token_type == "SYMBOL" and token in ["+", "-", "*", "/", "&", "|", "<", ">", "=", "~", "-"]:
                while (
                    len(stack) > 0
                    and stack[-1]["token"] in ["+", "-", "*", "/", "&", "|", "<", ">", "=", "~", "-"]
                    and priority[stack[-1]["token"]] >= priority[token]
                ):
                    queue.append(stack.pop())
                stack.append(expression_token)
            
            elif token_type == "SYMBOL" and token == "(":
                stack.append(expression_token)

            elif token_type == "SYMBOL" and token == ")":
                while stack[-1]["token"] != "(":
                    queue.append(stack.pop())
                stack.pop()

        while not len(stack) == 0:
            queue.append(stack.pop())

        for term in queue:
            self.compile_term(term["token"], term["type"])
            

    def handle_string_expression(self, expression_tokens):
        if len(expression_tokens) != 1:
            raise SystemExit("ERROR: invalid token in string expression")
            
        token_type = expression_tokens[0]["type"]
        token = expression_tokens[0]["token"]
        self.compile_term(token, token_type)
    

    # subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList ')'
    def handle_object_expression(self, expression_tokens):

        ## function()
        if (
            expression_tokens[0]["type"] == "IDENTIFIER"
            and expression_tokens[1]["type"] == "SYMBOL" 
            and expression_tokens[1]["token"] == "("
            and expression_tokens[-1]["type"] == "SYMBOL"
            and expression_tokens[-1]["token"] == ")"
        ):
            subroutine_name = expression_tokens[0]["token"]
            expression_list_tokens = expression_tokens[4:-1]   

            expressions_count = 0
            if len(expression_list_tokens) > 0 and len(expression_tokens) != 5:
                expressions_count += self.compile_expression_list(expression_list_tokens)
                
            self.__vm_writer.write_call(subroutine_name, expressions_count)
            return

        # object.foo()
        elif (
            expression_tokens[0]["type"] == "IDENTIFIER"
            and expression_tokens[1]["type"] == "SYMBOL"
            and expression_tokens[1]["token"] == "."
            and expression_tokens[2]["type"] == "IDENTIFIER"
            and expression_tokens[-1]["type"] == "SYMBOL" 
            and expression_tokens[-1]["token"] == ")" 
        ):
            classname = expression_tokens[0]["token"]
            subroutine_name = expression_tokens[2]["token"]

            type = self.__symbol_table.type_of(expression_tokens[0]["token"])
            kind = self.__symbol_table.kind_of(expression_tokens[0]["token"])
            index = self.__symbol_table.index_of(expression_tokens[0]["token"])
            segment = {"ARG": "ARG", "VAR": "LOCAL", "STATIC": "STATIC", "FIELD": "THIS"}.get(kind, None) 

            if segment is not None and index is not None:
                self.__vm_writer.write_push(segment, index)
            
            if not type in ["int", "char", "boolean"]:
                expression_list_tokens = expression_tokens[4:-1]
                
                if type == "object": expressions_count = 1
                else: expressions_count = 0

                if len(expression_list_tokens) > 0 and len(expression_tokens) != 5:
                    expressions_count += self.compile_expression_list(expression_list_tokens)

                self.__vm_writer.write_call(f"{classname}.{subroutine_name}", expressions_count)
                return
        
        raise SystemExit("ERROR: object expression")
    

    def __get_expression_tokens(self, expression_type=None):
        expression_tokens = []
        parentheses_count = 0
        squarebrackets_count = 0
        
        limiters = None

        if expression_type == "object": limiters = (";", None)
        else: limiters = (";", ",", None)
        
        while self.__tokenizer.has_more_tokens():
            current_token = {
                "token": self.__tokenizer.get_current_token(),
                "type": self.__tokenizer.token_type()
            }

            if current_token["token"] == "(":
                parentheses_count += 1

            elif current_token["token"] == "[":
                squarebrackets_count += 1
            
            elif current_token["token"] == ")":
                parentheses_count -= 1
                if parentheses_count == -1:
                    break

            elif current_token["token"] == "]":
                squarebrackets_count -= 1
                if squarebrackets_count == -1:
                    break

            elif current_token["token"] in limiters:
                break
            
            expression_tokens.append(current_token)
            self.__tokenizer.advance()

        if len(expression_tokens) == 0:
            raise SystemExit("ERROR: get expression error")

        return expression_tokens
    