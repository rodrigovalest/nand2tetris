class CompilationEngine:
    def __init__(self, jackTokenizer, xmlfilename):
        self.__jackTokenizer = jackTokenizer
        self.__xmlfile = open(xmlfilename, "w")

    #####
    # API

    ## program structure

    # 'class' className '{' classVarDec* subroutineDec* '}'
    def compile_class(self):
        return


    # ('static' | 'field') type varName (',' varName)* ';'
    def compile_class_var_dec(self):
        return


    # ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
    def compile_subroutine_dec(self):
        return


    # ((type varName) (',' type varName)*)?
    def compile_parameter_list(self):
        return


    # 'var' type varName (',' varName)* ';'
    def compile_var_dec(self):
        return


    ## statements

    # statement*
    def compile_statements(self):
        return


    # 'let' varName ('[' expression ']')? '=' expression ';'
    def compile_let(self):
        return


    # if '(' expression ')' '{' statements '}' ('else' '{' statements '}')
    def compile_if(self):
        return


    # 'while' '(' expression ')' '{' statements '}'
    def compile_while(self):
        return


    # 'do' subroutineCall
    def compile_do(self):
        return
    

    # 'return' expression? ';'
    def compile_return(self):
        return
    

    ## expressions

    # term (op term)*
    def compile_expression(self):
        return
    

    # integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
    def compile_term(self):
        return
    

    # (expression (',' expression)*)?
    def compile_expression_list(self):
        return

    
    # END API
    #########
    