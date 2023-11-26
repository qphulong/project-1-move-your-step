import re
import tkinter as tk

class Cell:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.values = []
        self.belongTo = None

    def setBelongTo(self, value):
        self.belongTo = value

    def getSpecialValue(self):
        if len(self.values) == 1:
            return ""
        else:
            # Return any element other than "0" or "-1" if there are multiple values
            for value in self.values:
                if value not in ["0", "-1"]:
                    return value
            return None  # Or return a default value if all values are "0" or "-1"

    def appendValue(self, value):
        self.values.append(value)

    def removeValue(self, value):
        self.values.remove(value)
        
    def checkValue(self, value):
        return value in self.values
    
    def getManhattanFrom(self, Cell):
        return abs(self.x - Cell.x) + abs(self.y - Cell.y)
    
    def getPhanTrungDucDistance(self,Cell):
        return max(abs(self.x - Cell.x), abs(self.y - Cell.y))
    
    def isWall(self):
        return "-1" in self.values

    def getY(self):
        return self.y
    
    def getX(self):
        return self.x
    
    def getBelongTo(self):
        return self.belongTo

    def __del__(self):
        pass

class Floor:
    def __init__(self,rows,cols):
        self.rows=rows
        self.cols=cols
        self.table = [[Cell(i, j) for j in range(cols)] for i in range(rows)]


        for i in range(self.rows):
            for j in range(self.cols):
                self.table[i][j].setBelongTo(self)     
        
    def getTagCell(self, stringTag):
        return next((cell for spread in self.listOfSpreads for cell in spread.tags if cell.checkValue(stringTag)), None)

    def appendToCell(self, row, col, value):
        self.table[row][col].appendValue(value)

    def removeFromCell(self, row, col, value):
        if self.checkValueInCell(row, col, value):
            self.table[row][col].removeValue(value)

    def checkValueInCell(self, row, col, value):
        return self.table[row][col].checkValue(value)
    
    def getCell(self, row, col):
        return self.table[row][col]
        
