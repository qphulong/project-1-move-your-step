import re
import tkinter as tk
from collections import Counter
from algorithm import export_heatmap


class Cell:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.values = []
        self.belongTo = None
        self.children = []
        self.parrent = None

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
            return ""  # Or return a empty string

    def appendValue(self, value):
        self.values.append(value)

    def removeValue(self, value):
        self.values.remove(value)

    def checkValue(self, value):
        return value in self.values

    def getManhattanFrom(self, GoalCell):
        return abs(self.x - GoalCell.x) + abs(self.y - GoalCell.y)

    def getPhanTrungDucDistance(self, Cell):
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
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.table = [[Cell(i, j) for j in range(cols)] for i in range(rows)]

        for i in range(self.rows):
            for j in range(self.cols):
                self.table[i][j].setBelongTo(self)

    # function that set children and parrent of every cell to empty
    def clearAllRelation(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.table[i][j].children = []
                self.table[i][j].parrent = None

    def getTagCell(self, stringTag):
        return next(
            (
                cell
                for spread in self.listOfSpreads
                for cell in spread.tags
                if cell.checkValue(stringTag)
            ),
            None,
        )

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
    def __init__(self, Cell, SearchTree):
        self.cell = Cell
        self.belongTo = SearchTree
        self.pathCost = 0
        self.heuristic = 0
        self.f = 0
        self.keys = []
        self.children = []
        self.parent = None
        # attribute that is array of cell leads from parrent node to self
        self.path = []

    def appendKey(self, value):
        if value not in self.keys:
            self.keys.append(value)

    def setParrent(self, node):
        self.parent = node

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
    def expandFrontierCell(self, cell, BFSvisited, BFSfrontier, BFStempFrontier):
        # add N cell to tempFrontier
        if (
            cell.y > 0
            and not self.belongTo.floor.getCell(cell.y - 1, cell.x).isWall()
            and self.belongTo.floor.getCell(cell.y - 1, cell.x) not in BFSvisited
            and self.belongTo.floor.getCell(cell.y - 1, cell.x) not in BFSfrontier
            and self.belongTo.floor.getCell(cell.y - 1, cell.x) not in BFStempFrontier
        ):
            northCell = self.belongTo.floor.getCell(cell.y - 1, cell.x)
            BFStempFrontier.append(northCell)
            cell.children.append(northCell)
            northCell.parrent = cell

        # add W cell to tempFrontier
        if (
            cell.x > 0
            and not self.belongTo.floor.getCell(cell.y, cell.x - 1).isWall()
            and self.belongTo.floor.getCell(cell.y, cell.x - 1) not in BFSvisited
            and self.belongTo.floor.getCell(cell.y, cell.x - 1) not in BFSfrontier
            and self.belongTo.floor.getCell(cell.y, cell.x - 1) not in BFStempFrontier
        ):
            westCell = self.belongTo.floor.getCell(cell.y, cell.x - 1)
            BFStempFrontier.append(westCell)
            cell.children.append(westCell)
            westCell.parrent = cell

        # add S cell to tempFrontier
        if (
            cell.y < self.belongTo.floor.rows - 1
            and not self.belongTo.floor.getCell(cell.y + 1, cell.x).isWall()
            and self.belongTo.floor.getCell(cell.y + 1, cell.x) not in BFSvisited
            and self.belongTo.floor.getCell(cell.y + 1, cell.x) not in BFSfrontier
            and self.belongTo.floor.getCell(cell.y + 1, cell.x) not in BFStempFrontier
        ):
            southCell = self.belongTo.floor.getCell(cell.y + 1, cell.x)
            BFStempFrontier.append(southCell)
            cell.children.append(southCell)
            southCell.parrent = cell

        # add E cell to tempFrontier
        if (
            cell.x < self.belongTo.floor.cols - 1
            and not self.belongTo.floor.getCell(cell.y, cell.x + 1).isWall()
            and self.belongTo.floor.getCell(cell.y, cell.x + 1) not in BFSvisited
            and self.belongTo.floor.getCell(cell.y, cell.x + 1) not in BFSfrontier
            and self.belongTo.floor.getCell(cell.y, cell.x + 1) not in BFStempFrontier
        ):
            eastCell = self.belongTo.floor.getCell(cell.y, cell.x + 1)
            BFStempFrontier.append(eastCell)
            cell.children.append(eastCell)
            eastCell.parrent = cell

        # add NE cell to tempFrontier
        if (
            cell.y > 0
            and cell.x < self.belongTo.floor.cols - 1
            and not self.belongTo.floor.getCell(cell.y - 1, cell.x).isWall()
            and not self.belongTo.floor.getCell(cell.y, cell.x + 1).isWall()
            and not self.belongTo.floor.getCell(cell.y - 1, cell.x + 1).isWall()
            and self.belongTo.floor.getCell(cell.y - 1, cell.x + 1) not in BFSvisited
            and self.belongTo.floor.getCell(cell.y - 1, cell.x + 1) not in BFSfrontier
            and self.belongTo.floor.getCell(cell.y - 1, cell.x + 1)
            not in BFStempFrontier
        ):
            neCell = self.belongTo.floor.getCell(cell.y - 1, cell.x + 1)
            BFStempFrontier.append(neCell)
            cell.children.append(neCell)
            neCell.parrent = cell

        # Add NW cell to tempFrontier
        if (
            cell.y > 0
            and cell.x > 0
            and not self.belongTo.floor.getCell(cell.y - 1, cell.x).isWall()
            and not self.belongTo.floor.getCell(cell.y, cell.x - 1).isWall()
            and not self.belongTo.floor.getCell(cell.y - 1, cell.x - 1).isWall()
            and self.belongTo.floor.getCell(cell.y - 1, cell.x - 1) not in BFSvisited
            and self.belongTo.floor.getCell(cell.y - 1, cell.x - 1) not in BFSfrontier
            and self.belongTo.floor.getCell(cell.y - 1, cell.x - 1)
            not in BFStempFrontier
        ):
            nwCell = self.belongTo.floor.getCell(cell.y - 1, cell.x - 1)
            BFStempFrontier.append(nwCell)
            cell.children.append(nwCell)
            nwCell.parrent = cell

        # Add SW cell to tempFrontier
        if (
            cell.y < self.belongTo.floor.rows - 1
            and cell.x > 0
            and not self.belongTo.floor.getCell(cell.y + 1, cell.x).isWall()
            and not self.belongTo.floor.getCell(cell.y, cell.x - 1).isWall()
            and not self.belongTo.floor.getCell(cell.y + 1, cell.x - 1).isWall()
            and self.belongTo.floor.getCell(cell.y + 1, cell.x - 1) not in BFSvisited
            and self.belongTo.floor.getCell(cell.y + 1, cell.x - 1) not in BFSfrontier
            and self.belongTo.floor.getCell(cell.y + 1, cell.x - 1)
            not in BFStempFrontier
        ):
            swCell = self.belongTo.floor.getCell(cell.y + 1, cell.x - 1)
            BFStempFrontier.append(swCell)
            cell.children.append(swCell)
            swCell.parrent = cell

        # Add SE cell to tempFrontier
        if (
            cell.y < self.belongTo.floor.rows - 1
            and cell.x < self.belongTo.floor.cols - 1
            and not self.belongTo.floor.getCell(cell.y + 1, cell.x).isWall()
            and not self.belongTo.floor.getCell(cell.y, cell.x + 1).isWall()
            and not self.belongTo.floor.getCell(cell.y + 1, cell.x + 1).isWall()
            and self.belongTo.floor.getCell(cell.y + 1, cell.x + 1) not in BFSvisited
            and self.belongTo.floor.getCell(cell.y + 1, cell.x + 1) not in BFSfrontier
            and self.belongTo.floor.getCell(cell.y + 1, cell.x + 1)
            not in BFStempFrontier
        ):
            seCell = self.belongTo.floor.getCell(cell.y + 1, cell.x + 1)
            BFStempFrontier.append(seCell)
            cell.children.append(seCell)
            seCell.parrent = cell

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
                # analize cell
                cell_tag = cell.getSpecialValue()
                # normal cell
                if cell_tag == "" or cell_tag[0] == "A":
                    self.expandFrontierCell(
                        cell, BFSvisited, BFSfrontier, BFStempFrontier
                    )
                # key cell
                elif cell_tag[0] == "K":
                    # first expand, cause it will not expand since first cell in frontier and dup key
                    if len(BFSfrontier) == 1 and BFSfrontier[0] == self.cell:
                        self.expandFrontierCell(
                            cell, BFSvisited, BFSfrontier, BFStempFrontier
                        )
                    else:
                        # check dups
                        tempNode = self
                        addNode = True
                        while tempNode:
                            if cell_tag in tempNode.keys:
                                addNode = False
                                break
                            tempNode = tempNode.parent

                        if addNode:
                            # create new node
                            newNode = Node(cell, self.belongTo)
                            newNode.setPathCost(self.pathCost + steps)
                            newNode.saveHeuristic(self.belongTo.goalCell)
                            newNode.saveF()

                            # append new node to tree
                            self.children.append(newNode)
                            newNode.parent = self

                            # inherit and append new key
                            for eachKey in self.keys:
                                newNode.appendKey(eachKey)
                            newNode.appendKey(cell_tag)

                            # get path from parrent to new node
                            tempCell = cell
                            while tempCell:
                                newNode.path.append(tempCell)
                                tempCell = tempCell.parrent

                            # expand this cell
                            self.expandFrontierCell(
                                cell, BFSvisited, BFSfrontier, BFStempFrontier
                            )
                # door cell
                elif cell_tag[0] == "D":
                    # first expand, cause it will not expand since first cell in frontier and dup key
                    if len(BFSfrontier) == 1 and BFSfrontier[0] == self.cell:
                        self.expandFrontierCell(
                            cell, BFSvisited, BFSfrontier, BFStempFrontier
                        )
                    else:
                        # if has key
                        if str("K" + str(cell_tag[1])) in self.keys:
                            # create new node
                            newNode = Node(cell, self.belongTo)
                            newNode.setPathCost(self.pathCost + steps)
                            newNode.saveHeuristic(self.belongTo.goalCell)
                            newNode.saveF()

                            # inherit key
                            for eachKey in self.keys:
                                newNode.appendKey(eachKey)

                            # append new node to tree
                            self.children.append(newNode)
                            newNode.parent = self

                            # get path from parrent to new node
                            tempCell = cell
                            while tempCell:
                                newNode.path.append(tempCell)
                                tempCell = tempCell.parrent

                            # if go through the same door with same keys,then delete this new node
                            tempNode = self.parent
                            while tempNode:
                                if (
                                    len(newNode.keys) == len(tempNode.keys)
                                    and newNode.cell == tempNode.cell
                                ):
                                    self.children.remove(newNode)
                                    newNode.parent = None
                                    del newNode
                                    break
                                tempNode = tempNode.parent
                        # if does not have key
                        else:
                            pass
                # goal cell
                elif cell_tag[0] == "T":
                    # create new node
                    newNode = Node(cell, self.belongTo)
                    newNode.setPathCost(self.pathCost + steps)
                    newNode.saveHeuristic(self.belongTo.goalCell)
                    newNode.saveF()

                    # append new node to tree
                    self.children.append(newNode)
                    newNode.parent = self

                    # get path from parrent to new node
                    tempCell = cell
                    while tempCell:
                        newNode.path.append(tempCell)
                        tempCell = tempCell.parrent

                BFSvisited.append(cell)
            pass

            # update the frontier
            BFSfrontier = BFStempFrontier
            BFStempFrontier = []
        # after finish the loop, which is expand a node in search tree, set all cell relation to empty
        self.cell.belongTo.clearAllRelation()


class SearchTree:
    def __init__(self):
        self.root = None
        self.frontier = []
        self.currentNode = None
        self.goalCell = None
        self.floor = None
        self.checkRoot = False
        self.finalPath=[]
        self.score = 0

    def getCheckRoot(self):
        return self.checkRoot
    def getInputFile(self, filePath):
        with open(filePath, "r") as file:
            lines = file.readlines()

        rows, cols = map(int, lines[0].strip().split(","))
        self.floor = Floor(rows, cols)

        for i in range(2, len(lines)):
            row_values = list(map(str, lines[i].strip().split(",")))

            for j in range(cols):
                cell_value = row_values[j]

                # Check if the cell value has the format "Ki", "Di"
                if re.match(r"[KD]\d+", cell_value):
                    self.floor.appendToCell(i - 2, j, "0")

                    # Extract the character and integer parts from the cell value
                    char_part, num_part = re.match(r"([KD])(\d+)", cell_value).groups()

                # if goalCell show up
                if re.match(r"[T]\d+", cell_value):
                    self.floor.appendToCell(i - 2, j, "0")

                    # Extract the character and integer parts from the cell value
                    char_part, num_part = re.match(
                        r"([AKTD])(\d+)", cell_value
                    ).groups()

                    self.goalCell = self.floor.getCell(i - 2, j)

                # if startCell show up
                if re.match(r"[A]\d+", cell_value):
                    self.floor.appendToCell(i - 2, j, "0")

                    # Extract the character and integer parts from the cell value
                    char_part, num_part = re.match(
                        r"([AKTD])(\d+)", cell_value
                    ).groups()

                    self.root = Node(self.floor.getCell(i - 2, j), self)
                    self.frontier.append(self.root)
                    self.currentNode = self.root

                # Regardless of the condition, add the original cell value to the cell
                self.floor.appendToCell(i - 2, j, cell_value)

    def AStar(self):
        self.root.saveHeuristic(self.goalCell)
        self.root.saveF()

        while self.frontier:
            self.frontier.sort(key=lambda x: x.getF())
            self.currentNode = self.frontier.pop(0)

            # if path found
            if self.currentNode.cell == self.goalCell:
                # tempNode = self.currentNode
                # while (tempNode):
                #     print(tempNode.cell.getSpecialValue())
                #     tempNode = tempNode.parent

                #animation
                tempNode = self.currentNode
                while (tempNode):
                    for eachCell in tempNode.path:
                        self.finalPath.append(eachCell)
                    tempNode = tempNode.parent
                self.finalPath.reverse()
                self.pathAnimation()

                #heatmap
                # self.heatMap()
                return

            self.currentNode.expand()
            for eachChild in self.currentNode.children:
                self.frontier.append(eachChild)
                pass

        print("No path found")

    def visualize(self):
        # Create the main window
        root = tk.Tk()
        root.title("Search Tree Visualization")

        # Create a canvas to draw on
        canvas = tk.Canvas(
            root, width=self.floor.cols * 50, height=self.floor.rows * 50
        )
        canvas.pack()

        # basic map
        for i in range(self.floor.rows):
            for j in range(self.floor.cols):
                x0, y0 = j * 20, i * 20
                x1, y1 = (j + 1) * 20, (i + 1) * 20

                # Set color for cells with value "-1" to black
                if self.floor.table[i][j].checkValue("-1"):
                    canvas.create_rectangle(x0, y0, x1, y1, fill="black")
                else:
                    canvas.create_rectangle(x0, y0, x1, y1, fill="white")
                    # print special value
                    specialValue = self.floor.table[i][j].getSpecialValue()
                    canvas.create_text(
                        x0 + 10, y0 + 10, text=specialValue, fill="black"
                    )

        # draw path
        tempNode = self.currentNode
        while tempNode:
            # Draw rectangles for each cell
            for i in range(self.floor.rows):
                for j in range(self.floor.cols):
                    x0, y0 = j * 20, i * 20
                    x1, y1 = (j + 1) * 20, (i + 1) * 20

                    # Set color for cells in the path to green
                    if self.floor.table[i][j] in tempNode.path:
                        canvas.create_rectangle(x0, y0, x1, y1, fill="green")
                    # Set color for cells pointed by tempNode to red
                    if tempNode.cell and self.floor.table[i][j] == tempNode.cell:
                        canvas.create_rectangle(x0, y0, x1, y1, fill="red")
                        specialValue = self.floor.table[i][j].getSpecialValue()
                        canvas.create_text(
                            x0 + 10, y0 + 10, text=specialValue, fill="black"
                        )

            # Move to the parent node
            tempNode = tempNode.parent
        # Run the GUI
        root.mainloop()

    def heatMap(self):
        # Create the main window
        root = tk.Tk()
        self.checkRoot = True
        root.title("Search Tree Visualization")

        # Create a canvas to draw on
        canvas = tk.Canvas(
            root, width=self.floor.cols * 40, height=self.floor.rows * 35
        )
        canvas.pack()

        #theo nut back
        def goback():
            self.checkRoot = False
            root.destroy()

        back_button = tk.Button(root, text="Back", height = 1, width = 20, bg = 'brown',command = goback)
        back_button.place(x=self.floor.cols * 25, y=self.floor.rows * 15)

        # basic map
        for i in range(self.floor.rows):
            for j in range(self.floor.cols):
                x0, y0 = j * 20, i * 20
                x1, y1 = (j + 1) * 20, (i + 1) * 20

                # Set color for cells with value "-1" to black
                if self.floor.table[i][j].checkValue("-1"):
                    canvas.create_rectangle(x0, y0, x1, y1, fill="black")
                else:
                    canvas.create_rectangle(x0, y0, x1, y1, fill="white")
                    # print special value
                    specialValue = self.floor.table[i][j].getSpecialValue()
                    canvas.create_text(
                        x0 + 10, y0 + 10, text=specialValue, fill="black"
                    )

        # draw path
        tempNode = self.currentNode
        generalPath = []
        while tempNode:
            for eachCell in tempNode.path:
                generalPath.append(eachCell)
            tempNode = tempNode.parent

        for eachCell in generalPath:
            for i in range(self.floor.rows):
                for j in range(self.floor.cols):
                    x0, y0 = j * 20, i * 20
                    x1, y1 = (j + 1) * 20, (i + 1) * 20

                    # Set color for cells in the path to green
                    if self.floor.table[i][j] in generalPath:
                        if Counter(generalPath)[self.floor.table[i][j]] == 1:
                            canvas.create_rectangle(x0, y0, x1, y1, fill="#ff8888")
                        elif Counter(generalPath)[self.floor.table[i][j]] == 2:
                            canvas.create_rectangle(x0, y0, x1, y1, fill="#ff4b4b")
                        elif Counter(generalPath)[self.floor.table[i][j]] == 3:
                            canvas.create_rectangle(x0, y0, x1, y1, fill="#ff0000")
                        elif Counter(generalPath)[self.floor.table[i][j]] == 4:
                            canvas.create_rectangle(x0, y0, x1, y1, fill="#cb0000")
                    # Set color for cells pointed by tempNode to red
                    if self.floor.table[i][j].getSpecialValue() != "":
                        canvas.create_rectangle(x0, y0, x1, y1, fill="#2ad500")
                        specialValue = self.floor.table[i][j].getSpecialValue()
                        canvas.create_text(
                            x0 + 10, y0 + 10, text=specialValue, fill="black"
                        )
            pass
        # Run the GUI

        root.mainloop()

    def pathAnimation(self):
        # Create the main window
        root = tk.Tk()
        root.title("Search Tree Path Animation")

        # Create a canvas to draw on
        canvas = tk.Canvas(root, width=self.floor.cols * 35, height=self.floor.rows * 25)
        canvas.pack()

        # Nut back
        def goback():
            self.checkRoot = False
            root.destroy()

        back_button = tk.Button(root, text="Back", height=1, width=10, bg='brown', command=goback)
        back_button.place(x=self.floor.cols * 21, y=self.floor.rows * 15)

        # score = tk.Label(root, font=('Arial', 25), text='Score: ' + str(self.score), fg='Black')
        # score.place(x=self.floor.cols * 23, y=self.floor.rows * 12)

        # Function to update the canvas for animation
        def update_animation(index):
            if index < len(self.finalPath):
                # Clear the canvas
                canvas.delete("all")

                # Draw rectangles for each cell
                for i in range(self.floor.rows):
                    for j in range(self.floor.cols):
                        x0, y0 = j * 20, i * 20
                        x1, y1 = (j + 1) * 20, (i + 1) * 20

                        # Set color for cells with value "-1" to black
                        if self.floor.table[i][j].checkValue("-1"):
                            canvas.create_rectangle(x0, y0, x1, y1, fill="black")
                        else:
                            # Set color for cells with a special value to red
                            if self.floor.table[i][j].getSpecialValue() != "":
                                canvas.create_rectangle(x0, y0, x1, y1, fill="red")
                                # print special value in black text
                                specialValue = self.floor.table[i][j].getSpecialValue()
                                canvas.create_text(
                                    x0 + 10, y0 + 10, text=specialValue, fill="black"
                                )
                            else:
                                canvas.create_rectangle(x0, y0, x1, y1, fill="white")

                        # Set color for cells in the path to green
                        if self.floor.table[i][j] == self.finalPath[index]:
                            canvas.create_rectangle(x0, y0, x1, y1, fill="green")
                            self.score+=1
                            score = tk.Label(root, font=('Arial', 15), text='Score: ' + str(self.score), fg='Black')
                            score.place(x=self.floor.cols * 22, y=self.floor.rows * 11)
                

                # Schedule the next update after a delay (adjust the delay as needed)
                root.after(100, update_animation, index + 1)

        # Start the animation loop
        update_animation(0)

        # Run the GUI
        export_heatmap(root)
        root.mainloop()



# searchTree2 = SearchTree()
# searchTree2.getInputFile("input//input2-level2.txt")
# searchTree2.AStar()
pass
