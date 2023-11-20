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
    
    def getManhattanFrom(self, Cell):
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

    def expandToward(self,goalCell):
         # Calculate heuristics for each cell in the frontier
        heuristics = [cell.getManhattanFrom(goalCell) for cell in self.frontier]

        # Find the index of the cell with the minimum heuristic value
        min_index = min(range(len(heuristics)), key=heuristics.__getitem__)

        # Retrieve the cell with the minimum heuristic value
        chosenCell = self.frontier[min_index]
        
        chosenCellY= chosenCell.getY()
        chosenCellX= chosenCell.getX()

        #try to connect N
        if (
            chosenCellY > 0 and
            not self.belongTo.getCell(chosenCellY - 1, chosenCellX).isWall() and
            self.belongTo.getCell(chosenCellY - 1, chosenCellX) not in self.visited and
            self.belongTo.getCell(chosenCellY - 1, chosenCellX) not in self.frontier
        ):
            northCell = self.belongTo.getCell(chosenCellY - 1, chosenCellX)
            chosenCell.connectToCell(northCell)
            if northCell not in self.frontier:
                self.appendToFrontier(northCell)


        # Try to connect S
        if (
            chosenCellY < self.belongTo.rows - 1 and
            not self.belongTo.getCell(chosenCellY + 1, chosenCellX).isWall() and
            self.belongTo.getCell(chosenCellY + 1, chosenCellX) not in self.visited and
            self.belongTo.getCell(chosenCellY + 1, chosenCellX) not in self.frontier
        ):
            southCell = self.belongTo.getCell(chosenCellY + 1, chosenCellX)
            chosenCell.connectToCell(southCell)
            if southCell not in self.frontier:
                self.appendToFrontier(southCell)


        # Try to connect E
        if (
            chosenCellX < self.belongTo.cols - 1 and
            not self.belongTo.getCell(chosenCellY, chosenCellX + 1).isWall() and
            self.belongTo.getCell(chosenCellY, chosenCellX + 1) not in self.visited and
            self.belongTo.getCell(chosenCellY, chosenCellX + 1) not in self.frontier
        ):
            eastCell = self.belongTo.getCell(chosenCellY, chosenCellX + 1)
            chosenCell.connectToCell(eastCell)
            if eastCell not in self.frontier:
                self.appendToFrontier(eastCell)


        # Try to connect W
        if (
            chosenCellX > 0 and
            not self.belongTo.getCell(chosenCellY, chosenCellX - 1).isWall() and
            self.belongTo.getCell(chosenCellY, chosenCellX - 1) not in self.visited and
            self.belongTo.getCell(chosenCellY, chosenCellX - 1) not in self.frontier
        ):
            westCell = self.belongTo.getCell(chosenCellY, chosenCellX - 1)
            chosenCell.connectToCell(westCell)
            if westCell not in self.frontier:
                self.appendToFrontier(westCell)


        # Try to connect NE
        if (
            chosenCellY > 0 and chosenCellX < self.belongTo.cols - 1 and
            not self.belongTo.getCell(chosenCellY - 1, chosenCellX).isWall() and
            not self.belongTo.getCell(chosenCellY, chosenCellX + 1).isWall() and
            not self.belongTo.getCell(chosenCellY - 1, chosenCellX + 1).isWall() and
            self.belongTo.getCell(chosenCellY - 1, chosenCellX + 1) not in self.visited and
            self.belongTo.getCell(chosenCellY - 1, chosenCellX + 1) not in self.frontier
        ):
            neCell = self.belongTo.getCell(chosenCellY - 1, chosenCellX + 1)
            chosenCell.connectToCell(neCell)
            if neCell not in self.frontier:
                self.appendToFrontier(neCell)


        # Try to connect NW
        if (
            chosenCellY > 0 and chosenCellX > 0 and
            not self.belongTo.getCell(chosenCellY - 1, chosenCellX).isWall() and
            not self.belongTo.getCell(chosenCellY, chosenCellX - 1).isWall() and
            not self.belongTo.getCell(chosenCellY - 1, chosenCellX - 1).isWall() and
            self.belongTo.getCell(chosenCellY - 1, chosenCellX - 1) not in self.visited and
            self.belongTo.getCell(chosenCellY - 1, chosenCellX - 1) not in self.frontier
        ):
            nwCell = self.belongTo.getCell(chosenCellY - 1, chosenCellX - 1)
            chosenCell.connectToCell(nwCell)
            if nwCell not in self.frontier:
                self.appendToFrontier(nwCell)


        # Try to connect SW
        if (
            chosenCellY < self.belongTo.rows - 1 and chosenCellX > 0 and
            not self.belongTo.getCell(chosenCellY + 1, chosenCellX).isWall() and
            not self.belongTo.getCell(chosenCellY, chosenCellX - 1).isWall() and
            not self.belongTo.getCell(chosenCellY + 1, chosenCellX - 1).isWall() and
            self.belongTo.getCell(chosenCellY + 1, chosenCellX - 1) not in self.visited and
            self.belongTo.getCell(chosenCellY + 1, chosenCellX - 1) not in self.frontier
        ):
            swCell = self.belongTo.getCell(chosenCellY + 1, chosenCellX - 1)
            chosenCell.connectToCell(swCell)
            if swCell not in self.frontier:
                self.appendToFrontier(swCell)


        # Try to connect SE
        if (
            chosenCellY < self.belongTo.rows - 1 and chosenCellX < self.belongTo.cols - 1 and
            not self.belongTo.getCell(chosenCellY + 1, chosenCellX).isWall() and
            not self.belongTo.getCell(chosenCellY, chosenCellX + 1).isWall() and
            not self.belongTo.getCell(chosenCellY + 1, chosenCellX + 1).isWall() and
            self.belongTo.getCell(chosenCellY + 1, chosenCellX + 1) not in self.visited and
            self.belongTo.getCell(chosenCellY + 1, chosenCellX + 1) not in self.frontier
        ):
            seCell = self.belongTo.getCell(chosenCellY + 1, chosenCellX + 1)
            chosenCell.connectToCell(seCell)
            if seCell not in self.frontier:
                self.appendToFrontier(seCell)

        self.visited.append(chosenCell)
        self.removeFromFrontier(chosenCell)

    def __del__(self):
        pass

class Floor2:
    def __init__(self,rows,cols):
        self.rows=rows
        self.cols=cols
        self.table = [[Cell2(i, j) for j in range(cols)] for i in range(rows)]
        self.listOfSpreads = []
        self.visited= []

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
                cell_values = self.table[i][j].values

                # Check if specific values are present
                specific_values = {"A1", "K1", "D1", "T1"}
                if any(value in specific_values for value in cell_values):
                    # Print specific values
                    print("[", end="")
                    for value in cell_values:
                        if value in specific_values:
                            print("'" + value + "'", end=" ")
                    print("]", end=" ")
                else:
                    # Print the entire values array
                    print(cell_values, end=" ")
            print()  # Move to the next row



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


myLevel2.floor.listOfSpreads[0].expandToward(myLevel2.floor.getCell(0,0))
myLevel2.floor.listOfSpreads[0].expandToward(myLevel2.floor.getCell(0,0))
cell70=myLevel2.floor.getCell(7,0)
cell71=myLevel2.floor.getCell(7,1)
cell60=myLevel2.floor.getCell(6,0)
cell61=myLevel2.floor.getCell(6,1)
cell50=myLevel2.floor.getCell(5,0)
cell51=myLevel2.floor.getCell(5,1)

myLevel2.floor.printTable()