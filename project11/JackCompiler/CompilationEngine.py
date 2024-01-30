from JackTokenizer import JackTokenizer
from VMWriter import VMWriter
from SymbolTable import SymbolTable

class CompilationEngine:
    def __init__(self, tokenizer: JackTokenizer, vmwriter: VMWriter, symbol_table: SymbolTable):
        self.__tokenizer = tokenizer
        self.__vm_writer = vmwriter
        self.__symbol_table = symbol_table
        self.__label_count = 0

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
                        self.compile_subroutine_dec()
                        self.__tokenizer.advance()

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

                        self.__vm_writer.write_function(subroutine_name, (argcount + 1))

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
                self.__tokenizer.advance()
                while self.__tokenizer.token_type() == "KEYWORD" and self.__tokenizer.get_current_token() == "var":
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
    def compile_do(self):
        return


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
    def compile_expression_list(self):
        self.compile_expression()

        while self.__tokenizer.get_current_token() == ",":
            self.__tokenizer.advance()
            self.compile_expression()
        

    # term (op term)*
    def compile_expression(self):
        expression_tokens = self.__get_expression_tokens()
        
        first_token_type = expression_tokens[0]["type"]
        first_token = expression_tokens[0]["token"]
        
        # first token type determine the expression type
        if first_token_type == "INT_CONST" or (first_token_type == "KEYWORD" and first_token in ["true", "false", "null"]):
            self.handle_integer_expression(expression_tokens)
            return "integer_expression"
        
        elif first_token_type == "STRING_CONST":
            self.handle_string_expression(expression_tokens)
            return "string_expression"
        
        elif first_token_type == "IDENTIFIER":
            var_type = self.__symbol_table.type_of(first_token)

            if not var_type:
                raise SystemExit("ERROR: invalid token in expression")

            if var_type in ["int", "boolean"]:
                self.handle_integer_expression(expression_tokens)
                return "integer_expression"
            elif var_type == "string":
                self.handle_string_expression(expression_tokens)
                return "string_expression"
            else:
                self.handle_object_expression(expression_tokens)
                return "object_expression"

        else:
            raise SystemExit("ERROR: invalid token in expression")


    # integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
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
            return
        
    
    # END API
    #########
    
    # subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList ')'
    def compile_subroutine_call(self):
        return
    

    def handle_integer_expression(self, expression_tokens):
        for expression_token in expression_tokens:
            token_type = expression_token["type"]
            token = expression_token["token"]
            
            if token_type == "STRING_CONST":
                raise SystemExit("ERROR: invalid token in integer expression")
            
            elif token_type == "IDENTIFIER":
                var_type = self.__symbol_table.type_of(token)
                
                if not var_type or var_type != "int":
                    raise SystemExit("ERROR: invalid token in expression")

            elif token_type == "KEYWORD":
                if token in ["false", "null"]:
                    expression_token["token"] = 0
                elif token == "true":
                    expression_token["token"] = 1
                else:
                    raise SystemExit("ERROR: invalid token in integer expression")

            elif token_type == "SYMBOL" and not token in ["+", "-", "*", "/", "&", "|", "<", ">", "(", ")", "~", "-"]:
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
    

    def handle_object_expression(self, expression_tokens):
        if len(expression_tokens) != 1:
            raise SystemExit("ERROR: invalid token in object expression")
            
        token_type = expression_tokens[0]["type"]
        token = expression_tokens[0]["token"]
        self.compile_term(token, token_type)
    

    def __get_expression_tokens(self):
        expression_tokens = []
        parentheses_count = 0
        
        while self.__tokenizer.has_more_tokens():
            current_token = {
                "token": self.__tokenizer.get_current_token(),
                "type": self.__tokenizer.token_type()
            }

            if current_token.get("token") == "(":
                parentheses_count += 1
            
            elif current_token.get("token") == ")":
                parentheses_count -= 1
                if parentheses_count == -1:
                    break

            elif current_token.get("token") in {";", ",", "]", None}:
                break
            
            expression_tokens.append(current_token)
            self.__tokenizer.advance()

        if len(expression_tokens) == 0:
            raise SystemExit("ERROR: expression error")

        return expression_tokens
    