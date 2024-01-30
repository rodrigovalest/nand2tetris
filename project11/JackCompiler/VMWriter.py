class VMWriter:
    def __init__(self, filename):
        self.__file = open(filename, "w")
    
    #####
    # API

    def write_push(self, segment, index):
        segments = {
            "CONST": "constant",
            "ARG": "argument",
            "LOCAL": "local",
            "STATIC": "static",
            "THIS": "this",
            "THAT": "that",
            "POINTER": "pointer",
            "TEMP": "temp"
        }

        segment = segments.get(segment, None)

        if segment is None or index is None:
            raise SystemExit("ERROR: VM writer push") 

        self.__file.write(f"push {segment} {index}\n")
    

    def write_pop(self, segment, index):
        segments = {
            "ARG": "argument",
            "LOCAL": "local",
            "STATIC": "static",
            "THIS": "this",
            "THAT": "that",
            "POINTER": "pointer",
            "TEMP": "temp"
        }

        segment = segments.get(segment, None)

        if segment is None or index is None:
            raise SystemExit("ERROR: VM writer pop")

        self.__file.write(f"pop {segment} {index}\n")
    

    def write_arithmetic(self, command):
        if not command in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not", "mult", "div", "neg", "not"]:
            return
        
        if command == "mult":
            command = "Math.multiply"
        elif command == "div":
            command = "Math.divide"
        
        self.__file.write(f"{command}\n")


    def write_label(self, label):
        self.__file.write(f"label {label}\n")

    
    def write_goto(self, label):
        self.__file.write(f"goto {label}\n")


    def write_if(self, label):
        self.__file.write(f"if-goto {label}\n")


    def write_call(self, name, num_args):
        self.__file.write(f"call {name} {num_args}\n")


    def write_function(self, name, num_locals):
        self.__file.write(f"function {name} {num_locals}\n")


    def write_return(self):
        self.__file.write("return\n")


    def close(self):
        self.__file.close()

    # END API
    #########
