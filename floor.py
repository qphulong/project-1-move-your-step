class Floor:
    def __init__(self,rows,cols):
        self.rows=rows
        self.cols=cols
        self.table = [['' for _ in range(cols)] for _ in range(rows)]

    def printSelf(self):
        for row in self.table:
            print(" ".join(map(str, row)))


        
        