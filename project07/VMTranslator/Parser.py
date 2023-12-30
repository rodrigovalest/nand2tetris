class Parser:
    def parse(self, line):
        line = line.strip()

        if not line or line.startswith("//"):
            return None

        line = line.split("//", 1)[0]
        parts = line.split()

        return parts
    