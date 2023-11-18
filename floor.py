class Cell:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.values = []

    def appendValue(self, value):
        self.values.append(value)

    def removeValue(self, value):
        self.values.remove(value)
        
    def checkValue(self, value):
        return value in self.values

    def __del__(self):
        pass

class Floor:
    def __init__(self,rows,cols):
        self.rows=rows
        self.cols=cols
        self.table = [[Cell(i, j) for j in range(cols)] for i in range(rows)]

    def appendToCell(self, row, col, value):
        self.table[row][col].appendValue(value)

    def removeFromCell(self, row, col, value):
        if self.table[row][col].checkValue(value):
            self.table[row][col].removeValue(value)

    def checkValueInCell(self, row, col, value):
        return self.table[row][col].checkValue(value)
    
    def getCell(self, row, col):
        return self.table[row][col]

    #cai function nay de debug trong console thoi
    def printSelf(self):
        for row in self.table:
            for cell_value in row:
                if "0" in cell_value:
                    print("A1" if "A1" in cell_value else "0", end=" ")
                elif "-1" in cell_value:
                    print("-1", end=" ")
                else:
                    print(" ".join(map(str, cell_value)), end=" ")
            print()


        
        