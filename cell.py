class Cell:

    def __init__(self, y, x, cellType):
        self.y = y
        self.x = x
        self.cellType = cellType

    def __del__(self):
        pass

    def print(self):
        print(self.y, self.x, self.cellType)