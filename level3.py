import re
import tkinter as tk
from enum import Enum
from collections import Counter


class Cell:
    def __init__(self, y, x, floor_no):
        self.y = y
        self.x = x
        self.floor_no = floor_no
        self.values = []
        self.belongTo = None
        self.children = []
        self.parrent = None

    def __eq__(self, other):
        return (
            self.y == other.y and self.x == other.x and self.floor_no == other.floor_no
        )

    def __hash__(self):
        return hash((self.y, self.x, self.floor_no))

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

    def getFloorsHeuristic(self, GoalCell):
        return self.getManhattanFrom(GoalCell) + abs(self.floor_no - GoalCell.floor_no)

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
    def __init__(self, rows, cols, floor_no):
        self.rows = rows
        self.cols = cols
        self.table = [[Cell(i, j, floor_no) for j in range(cols)] for i in range(rows)]
        self.floor_no = floor_no

        for i in range(self.rows):
            for j in range(self.cols):
                self.table[i][j].setBelongTo(self)  # belong to a floor

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

    # function that set children and parrent of every cell to empty
    def clearAllRelation(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.table[i][j].children = []
                self.table[i][j].parrent = None

    def appendToCell(self, row, col, value):
        self.table[row][col].appendValue(value)

    def removeFromCell(self, row, col, value):
        if self.checkValueInCell(row, col, value):
            self.table[row][col].removeValue(value)

    def checkValueInCell(self, row, col, value):
        return self.table[row][col].checkValue(value)

    def getCell(self, row, col):
        return self.table[row][col]


class ClimbStatus(Enum):
    START = 0
    CLIMBING = 0.5
    REACHED_ONCE = 1
    CLIMBING_AFTER = 1.5
    DONE_TWO_WAY = 2


class Node:
    def __init__(self, Cell, SearchTree):
        self.cell = Cell
        self.belongTo = SearchTree  # node belong to search tree
        self.pathCost = 0
        self.heuristic = 0
        self.f = 0
        self.keys = []  # obtained keys
        self.stairs = {}  # stairs that have been used
        self.children = []  # những con (successor) của node này
        self.parent = None  # cha của node này

        self.path = []

    def appendKey(self, value):
        if value not in self.keys:
            self.keys.append(value)

    def setParent(self, node):
        self.parent = node

    def getParent(self):
        return self.parent

    def setPathCost(self, value):
        self.pathCost = value

    def getPathCost(self):
        return self.pathCost

    def saveHeuristic(
        self, GoalCell
    ):  # calculate heuristic of the current cell to the goal (can be any goal)
        self.heuristic = self.cell.getFloorsHeuristic(GoalCell)
        return self.heuristic

    # f is total cost
    def saveF(self):
        self.f = self.pathCost + self.heuristic
        return self.f

    def getF(self):
        return self.f

    # a function that add neighbour cell to tempFrontier if they not in frontier and
    # not in visited and not in tempFrontier
    def expandFrontierCell(self, cell, BFSvisited, BFSfrontier, BFStempFrontier):
        floor_no = cell.floor_no
        # add N cell to tempFrontier
        if (
            cell.y > 0
            and not self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x).isWall()
            and self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x)
            not in BFSvisited
            and self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x)
            not in BFSfrontier
            and self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x)
            not in BFStempFrontier
        ):
            northCell = self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x)
            BFStempFrontier.append(northCell)
            cell.children.append(northCell)
            northCell.parrent = cell

        # add W cell to tempFrontier
        if (
            cell.x > 0
            and not self.belongTo.floors[floor_no].getCell(cell.y, cell.x - 1).isWall()
            and self.belongTo.floors[floor_no].getCell(cell.y, cell.x - 1)
            not in BFSvisited
            and self.belongTo.floors[floor_no].getCell(cell.y, cell.x - 1)
            not in BFSfrontier
            and self.belongTo.floors[floor_no].getCell(cell.y, cell.x - 1)
            not in BFStempFrontier
        ):
            westCell = self.belongTo.floors[floor_no].getCell(cell.y, cell.x - 1)
            BFStempFrontier.append(westCell)
            cell.children.append(westCell)
            westCell.parrent = cell

        # add S cell to tempFrontier
        if (
            cell.y < self.belongTo.floors[floor_no].rows - 1
            and not self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x).isWall()
            and self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x)
            not in BFSvisited
            and self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x)
            not in BFSfrontier
            and self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x)
            not in BFStempFrontier
        ):
            southCell = self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x)
            BFStempFrontier.append(southCell)
            cell.children.append(southCell)
            southCell.parrent = cell

        # add E cell to tempFrontier
        if (
            cell.x < self.belongTo.floors[floor_no].cols - 1
            and not self.belongTo.floors[floor_no].getCell(cell.y, cell.x + 1).isWall()
            and self.belongTo.floors[floor_no].getCell(cell.y, cell.x + 1)
            not in BFSvisited
            and self.belongTo.floors[floor_no].getCell(cell.y, cell.x + 1)
            not in BFSfrontier
            and self.belongTo.floors[floor_no].getCell(cell.y, cell.x + 1)
            not in BFStempFrontier
        ):
            eastCell = self.belongTo.floors[floor_no].getCell(cell.y, cell.x + 1)
            BFStempFrontier.append(eastCell)
            cell.children.append(eastCell)
            eastCell.parrent = cell

        # add NE cell to tempFrontier
        if (
            cell.y > 0
            and cell.x < self.belongTo.floors[floor_no].cols - 1
            and not self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x).isWall()
            and not self.belongTo.floors[floor_no].getCell(cell.y, cell.x + 1).isWall()
            and not self.belongTo.floors[floor_no]
            .getCell(cell.y - 1, cell.x + 1)
            .isWall()
            and self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x + 1)
            not in BFSvisited
            and self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x + 1)
            not in BFSfrontier
            and self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x + 1)
            not in BFStempFrontier
        ):
            neCell = self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x + 1)
            BFStempFrontier.append(neCell)
            cell.children.append(neCell)
            neCell.parrent = cell

        # Add NW cell to tempFrontier
        if (
            cell.y > 0
            and cell.x > 0
            and not self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x).isWall()
            and not self.belongTo.floors[floor_no].getCell(cell.y, cell.x - 1).isWall()
            and not self.belongTo.floors[floor_no]
            .getCell(cell.y - 1, cell.x - 1)
            .isWall()
            and self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x - 1)
            not in BFSvisited
            and self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x - 1)
            not in BFSfrontier
            and self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x - 1)
            not in BFStempFrontier
        ):
            nwCell = self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x - 1)
            BFStempFrontier.append(nwCell)
            cell.children.append(nwCell)
            nwCell.parrent = cell

        # Add SW cell to tempFrontier
        if (
            cell.y < self.belongTo.floors[floor_no].rows - 1
            and cell.x > 0
            and not self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x).isWall()
            and not self.belongTo.floors[floor_no].getCell(cell.y, cell.x - 1).isWall()
            and not self.belongTo.floors[floor_no]
            .getCell(cell.y + 1, cell.x - 1)
            .isWall()
            and self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x - 1)
            not in BFSvisited
            and self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x - 1)
            not in BFSfrontier
            and self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x - 1)
            not in BFStempFrontier
        ):
            swCell = self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x - 1)
            BFStempFrontier.append(swCell)
            cell.children.append(swCell)
            swCell.parrent = cell

        # Add SE cell to tempFrontier
        if (
            cell.y < self.belongTo.floors[floor_no].rows - 1
            and cell.x < self.belongTo.floors[floor_no].cols - 1
            and not self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x).isWall()
            and not self.belongTo.floors[floor_no].getCell(cell.y, cell.x + 1).isWall()
            and not self.belongTo.floors[floor_no]
            .getCell(cell.y + 1, cell.x + 1)
            .isWall()
            and self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x + 1)
            not in BFSvisited
            and self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x + 1)
            not in BFSfrontier
            and self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x + 1)
            not in BFStempFrontier
        ):
            seCell = self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x + 1)
            BFStempFrontier.append(seCell)
            cell.children.append(seCell)
            seCell.parrent = cell

    def expand(self, goal):
        BFSfrontier = []
        BFStempFrontier = []
        BFSvisited = []

        BFSfrontier.append(self.cell)
        steps = -1

        while BFSfrontier:
            steps += 1

            for cell in BFSfrontier:
                if cell is None:
                    continue

                # analyze cell
                cell_tag = cell.getSpecialValue()  # special value của cell

                # normal cell
                if cell_tag == "" or cell_tag[0] == "A":
                    # if self.cell.floor_no != cell.floor_no:
                    #     has_stairs = True
                    #     change = 1 if self.cell.floor_no < cell.floor_no else -1
                    #     i = self.cell.floor_no
                    #     while i != cell.floor_no:
                    #         if self.stairs.get((i, i + change)) is None:
                    #             BFSvisited.append(cell)
                    #             has_stairs = False
                    #             break
                    #         i = i + change
                    #
                    #     if has_stairs:
                    #         continue

                    self.expandFrontierCell(
                        cell, BFSvisited, BFSfrontier, BFStempFrontier
                    )

                # key
                elif cell_tag[0] == "K":
                    #
                    # if self.cell.floor_no != cell.floor_no:
                    #     has_stairs = True
                    #     change = 1 if self.cell.floor_no < cell.floor_no else -1
                    #     i = self.cell.floor_no
                    #     while i != cell.floor_no:
                    #         if self.stairs.get((i, i + change)) is None:
                    #             BFSvisited.append(cell)
                    #             has_stairs = False
                    #             break
                    #         i = i + change
                    #
                    #     if has_stairs:
                    #         continue

                    # first expand (not worry about duplicates)
                    if len(BFSfrontier) == 1 and BFSfrontier[0] == self.cell:
                        self.expandFrontierCell(
                            cell, BFSvisited, BFSfrontier, BFStempFrontier
                        )
                    else:
                        # check duplicates
                        tempNode = self
                        addNode = True
                        while tempNode:
                            if (
                                cell_tag in tempNode.keys
                            ):  # if current key is used before
                                addNode = False  # found duplicate
                                break
                            tempNode = tempNode.parent

                        # key not used before
                        if addNode:
                            # create new node
                            newNode = Node(cell, self.belongTo)
                            newNode.setPathCost(self.pathCost + steps)
                            newNode.saveHeuristic(goal)
                            newNode.saveF()

                            # append new node to tree
                            if self.cell != cell:
                              self.children.append(newNode)
                              newNode.parent = self

                            # inherit collected keys so far
                            for eachKey in self.keys:
                                newNode.appendKey(
                                    eachKey
                                )  # add previously collected keys
                            newNode.appendKey(cell_tag)  # add current key

                            # # add to path
                            tempCell = cell
                            while tempCell:
                                newNode.path.append(tempCell)
                                tempCell = tempCell.parrent

                            # expand this cell
                            self.expandFrontierCell(
                                cell, BFSvisited, BFSfrontier, BFStempFrontier
                            )

                # door
                elif cell_tag[0] == "D" and cell_tag[1] != "O":
                    # if self.cell.floor_no != cell.floor_no:
                    #     has_stairs = True
                    #     change = 1 if self.cell.floor_no < cell.floor_no else -1
                    #     i = self.cell.floor_no
                    #     while i != cell.floor_no:
                    #         if self.stairs.get((i, i + change)) is None:
                    #             BFSvisited.append(cell)
                    #             has_stairs = False
                    #             break
                    #         i = i + change
                    #
                    #     if has_stairs:
                    #         continue

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
                            newNode.saveHeuristic(goal)
                            newNode.saveF()

                            # inherit key
                            for eachKey in self.keys:
                                newNode.appendKey(eachKey)

                            # append new node to tree
                            if self.cell != cell:
                                self.children.append(newNode)
                                newNode.parent = self

                            # # add to path
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

                elif cell_tag[0] == "T":
                    # if self.cell.floor_no != cell.floor_no:
                    #     has_stairs = True
                    #     change = 1 if self.cell.floor_no < cell.floor_no else -1
                    #     i = self.cell.floor_no
                    #     while i != cell.floor_no:
                    #         if self.stairs.get((i, i + change)) is None:
                    #             BFSvisited.append(cell)
                    #             has_stairs = False
                    #             break
                    #         i = i + change
                    #
                    #     if has_stairs:
                    #         continue

                    # create new node
                    newNode = Node(cell, self.belongTo)
                    newNode.setPathCost(self.pathCost + steps)
                    newNode.saveHeuristic(goal)
                    newNode.saveF()

                    # append new node to tree
                    if self.cell != cell:
                        self.children.append(newNode)
                        newNode.parent = self

                    # # add to path
                    tempCell = cell
                    while tempCell:
                        newNode.path.append(tempCell)
                        tempCell = tempCell.parrent

                # stairs
                elif cell_tag == "UP" or cell_tag == "DO":
                    # if self.cell.floor_no != cell.floor_no:
                    #     has_stairs = True
                    #     change = 1 if self.cell.floor_no < cell.floor_no else -1
                    #     i = self.cell.floor_no
                    #     while i != cell.floor_no:
                    #         if self.stairs.get((i, i + change)) is None:
                    #             BFSvisited.append(cell)
                    #             has_stairs = False
                    #             break
                    #         i = i + change
                    #
                    #     if has_stairs:
                    #         continue

                    if len(BFSfrontier) > 1 and (
                            (
                                    BFSfrontier[-1].getSpecialValue() == "UP"
                                    and self.cell.getSpecialValue() == "DO"
                            )
                            or (
                                    BFSfrontier[-1].getSpecialValue() == "DO"
                                    and self.cell.getSpecialValue() == "UP"
                            )
                    ):
                        continue

                    newNode = Node(
                        cell, self.belongTo
                    )  # tạo node mới từ cell (đang duyệt BFSFrontier)
                    newNode.setPathCost(self.pathCost + steps)
                    newNode.saveHeuristic(goal)
                    newNode.saveF()

                    # inherit collected stairs so far
                    newNode.stairs.update(self.stairs)
                    next_floor = (
                        cell.floor_no + 1 if cell_tag == "UP" else cell.floor_no - 1
                    )
                    if newNode.stairs.get((cell.floor_no, next_floor)) is None:
                        newNode.stairs[(cell.floor_no, next_floor)] = []
                    newNode.stairs[(cell.floor_no, next_floor)].append(cell)

                    if self.cell != cell:
                      newNode.parent = self

                    if cell_tag == "UP":
                        copyCell = self.belongTo.floors[cell.floor_no + 1].getCell(
                            cell.y, cell.x
                        )
                    else:
                        copyCell = self.belongTo.floors[cell.floor_no - 1].getCell(
                            cell.y, cell.x
                        )
                    # Expand the neighbors of the updated cell
                    self.expandFrontierCell(
                        copyCell, BFSvisited, BFSfrontier, BFStempFrontier
                    )

                    BFSvisited.append(copyCell)

                BFSvisited.append(cell)

            pass

            # update the frontier
            BFSfrontier = BFStempFrontier
            BFStempFrontier = []

        for floor in self.belongTo.floors:
            self.belongTo.floors[floor].clearAllRelation()


