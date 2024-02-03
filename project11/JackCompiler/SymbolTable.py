class SymbolTable:
    def __init__(self):
        self.__class_table = {}
        self.__subroutine_table = {}

    #####
    # API

    def start_subroutine(self):
        self.__subroutine_table = {}


    def define(self, name, type, kind):  
        if name in self.__class_table or name in self.__subroutine_table:
            return
        
        if kind in ["STATIC", "FIELD"]:
            self.__class_table[name] = {
                "type": type,
                "kind": kind,
                "index": self.var_count(kind, "class")
            }
        elif kind in ["ARG", "VAR"]:
            self.__subroutine_table[name] = {
                "type": type,
                "kind": kind,
                "index": self.var_count(kind, "subroutine")
            }
        else:
            raise SystemExit("ERROR: symbol table define")


    def var_count(self, kind, class_or_subroutine):
        if kind not in ["STATIC", "FIELD", "ARG", "VAR"]:
            return 0

        count = 0

        if class_or_subroutine in ["class", "both"]:
            count += sum(1 for entry in self.__class_table.values() if entry["kind"] == kind)

        if class_or_subroutine in ["subroutine", "both"]:
            count += sum(1 for entry in self.__subroutine_table.values() if entry["kind"] == kind)

        return count
    
    
    # kind: [STATIC, FIELD, ARG, VAR]
    def kind_of(self, name):
        kind = self.__class_table.get(name, {}).get("kind", None)

        if kind is None:
            kind = self.__subroutine_table.get(name, {}).get("kind", None)

        return kind
    

    # type: [int, char, boolean, object]
    def type_of(self, name):
        type = self.__class_table.get(name, {}).get("type", None)

        if type is None:
            type = self.__subroutine_table.get(name, {}).get("type", None)

        return type


    def index_of(self, name):
        index = self.__class_table.get(name, {}).get("index", None)

        if index is None:
            index = self.__subroutine_table.get(name, {}).get("index", None)

        return index


    # END API
    #########

    def print_symbol_table(self):
        print(self.__class_table)
        print(self.__subroutine_table)
