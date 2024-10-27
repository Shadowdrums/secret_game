class GameTile:
    def __init__(self, glyph, color):
        self.glyph = glyph
        self.color = color
    
    def __str__(self):
        return f"{self.color}{self.glyph}\x1b[39m"
    
    def __repr__(self):
        return self.__str__()
    
    def __add__(self, other):
        return self.glyph + other
    
    def __radd__(self, other):
        return other + self.glyph