class SearchTree:
    def __init__(self):
        self.floors = {}
        self.agent = None
        self.currentNode = None
        self.currentNode_subgoal = None
        self.frontier = []
        self.frontier_subgoal = []
        self.visited = []
        self.visited_subgoal = []
        self.root = None
        self.root_subgoal = None

        self.keys = {}

        self.goals = []

    def getInputFile(self, filePath):
        with open(filePath, "r") as file:
            lines = file.readlines()

        rows, cols = map(int, lines[0].strip().split(","))

        lines.pop(0)  # delete first line

        current_floor = 0
        i = 0

        for line in lines:
            if line.__contains__("floor"):
                i = -1  # for row index
                current_floor += 1
                self.floors[current_floor] = Floor(rows, cols, current_floor)
                continue

            row_values = list(map(str, line.strip().split(",")))

            i += 1  # increase row index

            for j in range(cols):
                cell_value = row_values[j]

                # Check if the cell value has the format "Ki", "Di"
                if re.match(r"[KD]\d+", cell_value):
                    self.floors[current_floor].appendToCell(i, j, "0")

                    # Extract the character and integer parts from the cell value
                    char_part, num_part = re.match(r"([KD])(\d+)", cell_value).groups()

                    if char_part == "K":
                        self.keys[int(num_part)] = self.floors[current_floor].getCell(
                            i, j
                        )

                # if goalCell show up
                if re.match(r"[T]\d+", cell_value):
                    self.floors[current_floor].appendToCell(i, j, "0")

                    # Extract the character and integer parts from the cell value
                    char_part, num_part = re.match(
                        r"([AKTD])(\d+)", cell_value
                    ).groups()

                    self.goals.append(self.floors[current_floor].getCell(i, j))

                # if startCell show up
                if re.match(r"[A]\d+", cell_value):
                    self.floors[current_floor].appendToCell(i, j, "0")

                    # Extract the character and integer parts from the cell value
                    char_part, num_part = re.match(
                        r"([AKTD])(\d+)", cell_value
                    ).groups()

                    current = Node(self.floors[current_floor].getCell(i, j), self)
                    self.frontier = [current]
                    self.currentNode = current
                    self.visited = []
                    self.root = current

                    self.agent = self.floors[current_floor].getCell(i, j)

                if cell_value == "UP" or cell_value == "DO":  # for stairs
                    self.floors[current_floor].appendToCell(i, j, "0")

                # Regardless of the condition, add the original cell value to the cell
                self.floors[current_floor].appendToCell(i, j, cell_value)

    class MainStatus(Enum):
        REACHED = 1
        UNSOLVABLE = -1
        IN_PROGRESS = 0

    def Greedy_BFS(self):
        self.root.saveHeuristic(self.goals[0])  # save heuristic for root

        while self.frontier:
            # self.visualize()
            self.frontier.sort(key=lambda x: x.heuristic)
            self.currentNode = self.frontier.pop(0)

            # if path found
            if self.currentNode.cell == self.goals[0]:
                tempNode = self.currentNode
                while tempNode:
                    print(
                        f"{tempNode.cell.getSpecialValue()} Floor: {tempNode.cell.floor_no}"
                    )
                    tempNode = tempNode.parent
                self.heatMap()
                return  # self.MainStatus.REACHED

            self.currentNode.expand(self.goals[0])
            for eachChild in set(self.currentNode.children):
                self.frontier.append(eachChild)

        print("No solution found")
        # return self.MainStatus.UNSOLVABLE

    def BFS(self):
        # self.root[1].saveHeuristic(self.goals[1])
        # self.root[1].saveF()
        while self.frontier:
            # self.visualize()
            # self.frontier[1].sort(key=lambda x: x.getF())
            self.currentNode = self.frontier.pop(0)
            print(f"{self.currentNode.cell.getSpecialValue()} Floor: {self.currentNode.cell.floor_no}")

            # if path found
            if self.currentNode.cell == self.goals[0]:

                tempNode = self.currentNode
                while tempNode:
                    print(
                        f"{tempNode.cell.getSpecialValue()} Floor: {tempNode.cell.floor_no}"
                    )
                    tempNode = tempNode.parent
                self.heatMap()
                return

            self.currentNode.expand(self.goals[0])
            for eachChild in self.currentNode.children:
                    self.frontier.append(eachChild)

        print("No solution found")

    def visualize(self, indexOfFloor):
        # Create the main window
        root = tk.Tk()
        root.title("Search Tree Visualization")

        # Create a canvas to draw on
        canvas = tk.Canvas(
            root,
            width=self.floors[indexOfFloor].cols * 50,
            height=self.floors[indexOfFloor].rows * 50,
        )
        canvas.pack()

        # basic map
        for i in range(self.floors[indexOfFloor].rows):
            for j in range(self.floors[indexOfFloor].cols):
                x0, y0 = j * 20, i * 20
                x1, y1 = (j + 1) * 20, (i + 1) * 20

                # Set color for cells with value "-1" to black
                if self.floors[indexOfFloor].table[i][j].checkValue("-1"):
                    canvas.create_rectangle(x0, y0, x1, y1, fill="black")
                else:
                    canvas.create_rectangle(x0, y0, x1, y1, fill="white")
                    # print special value
                    specialValue = (
                        self.floors[indexOfFloor].table[i][j].getSpecialValue()
                    )
                    canvas.create_text(
                        x0 + 10, y0 + 10, text=specialValue, fill="black"
                    )

        # draw path
        tempNode = self.currentNode
        while tempNode:
            # Draw rectangles for each cell
            for i in range(self.floors[indexOfFloor].rows):
                for j in range(self.floors[indexOfFloor].cols):
                    x0, y0 = j * 20, i * 20
                    x1, y1 = (j + 1) * 20, (i + 1) * 20
                    # TODO need to add path attribute to Node class, path is array of Cell that leads from parrent node to this node
                    # Set color for cells in the path to green
                    # if self.floors[indexOfFloor].table[i][j] in tempNode.path:
                    #     canvas.create_rectangle(x0, y0, x1, y1, fill="green")
                    # Set color for cells pointed by tempNode to red
                    if (
                        tempNode.cell
                        and self.floors[indexOfFloor].table[i][j] == tempNode.cell
                    ):
                        canvas.create_rectangle(x0, y0, x1, y1, fill="red")
                        specialValue = (
                            self.floors[indexOfFloor].table[i][j].getSpecialValue()
                        )
                        canvas.create_text(
                            x0 + 10, y0 + 10, text=specialValue, fill="black"
                        )

            # Move to the parent node
            tempNode = tempNode.parent
        # Run the GUI
        root.mainloop()

    def heatMap(self):
        root = tk.Tk()
        self.checkRoot = True
        root.title("Search Tree Visualization - All Floors")

        canvas_width = max(self.floors[floor].cols for floor in self.floors) * 40
        canvas_height = sum(self.floors[floor].rows for floor in self.floors) * 35 * len(self.floors)
        canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        canvas.pack()

        y_offset = 0  # Offset for drawing floors vertically

        for floor_no in self.floors:
            floor = self.floors[floor_no]

            # Draw each row of the floor
            for i in range(floor.rows):
                for j in range(floor.cols):
                    x0, y0 = j * 20, i * 35 + y_offset
                    x1, y1 = (j + 1) * 20, (i + 1) * 35 + y_offset

                    if floor.table[i][j].checkValue("-1"):
                        canvas.create_rectangle(x0, y0, x1, y1, fill="black", outline="black")
                    else:
                        canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
                        specialValue = floor.table[i][j].getSpecialValue()
                        canvas.create_text(
                            x0 + 10, y0 + 10, text=specialValue, fill="black"
                        )

            # Draw path for the current floor
            tempNode = self.currentNode
            generalPath = []
            while tempNode:
                for eachCell in tempNode.path:
                    generalPath.append(eachCell)
                tempNode = tempNode.parent

            for eachCell in generalPath:
                for i in range(floor.rows):
                    for j in range(floor.cols):
                        x0, y0 = j * 20, i * 35 + y_offset
                        x1, y1 = (j + 1) * 20, (i + 1) * 35 + y_offset

                        if floor.table[i][j] in generalPath:
                            if Counter(generalPath)[floor.table[i][j]] == 1:
                                canvas.create_rectangle(
                                    x0, y0, x1, y1, fill="#ff8888", outline="black"
                                )
                            elif Counter(generalPath)[floor.table[i][j]] == 2:
                                canvas.create_rectangle(
                                    x0, y0, x1, y1, fill="#ff4b4b", outline="black"
                                )
                            elif Counter(generalPath)[floor.table[i][j]] == 3:
                                canvas.create_rectangle(
                                    x0, y0, x1, y1, fill="#ff0000", outline="black"
                                )
                            elif Counter(generalPath)[floor.table[i][j]] == 4:
                                canvas.create_rectangle(
                                    x0, y0, x1, y1, fill="#cb0000", outline="black"
                                )
                        if floor.table[i][j].getSpecialValue() != "":
                            canvas.create_rectangle(x0, y0, x1, y1, fill="#2ad500", outline="black")
                            specialValue = floor.table[i][j].getSpecialValue()
                            canvas.create_text(
                                x0 + 10, y0 + 10, text=specialValue, fill="black"
                            )

            y_offset += floor.rows * 35 + 20  # Adjust y_offset for next floor

        root.mainloop()


searchTree2 = SearchTree()
searchTree2.getInputFile("input//input3-level3.txt")
searchTree2.Greedy_BFS()
pass
