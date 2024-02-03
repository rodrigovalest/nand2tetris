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
        self.eat(["KEYWORD"], ["class"])

        # className
        self.eat(["IDENTIFIER"])
        self.__classname = self.__tokenizer.get_current_token()

        # '{'
        self.eat(["SYMBOL"], ["{"])

        # classVarDec*
        while self.__tokenizer.get_next_token() in ["static", "field"]:
            self.eat(["KEYWORD"], ["static", "field"])
            self.compile_class_var_dec()

        # subroutineDec*
        while self.__tokenizer.get_next_token() in ["function", "method", "constructor"]:
            self.eat(["KEYWORD"], ["function", "method", "constructor"])
            self.compile_subroutine_dec()

        # '}'
        self.eat(["SYMBOL"], ["}"])



    # ('static' | 'field') type varName (',' varName)* ';'
    def compile_class_var_dec(self):
        vartype = None
        varnames = []

        # ('static' | 'field')
        self.eat(["KEYWORD"], ["static", "field"], False)
        varkind = self.__tokenizer.get_current_token()

        # type
        self.eat(["KEYWORD", "IDENTIFIER"])
        vartype = self.__tokenizer.get_current_token()

        # varName
        self.eat(["IDENTIFIER"])
        varnames.append(self.__tokenizer.get_current_token())

        # (',' varName)*
        while self.__tokenizer.get_next_token() == ",":
            self.eat(["SYMBOL"], [","])
            self.eat(["IDENTIFIER"])
            varnames.append(self.__tokenizer.get_current_token())            

        # ';'
        self.eat(["SYMBOL"], [";"])
        for varname in varnames:
            self.__symbol_table.define(name=varname, type=vartype, kind=varkind.upper())



    # ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' '{' varDec* statements '}'
    def compile_subroutine_dec(self):
        self.__symbol_table.start_subroutine()

        # ('constructor' | 'function' | 'method')
        self.eat(["KEYWORD"], ["function", "method", "constructor"], False)
        subroutine_type = self.__tokenizer.get_current_token()

        if subroutine_type == "method":
            self.__symbol_table.define(name="this", type=self.__classname, kind="ARG")

        # ('void' | type)
        self.eat(["KEYWORD", "IDENTIFIER"])

        # subroutineName
        self.eat(["IDENTIFIER"])
        subroutine_name = self.__tokenizer.get_current_token()

        # '('
        self.eat(["SYMBOL"], ["("])
        # parameterList
        self.compile_parameter_list()
        # ')'
        self.eat(["SYMBOL"], [")"])
        # '{'
        self.eat(["SYMBOL"], ["{"])
            
        # varDec*
        while self.__tokenizer.get_next_token() == "var":
            self.eat(["KEYWORD"], ["var"])
            self.compile_var_dec()

        var_count = str(self.__symbol_table.var_count("VAR", "subroutine"))
        
        self.__vm_writer.write_function(f"{self.__classname}.{subroutine_name}", var_count)

        if subroutine_type == "constructor":
            self.__symbol_table.define("this", self.__classname, "FIELD")

            field_count = str(self.__symbol_table.var_count("FIELD", "class"))
            self.__vm_writer.write_push("CONST", field_count)
            self.__vm_writer.write_call("Memory.alloc", 1)
            self.__vm_writer.write_pop("POINTER", 0)
            
        elif subroutine_type == "method":
            self.__vm_writer.write_push("ARG", 0)
            self.__vm_writer.write_pop("POINTER", 0)


        # statements
        if self.__tokenizer.get_next_token() != "}":
            self.compile_statements()

        # '}'
        self.eat(["SYMBOL"], ["}"])




    # (type varName) (',' type varName)*
    def compile_parameter_list(self):
        vartype = None
        varname = None
        argcount = 0
        
        if self.__tokenizer.get_next_token() == ")":
            return 0

        # type
        self.eat(["IDENTIFIER", "KEYWORD"])
        vartype = self.__tokenizer.get_current_token()
        
        # varName
        self.eat(["IDENTIFIER"])
        varname = self.__tokenizer.get_current_token()

        self.__symbol_table.define(name=varname, type=vartype, kind="ARG")
        argcount += 1

        # (',' type varName)*
        while self.__tokenizer.get_next_token() == ",":
            self.eat(["SYMBOL"], [","])

            self.eat(["IDENTIFIER", "KEYWORD"])
            vartype = self.__tokenizer.get_current_token()

            self.eat(["IDENTIFIER"])
            varname = self.__tokenizer.get_current_token()
            self.__symbol_table.define(name=varname, type=vartype, kind="ARG")
            
            argcount += 1
        
        return argcount
    
    

    # 'var' type varName (',' varName)* ';'
    def compile_var_dec(self):
        vartype = None
        varnames = []

        # 'var'
        self.eat(["KEYWORD"], ["var"], False)

        # type
        self.eat(["IDENTIFIER", "KEYWORD"])
        vartype = self.__tokenizer.get_current_token()
                
        # varName
        self.eat(["IDENTIFIER"])
        varnames.append(self.__tokenizer.get_current_token())

        # (',' varName)*
        self.eat()
        while self.__tokenizer.get_current_token() == ",":
            self.eat()
            
            if self.__tokenizer.token_type() == "IDENTIFIER":
                varnames.append(self.__tokenizer.get_current_token())
                self.eat()
            else:
                raise SystemExit(f"ERROR: var_dec. File: {self.__classname}. Line: {self.__tokenizer.get_line_count()}")
                    
        # ';'
        self.eat(["SYMBOL"], [";"], False)
        
        for varname in varnames: 
            self.__symbol_table.define(name=varname, type=vartype, kind="VAR")
            


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
                raise SystemExit(f"ERROR: statements. File: {self.__classname}. Line: {self.__tokenizer.get_line_count()}")



    # 'let' varName ('[' expression ']')? '=' expression ';'
    def compile_let(self):

        # 'let'
        self.eat(["KEYWORD"], ["let"], False)
            
        # 'varName'
        self.eat(["IDENTIFIER"])
        varname = self.__tokenizer.get_current_token()

        type = self.__symbol_table.type_of(varname)
        index = self.__symbol_table.index_of(varname)
        kind = self.__symbol_table.kind_of(varname)
        segment = {"ARG": "ARG", "VAR": "LOCAL", "STATIC": "STATIC", "FIELD": "THIS"}.get(kind, None)

        if type is None or index is None or kind is None:
            raise SystemExit(f"ERROR: let. File: {self.__classname}. Line: {self.__tokenizer.get_line_count()}")

        # ('[' expression ']')?
        self.eat()
        if self.__tokenizer.get_current_token() == "[":
            self.eat(["SYMBOL"], ["["], False)
            self.eat()
            self.compile_expression()
            self.eat(["SYMBOL"], ["]"], False)

            self.__vm_writer.write_push(segment, index)
            self.__vm_writer.write_arithmetic("add")
            self.__vm_writer.write_pop("TEMP", 0)

            # '='
            self.eat(["SYMBOL"], ["="])
            self.eat()
            self.compile_expression()

            self.__vm_writer.write_push("TEMP", 0)
            self.__vm_writer.write_pop("POINTER", 0)
            self.__vm_writer.write_pop("THAT", 0)

        else:
            # '='
            self.eat(["SYMBOL"], ["="], False)
        
            # expression
            self.eat()
            self.compile_expression()
            self.__vm_writer.write_pop(segment, index)

        # ';'
        self.eat(["SYMBOL"], [";"], False)



    # if '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
    def compile_if(self):
        label_true = f"L{self.__label_count}"
        label_false = f"L{self.__label_count + 1}"
        label_end = f"L{self.__label_count + 2}"
        self.__label_count += 3

        # 'if'
        self.eat(["KEYWORD"], ["if"], False)
            
        # '('
        self.eat(["SYMBOL"], ["("])
            
        # expression
        self.eat()
        self.compile_expression()
        self.__vm_writer.write_if(label_true)
        self.__vm_writer.write_goto(label_false)
        self.__vm_writer.write_label(label_true)

        # ')'
        self.eat(["SYMBOL"], [")"], False)

        # '{'
        self.eat(["SYMBOL"], ["{"])
                       
        # statements
        if self.__tokenizer.get_next_token() != "}":
            self.compile_statements()
        
        self.__vm_writer.write_goto(label_end)
        # '}'
        self.eat(["SYMBOL"], ["}"])
        self.__vm_writer.write_label(label_false)

        # ('else' '{' statements '}')?
        if self.__tokenizer.get_next_token() == "else":
            self.eat(["KEYWORD"], ["else"])

            # '{'
            self.eat(["SYMBOL"], ["{"])
                
            # statements
            if self.__tokenizer.get_next_token() != "}":
                self.compile_statements()

                # '}'
                self.eat(["SYMBOL"], ["}"])

        self.__vm_writer.write_label(label_end)
        
            

    # 'while' '(' expression ')' '{' statements '}'
    def compile_while(self):
        label_initloop = f"L{self.__label_count}"
        label_endloop = f"L{self.__label_count + 1}"
        self.__label_count += 2

        # 'while'
        self.eat(["KEYWORD"], ["while"], False)
        self.__vm_writer.write_label(label_initloop)
            
        # '('
        self.eat(["SYMBOL"], ["("])
                
        # expression
        self.eat()
        self.compile_expression()
        self.__vm_writer.write_arithmetic("not")
        self.__vm_writer.write_if(label_endloop)

        # ')'
        self.eat(["SYMBOL"], [")"], False)
        
        # '{'
        self.eat(["SYMBOL"], ["{"])

        # statements
        if self.__tokenizer.get_next_token() != "}":
            self.compile_statements()

        # '}'
        self.eat(["SYMBOL"], ["}"])
        self.__vm_writer.write_goto(label_initloop)
        self.__vm_writer.write_label(label_endloop)
        


    # 'do' subroutineCall ';'
    def compile_do(self):
        
        # 'do'
        self.eat(["KEYWORD"], ["do"], False)
            
        # expression?
        self.eat(["IDENTIFIER"])
        self.compile_expression()

        self.__vm_writer.write_pop("TEMP", 0)

        # ';'
        self.eat(["SYMBOL"], [";"], False)


    # 'return' expression? ';'
    def compile_return(self):

        # 'return'
        self.eat(["KEYWORD"], ["return"], False)
            
        # expression?
        self.eat()
        if self.__tokenizer.get_current_token() != ";":
            self.compile_expression()

            # ';'
            self.eat(["SYMBOL"], [";"], False)

        # ';'
        else:
            self.__vm_writer.write_push("CONST", 0)

        self.__vm_writer.write_return()
        

    ## expressions

    # (expression (',' expression)*)?
    def compile_expression_list(self):
        count = 0

        if self.__tokenizer.get_current_token() == ")":
            return count

        self.compile_expression()
        count += 1

        while self.__tokenizer.get_current_token() == ",":
            self.eat()
            self.compile_expression()
            count += 1

        return count



    # term (op term)*
    def compile_expression(self):
        self.compile_term()

        while self.__tokenizer.get_current_token() in ["+", "~", "*", "/", "&", "|", "<", ">", "="]:
            op = self.__tokenizer.get_current_token()
            self.eat()

            self.compile_term()
            op = {"+": "add", "~": "sub", "=": "eq", ">": "gt", "<": "lt", "&": "and", "|": "or", "*": "mult", "/": "div"}.get(op)
            self.__vm_writer.write_arithmetic(op)



    # integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | '(' expression ')' | unaryOp term
    def compile_term(self):
        if self.__tokenizer.token_type() == "INT_CONST":
            self.__vm_writer.write_push("CONST", self.__tokenizer.get_current_token())
            self.eat()

        elif self.__tokenizer.token_type() == "STRING_CONST":
            self.compile_string()
            self.eat()

        elif self.__tokenizer.token_type() == "KEYWORD" and self.__tokenizer.get_current_token() in ["true", "false", "null"]:
            if self.__tokenizer.get_current_token() == "true":
                self.__vm_writer.write_push("CONST", 1)
                self.__vm_writer.write_arithmetic("neg")
            else:
                self.__vm_writer.write_push("CONST", 0)
            self.eat()

        elif self.__tokenizer.token_type() == "KEYWORD" and self.__tokenizer.get_current_token() == "this":
            self.__vm_writer.write_push("POINTER", 0)
            self.eat()

        elif self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() in ["!", "-"]:
            op = self.__tokenizer.get_current_token()
            self.eat()
            self.compile_term()
            if op == "!":
                self.__vm_writer.write_arithmetic("not")
            else:
                self.__vm_writer.write_arithmetic("neg")

        elif self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() == "(":
            self.eat()
            self.compile_expression()
            self.eat(["SYMBOL"], [")"], False)
            self.eat()
                
        else:
            if self.__tokenizer.token_type() != "IDENTIFIER":
                raise SystemExit(f"ERROR: invalid type in term. File: {self.__classname}. Line: {self.__tokenizer.get_line_count()}. Token: {self.__tokenizer.get_current_token()}. Expected: IDENTIFIER")

            varname = self.__tokenizer.get_current_token()

            self.eat()
            if self.__tokenizer.get_current_token() == "[":
                self.eat()
                self.compile_expression()
                self.eat(["SYMBOL"], ["]"], False)
                self.eat()

                kind = self.__symbol_table.kind_of(varname)
                index = self.__symbol_table.index_of(varname)
                segment = {"ARG": "ARG", "VAR": "LOCAL", "STATIC": "STATIC", "FIELD": "THIS"}.get(kind, None)

                self.__vm_writer.write_push(segment, index)
                self.__vm_writer.write_arithmetic("add")
                self.__vm_writer.write_pop("POINTER", 1)
                self.__vm_writer.write_push("THAT", 0)

            elif self.__tokenizer.get_current_token() in [".", "("]:
                self.compile_subroutine(varname)

            else:
                kind = self.__symbol_table.kind_of(varname)
                index = self.__symbol_table.index_of(varname)
                segment = {"ARG": "ARG", "VAR": "LOCAL", "STATIC": "STATIC", "FIELD": "THIS"}.get(kind, None)
                if kind is not None and segment is not None:
                    self.__vm_writer.write_push(segment, index)


    # END API
    #########            

    def compile_string(self):
        string = self.__tokenizer.string_val()

        self.__vm_writer.write_push("CONST", len(string))
        self.__vm_writer.write_call("String.new", 1)

        for char in string:
            self.__vm_writer.write_push("CONST", ord(char))
            self.__vm_writer.write_call("String.appendChar", 2)



    # subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList ')'
    def compile_subroutine(self, varname):
        if self.__tokenizer.get_current_token() == "(":
            self.eat()
            num_args = self.compile_expression_list()
            num_args += 1
            self.__vm_writer.write_push("POINTER", 0)
            self.__vm_writer.write_call(f"{self.__classname}.{varname}", num_args)
            
        elif self.__tokenizer.get_current_token() == ".":
            self.eat(["IDENTIFIER"])
            subroutine_name = self.__tokenizer.get_current_token()

            type = self.__symbol_table.type_of(varname)
            kind = self.__symbol_table.kind_of(varname)
            index = self.__symbol_table.index_of(varname)
            segment = {"ARG": "ARG", "VAR": "LOCAL", "STATIC": "STATIC", "FIELD": "THIS"}.get(kind, None)
            if type:
                self.__vm_writer.write_push(segment, index)
            
            self.eat(["SYMBOL"], ["("])
            self.eat()
            num_args = self.compile_expression_list()

            if type:
                num_args += 1
                self.__vm_writer.write_call(f"{type}.{subroutine_name}", num_args)
            else:
                self.__vm_writer.write_call(f"{varname}.{subroutine_name}", num_args)

        self.eat(["SYMBOL"], [")"], False)
        self.eat()



    def eat(self, expected_types=None, expected_tokens=None, advance=True):

        if expected_types and not all(t in ["IDENTIFIER", "SYMBOL", "STRING_CONST", "INT_CONST", "KEYWORD", None] for t in expected_types):
            raise SystemError("ERROR: invalid expected types")

        if advance: self.__tokenizer.advance()
        current_token = self.__tokenizer.get_current_token()
        current_type = self.__tokenizer.token_type()

        if expected_tokens is None and expected_types and current_type not in expected_types:
            raise SystemExit(f"ERROR: unexpected token type. File: {self.__classname}. Expected types: {expected_types}. Type: {current_type}. Token: {current_token}. Line: {self.__tokenizer.get_line_count()}")

        elif expected_tokens and current_token not in expected_tokens or expected_types and current_type not in expected_types:
            raise SystemExit(f"ERROR: unexpected token. File: {self.__classname}. Expected tokens: {expected_tokens}. Token: {current_token}. Line: {self.__tokenizer.get_line_count()}")
