class Piece:
    def __init__(self, rank, colour=None):
        self.rank = rank
        self.colour = colour

    def getValue(self):
        return self.rank

    def getColour(self):
        return self.colour
