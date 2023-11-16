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

    def printSelf(self):
        for row in self.table:
            print(" ".join(map(str, row)))


        
        