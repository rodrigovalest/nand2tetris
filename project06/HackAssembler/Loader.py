import Dicts

# Load new labels and variables in the symbols table
class Loader:
    def load_label(self, label, count_line):
        if label == None:
            return False

        if label.startswith("("):
            label = label.replace("(", "")
            label = label.replace(")", "")

            label_code = Dicts.symbol.get(label, None)

            if not label_code:
                count_line = bin(int(count_line))[2:].zfill(15)
                Dicts.symbol[label] = count_line
            
            return False

        return True
    
    def load_variable(self, variable, variable_count):
        if variable == None:
            return False

        if variable.startswith("@"):
            variable = variable.replace("@", "")

            if not variable.isdigit():
                variable_code = Dicts.symbol.get(variable, None)

                if not variable_code:
                    variable_count = bin(int(variable_count))[2:].zfill(15)
                    Dicts.symbol[variable] = variable_count

                    return True

        return False