class Node:
    def __init__(self,Cell,SearchTree):
        self.cell=Cell
        self.belongTo = SearchTree
        self.pathCost = 0
        self.heuristic = 0
        self.f=0
        self.keys=[]
        self.children=[]
        self.parent=None

    def appendKey(self,value):
        if value not in self.keys:
            self.keys.append(value)

    def setParrent(self, node):
        self.parent=node   

    def getParrent(self):
        return self.parent
    
    def setPathCost(self, value):
        self.pathCost = value

    def getPathCost(self):
        return self.pathCost
    
    def saveHeuristic(self, Cell):
        self.heuristic = self.cell.getManhattanFrom(Cell)
        return self.heuristic
    
    def saveF(self):
        self.f = self.pathCost + self.heuristic
        return self.f
    
    def getF(self):
        return self.f
          
    # a function that add neighbour cell to tempFrontier if they not in frontier and
    # not in visited and not in tempFrontier
    def expandFrontierCell(self,cell,BFSvisited,BFSfrontier,BFStempFrontier):
        # add N cell to tempFrontier
        if (
            cell.y > 0 and
            not self.belongTo.floor.getCell(cell.y - 1, cell.x).isWall() and
            self.belongTo.floor.getCell(cell.y - 1, cell.x) not in BFSvisited and
            self.belongTo.floor.getCell(cell.y - 1, cell.x) not in BFSfrontier and 
            self.belongTo.floor.getCell(cell.y - 1, cell.x) not in BFStempFrontier
        ):
            northCell = self.belongTo.floor.getCell(cell.y - 1, cell.x)
            BFStempFrontier.append(northCell)

        # add W cell to tempFrontier
        if (
            cell.x > 0 and
            not self.belongTo.floor.getCell(cell.y, cell.x - 1).isWall() and
            self.belongTo.floor.getCell(cell.y, cell.x - 1) not in BFSvisited and
            self.belongTo.floor.getCell(cell.y, cell.x - 1) not in BFSfrontier and 
            self.belongTo.floor.getCell(cell.y, cell.x - 1) not in BFStempFrontier
        ):
            westCell = self.belongTo.floor.getCell(cell.y, cell.x - 1)
            BFStempFrontier.append(westCell)

        # add S cell to tempFrontier
        if (
            cell.y < self.belongTo.floor.rows - 1 and
            not self.belongTo.floor.getCell(cell.y + 1, cell.x).isWall() and
            self.belongTo.floor.getCell(cell.y + 1, cell.x) not in BFSvisited and
            self.belongTo.floor.getCell(cell.y + 1, cell.x) not in BFSfrontier and
            self.belongTo.floor.getCell(cell.y + 1, cell.x) not in BFStempFrontier
        ):
            southCell = self.belongTo.floor.getCell(cell.y + 1, cell.x)
            BFStempFrontier.append(southCell)

        # add E cell to tempFrontier
        if (
            cell.x < self.belongTo.floor.cols - 1 and
            not self.belongTo.floor.getCell(cell.y, cell.x + 1).isWall() and
            self.belongTo.floor.getCell(cell.y, cell.x + 1) not in BFSvisited and
            self.belongTo.floor.getCell(cell.y, cell.x + 1) not in BFSfrontier and
            self.belongTo.floor.getCell(cell.y, cell.x + 1) not in BFStempFrontier
        ):
            eastCell = self.belongTo.floor.getCell(cell.y, cell.x + 1)
            BFStempFrontier.append(eastCell)

        # add NE cell to tempFrontier
        if (
            cell.y > 0 and cell.x < self.belongTo.floor.cols - 1 and
            not self.belongTo.floor.getCell(cell.y - 1, cell.x).isWall() and
            not self.belongTo.floor.getCell(cell.y,cell.x + 1).isWall() and
            not self.belongTo.floor.getCell(cell.y - 1, cell.x + 1).isWall() and
            self.belongTo.floor.getCell(cell.y - 1, cell.x + 1) not in BFSvisited and
            self.belongTo.floor.getCell(cell.y - 1, cell.x + 1) not in BFSfrontier and
            self.belongTo.floor.getCell(cell.y - 1, cell.x + 1) not in BFStempFrontier
        ):
            neCell = self.belongTo.floor.getCell(cell.y - 1, cell.x + 1)
            BFStempFrontier.append(neCell)

        # Add NW cell to tempFrontier
        if (
            cell.y > 0 and cell.x > 0 and
            not self.belongTo.floor.getCell(cell.y - 1, cell.x).isWall() and
            not self.belongTo.floor.getCell(cell.y, cell.x - 1).isWall() and
            not self.belongTo.floor.getCell(cell.y - 1, cell.x - 1).isWall() and
            self.belongTo.floor.getCell(cell.y - 1, cell.x - 1) not in BFSvisited and
            self.belongTo.floor.getCell(cell.y - 1, cell.x - 1) not in BFSfrontier and
            self.belongTo.floor.getCell(cell.y - 1, cell.x - 1) not in BFStempFrontier
        ):
            nwCell = self.belongTo.floor.getCell(cell.y - 1, cell.x - 1)
            BFStempFrontier.append(nwCell)

        # Add SW cell to tempFrontier
        if (
            cell.y < self.belongTo.floor.rows - 1 and cell.x > 0 and
            not self.belongTo.floor.getCell(cell.y + 1, cell.x).isWall() and
            not self.belongTo.floor.getCell(cell.y, cell.x - 1).isWall() and
            not self.belongTo.floor.getCell(cell.y + 1, cell.x - 1).isWall() and
            self.belongTo.floor.getCell(cell.y + 1, cell.x - 1) not in BFSvisited and
            self.belongTo.floor.getCell(cell.y + 1, cell.x - 1) not in BFSfrontier and
            self.belongTo.floor.getCell(cell.y + 1, cell.x - 1) not in BFStempFrontier
        ):
            swCell = self.belongTo.floor.getCell(cell.y + 1, cell.x - 1)
            BFStempFrontier.append(swCell)

        # Add SE cell to tempFrontier
        if (
            cell.y < self.belongTo.floor.rows - 1 and cell.x < self.belongTo.floor.cols - 1 and
            not self.belongTo.floor.getCell(cell.y + 1, cell.x).isWall() and
            not self.belongTo.floor.getCell(cell.y, cell.x + 1).isWall() and
            not self.belongTo.floor.getCell(cell.y + 1, cell.x + 1).isWall() and
            self.belongTo.floor.getCell(cell.y + 1, cell.x + 1) not in BFSvisited and
            self.belongTo.floor.getCell(cell.y + 1, cell.x + 1) not in BFSfrontier and
            self.belongTo.floor.getCell(cell.y + 1, cell.x + 1) not in BFStempFrontier
        ):
            seCell = self.belongTo.floor.getCell(cell.y + 1, cell.x + 1)
            BFStempFrontier.append(seCell)
        

    def expand(self):
        BFSfrontier = []
        BFStempFrontier = []
        BFSvisited = []
        BFSfrontier.append(self.cell)
        steps = -1
        while BFSfrontier:
            steps += 1

            # block nay de debug
            # if self.cell.checkValue("K1"):
            #     print("Frontier")
            #     for eachCell in BFSfrontier:
            #         print(eachCell.y,eachCell.x)

            for cell in BFSfrontier:

                #analize cell
                cell_tag = cell.getSpecialValue()
                #normal cell
                if cell_tag == "" or cell_tag[0]=="A":
                    self.expandFrontierCell(cell,BFSvisited,BFSfrontier,BFStempFrontier)
                elif cell_tag[0] == "K":
                    #first expand, cause it will not expand since first cell in frontier and dup key
                    if len(BFSfrontier)==1 and BFSfrontier[0]==self.cell:
                        self.expandFrontierCell(cell,BFSvisited,BFSfrontier,BFStempFrontier)
                    else:
                        #check dups
                        tempNode=self
                        addNode=True
                        while(tempNode):
                            if cell_tag in tempNode.keys:
                                addNode = False
                                break
                            tempNode=tempNode.parent

                        if addNode:
                            #create new node
                            newNode = Node(cell,self.belongTo)
                            newNode.setPathCost(self.pathCost+steps)
                            newNode.saveHeuristic(self.belongTo.goalCell)
                            newNode.saveF()

                            #append new node to tree
                            self.children.append(newNode)
                            newNode.parent=self

                            #inherit and append new key
                            for eachKey in self.keys:
                                newNode.appendKey(eachKey)
                            newNode.appendKey(cell_tag)

                            #expand this cell
                            self.expandFrontierCell(cell,BFSvisited,BFSfrontier,BFStempFrontier)

                elif cell_tag[0] == "D":
                    #first expand, cause it will not expand since first cell in frontier and dup key
                    if len(BFSfrontier)==1 and BFSfrontier[0]==self.cell:
                        self.expandFrontierCell(cell,BFSvisited,BFSfrontier,BFStempFrontier)
                    else:
                        # if has key
                        if str("K"+str(cell_tag[1])) in self.keys:
                            #create new node
                            newNode = Node(cell,self.belongTo)
                            newNode.setPathCost(self.pathCost+steps)
                            newNode.saveHeuristic(self.belongTo.goalCell)
                            newNode.saveF()
                            
                            #inherit key
                            for eachKey in self.keys:
                                newNode.appendKey(eachKey)

                            #append new node to tree
                            self.children.append(newNode)
                            newNode.parent=self

                            # if go through the same door with same keys,then delete this new node
                            tempNode = self
                            while(tempNode):
                                if len(newNode.keys) == (tempNode.keys):
                                    self.children.remove(newNode)
                                    newNode.parent=None
                                    del newNode
                                tempNode=tempNode.parent
                        #if does not have key
                        else:
                            pass

                elif cell_tag[0] == "T":
                    #create new node
                    newNode = Node(cell,self.belongTo)
                    newNode.setPathCost(self.pathCost+steps)
                    newNode.saveHeuristic(self.belongTo.goalCell)
                    newNode.saveF()

                    #append new node to tree
                    self.children.append(newNode)
                    newNode.parent=self
                BFSvisited.append(cell)
            pass

            #update the frontier
            BFSfrontier=BFStempFrontier
            BFStempFrontier=[]
            pass

