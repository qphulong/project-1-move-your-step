import heapq
import random
import re
import time
import tkinter as tk
from collections import Counter
from enum import Enum
import copy
from algorithm import export_heatmap
import math


class Cell:
    def __init__(self, y, x, floor_no):
        self.y = y
        self.x = x
        self.floor_no = floor_no
        self.values = []
        self.belongTo = None
        self.children = []
        self.parrent = None
        self.waitingCell = False

    def __eq__(self, other):
        return (
                self.y == other.y and self.x == other.x and self.floor_no == other.floor_no
        )

    def __hash__(self):
        return hash((self.y, self.x, self.floor_no))

    def __str__(self):
        return f"({self.y}, {self.x} Floor {self.floor_no} Special value {self.getSpecialValue()})"

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

    def getEuclidean(self, Cell):
        return math.sqrt((self.x - Cell.x) ** 2 + (self.y - Cell.y) ** 2)

    def getFloorsHeuristic(self, GoalCell):
        return self.getPhanTrungDucDistance(GoalCell) + abs(self.floor_no - GoalCell.floor_no)

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

    def neighbors(self, agent_no, searchTree, path):
        children = []
        floor_no = self.floor_no

        def is_valid_position(y, x):
            return 0 <= y < searchTree.floors[floor_no].rows and 0 <= x < searchTree.floors[floor_no].cols

        def add_cell_if_valid(y, x):
            if is_valid_position(y, x):
                cell = searchTree.floors[floor_no].getCell(y, x)
                special = cell.getSpecialValue() if len(cell.getSpecialValue()) > 0 else ""
                if not cell.isWall() and special != "DO" and special != "UP" and searchTree.isOtherAgent(cell,agent_no) is None:
                    if len(special)>0 and special[0] == "D":
                        if str("K" + str(special[1])) not in searchTree.currentNode[agent_no].keys and (key_cell for cell in path if cell.getSpecialValue() == str("K" + str(special[1]))) is None:
                            return
                    children.append(cell)
                    cell.parrent = self

        # Check neighboring cells
        add_cell_if_valid(self.y - 1, self.x)  # North
        add_cell_if_valid(self.y, self.x - 1)  # West
        add_cell_if_valid(self.y + 1, self.x)  # South
        add_cell_if_valid(self.y, self.x + 1)  # East

        # Check diagonal cells considering neighboring walls
        if self.y > 0 and self.x < searchTree.floors[floor_no].cols - 1:  # NE
            if not searchTree.floors[floor_no].getCell(self.y - 1, self.x).isWall() and \
                    not searchTree.floors[floor_no].getCell(self.y, self.x + 1).isWall():
                add_cell_if_valid(self.y - 1, self.x + 1)

        if self.y > 0 and self.x > 0:  # NW
            if not searchTree.floors[floor_no].getCell(self.y - 1, self.x).isWall() and \
                    not searchTree.floors[floor_no].getCell(self.y, self.x - 1).isWall():
                add_cell_if_valid(self.y - 1, self.x - 1)

        if self.y < searchTree.floors[floor_no].rows - 1 and self.x > 0:  # SW
            if not searchTree.floors[floor_no].getCell(self.y + 1, self.x).isWall() and \
                    not searchTree.floors[floor_no].getCell(self.y, self.x - 1).isWall():
                add_cell_if_valid(self.y + 1, self.x - 1)

        if self.y < searchTree.floors[floor_no].rows - 1 and self.x < searchTree.floors[floor_no].cols - 1:  # SE
            if not searchTree.floors[floor_no].getCell(self.y + 1, self.x).isWall() and \
                    not searchTree.floors[floor_no].getCell(self.y, self.x + 1).isWall():
                add_cell_if_valid(self.y + 1, self.x + 1)

        return children


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

        self.waitingNode = False  # node indicating that this is a place where the agent is waiting for another agent

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
    def expandFrontierCell(self, cell, BFSvisited, BFSfrontier, BFStempFrontier, prevCell=None):
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
            if prevCell is not None:
                prevCell.children.append(cell)
                cell.parrent = prevCell

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
            if prevCell is not None:
                prevCell.children.append(cell)
                cell.parrent = prevCell

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
            if prevCell is not None:
                prevCell.children.append(cell)
                cell.parrent = prevCell

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
            if prevCell is not None:
                prevCell.children.append(cell)
                cell.parrent = prevCell

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
            if prevCell is not None:
                prevCell.children.append(cell)
                cell.parrent = prevCell

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
            if prevCell is not None:
                prevCell.children.append(cell)
                cell.parrent = prevCell

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
            if prevCell is not None:
                prevCell.children.append(cell)
                cell.parrent = prevCell

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
            if prevCell is not None:
                prevCell.children.append(cell)
                cell.parrent = prevCell

    def expand(self, goal, agent_no):
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
                if cell_tag == "" or cell_tag[0] == "A" or (cell_tag[0] == "T" and cell_tag[1] != str(agent_no)):
                    self.expandFrontierCell(
                        cell, BFSvisited, BFSfrontier, BFStempFrontier
                    )

                # key
                elif cell_tag[0] == "K":

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

                elif cell_tag[0] == "T" and cell_tag[1] == str(agent_no):
                    # create new node
                    newNode = Node(cell, self.belongTo)
                    newNode.setPathCost(self.pathCost + steps)
                    newNode.saveHeuristic(goal)
                    newNode.saveF()

                    # append new node to tree
                    if self.cell != cell:
                        self.children.append(newNode)
                        newNode.parent = self

                    # add to path
                    tempCell = cell
                    while tempCell:
                        newNode.path.append(tempCell)
                        tempCell = tempCell.parrent

                # stairs
                elif cell_tag == "UP" or cell_tag == "DO":
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

                    newNode.path.append(copyCell)
                    tempCell = cell

                    while tempCell:
                        newNode.path.append(tempCell)
                        tempCell = tempCell.parrent

                    # Expand the neighbors of the updated cell
                    self.expandFrontierCell(
                        copyCell, BFSvisited, BFSfrontier, BFStempFrontier, cell
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
        self.agents = {}
        self.goals = {}
        self.currentNode = {}  # save for all agents
        self.path_iteration = {}  # save current position in path iteration for all agents
        self.frontier = {}
        self.visited = {}
        self.root = {}
        self.keys = {}
        self.upcoming = {}  # save next cells of each agent

        self.number_agents = 0  # số agent

        self.tkRoot = tk.Tk()
        self.canvas = tk.Canvas(self.tkRoot, width=0, height=0)
        self.canvas.pack()
        self.score = 0
        self.checkRoot = False

    def getCheckRoot(self):
        return self.checkRoot

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

                    agent_no = int(cell_value[1])
                    if self.goals.get(agent_no) is None:
                        self.goals[agent_no] = []
                    self.goals[agent_no].append(self.floors[current_floor].getCell(i, j))

                # if startCell show up
                if re.match(r"[A]\d+", cell_value):
                    self.floors[current_floor].appendToCell(i, j, "0")

                    # Extract the character and integer parts from the cell value
                    char_part, num_part = re.match(
                        r"([AKTD])(\d+)", cell_value
                    ).groups()

                    current = Node(self.floors[current_floor].getCell(i, j), self)
                    agent_no = int(cell_value[1])
                    self.frontier[agent_no] = [current]
                    self.currentNode[agent_no] = current
                    self.visited[agent_no] = []
                    self.root[agent_no] = current

                    self.agents[agent_no] = self.floors[current_floor].getCell(i, j)

                    self.number_agents += 1

                if cell_value == "UP" or cell_value == "DO":  # for stairs
                    self.floors[current_floor].appendToCell(i, j, "0")

                # Regardless of the condition, add the original cell value to the cell
                self.floors[current_floor].appendToCell(i, j, cell_value)

        canvas_width = max(self.floors[floor].cols for floor in self.floors) * 40
        canvas_height = sum(self.floors[floor].rows for floor in self.floors) * 35 * len(self.floors)
        self.canvas = tk.Canvas(self.tkRoot, width=canvas_width, height=canvas_height)

    class MainStatus(Enum):
        REACHED = 1
        UNSOLVABLE = -1
        IN_PROGRESS = 0

    def isOtherAgent(self, cell, agent_no):
        for agent in self.agents:
            if (
                    agent != agent_no
                    and cell.y == self.agents[agent].y
                    and cell.x == self.agents[agent].x
                    and cell.floor_no == self.agents[agent].floor_no
            ):
                return agent
        return None

    def Greedy_BFS(self):
        self.root[1].saveHeuristic(self.goals[1][-1])  # save heuristic for root

        while self.frontier[1]:
            # self.visualize()
            self.frontier[1].sort(key=lambda x: x.heuristic)
            self.currentNode[1] = self.frontier[1].pop(0)

            # if path found
            if self.currentNode[1].cell == self.goals[1][-1]:
                pathToGoal = []
                tempNode = self.currentNode[1]
                while tempNode:
                    print(
                        f"{tempNode.cell.getSpecialValue()} Floor: {tempNode.cell.floor_no}"
                    )
                    pathToGoal.append(tempNode)
                    tempNode = tempNode.parent
                pathToGoal.reverse()
                return (self.MainStatus.REACHED, pathToGoal)

            self.currentNode[1].expand(self.goals[1][-1], 1)
            for eachChild in set(self.currentNode[1].children):
                self.frontier[1].append(eachChild)

        print("No solution found")
        return (self.MainStatus.UNSOLVABLE, None)

    def BFS(self):
        # self.root[1].saveHeuristic(self.goals[1])
        # self.root[1].saveF()
        while self.frontier[1]:
            # self.visualize()
            # self.frontier[1].sort(key=lambda x: x.getF())

            self.currentNode[1] = self.frontier[1].pop(0)

            # self.agents[1] = self.currentNode[1].cell

            # if path found
            if self.currentNode[1].cell == self.goals[1][-1]:
                pathToGoal = []
                tempNode = self.currentNode[1]
                while tempNode:
                    print(
                        f"{tempNode.cell.getSpecialValue()} Floor: {tempNode.cell.floor_no}"
                    )
                    pathToGoal.append(tempNode)
                    tempNode = tempNode.parent
                pathToGoal.reverse()
                return (self.MainStatus.REACHED, pathToGoal)

            self.currentNode[1].expand(self.goals[1][-1], 1)

            for eachChild in self.currentNode[1].children:
                self.frontier[1].append(eachChild)

        return (self.MainStatus.UNSOLVABLE, None)

    def BFS_OtherAgents(self, agent_no):

        # self.root[agent_no].saveF()
        if self.frontier[agent_no]:

            self.frontier[agent_no].sort(key=lambda x: x.heuristic)

            self.currentNode[agent_no] = self.frontier[agent_no].pop(0)

            # if path found
            if self.currentNode[agent_no].cell == self.goals[agent_no][-1]:
                return self.MainStatus.REACHED

            self.currentNode[agent_no].expand(self.goals[agent_no][-1], agent_no)

            for eachChild in self.currentNode[agent_no].children:
                self.frontier[agent_no].append(eachChild)
            return self.MainStatus.IN_PROGRESS

        return self.MainStatus.UNSOLVABLE

    def agent_turn_based_movement(self, path_to_goal):
        self.initialHeatMap()

        current_agent = 1  # Initialize the index to track the current agent

        current_node = -1

        visited = {}

        prev = None

        while True:
            prev = self.agents[current_agent]

            if current_agent == 1:  # A1

                if self.path_iteration.get(1) is None or self.path_iteration[1] < 0:
                    current_node += 1  # node thứ mấy trong path to goal

                    self.path_iteration[1] = len(path_to_goal[current_node].path) - 1  # duyệt từng path

                if self.path_iteration[1] >= 0:
                    current_cell = path_to_goal[current_node].path[self.path_iteration[1]]

                    if self.isOtherAgent(current_cell, 1) is None:  # nếu không đụng agent khác

                        self.agents[1] = current_cell

                        self.path_iteration[1] -= 1

                        if current_cell == self.goals[1][-1]:
                            print("Reached goal")
                            if visited.get(self.agents[current_agent]) is None:
                                visited[self.agents[current_agent]] = 0
                            visited[self.agents[current_agent]] += 1

                            self.heatMapUpdate(current_agent, self.agents[current_agent], prev, visited)
                            export_heatmap(self.tkRoot)
                            self.tkRoot.mainloop()
                            break

                    else:  # đụng agent khác

                        prevCell = self.agents[1]
                        prevCell.waitingCell = True

                        neighbors = self.agents[1].neighbors(1, self, path_to_goal[current_node].path)

                        if len(neighbors) > 0:
                            tempCell = None
                            while tempCell is None or self.isOtherAgent(tempCell, 1) is not None:
                                tempCell = neighbors[random.randint(0, len(neighbors) - 1)]

                            path_to_goal[current_node].path.insert(self.path_iteration[1] + 1,
                                                                   tempCell)  # thêm cell tương tự để chỉ là đang đợi

                            path_to_goal[current_node].path.insert(self.path_iteration[1] + 1,
                                                                   prevCell)  # thêm cell tương tự để chỉ là đang đợi
                            self.agents[1] = tempCell
                            self.path_iteration[1] += 1
                        else:

                            path_to_goal[current_node].path.insert(self.path_iteration[1] + 1,
                                                                   prevCell)  # thêm cell tương tự để chỉ là đang đợi


            else:  # other agents
                # mai thử cho chạy hết 3 thằng rồi mới đi tìm path
                if self.path_iteration.get(current_agent) is None or self.path_iteration[
                    current_agent] < 0:
                    res = self.BFS_OtherAgents(current_agent)

                    if res == self.MainStatus.UNSOLVABLE:  # agent khác không đến được goal
                        old_goal = self.goals[current_agent][-1]
                        self.floors[old_goal.floor_no].table[old_goal.y][old_goal.x].removeValue(
                            "T" + str(current_agent))

                        new_goal = self.generate_goal(current_agent)
                        self.floors[new_goal.floor_no].table[new_goal.y][new_goal.x].appendValue(
                            "T" + str(current_agent))

                        self.frontier[current_agent].clear()

                        i = self.currentNode[current_agent].cell.y
                        j = self.currentNode[current_agent].cell.x
                        floor_no = self.currentNode[current_agent].cell.floor_no

                        self.floors[floor_no].table[i][j].appendValue("A" + str(current_agent))
                        self.agents[current_agent] = self.floors[floor_no].getCell(i, j)
                        nextStartNode = Node(self.floors[floor_no].getCell(i, j), self)
                        nextStartNode.saveHeuristic(new_goal)

                        nextStartNode.saveHeuristic(new_goal)
                        self.frontier[current_agent].append(nextStartNode)

                        self.goals[current_agent].append(new_goal)

                    self.path_iteration[current_agent] = len(
                        self.currentNode[current_agent].path) - 1  # duyệt từng path

                if self.path_iteration[current_agent] >= 0:
                    current_cell = self.currentNode[current_agent].path[self.path_iteration[current_agent]]

                    if self.isOtherAgent(current_cell, current_agent) is None:  # nếu không đụng agent khác
                        self.agents[current_agent] = current_cell

                        self.path_iteration[current_agent] -= 1

                        if current_cell == self.goals[current_agent][-1]:  # đụng goal hiện tại thì generate goal mới
                            old_goal = self.goals[current_agent][-1]
                            self.floors[old_goal.floor_no].table[old_goal.y][old_goal.x].removeValue(
                                "T" + str(current_agent))

                            new_goal = self.generate_goal(current_agent)
                            self.floors[new_goal.floor_no].table[new_goal.y][new_goal.x].appendValue(
                                "T" + str(current_agent))

                            self.frontier[current_agent].clear()

                            i = self.currentNode[current_agent].cell.y
                            j = self.currentNode[current_agent].cell.x
                            floor_no = self.currentNode[current_agent].cell.floor_no

                            self.floors[floor_no].table[i][j].appendValue("A" + str(current_agent))
                            self.agents[current_agent] = self.floors[floor_no].getCell(i, j)
                            nextStartNode = Node(self.floors[floor_no].getCell(i, j), self)
                            nextStartNode.saveHeuristic(new_goal)

                            self.frontier[current_agent].append(nextStartNode)

                            self.goals[current_agent].append(new_goal)

                            self.path_iteration[current_agent] = None

                    else:  # đụng agent khác
                        neighbors = self.agents[current_agent].neighbors(current_agent, self, self.currentNode[current_agent].path)

                        prevCell = self.agents[current_agent]
                        prevCell.waitingCell = True

                        if len(neighbors) > 0:
                            tempCell = None
                            while tempCell is None or self.isOtherAgent(tempCell, 1) is not None:
                                tempCell = neighbors[random.randint(0, len(neighbors) - 1)]

                            tempCell.waitingCell = True

                            self.currentNode[current_agent].path.insert(self.path_iteration[current_agent] + 1,
                                                                        tempCell)  # thêm cell tương tự để chỉ là đang đợi

                            self.currentNode[current_agent].path.insert(self.path_iteration[current_agent] + 1,
                                                                        prevCell)  # thêm cell tương tự để chỉ là đang đợi

                            self.agents[current_agent] = tempCell
                            self.path_iteration[current_agent] += 1
                        else:
                            self.currentNode[current_agent].path.insert(self.path_iteration[current_agent] + 1,
                                                                        prevCell)  # thêm cell tương tự để chỉ là đang đợi

            if visited.get(self.agents[current_agent]) is None:
                visited[self.agents[current_agent]] = 0
            visited[self.agents[current_agent]] += 1

            self.heatMapUpdate(current_agent, self.agents[current_agent], prev, visited)

            current_agent += 1

            if current_agent > self.number_agents:
                current_agent = 1

    def solve(self):
        res = self.BFS()
        if res[0] == self.MainStatus.REACHED:
            print("Found a way to reach the goal")
            path_to_goal = res[1]

            for agent in range(2, self.number_agents):
                self.root[agent].saveHeuristic(self.goals[agent][-1])
            self.agent_turn_based_movement(path_to_goal)
        else:
            print("No solution")

    def generate_goal(self, current_agent):
        random_goal = None
        while True:
            current_floor = self.goals[current_agent][-1].floor_no
            random_y = random.randint(0, self.floors[current_floor].rows - 1)
            random_x = random.randint(0, self.floors[current_floor].cols - 1)
            random_goal = self.floors[current_floor].getCell(random_y, random_x)
            if not random_goal.isWall() and random_goal.getSpecialValue() == "" and self.isOtherAgent(random_goal,
                                                                                                     current_agent) is None:
                break

        y_offset = (self.floors[random_goal.floor_no].rows * 35 + 20) * (random_goal.floor_no - 1)
        x0, y0 = random_goal.x * 20, random_goal.y * 35 + y_offset
        x1, y1 = (random_goal.x + 1) * 20, (random_goal.y + 1) * 35 + y_offset

        self.canvas.delete(f"T{current_agent}")
        self.canvas.delete(f"T{current_agent}text")
        self.tkRoot.update()

        self.canvas.create_rectangle(x0, y0, x1, y1, fill="#152b52", outline="black", tags=f"T{current_agent}")
        self.canvas.create_text(
            x0 + 10, y0 + 10, text=f"T{current_agent}", tags=f"T{current_agent}text"
        )

        self.tkRoot.update()

        return random_goal

    def competing_cell(self, agent_1, agent_2):
        return agent_1 < agent_2

    def initialHeatMap(self):
        self.checkRoot = True
        # self.score+=1
        score = tk.Label(self.tkRoot, font=('Arial', 15), text='Score: ' + str(self.score), fg='Black')
        score.place(x=self.floors[1].cols * 21, y=100)
        self.canvas.pack()

        y_offset = 0  # Offset for drawing floors vertically

        for floor_no in self.floors:
            floor = self.floors[floor_no]

            # Draw each row of the floor
            for i in range(floor.rows):
                for j in range(floor.cols):
                    x0, y0 = j * 20, i * 35 + y_offset
                    x1, y1 = (j + 1) * 20, (i + 1) * 35 + y_offset

                    if floor.table[i][j].checkValue("-1"):
                        self.canvas.create_rectangle(x0, y0, x1, y1, fill="black", outline="black")
                    else:
                        self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")

                    special = floor.table[i][j].getSpecialValue()
                    if special != "":
                        if special == "UP" or special == "DO":
                            self.canvas.create_rectangle(x0, y0, x1, y1,
                                                         fill="#34cceb" if special == "UP" else "#f5aa42",
                                                         outline="black")
                            self.canvas.create_text(
                                x0 + 10, y0 + 10, text="↑" if special == "UP" else "↓", fill="black"
                            )
                            continue

                        if special == "T1":
                            self.canvas.create_rectangle(x0, y0, x1, y1, fill="#ebb121", outline="black")
                            self.canvas.create_text(
                                x0 + 10, y0 + 10, text="T1"
                            )
                            continue

                        if special[0] == "T":
                            self.canvas.create_rectangle(x0, y0, x1, y1, fill="#152b52", outline="black", tags=special)
                            self.canvas.create_text(
                                x0 + 10, y0 + 10, text=special, tags=special + "text"
                            )
                            continue

                        self.canvas.create_rectangle(x0, y0, x1, y1, fill="#78977F", outline="black")
                        self.canvas.create_text(
                            x0 + 10, y0 + 10, text=special, fill="black"
                        )

            y_offset += floor.rows * 35 + 20  # Adjust y_offset for next floor

    def heatMapUpdate(self, current_agent, cell, prev, visited):
        print(f"A{current_agent}: {cell}")
        if current_agent == 1 and prev != cell: self.score += 1
        score = tk.Label(self.tkRoot, font=('Arial', 15), text='Score: ' + str(self.score), fg='Black')
        score.place(x=self.floors[1].cols * 21, y=100)
        if prev is not None:
            prevY = prev.y
            prevX = prev.x
            prevFloor = prev.floor_no
            self.canvas.delete(f"{prevY}-{prevX}-{prevFloor}")
            self.tkRoot.update()

        y = cell.y
        x = cell.x
        floor_no = cell.floor_no
        y_offset = (self.floors[floor_no].rows * 35 + 20) * (floor_no - 1)
        x0, y0 = x * 20, y * 35 + y_offset
        x1, y1 = (x + 1) * 20, (y + 1) * 35 + y_offset

        if visited[cell] == 1:
            self.canvas.create_rectangle(
                x0, y0, x1, y1, fill="#ff8888", outline="black"
            )

        elif visited[cell] == 1:
            self.canvas.create_rectangle(
                x0, y0, x1, y1, fill="#ff4b4b", outline="black"
            )

        elif visited[cell] == 1:
            self.canvas.create_rectangle(
                x0, y0, x1, y1, fill="#ff0000", outline="black"
            )

        elif visited[cell] == 1:
            self.canvas.create_rectangle(
                x0, y0, x1, y1, fill="#cb0000", outline="black"
            )

        else:
            self.canvas.create_rectangle(
                x0, y0, x1, y1, fill="#977878", outline="black"
            )


        self.canvas.create_text(
            x0 + 10, y0 + 10, text=f"A{current_agent}", fill="black", tags=f"{y}-{x}-{floor_no}"
        )

        self.tkRoot.update()
        time.sleep(0.4)

    def heatMapAnimation(self, path_to_goal):
        generalPath = {}

        for agent in self.agents:
            if generalPath.get(agent) is None:
                if agent == 1:
                    tempNode = path_to_goal[-1]
                else:
                    tempNode = self.currentNode[agent]
                generalPath[agent] = []
                while tempNode:
                    for eachCell in tempNode.path:
                        generalPath[agent].append(eachCell)
                    tempNode = tempNode.parent

        agent = 1
        prevCell = {}  # lưu cell trước mà agent đi để xoá chữ
        while True:
            if len(generalPath[agent]) > 0:
                if prevCell.get(agent) is not None:
                    prevY = prevCell[agent].y
                    prevX = prevCell[agent].x
                    prevFloor = prevCell[agent].floor_no
                    self.canvas.delete(f"{prevY}-{prevX}-{prevFloor}")
                    self.tkRoot.update()

                eachCell = generalPath[agent][-1]
                prevCell[agent] = eachCell

                y = eachCell.y
                x = eachCell.x
                floor_no = eachCell.floor_no
                y_offset = (self.floors[floor_no].rows * 35 + 20) * (floor_no - 1)
                x0, y0 = x * 20, y * 35 + y_offset
                x1, y1 = (x + 1) * 20, (y + 1) * 35 + y_offset

                if Counter(generalPath[agent])[eachCell] == 1:
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1, fill="#ff8888", outline="black"
                    )
                elif Counter(generalPath[agent])[eachCell] == 2:
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1, fill="#ff4b4b", outline="black"
                    )
                elif Counter(generalPath[agent])[eachCell] == 3:
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1, fill="#ff0000", outline="black"
                    )
                elif Counter(generalPath[agent])[eachCell] == 4:
                    self.canvas.create_rectangle(
                        x0, y0, x1, y1, fill="#cb0000", outline="black"
                    )

                self.canvas.create_text(
                    x0 + 10, y0 + 10, text=f"A{agent}", fill="black", tags=f"{y}-{x}-{floor_no}"
                )

                generalPath[agent].pop(-1)

                self.tkRoot.update()
                time.sleep(0.4)

            else:
                if agent == 1:
                    break

            agent += 1
            if agent > self.number_agents:
                agent = 1


searchTree2 = SearchTree()
searchTree2.getInputFile("input//input3-level4.txt")
searchTree2.solve()
# searchTree2.tkRoot.mainloop()
