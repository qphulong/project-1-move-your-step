class Floor:
    def __init__(self,rows,cols):
        self.rows=rows
        self.cols=cols
        self.table = [[[]    for _ in range(cols)] for _ in range(rows)]

    def appendToCell(self, row, col, value):
        self.table[row][col].append(value)

    def removeFromCell(self, row, col, value):
        if value in self.table[row][col]:
            self.table[row][col].remove(value)

    def checkValueInCell(self, row, col, value):
        return value in self.table[row][col]

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


        
        