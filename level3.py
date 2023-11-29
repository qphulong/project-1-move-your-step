import heapq
import random
import re
import tkinter as tk
from enum import Enum
import copy


class Cell:
    def __init__(self, y, x, floor_no):
        self.y = y
        self.x = x
        self.floor_no = floor_no
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

    def getFloorsHeuristic(self, GoalCell):
        return self.getManhattanFrom(GoalCell) + abs(self.floor_no - GoalCell.floor_no)

    def getPhanTrungDucDistance(self, Cell):
        return max(abs(self.x - Cell.x), abs(self.y - Cell.y))

    def isWall(self):
        return "-1" in self.values or any("A" in value for value in self.values)

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

    def appendToCell(self, row, col, value):
        self.table[row][col].appendValue(value)

    def removeFromCell(self, row, col, value):
        if self.checkValueInCell(row, col, value):
            self.table[row][col].removeValue(value)

    def checkValueInCell(self, row, col, value):
        return self.table[row][col].checkValue(value)

    def getCell(self, row, col):
        return self.table[row][col]

    def findStair(self, direction):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.table[i][j].checkValue(direction):
                    return self.table[i][j]
        return None


custom_goals = []
floor_priorities = []


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
        self.keys = []
        self.children = [] # những con (successor) của node này
        self.parent = None # cha của node này

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

    def saveHeuristic(self, GoalCell):  # calculate heuristic of the current cell
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

    def expand(self, agent_no):
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
                cell_tag = cell.getSpecialValue() # special value của cell

                # normal cell
                if cell_tag == "" or cell_tag[0] == "A":
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
                            newNode.saveHeuristic(self.belongTo.goals[agent_no])
                            newNode.saveF()

                            # append new node to tree
                            self.children.append(newNode)
                            newNode.parent = self

                            # inherit collected keys so far
                            for eachKey in self.keys:
                                newNode.appendKey(
                                    eachKey
                                )  # keep track of collected keys
                            newNode.appendKey(cell_tag)  # add current key

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
                            newNode.saveHeuristic(self.belongTo.goals[agent_no])
                            newNode.saveF()

                            # inherit key
                            for eachKey in self.keys:
                                newNode.appendKey(eachKey)

                            # append new node to tree
                            self.children.append(newNode)
                            newNode.parent = self

                            # if go through the same door with same keys,then delete this new node
                            tempNode = self
                            while tempNode:
                                if len(newNode.keys) == (tempNode.keys):
                                    self.children.remove(newNode)
                                    newNode.parent = None
                                    del newNode
                                tempNode = tempNode.parent
                        # if does not have key
                        else:
                            pass

                elif cell_tag[0] == "T":
                    # create new node
                    newNode = Node(cell, self.belongTo)
                    newNode.setPathCost(self.pathCost + steps)
                    newNode.saveHeuristic(self.belongTo.goals[agent_no])
                    newNode.saveF()

                    # append new node to tree
                    self.children.append(newNode)
                    newNode.parent = self


                # stairs
                elif cell_tag == "UP" or cell_tag == "DO":
                    if len(BFSfrontier) > 1 and (
                            (BFSfrontier[-2].getSpecialValue() == "UP" and self.cell.getSpecialValue() == "DO") or
                            (BFSfrontier[-2].getSpecialValue() == "DO" and self.cell.getSpecialValue() == "UP")):
                        continue

                    newNode = Node(cell, self.belongTo) # tạo node mới từ cell (duyệt BFSFrontier)
                    newNode.setPathCost(self.pathCost + steps)
                    newNode.saveHeuristic(self.belongTo.goals[agent_no])
                    newNode.saveF()

                    # append new node to tree
                    self.children.append(newNode) # children của node hiện tại là thêm node mới
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


class SearchTree:
    def __init__(self):
        self.floors = {}
        self.agents = {}
        self.goals = {}
        self.currentNode = {}  # save for all agents
        self.frontier = {}
        self.visited = {}
        self.root = {}
        self.keys = {}

        self.number_agents = 0  # số agent

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
                    self.goals[agent_no] = self.floors[current_floor].getCell(i, j)

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

    class MainStatus(Enum):
        REACHED = 1
        UNSOLVABLE = -1
        IN_PROGRESS = 0

    def AStar(self):
        # self.root[1].saveHeuristic(self.goals[1])
        # self.root[1].saveF()
        while (self.frontier[1]):
            # self.visualize()
            # self.frontier[1].sort(key=lambda x: x.getF())
            self.currentNode[1] = self.frontier[1].pop(0)

            # if path found
            if self.currentNode[1].cell == self.goals[1]:
                tempNode = self.currentNode[1]
                while (tempNode):
                    print(tempNode.cell.getSpecialValue())
                    tempNode = tempNode.parent
                # self.visualize()
                return

            self.currentNode[1].expand(1)
            for eachChild in self.currentNode[1].children:
                self.frontier[1].append(eachChild)


        print("No solution found")


searchTree2 = SearchTree()
searchTree2.getInputFile("input//input2-level4.txt")
searchTree2.AStar()
pass