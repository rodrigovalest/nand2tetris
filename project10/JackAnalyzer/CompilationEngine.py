class CompilationEngine:
    def __init__(self, tokenizer, xmlfilename):
        self.__tokenizer = tokenizer
        self.__xmlfile = open(xmlfilename, "w")

    #####
    # API

    ## program structure

    # 'class' className '{' classVarDec* subroutineDec* '}'
    def compile_class(self):
        self.__tokenizer.advance()

        if self.__tokenizer.token_type() == "KEYWORD" and self.__tokenizer.get_current_token() == "class":
            self.__xmlfile.write("<class>\n")

            self.__xmlfile.write(self.__tokenizer.keyword())
            
            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "IDENTIFIER":
                self.__xmlfile.write(self.__tokenizer.identifier())

                self.__tokenizer.advance()
                if self.__tokenizer.get_current_token() == "{":
                    self.__xmlfile.write(self.__tokenizer.symbol())

                    while self.__tokenizer.get_next_token() in ["static", "field"]:
                        self.compile_class_var_dec()

                    while self.__tokenizer.get_next_token() in ["constructor", "function", "method"]:
                        self.compile_subroutine_dec()

                    self.__tokenizer.advance()
                    if self.__tokenizer.get_current_token() == "}":
                        self.__xmlfile.write(self.__tokenizer.symbol())

                        self.__xmlfile.write("</class>\n")
                        return

        raise SystemExit("Error")


    # ('static' | 'field') type varName (',' varName)* ';'
    def compile_class_var_dec(self):
        self.__tokenizer.advance()

        if self.__tokenizer.token_type() == "KEYWORD" and self.__tokenizer.get_current_token() in ["static", "field"]:
            self.__xmlfile.write("<classVarDec>\n")

            self.__xmlfile.write(self.__tokenizer.keyword())

            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "KEYWORD" and self.__tokenizer.get_current_token() in ["int", "char", "boolean", "void"]:
                self.__xmlfile.write(self.__tokenizer.keyword())
            elif self.__tokenizer.token_type() == "IDENTIFIER":
                self.__xmlfile.write(self.__tokenizer.identifier())
            else:
                raise SystemExit("Error")

            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "IDENTIFIER":
                self.__xmlfile.write(self.__tokenizer.identifier())

                while self.__tokenizer.get_next_token() == ",":
                    self.__tokenizer.advance()
                    self.__xmlfile.write(self.__tokenizer.symbol())

                    self.__tokenizer.advance()
                    if self.__tokenizer.token_type() == "IDENTIFIER":
                        self.__xmlfile.write(self.__tokenizer.identifier())
                    else:
                        raise SystemExit("Error")
                        
                if self.__tokenizer.get_next_token() == ";":
                    self.__tokenizer.advance()
                    self.__xmlfile.write(self.__tokenizer.symbol())

                    self.__xmlfile.write("</classVarDec>\n")
                    return

        raise SystemExit("Error")


    # ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
    def compile_subroutine_dec(self):
        self.__tokenizer.advance()
        
        if self.__tokenizer.get_current_token() in ["constructor", "function", "method"]:
            self.__xmlfile.write("<subroutineDec>\n")

            self.__xmlfile.write(self.__tokenizer.keyword())

            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "KEYWORD" and self.__tokenizer.get_current_token() in ["int", "char", "boolean", "void"]:
                self.__xmlfile.write(self.__tokenizer.keyword())
            elif self.__tokenizer.token_type() == "IDENTIFIER":
                self.__xmlfile.write(self.__tokenizer.identifier())
            else:
                raise SystemExit("Error")
            
            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "IDENTIFIER":
                self.__xmlfile.write(self.__tokenizer.identifier())

                self.__tokenizer.advance()
                if self.__tokenizer.get_current_token() == "(":
                    self.__xmlfile.write(self.__tokenizer.symbol())

                    self.compile_parameter_list()

                    self.__tokenizer.advance()
                    if self.__tokenizer.get_current_token() == ")":
                        self.__xmlfile.write(self.__tokenizer.symbol())

                        self.compile_subroutine_body()

                        self.__xmlfile.write("</subroutineDec>\n")
                        return

        raise SystemExit("Error")


    # ((type varName) (',' type varName)*)?
    def compile_parameter_list(self):
        if self.__tokenizer.get_next_token() != ")":
            self.__xmlfile.write("<parameterList>\n")

            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "KEYWORD" and self.__tokenizer.get_current_token() in ["int", "char", "boolean", "void"]:
                self.__xmlfile.write(self.__tokenizer.keyword())
            elif self.__tokenizer.token_type() == "IDENTIFIER":
                self.__xmlfile.write(self.__tokenizer.identifier())
            else:
                raise SystemExit("Error")

            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "IDENTIFIER":
                self.__xmlfile.write(self.__tokenizer.identifier()) 

                while self.__tokenizer.get_next_token() == ",":
                    self.__tokenizer.advance()
                    self.__xmlfile.write(self.__tokenizer.symbol())

                    self.__tokenizer.advance()
                    if self.__tokenizer.token_type() == "KEYWORD" and self.__tokenizer.get_current_token() in ["int", "char", "boolean", "void"]:
                        self.__xmlfile.write(self.__tokenizer.keyword())
                    elif self.__tokenizer.token_type() == "IDENTIFIER":
                        self.__xmlfile.write(self.__tokenizer.identifier())
                    else:
                        raise SystemExit("Error")

                    self.__tokenizer.advance()
                    if self.__tokenizer.token_type() == "IDENTIFIER":
                        self.__xmlfile.write(self.__tokenizer.identifier())
                    else:
                        raise SystemExit("Error")
                    
                self.__xmlfile.write("</parameterList>\n")
                return
        else:
            self.__xmlfile.write("<parameterList>\n")
            self.__xmlfile.write("</parameterList>\n")
            return

        raise SystemExit("Error")
    

    # '{' varDec* statements '}'
    def compile_subroutine_body(self):
        self.__tokenizer.advance()

        if self.__tokenizer.get_current_token() == "{":
            self.__xmlfile.write("<subroutineBody>\n")

            self.__xmlfile.write(self.__tokenizer.symbol())

            while self.__tokenizer.get_next_token() == "var":
                self.compile_var_dec()

            self.compile_statements()

            self.__tokenizer.advance()
            if self.__tokenizer.get_current_token() == "}":
                self.__xmlfile.write(self.__tokenizer.symbol())

                self.__xmlfile.write("</subroutineBody>\n")
                return
            
        raise SystemExit("Error")


    # 'var' type varName (',' varName)* ';'
    def compile_var_dec(self):
        self.__tokenizer.advance()

        if self.__tokenizer.get_current_token() == "var":
            self.__xmlfile.write("<varDec>\n")

            self.__xmlfile.write(self.__tokenizer.keyword())

            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "KEYWORD" and self.__tokenizer.get_current_token() in ["int", "char", "boolean", "void"]:
                self.__xmlfile.write(self.__tokenizer.keyword())
            elif self.__tokenizer.token_type() == "IDENTIFIER":
                self.__xmlfile.write(self.__tokenizer.identifier())
            else:
                raise SystemExit("Error")

            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "IDENTIFIER":
                self.__xmlfile.write(self.__tokenizer.identifier())

                while self.__tokenizer.get_next_token() == ",":
                    self.__tokenizer.advance()
                    self.__xmlfile.write(self.__tokenizer.symbol())

                    self.__tokenizer.advance()
                    if self.__tokenizer.token_type() == "IDENTIFIER":
                        self.__xmlfile.write(self.__tokenizer.identifier())
                    else:
                        raise SystemExit("Error")
                    
                if self.__tokenizer.get_next_token() == ";":
                    self.__tokenizer.advance()
                    self.__xmlfile.write(self.__tokenizer.symbol())

                    self.__xmlfile.write("</varDec>\n")
                    return                            

        raise SystemExit("Error")


    ## statements

    # statement*
    def compile_statements(self):
        self.__xmlfile.write("<statements>\n")
        
        while True:
            next_token = self.__tokenizer.get_next_token()
            
            if next_token == "let":
                self.compile_let()
            elif next_token == "if":
                self.compile_if()
            elif next_token == "while":
                self.compile_while()
            elif next_token == "do":
                self.compile_do()
            elif next_token == "return":
                self.compile_return()
            else:
                break

        self.__xmlfile.write("</statements>\n")


    # 'let' varName ('[' expression ']')? '=' expression ';'
    def compile_let(self):
        self.__tokenizer.advance()

        if self.__tokenizer.get_current_token() == "let":
            self.__xmlfile.write("<letStatement>\n")

            self.__xmlfile.write(self.__tokenizer.keyword())

            self.__tokenizer.advance()
            if self.__tokenizer.token_type() == "IDENTIFIER":
                self.__xmlfile.write(self.__tokenizer.identifier())

                if self.__tokenizer.get_next_token() == "[":
                    self.__tokenizer.advance()
                    self.__xmlfile.write(self.__tokenizer.symbol())

                    self.compile_expression()

                    if self.__tokenizer.get_next_token() == "]":
                        self.__tokenizer.advance()
                        self.__xmlfile.write(self.__tokenizer.symbol())
                    else:
                        raise SystemExit("Error")
                    
                if self.__tokenizer.get_next_token() == "=":
                    self.__tokenizer.advance()
                    self.__xmlfile.write(self.__tokenizer.symbol())

                    self.compile_expression()

                    if self.__tokenizer.get_next_token() == ";":
                        self.__tokenizer.advance()
                        self.__xmlfile.write(self.__tokenizer.symbol())
                        
                        self.__xmlfile.write("</letStatement>\n")
                        return

        raise SystemExit("Error")


    # if '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
    def compile_if(self):
        self.__tokenizer.advance()

        if self.__tokenizer.get_current_token() == "if":
            self.__xmlfile.write("<ifStatement>\n")

            self.__xmlfile.write(self.__tokenizer.keyword())

            self.__tokenizer.advance()
            if self.__tokenizer.get_current_token() == "(":
                self.__xmlfile.write(self.__tokenizer.symbol())

                self.compile_expression()

                self.__tokenizer.advance()
                if self.__tokenizer.get_current_token() == ")":
                    self.__xmlfile.write(self.__tokenizer.symbol())

                    self.__tokenizer.advance()
                    if self.__tokenizer.get_current_token() == "{":
                        self.__xmlfile.write(self.__tokenizer.symbol())

                        self.compile_statements()

                        self.__tokenizer.advance()
                        if self.__tokenizer.get_current_token() == "}":
                            self.__xmlfile.write(self.__tokenizer.symbol())

                            if self.__tokenizer.get_next_token() != "else":
                                self.__xmlfile.write("</ifStatement>\n")
                                return
                            else:
                                self.__tokenizer.advance()
                                self.__xmlfile.write(self.__tokenizer.keyword())

                                self.__tokenizer.advance()
                                if self.__tokenizer.get_current_token() == "{":
                                    self.__xmlfile.write(self.__tokenizer.symbol())

                                    self.compile_statements()

                                    self.__tokenizer.advance()
                                    if self.__tokenizer.get_current_token() == "}":
                                        self.__xmlfile.write(self.__tokenizer.symbol())

                                        self.__xmlfile.write("</ifStatement>\n")
                                        return
            
        raise SystemExit("Error")


    # 'while' '(' expression ')' '{' statements '}'
    def compile_while(self):
        self.__tokenizer.advance()

        if self.__tokenizer.get_current_token() == "while":
            self.__xmlfile.write("<whileStatement>\n")

            self.__xmlfile.write(self.__tokenizer.keyword())

            self.__tokenizer.advance()
            if self.__tokenizer.get_current_token() == "(":
                self.__xmlfile.write(self.__tokenizer.symbol())

                self.compile_expression()

                self.__tokenizer.advance()
                if self.__tokenizer.get_current_token() == ")":
                    self.__xmlfile.write(self.__tokenizer.symbol())

                    self.__tokenizer.advance()
                    if self.__tokenizer.get_current_token() == "{":
                        self.__xmlfile.write(self.__tokenizer.symbol())

                        self.compile_statements()

                        self.__tokenizer.advance()
                        if self.__tokenizer.get_current_token() == "}":
                            self.__xmlfile.write(self.__tokenizer.symbol())
                
                            self.__xmlfile.write("</whileStatement>\n")
                            return

        raise SystemExit("Error")


    # 'do' subroutineCall ';'
    def compile_do(self):
        self.__tokenizer.advance()

        if self.__tokenizer.get_current_token() == "do":
            self.__xmlfile.write("<doStatement>\n")

            self.__xmlfile.write(self.__tokenizer.keyword())

            self.__tokenizer.advance()
            self.compile_subroutine_call()

            if self.__tokenizer.get_next_token() == ";":
                self.__tokenizer.advance()
                self.__xmlfile.write(self.__tokenizer.symbol())

                self.__xmlfile.write("</doStatement>\n")
                return

        raise SystemExit("Error")
    

    # 'return' expression? ';'
    def compile_return(self):
        self.__tokenizer.advance()

        if self.__tokenizer.get_current_token() == "return":
            self.__xmlfile.write("<returnStatement>\n")

            self.__xmlfile.write(self.__tokenizer.keyword())

            if self.__tokenizer.get_next_token() != ";":
                self.compile_expression()

            if self.__tokenizer.get_next_token() == ";":
                self.__tokenizer.advance()
                self.__xmlfile.write(self.__tokenizer.symbol())

                self.__xmlfile.write("</returnStatement>\n")

                return

        raise SystemExit("Error")
    

    ## expressions

    # (expression (',' expression)*)?
    def compile_expression_list(self):
        self.__xmlfile.write("<expressionList>\n")

        if self.__tokenizer.get_next_token() != ")":
            while True:
                self.compile_expression()

                if self.__tokenizer.get_next_token() == ",":
                    self.__tokenizer.advance()
                    self.__xmlfile.write(self.__tokenizer.symbol())
                else:
                    break

        self.__xmlfile.write("</expressionList>\n")


    # term (op term)*
    def compile_expression(self):      
        self.__xmlfile.write("<expression>\n")

        self.compile_term()

        while self.__tokenizer.get_next_token() in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            self.__tokenizer.advance()
            self.__xmlfile.write(self.__tokenizer.symbol())

            self.compile_term()

        self.__xmlfile.write("</expression>\n")
    

    # integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
    def compile_term(self):
        self.__tokenizer.advance()

        self.__xmlfile.write("<term>\n")
        
        if self.__tokenizer.token_type() == "INT_CONST":
            self.__xmlfile.write(self.__tokenizer.int_val())
        
        elif self.__tokenizer.token_type() == "STRING_CONST":
            self.__xmlfile.write(self.__tokenizer.string_val())
        
        elif self.__tokenizer.token_type() == "KEYWORD" and self.__tokenizer.get_current_token() in ["true", "false", "null", "this"]:
            self.__xmlfile.write(self.__tokenizer.keyword())
        
        elif self.__tokenizer.token_type() == "IDENTIFIER":
            if self.__tokenizer.get_next_token() == ".":
                self.compile_subroutine_call()

            else:
                self.__xmlfile.write(self.__tokenizer.identifier())

                if self.__tokenizer.get_next_token() == "[":
                    self.__tokenizer.advance()
                    self.__xmlfile.write(self.__tokenizer.symbol())

                    self.compile_expression()

                    self.__tokenizer.advance()
                    self.__xmlfile.write(self.__tokenizer.symbol())
        
        elif self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() == "(":
            self.__xmlfile.write(self.__tokenizer.symbol())

            self.compile_expression()

            self.__tokenizer.advance()
            self.__xmlfile.write(self.__tokenizer.symbol())
        
        elif self.__tokenizer.token_type() == "SYMBOL" and self.__tokenizer.get_current_token() in ["-", "~"]:
            self.__xmlfile.write(self.__tokenizer.symbol())

            self.compile_term()
        else:
            raise SystemExit("Error")

        self.__xmlfile.write("</term>\n")

    
    # END API
    #########
    
    # subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList ')'
    def compile_subroutine_call(self):
        if self.__tokenizer.token_type() == "IDENTIFIER":
            self.__xmlfile.write(self.__tokenizer.identifier())

            if self.__tokenizer.get_next_token() == ".":
                self.__tokenizer.advance()
                self.__xmlfile.write(self.__tokenizer.symbol())
                
                self.__tokenizer.advance()
                if self.__tokenizer.token_type() == "IDENTIFIER":
                    self.__xmlfile.write(self.__tokenizer.identifier())

            if self.__tokenizer.get_next_token() == "(":
                self.__tokenizer.advance()
                self.__xmlfile.write(self.__tokenizer.symbol())

                self.compile_expression_list()

                if self.__tokenizer.get_next_token() == ")":
                    self.__tokenizer.advance()
                    self.__xmlfile.write(self.__tokenizer.symbol())
                    return

        raise SystemExit("Error")
