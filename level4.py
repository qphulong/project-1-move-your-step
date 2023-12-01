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
        return "-1" in self.values

    def isAgent(self):
        special = self.getSpecialValue()
        return special and special[0] == "A"

    def isOtherAgent(self, agent_no):
        special = self.getSpecialValue()
        return special and special[0] == "A" and special[1] != str(agent_no)

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
        self.keys = []  # obtained keys
        self.stairs = {}  # stairs that have been used
        self.children = []  # những con (successor) của node này
        self.parent = None  # cha của node này

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
                cell_tag = cell.getSpecialValue()  # special value của cell

                # normal cell
                if cell_tag == "" or (
                    cell_tag[0] == "A" and int(cell_tag[1]) == agent_no
                ):
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

                elif cell_tag[0] == "A" and int(cell_tag[1]) != agent_no:
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

                    if (
                        self.belongTo.agents[int(cell_tag[1])].y == cell.y
                        and self.belongTo.agents[int(cell_tag[1])].x == cell.x
                        and self.belongTo.agents[int(cell_tag[1])].floor_no
                        == cell.floor_no
                    ):
                        # create new node
                        newNode = Node(cell, self.belongTo)
                        newNode.setPathCost(self.pathCost + steps)
                        newNode.saveHeuristic(self.belongTo.goals[agent_no])
                        newNode.saveF()

                        # append new node to tree
                        self.children.append(newNode)
                        newNode.parent = self
                    else:
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
                                if len(newNode.keys) == tempNode.keys:
                                    self.children.remove(newNode)
                                    newNode.parent = None
                                    del newNode
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
                    newNode.saveHeuristic(self.belongTo.goals[agent_no])
                    newNode.saveF()

                    # append new node to tree
                    self.children.append(newNode)
                    newNode.parent = self

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

                    # append new node to tree
                    self.children.append(
                        newNode
                    )  # children của node hiện tại là thêm node mới
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

                    self.expandFrontierCell(
                        cell, BFSvisited, BFSfrontier, BFStempFrontier
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
                return True
        return False

    def AStar(self):
        self.root[1].saveHeuristic(self.goals[1])
        self.root[1].saveF()
        if self.frontier[1]:
            # self.visualize()
            self.frontier[1].sort(key=lambda x: x.getF())
            self.currentNode[1] = self.frontier[1].pop(0)

            # if path found
            if self.currentNode[1].cell == self.goals[1]:
                tempNode = self.currentNode[1]
                while tempNode:
                    print(
                        f"{tempNode.cell.getSpecialValue()} Floor: {tempNode.cell.floor_no}"
                    )
                    tempNode = tempNode.parent
                # self.visualize()
                return (self.MainStatus.REACHED, None)

            self.currentNode[1].expand(1)
            for eachChild in self.currentNode[1].children:
                self.frontier[1].append(eachChild)
            return (self.MainStatus.IN_PROGRESS, self.frontier[1][0])

        return (self.MainStatus.UNSOLVABLE, None)

    def AStar_CustomGoal(self, goal):
        self.root[1].saveHeuristic(goal)
        self.root[1].saveF()
        if self.frontier[1]:
            # self.visualize()
            self.frontier[1].sort(key=lambda x: x.getF())
            self.currentNode[1] = self.frontier[1].pop(0)

            # if path found
            if self.currentNode[1].cell == goal:
                tempNode = self.currentNode[1]
                while tempNode:
                    print(
                        f"{tempNode.cell.getSpecialValue()} Floor: {tempNode.cell.floor_no}"
                    )
                    tempNode = tempNode.parent
                # self.visualize()
                return (self.MainStatus.REACHED, None)

            self.currentNode[1].expand(1)
            for eachChild in self.currentNode[1].children:
                self.frontier[1].append(eachChild)
            return (self.MainStatus.IN_PROGRESS, self.frontier[1][0])

        return (self.MainStatus.UNSOLVABLE, None)

    def BFS(self):
        # self.root[1].saveHeuristic(self.goals[1])
        # self.root[1].saveF()
        if self.frontier[1]:
            # self.visualize()
            # self.frontier[1].sort(key=lambda x: x.getF())

            if self.isOtherAgent(self.frontier[1][0].cell, 1):  # meet other agent
                # print(f"Agent 1 meet other agent {self.frontier[1][0].cell.getSpecialValue()}")
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
                        return (self.MainStatus.IN_PROGRESS, self.frontier[1][0])
                else:
                    return (self.MainStatus.IN_PROGRESS, self.frontier[1][0])

            self.currentNode[1] = self.frontier[1].pop(0)

            self.agents[1] = self.currentNode[1].cell
            # if path found
            if self.currentNode[1].cell == self.goals[1]:
                tempNode = self.currentNode[1]
                while tempNode:
                    print(tempNode.cell.getSpecialValue())
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

    def BFS_CustomGoal(self, goal):
        # self.root[1].saveHeuristic(self.goals[1])
        # self.root[1].saveF()
        if self.frontier[1]:
            # self.visualize()
            # self.frontier[1].sort(key=lambda x: x.getF())
            self.currentNode[1] = self.frontier[1].pop(0)

            # if path found
            if self.currentNode[1].cell == goal:
                tempNode = self.currentNode[1]
                while tempNode:
                    print(tempNode.cell.getSpecialValue())
                    tempNode = tempNode.parent
                    # self.visualize()
                return (self.MainStatus.REACHED, None)

            self.currentNode[1].expand(1)
            for eachChild in self.currentNode[1].children:
                self.frontier[1].append(eachChild)
            return (self.MainStatus.IN_PROGRESS, self.frontier[1][0])

        return (self.MainStatus.UNSOLVABLE, None)

    def BFS_OtherAgents(self, agent_no):
        # self.root[agent_no].saveHeuristic(self.goals[agent_no])
        # self.root[agent_no].saveF()
        if self.frontier[agent_no]:
            # self.visualize()
            # self.frontier[agent_no].sort(key=lambda x: x.getF())
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
                        print("Found goal")
                    elif res[0] == self.MainStatus.UNSOLVABLE:
                        print("Cannot solve")
                    break
                else:
                    if res[1] is None:
                        print("Cannot solve")
                        break

                # self.upcoming[current_agent] = res[1].cell
                #
                # for agent, upcoming_cell in self.upcoming.items():  # competing for a cell
                #     if upcoming_cell is not None and upcoming_cell == res[
                #         1].cell and agent != 1:  # if there is a cell that is upcoming for other agent
                #         win_agent = self.competing_cell(agent, current_agent)
                #         lose_agent = agent if agent != win_agent else current_agent
                #         self.upcoming[lose_agent] = None  # lose agent will wait

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
                        continue

                    # self.upcoming[current_agent] = res[1].cell
                    #
                    # for agent, upcoming_cell in self.upcoming.items():
                    #     if upcoming_cell is not None and upcoming_cell == res[1].cell and agent != current_agent:
                    #         win_agent = self.competing_cell(agent, current_agent)
                    #         lose_agent = agent if agent != win_agent else current_agent
                    #         self.upcoming[lose_agent] = None

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


searchTree2 = SearchTree()
searchTree2.getInputFile("input//input1-level3.txt")
searchTree2.agent_turn_based_movement()
pass
