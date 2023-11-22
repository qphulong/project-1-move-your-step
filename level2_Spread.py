import re
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
    def __init__(self,floor,firstCell):
        self.frontier = []
        self.visited = []
        self.tags = []
        self.belongTo = None
        self.tags.append(firstCell)
        self.belongTo = floor
        self.frontier.append(firstCell)
    
    def checkTagCell(self, Cell):
        return Cell in self.tags
    
    def checkTagString(self, stringTag):
        return any(eachCell.checkValue(stringTag) for eachCell in self.tags)

    def appendToFrontier(self, Cell):
        self.frontier.append(Cell)

    def removeFromFrontier(self, Cell):
        if Cell in self.frontier:
            self.frontier.remove(Cell)

    def appendToTags(self, Cell):
        self.tags.append(Cell)

    def removeFromTags(self, cell):
        if cell in self.tags:
            self.tags.remove(cell)

    def mergeSpread(self, otherSpread):
        for eachVisitedCell in self.visited:
            if eachVisitedCell in otherSpread.frontier:
                #merge tag
                for otherSpreadTag in otherSpread.tags:
                     self.appendToTags(otherSpreadTag)
                #merge visited
                for otherSpreadVisited in otherSpread.visited:
                    self.visited.append(otherSpreadVisited)
                    if otherSpreadVisited in self.frontier:
                        self.frontier.remove(otherSpreadVisited)
                #merge frontier
                for otherSpreadFrontier in otherSpread.frontier:
                    if otherSpreadFrontier not in self.frontier and otherSpreadFrontier not in self.visited:
                        self.frontier.append(otherSpreadFrontier)
                break
        self.belongTo.removeSpread(otherSpread)
        
    def expandToward(self,goalCell):
         # Calculate heuristics for each cell in the frontier
        heuristics = [cell.getManhattanFrom(goalCell) for cell in self.frontier]

        # Find the index of the cell with the minimum heuristic value
        min_index = min(range(len(heuristics)), key=heuristics.__getitem__)

        # Retrieve the cell with the minimum heuristic value
        chosenCell = self.frontier[min_index]

        # if chosen cell is in frontier of another spread, mergeThem = True
        needToMerge = chosenCell.connectedCells.__len__() > 1
        if needToMerge:
            for eachSpread in self.belongTo.listOfSpreads:
                if eachSpread!=self and chosenCell in eachSpread.frontier:
                    otherSpread = eachSpread
                    break
        
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

        if needToMerge:
            self.mergeSpread(otherSpread)

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
    
    #function return a spread that has at least 1 tag that has same value
    def getSpread(self, tagCell):
        return next((spread for spread in self.listOfSpreads if tagCell in spread.tags), None)
    
    def getSpread(self, stringTag):
        return next((spread for spread in self.listOfSpreads if any(stringTag in cell.values for cell in spread.tags)), None)

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

            for j in range(cols):
                cell_value = row_values[j]

                # Check if the cell value has the format "Ai", "Ki", "Ti", "Di"
                if re.match(r'[AKTD]\d+', cell_value):
                    self.floor.appendToCell(i - 2, j, "0")

                    # Extract the character and integer parts from the cell value
                    char_part, num_part = re.match(r'([AKTD])(\d+)', cell_value).groups()

                    # Create a Spread with the extracted values
                    self.floor.appendSpread(Spread(self.floor, self.floor.getCell(i - 2, j)))

                # Regardless of the condition, add the original cell value to the cell
                self.floor.appendToCell(i - 2, j, cell_value)
        

    #TODO generalize this function
    def tryToSpread(self):
        # while none spread has both value "T1" and "A1"
        while not any(spread.checkTagString("T1") and spread.checkTagString("A1") for spread in self.floor.listOfSpreads):
            numberOfVisitedCells = self.floor.visited.__len__()
            for eachSpread in self.floor.listOfSpreads:
                for eachTag in eachSpread.tags:
                    #TODO handle spread hierachy logic
                    break
            # if after a spread but no cell is added to visited means no path found
            if numberOfVisitedCells == self.floor.visited.__len__():
                print("No Path Found")
                return


myLevel2 = Level2()
myLevel2.getInputFile("input//input1-level2.txt")
A1 = myLevel2.floor.getSpread("A1")
K1 = myLevel2.floor.getSpread("K1")
K1.expandToward(myLevel2.floor.getCell(0, 0))
A1.expandToward(myLevel2.floor.getCell(0, 0))
A1.expandToward(myLevel2.floor.getCell(0, 0))
A1.expandToward(myLevel2.floor.getCell(0, 0))
myLevel2.floor.printTable()