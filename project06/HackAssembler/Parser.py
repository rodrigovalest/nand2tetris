# Remove the comments and white spaces
class Parser:
    def parse(self, line):
        line = line.replace(" ", "")
        line = line.strip()

        if not line or line.startswith("//"):
            return None

        split = line.split("//", 1)
        line = split[0]

        return line
