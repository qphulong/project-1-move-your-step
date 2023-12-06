import heapq
import random
import re
import tkinter as tk
from collections import Counter
from enum import Enum
import copy


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

        self.waitingNode = False # node indicating that this is a place where the agent is waiting for another agent

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

    def expandAround(self, cell, TempFrontier, SearchTree, agent_no):
        def inTempFrontier(cell, TempFrontier):
            for node in TempFrontier:
                if cell == node.cell:
                    return True
            return False

        floor_no = cell.floor_no


        # add N cell to tempFrontier
        if (
                cell.y > 0
                and not self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x).isWall()
                and inTempFrontier(self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x), TempFrontier)
        ):
            northCell = self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x)

            TempFrontier.append(Node(northCell, SearchTree))

            cell.children.append(northCell)
            northCell.parrent = cell


        # add W cell to tempFrontier
        if (
                cell.x > 0
                and not self.belongTo.floors[floor_no].getCell(cell.y, cell.x - 1).isWall()
                and inTempFrontier(self.belongTo.floors[floor_no].getCell(cell.y, cell.x - 1), TempFrontier)
        ):
            westCell = self.belongTo.floors[floor_no].getCell(cell.y, cell.x - 1)

            TempFrontier.append(Node(westCell, SearchTree))

            cell.children.append(westCell)
            westCell.parrent = cell

        # add S cell to tempFrontier
        if (
                cell.y < self.belongTo.floors[floor_no].rows - 1
                and not self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x).isWall()
                and inTempFrontier(self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x), TempFrontier)
        ):
            southCell = self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x)

            TempFrontier.append(Node(southCell, SearchTree))

            cell.children.append(southCell)
            southCell.parrent = cell


        # add E cell to tempFrontier
        if (
                cell.x < self.belongTo.floors[floor_no].cols - 1
                and not self.belongTo.floors[floor_no].getCell(cell.y, cell.x + 1).isWall()
                and inTempFrontier(self.belongTo.floors[floor_no].getCell(cell.y, cell.x + 1), TempFrontier)
        ):
            eastCell = self.belongTo.floors[floor_no].getCell(cell.y, cell.x + 1)

            TempFrontier.append(Node(eastCell, SearchTree))

            cell.children.append(eastCell)
            eastCell.parrent = cell


        # add NE cell to tempFrontier
        if (
                cell.y > 0
                and cell.x < self.belongTo.floors[floor_no].cols - 1
                and not self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x).isWall()
                and not self.belongTo.floors[floor_no].getCell(cell.y, cell.x + 1).isWall()
                and not self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x + 1).isWall()
                and inTempFrontier(self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x + 1), TempFrontier)
        ):
            neCell = self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x + 1)

            TempFrontier.append(Node(neCell, SearchTree))

            cell.children.append(neCell)
            neCell.parrent = cell


        # Add NW cell to tempFrontier
        if (
                cell.y > 0
                and cell.x > 0
                and not self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x).isWall()
                and not self.belongTo.floors[floor_no].getCell(cell.y, cell.x - 1).isWall()
                and not self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x - 1).isWall()
                and inTempFrontier(self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x - 1), TempFrontier)
        ):
            nwCell = self.belongTo.floors[floor_no].getCell(cell.y - 1, cell.x - 1)

            TempFrontier.append(Node(nwCell, SearchTree))

            cell.children.append(nwCell)
            nwCell.parrent = cell

        # Add SW cell to tempFrontier
        if (
                cell.y < self.belongTo.floors[floor_no].rows - 1
                and cell.x > 0
                and not self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x).isWall()
                and not self.belongTo.floors[floor_no].getCell(cell.y, cell.x - 1).isWall()
                and not self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x - 1).isWall()
                and inTempFrontier(self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x - 1), TempFrontier)
        ):
            swCell = self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x - 1)

            TempFrontier.append(Node(swCell, SearchTree))

            cell.children.append(swCell)
            swCell.parrent = cell

        special = self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x + 1).getSpecialValue() if cell.y < \
                                                                                                      self.belongTo.floors[
                                                                                                          floor_no].rows - 1 and cell.x < \
                                                                                                      self.belongTo.floors[
                                                                                                          floor_no].cols - 1 else None
        # Add SE cell to tempFrontier
        if (
                cell.y < self.belongTo.floors[floor_no].rows - 1
                and cell.x < self.belongTo.floors[floor_no].cols - 1
                and not self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x).isWall()
                and not self.belongTo.floors[floor_no].getCell(cell.y, cell.x + 1).isWall()
                and (special == "" or (special[0] == "A" and special[1] == str(agent_no)))
                and inTempFrontier(self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x + 1), TempFrontier)
        ):
            seCell = self.belongTo.floors[floor_no].getCell(cell.y + 1, cell.x + 1)

            TempFrontier.append(Node(seCell, SearchTree))

            cell.children.append(seCell)
            seCell.parrent = cell

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
                cell_tag = cell.getSpecialValue()  # special value của cell

                other = self.belongTo.isOtherAgent(cell, agent_no)

                if other:
                    # create new node
                    newNode = Node(cell, self.belongTo)
                    newNode.setPathCost(self.pathCost + steps)
                    newNode.saveHeuristic(self.belongTo.goals[agent_no])
                    newNode.saveF()

                    # append new node to tree
                    self.children.append(newNode)
                    newNode.parent = self

                    tempCell = cell
                    while tempCell:
                        newNode.path.append(tempCell)
                        tempCell = tempCell.parrent

                    # wait here
                    continue

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
                            newNode.saveHeuristic(self.belongTo.goals[agent_no])
                            newNode.saveF()

                            # append new node to tree
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
                            newNode.saveHeuristic(self.belongTo.goals[agent_no])
                            newNode.saveF()

                            # inherit key
                            for eachKey in self.keys:
                                newNode.appendKey(eachKey)

                            # append new node to tree
                            self.children.append(newNode)
                            newNode.parent = self

                            tempCell = cell
                            while tempCell:
                                newNode.path.append(tempCell)
                                tempCell = tempCell.parrent

                            # if go through the same door with same keys,then delete this new node
                            tempNode = self
                            while tempNode:
                                if len(newNode.keys) == tempNode.keys:
                                    self.children.remove(newNode)
                                    newNode.parent = None
                                    del newNode
                                tempNode = tempNode.parent
                        # if does not have key
                        else:
                            pass

                elif cell_tag[0] == "T" and cell_tag[1] == str(agent_no):
                    # create new node
                    newNode = Node(cell, self.belongTo)
                    newNode.setPathCost(self.pathCost + steps)
                    newNode.saveHeuristic(self.belongTo.goals[agent_no])
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
                    newNode.saveHeuristic(self.belongTo.goals[agent_no])
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

                    tempCell = cell
                    while tempCell:
                        newNode.path.append(tempCell)
                        tempCell = tempCell.parrent

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
        self.agents = {}
        self.goals = {}
        self.currentNode = {}  # save for all agents
        self.frontier = {}
        self.visited = {}
        self.root = {}
        self.keys = {}
        self.upcoming = {}  # save next cells of each agent

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

    def BFS(self):
        # self.root[1].saveHeuristic(self.goals[1])
        # self.root[1].saveF()
        if self.frontier[1]:
            # self.visualize()
            # self.frontier[1].sort(key=lambda x: x.getF())

            if self.isOtherAgent(self.frontier[1][0].cell, 1):  # meet other agentß
                frontier_length = len(self.frontier[1])
                if frontier_length > 1:
                    i = 1
                    while i < frontier_length and self.isOtherAgent(
                            self.frontier[1][i].cell, 1
                    ):
                        self.frontier[1][i - 1], self.frontier[1][i] = (
                            self.frontier[1][i],
                            self.frontier[1][i - 1],
                        )
                        i += 1
                    if i == frontier_length:
                        # return (self.MainStatus.IN_PROGRESS, self.frontier[1][0])
                        # nếu hết lựa chọn checkpoint thì ta chọn những chỗ bth để đi
                        tempFrontier = []
                        self.frontier[1][0].expandAround(self.agents[1], tempFrontier, self, 1)

                        if len(tempFrontier)>0:
                            self.frontier[1] = tempFrontier + self.frontier[1]
                        else:
                            waitingNode = copy.copy(self.frontier[1][0])
                            waitingNode.waitingNode = True
                            waitingNode.cell.waitingCell = True
                            current_parent = self.frontier[1][0].parent
                            waitingNode.parent = current_parent
                            self.frontier[1][0].parent = waitingNode
                            self.frontier[1][0].path.insert(0, waitingNode.cell)
                            return (self.MainStatus.IN_PROGRESS, self.frontier[1][0])
                else:
                    waitingNode = copy.copy(self.frontier[1][0])
                    waitingNode.waitingNode = True
                    waitingNode.cell.waitingCell = True
                    current_parent = self.frontier[1][0].parent
                    waitingNode.parent = current_parent
                    self.frontier[1][0].parent = waitingNode
                    self.frontier[1][0].path.insert(0, waitingNode.cell)
                    return (self.MainStatus.IN_PROGRESS, self.frontier[1][0])

            self.currentNode[1] = self.frontier[1].pop(0)

            self.agents[1] = self.currentNode[1].cell



            # if path found
            if self.currentNode[1].cell == self.goals[1]:
                tempNode = self.currentNode[1]
                while tempNode:
                    if tempNode.waitingNode:
                        print(f"Waiting at {tempNode.cell.y} {tempNode.cell.x} Floor: {tempNode.cell.floor_no} Value: {tempNode.cell.getSpecialValue()}")
                    else:
                        print(f"{tempNode.cell.y} {tempNode.cell.x} Floor: {tempNode.cell.floor_no} Value: {tempNode.cell.getSpecialValue()}")
                    tempNode = tempNode.parent
                # self.visualize()
                return (self.MainStatus.REACHED, None)

            self.currentNode[1].expand(1)
            for eachChild in self.currentNode[1].children:
                self.frontier[1].append(eachChild)

            return (
                self.MainStatus.IN_PROGRESS,
                self.frontier[1][0] if len(self.frontier[1]) > 0 else None,
            )

        return (self.MainStatus.UNSOLVABLE, None)

    def BFS_OtherAgents(self, agent_no):
        # self.root[agent_no].saveHeuristic(self.goals[agent_no])
        # self.root[agent_no].saveF()
        if self.frontier[agent_no]:
            # self.visualize()
            # self.frontier[agent_no].sort(key=lambda x: x.getF())

            if self.isOtherAgent(self.frontier[agent_no][0].cell, agent_no):  # meet other agentß
                frontier_length = len(self.frontier[agent_no])
                if frontier_length > 1:
                    i = 1
                    while i < frontier_length and self.isOtherAgent(
                            self.frontier[agent_no][i].cell, agent_no
                    ):
                        self.frontier[agent_no][i - 1], self.frontier[agent_no][i] = (
                            self.frontier[agent_no][i],
                            self.frontier[agent_no][i - 1],
                        )
                        i += 1
                    if i == frontier_length:
                        # nếu hết lựa chọn checkpoint thì ta chọn những chỗ bth để đi
                        tempFrontier = []
                        self.frontier[agent_no][0].expandAround(self.agents[agent_no], tempFrontier, self, agent_no)

                        if len(tempFrontier) > 0:
                            self.frontier[agent_no] = tempFrontier + self.frontier[agent_no]
                        else:
                            return (self.MainStatus.IN_PROGRESS, self.frontier[agent_no][0])
                else:
                    return (self.MainStatus.IN_PROGRESS, self.frontier[agent_no][0])

            self.currentNode[agent_no] = self.frontier[agent_no].pop(0)

            self.agents[agent_no] = self.currentNode[agent_no].cell

            # if path found
            if self.currentNode[agent_no].cell == self.goals[agent_no]:
                return (self.MainStatus.REACHED, None)

            self.currentNode[agent_no].expand(agent_no)
            for eachChild in self.currentNode[agent_no].children:
                self.frontier[agent_no].append(eachChild)
            return (
                self.MainStatus.IN_PROGRESS,
                self.frontier[agent_no][0]
                if len(self.frontier[agent_no]) > 0
                else None,
            )

        return (self.MainStatus.UNSOLVABLE, None)

    def agent_turn_based_movement(self):
        current_agent = 1  # Initialize the index to track the current agent

        while True:
            if current_agent == 1:  # A1
                res = self.BFS()
                if res[0] != self.MainStatus.IN_PROGRESS:  # reached goal or unsolvable
                    if res[0] == self.MainStatus.REACHED:
                        self.heatMap()
                    elif res[0] == self.MainStatus.UNSOLVABLE:
                        print("Cannot solve")
                    break
                else:
                    if res[1] is None:
                        print("Cannot solve")
                        break

            else:  # other agents
                res = self.BFS_OtherAgents(
                    current_agent
                )  # other agents reached their goals
                if res[0] != self.MainStatus.IN_PROGRESS:  # reached goal or unsolvable
                    self.goals[
                        current_agent
                    ] = self.generate_goal()  # generate new goal for this agent

                else:
                    if res[1] is None:
                        self.goals[
                            current_agent
                        ] = self.generate_goal()  # generate new goal for this agent

            current_agent += 1

            if current_agent > self.number_agents:
                current_agent = 1

    def generate_goal(self):
        random_goal = None

        while random_goal is None or random_goal.isWall():
            random_floor = random.randint(1, len(self.floors))
            random_y = random.randint(0, self.floors[random_floor].rows - 1)
            random_x = random.randint(0, self.floors[random_floor].cols - 1)
            random_goal = self.floors[random_floor].getCell(random_y, random_x)
        return random_goal

    def competing_cell(self, agent_1, agent_2):
        higher_priority = (
            agent_1 if agent_1 < agent_2 else agent_2
        )  # agent thấp hơn thì ưu tiên hơn

        return higher_priority

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
            tempNode = self.currentNode[1]
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
                            if floor.table[i][j].waitingCell:
                                canvas.create_rectangle(
                                    x0, y0, x1, y1, fill="#a7f542", outline="black"
                                )
                                canvas.create_text(
                                    x0 + 10, y0 + 10, text="Waiting", fill="black"
                                )
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

                        special = floor.table[i][j].getSpecialValue()
                        if special != "":
                            if special == "UP" or special == "DO":
                                canvas.create_rectangle(x0, y0, x1, y1,
                                                        fill="#34cceb" if special == "UP" else "#f5aa42",
                                                        outline="black")
                                canvas.create_text(
                                    x0 + 10, y0 + 10, text="↑" if special == "UP" else "↓", fill="black"
                                )
                                continue

                            if special == "T1":
                                canvas.create_rectangle(x0, y0, x1, y1, fill="#ebb121", outline="black")
                                canvas.create_text(
                                    x0 + 10, y0 + 10, text="T1"
                                )
                                continue

                            if special[0] == "T":
                                canvas.create_rectangle(x0, y0, x1, y1, fill="#152b52", outline="black")
                                canvas.create_text(
                                    x0 + 10, y0 + 10, text=special
                                )
                                continue

                            if special == "A1":
                                canvas.create_rectangle(x0, y0, x1, y1, fill="#5750ba", outline="black")
                                canvas.create_text(
                                    x0 + 10, y0 + 10, text="A1"
                                )
                                continue

                            if special[0] == "A":
                                canvas.create_rectangle(x0, y0, x1, y1, fill="#eb6721", outline="black")
                                canvas.create_text(
                                    x0 + 10, y0 + 10, text=special
                                )
                                continue

                            canvas.create_rectangle(x0, y0, x1, y1, fill="#2ad500", outline="black")
                            canvas.create_text(
                                x0 + 10, y0 + 10, text=special, fill="black"
                            )

            y_offset += floor.rows * 35 + 20  # Adjust y_offset for next floor

        root.mainloop()


searchTree2 = SearchTree()
searchTree2.getInputFile("input//input4-level4.txt")
searchTree2.agent_turn_based_movement()
