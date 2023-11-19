#pls dont touch
#làm hierachy heuristic cho spread
class Cell2:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.values = []
        self.connectedCells = []
        self.belongTo = None

    def setBelongTo(self, value):
        self.belongTo = value

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

    def getY(self):
        return self.y
    
    def getX(self):
        return self.x
    
    def getBelongTo(self):
        return self.belongTo

    def connectToCell(self, Cell):
        self.connectedCells.append(Cell)
        Cell.connectedCells.append(self)

    def __del__(self):
        pass

class Spread:
    def __init__(self,newTag,floor,firstCell):
        self.frontier = []
        self.visited = []
        self.tags = []
        self.belongTo = None
        self.tags.append(newTag)
        self.belongTo = floor
        self.frontier.append(firstCell)

    def appendToFrontier(self, Cell):
        self.frontier.append(Cell)

    def removeFromFrontier(self, Cell):
        if Cell in self.frontier:
            self.frontier.remove(Cell)

    def appendToTags(self, value):
        self.tags.append(value)

    def removeFromTags(self, value):
        if value in self.tags:
            self.tags.remove(value)
    
    def expandCell(self, Cell):
        if Cell in self.frontier:
            self.frontier.remove(Cell)
            self.visited.append(Cell)
            cell_y= Cell.getY()
            cell_x= Cell.getX()
            #try to connect N
            if cell_y > 0 and not self.belongTo.getCell(cell_y - 1, cell_x).isWall():
                Cell.connectToCell(self.belongTo.getCell(cell_y - 1, cell_x))
            # Try to connect S
            if cell_y < self.belongTo.rows - 1 and not self.belongTo.getCell(cell_y + 1, cell_x).isWall():
                Cell.connectToCell(self.belongTo.getCell(cell_y + 1, cell_x))

            # Try to connect E
            if cell_x < self.belongTo.cols - 1 and not self.belongTo.getCell(cell_y, cell_x + 1).isWall():
                Cell.connectToCell(self.belongTo.getCell(cell_y, cell_x + 1))

            # Try to connect W
            if cell_x > 0 and not self.belongTo.getCell(cell_y, cell_x - 1).isWall():
                Cell.connectToCell(self.belongTo.getCell(cell_y, cell_x - 1))

            # Try to connect NE
            if (
                cell_y > 0 and cell_x < self.belongTo.cols - 1 and
                not self.belongTo.getCell(cell_y - 1, cell_x + 1).isWall() and
                not self.belongTo.getCell(cell_y, cell_x + 1).isWall() and
                not self.belongTo.getCell(cell_y - 1, cell_x).isWall()
            ):
                Cell.connectToCell(self.belongTo.getCell(cell_y - 1, cell_x + 1))

            # Try to connect NW
            if (
                cell_y > 0 and cell_x > 0 and
                not self.belongTo.getCell(cell_y - 1, cell_x - 1).isWall() and
                not self.belongTo.getCell(cell_y, cell_x - 1).isWall() and
                not self.belongTo.getCell(cell_y - 1, cell_x).isWall()
            ):
                Cell.connectToCell(self.belongTo.getCell(cell_y - 1, cell_x - 1))

            # Try to connect SE
            if (
                cell_y < self.belongTo.rows - 1 and cell_x < self.belongTo.cols - 1 and
                not self.belongTo.getCell(cell_y + 1, cell_x + 1).isWall() and
                not self.belongTo.getCell(cell_y, cell_x + 1).isWall() and
                not self.belongTo.getCell(cell_y + 1, cell_x).isWall()
            ):
                Cell.connectToCell(self.belongTo.getCell(cell_y + 1, cell_x + 1))

            # Try to connect SW
            if (
                cell_y < self.belongTo.rows - 1 and cell_x > 0 and
                not self.belongTo.getCell(cell_y + 1, cell_x - 1).isWall() and
                not self.belongTo.getCell(cell_y, cell_x - 1).isWall() and
                not self.belongTo.getCell(cell_y + 1, cell_x).isWall()
            ):
                Cell.connectToCell(self.belongTo.getCell(cell_y + 1, cell_x - 1))
        else:
            return

    def __del__(self):
        pass

class Floor2:
    def __init__(self,rows,cols):
        self.rows=rows
        self.cols=cols
        self.table = [[Cell2(i, j) for j in range(cols)] for i in range(rows)]
        self.listOfSpreads = []

        for i in range(self.rows):
            for j in range(self.cols):
                self.table[i][j].setBelongTo(self)     

    def appendToCell(self, row, col, value):
        self.table[row][col].appendValue(value)

    def removeFromCell(self, row, col, value):
        if self.checkValueInCell(row, col, value):
            self.table[row][col].removeValue(value)

    def checkValueInCell(self, row, col, value):
        return self.table[row][col].checkValue(value)
    
    def getCell(self, row, col):
        return self.table[row][col]
    
    def appendSpread(self, newSpread):
        self.listOfSpreads.append(newSpread)
    
    def removeSpread(self, spread):
        if spread in self.listOfSpreads:
            self.listOfSpreads.remove(spread)
    
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
            #khuc input nay dang test, se hoan thien sau
            for j in range(cols):
                if str(row_values[j])=="A1":
                    self.floor.appendToCell(i-2, j, "0")
                    self.floor.appendSpread(Spread("A1",self.floor,self.floor.getCell(i-2, j)))
                elif str(row_values[j])=="T1":
                    self.floor.appendToCell(i-2, j, "0")
                elif str(row_values[j])=="K1":
                    self.floor.appendToCell(i-2, j, "0")
                elif str(row_values[j])=="D1":
                    self.floor.appendToCell(i-2, j, "0")
                self.floor.appendToCell(i-2, j, row_values[j])

myLevel2 = Level2()
myLevel2.getInputFile("input//input1-level2.txt")


myLevel2.floor.listOfSpreads[0].expandCell(myLevel2.floor.getCell(2,3))
cell23=myLevel2.floor.getCell(2,3)
cell13=myLevel2.floor.getCell(1,3)
cell33=myLevel2.floor.getCell(3,3)
cell22=myLevel2.floor.getCell(2,2)
cell24=myLevel2.floor.getCell(2,4)
cell14=myLevel2.floor.getCell(1,4)
cell34=myLevel2.floor.getCell(3,4)
cell32=myLevel2.floor.getCell(3,2)
cell12=myLevel2.floor.getCell(1,2)
myLevel2.floor.printTable()