class SearchTree:
    def __init__(self):
        self.root = None
        self.frontier = []
        self.visited = []
        self.currentNode = None
        self.goalCell = None
        self.floor = None
    
    def getInputFile(self,filePath):
        with open (filePath, "r") as file:
            lines = file.readlines()
        
        rows, cols = map(int, lines[0].strip().split(','))
        self.floor=Floor(rows, cols)
        
        for i in range(2, len(lines)):
            row_values = list(map(str, lines[i].strip().split(',')))

            for j in range(cols):
                cell_value = row_values[j]

                # Check if the cell value has the format "Ki", "Di"
                if re.match(r'[KD]\d+', cell_value):
                    self.floor.appendToCell(i - 2, j, "0")

                    # Extract the character and integer parts from the cell value
                    char_part, num_part = re.match(r'([KD])(\d+)', cell_value).groups()

                #if goalCell show up
                if re.match(r'[T]\d+', cell_value):
                    self.floor.appendToCell(i - 2, j, "0")

                    # Extract the character and integer parts from the cell value
                    char_part, num_part = re.match(r'([AKTD])(\d+)', cell_value).groups()

                    self.goalCell=self.floor.getCell(i - 2, j)

                #if startCell show up
                if re.match(r'[A]\d+', cell_value):
                    self.floor.appendToCell(i - 2, j, "0")

                    # Extract the character and integer parts from the cell value
                    char_part, num_part = re.match(r'([AKTD])(\d+)', cell_value).groups()

                    self.root = Node(self.floor.getCell(i - 2, j), self)
                    self.frontier.append(self.root)
                    self.currentNode=self.root

                # Regardless of the condition, add the original cell value to the cell
                self.floor.appendToCell(i - 2, j, cell_value)

    def AStar(self):
        self.root.saveHeuristic(self.goalCell)
        self.root.saveF()
        while(self.frontier):
            #self.visualize()
            self.frontier.sort(key=lambda x: x.getF())
            self.currentNode = self.frontier.pop(0)

            # if path found
            if self.currentNode.cell == self.goalCell:
                tempNode = self.currentNode
                while(tempNode):
                    print(tempNode.cell.getSpecialValue())
                    tempNode=tempNode.parent
                return
            
            self.currentNode.expand()
            for eachChild in self.currentNode.children:
                self.frontier.append(eachChild)
                pass

        print("No path found")

searchTree2 = SearchTree()
searchTree2.getInputFile("input//input2-level2.txt")
searchTree2.AStar()
pass