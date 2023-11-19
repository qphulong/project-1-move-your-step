class Cell2:
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
    
    def calculateManhattanFrom(self, Cell):
        return abs(self.x - Cell.x) + abs(self.y - Cell.y)
    
    def isWall(self):
        return "-1" in self.values

    def __del__(self):
        pass

class Floor2:
    def __init__(self,rows,cols):
        self.rows=rows
        self.cols=cols
        self.table = [[Cell2(i, j) for j in range(cols)] for i in range(rows)]

    def appendToCell(self, row, col, value):
        self.table[row][col].appendValue(value)

    def removeFromCell(self, row, col, value):
        if self.checkValueInCell(row, col, value):
            self.table[row][col].removeValue(value)

    def checkValueInCell(self, row, col, value):
        return self.table[row][col].checkValue(value)
    
    def getCell(self, row, col):
        return self.table[row][col]
    
    #console
    def printTable(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(self.table[i][j].values, end=" ")
            print()


class Level2:
    def __init__(self):
        self.floor = None
        
        
    def getInputFile(self,filePath):
        with open (filePath, "r") as file:
            lines = file.readlines()
        
        rows, cols = map(int, lines[0].strip().split(','))
        self.floor=Floor2(rows, cols)
        
        for i in range(2, len(lines)):
            row_values = list(map(str, lines[i].strip().split(',')))
            for j in range(cols):
                if str(row_values[j])=="A1":
                    self.agent_Xposition = i-2
                    self.agent_Yposition = j
                elif str(row_values[j])=="T1":
                    self.goal_Xposition = i-2
                    self.goal_Yposition = j
                self.floor.appendToCell(i-2, j, row_values[j])

myLevel2 = Level2()
myLevel2.getInputFile("input//input1-level2.txt")

myLevel2.floor.printTable()