import copy
from enum import Enum, auto

import numpy as np

import floor
from level1 import Level1

class GOAL(Enum):
    KEY = 1
    ROOM = 2
    FLOOR = 3
    FINAL_GOAL = 4
    UNDEFINED = 5


class Level4(Level1):
    def __init__(self):
        super.__init__()

        self.subgoal_stack = [] # subgoals before achieving the ultimate goal

        self.keys = {}  # save position of keys for each rooms with a dictionary
        self.doors = {} # save positions of room doors
        self.agents = {} # initial positions of agents
        self.goals = {} # pos of goals
        self.stairs = {}

        self.floors = [] # list of floors
        self.obtained_keys = [] # list of obtained keys (Save room no)
        self.rooms = 0

        self.currentGoal = None # there are many goals, from smaller to the biggest (T1)

        self.moves = {} # number of moves for each agent

    def setPrevious(self,prev):
        self.previous = prev


    def heuristic_lvl4(self,current_agent):
        point1 = np.array(current_pos.x, current_pos.y)
        point2 = np.array(goal_pos.x, goal_pos.y)

        floor_diff = abs(current_pos.floor - goal_pos.floor)

        dist = np.linalg.norm(point1 - point2)

        return floor_diff * dist

    def floor_rep(self):
        rep = tuple([tuple(self.agents), tuple(self.keys), tuple(self.agents)])
        return rep

    class Pos():
        def __init__(self,floor,x,y):
            self.floor = floor
            self.x = x
            self.y = y

    def getInputFile(self, filePath):
        with open(filePath, "r") as file:
            lines = file.readlines()

        rows, cols = map(int, lines[0].strip().split(','))
        current_floor = 0

        for i in range(1, len(lines)):
            self.floor = floor.Floor(rows, cols)
            if lines[i].__contains__("floor"):
                current_floor+=1
                self.floors.append(floor.Floor(rows,cols))
            else:
                row_values = list(map(str, lines[i].strip().split(',')))
                for j in range(cols):

                    pos = self.Pos(current_floor, i - 2, j)

                    if str(row_values[j]).__contains__("A"):  # agent
                        agent_no = row_values[j][1]
                        self.agents[agent_no] = pos
                    elif str(row_values[j]).__contains__("T"):
                        goal_no = row_values[j][1]
                        self.goals[goal_no] = pos
                    elif str(row_values[j].__contains__("K")):  # key
                        key_no = row_values[j][1]
                        self.keys[key_no] = pos
                    elif str(row_values[j].__contains__("D")):  # door
                        door_no = row_values[j][1]
                        self.doors[door_no] = pos
                        self.rooms += 1
                    elif str(row_values[j])=="UP" or str(row_values[j])=="DO":
                        if str(row_values[j])=="UP":
                            self.stairs[current_floor+1] = pos
                        else:
                            self.stairs[current_floor-1] = pos

                    self.floor.appendToCell(i - 2, j, row_values[j])  # set value for the board cell

    def move(self):
        _current_floor = 1

        def goUp(_current_floor):
            _current_floor += 1
        def goDown(_current_floor):
            _current_floor -= 1


    def solve(self):
        path = self.algo.BFS_Level4(self)[1]
        if path is None:
            print("No solutions found")
            return False
        print(f"Path: {path}")
        self.algo.visualize_path(self.floor, path)
        return True

    def moveN(self,current_agent):
        copyState = copy.deepcopy(self)
        copyState.setPrevious(self)

        if copyState.agent_Xposition > 0 and copyState.floor.checkValueInCell(copyState.agent_Xposition - 1,
                                                                              copyState.agent_Yposition, "-1") == False:
            old_x, old_y = copyState.agent_Xposition, copyState.agent_Yposition
            copyState.agent_Xposition -= 1
            copyState.floor.removeFromCell(old_x, old_y, "A1")
            copyState.floor.appendToCell(copyState.agent_Xposition, copyState.agent_Yposition, "A1")
            return copyState
        return None

    def moveS(self,current_agent):
        copyState = copy.deepcopy(self)
        copyState.setPrevious(self)

        if copyState.agent_Xposition < copyState.floor.rows - 1 and copyState.floor.checkValueInCell(
                copyState.agent_Xposition + 1, copyState.agent_Yposition, "-1") == False:
            old_x, old_y = copyState.agent_Xposition, copyState.agent_Yposition
            copyState.agent_Xposition += 1
            copyState.floor.removeFromCell(old_x, old_y, "A1")
            copyState.floor.appendToCell(copyState.agent_Xposition, copyState.agent_Yposition, "A1")
            return copyState
        return None

    def moveE(self,current_agent):
        copyState = copy.deepcopy(self)
        copyState.setPrevious(self)

        if copyState.agent_Yposition < copyState.floor.cols - 1 and copyState.floor.checkValueInCell(
                copyState.agent_Xposition, copyState.agent_Yposition + 1, "-1") == False:
            old_x, old_y = copyState.agent_Xposition, copyState.agent_Yposition
            copyState.agent_Yposition += 1
            copyState.floor.removeFromCell(old_x, old_y, "A1")
            copyState.floor.appendToCell(copyState.agent_Xposition, copyState.agent_Yposition, "A1")
            return copyState
        return None

    def moveW(self,current_agent):
        copyState = copy.deepcopy(self)
        copyState.setPrevious(self)

        if copyState.agent_Yposition > 0 and copyState.floor.checkValueInCell(copyState.agent_Xposition,
                                                                              copyState.agent_Yposition - 1,
                                                                              "-1") == False:
            old_x, old_y = copyState.agent_Xposition, copyState.agent_Yposition
            copyState.agent_Yposition -= 1
            copyState.floor.removeFromCell(old_x, old_y, "A1")
            copyState.floor.appendToCell(copyState.agent_Xposition, copyState.agent_Yposition, "A1")
            return copyState
        return None

    def moveNE(self,current_agent):
        copyState = copy.deepcopy(self)
        copyState.setPrevious(self)

        destination_x = copyState.agent_Xposition - 1
        destination_y = copyState.agent_Yposition + 1

        # Check if the destination cell is within bounds and available
        if (
                destination_x >= 0 and destination_y < copyState.floor.cols and
                copyState.floor.checkValueInCell(destination_x, copyState.agent_Yposition, "-1") == False and
                copyState.floor.checkValueInCell(copyState.agent_Xposition, destination_y, "-1") == False and
                copyState.floor.checkValueInCell(destination_x, destination_y, "-1") == False
        ):
            old_x, old_y = copyState.agent_Xposition, copyState.agent_Yposition
            copyState.agent_Xposition, copyState.agent_Yposition = destination_x, destination_y

            # Remove value "A1" from the old cell
            copyState.floor.removeFromCell(old_x, old_y, "A1")

            # Add value "A1" to the new cell
            copyState.floor.appendToCell(copyState.agent_Xposition, copyState.agent_Yposition, "A1")
            return copyState
        return None

    def moveSE(self,current_agent):
        copyState = copy.deepcopy(self)
        copyState.setPrevious(self)

        destination_y = copyState.agent_Yposition + 1
        destination_x = copyState.agent_Xposition + 1

        # Check if the destination cell is within bounds and available
        if (
                destination_x < copyState.floor.rows and destination_y < copyState.floor.cols and
                copyState.floor.checkValueInCell(destination_x, copyState.agent_Yposition, "-1") == False and
                copyState.floor.checkValueInCell(copyState.agent_Xposition, destination_y, "-1") == False and
                copyState.floor.checkValueInCell(destination_x, destination_y, "-1") == False
        ):
            old_x, old_y = copyState.agent_Xposition, copyState.agent_Yposition
            copyState.agent_Xposition, copyState.agent_Yposition = destination_x, destination_y

            # Remove value "A1" from the old cell
            copyState.floor.removeFromCell(old_x, old_y, "A1")

            # Add value "A1" to the new cell
            copyState.floor.appendToCell(copyState.agent_Xposition, copyState.agent_Yposition, "A1")
            return copyState
        return None

    def moveSW(self,current_agent):
        copyState = copy.deepcopy(self)
        copyState.setPrevious(self)

        destination_x = copyState.agent_Xposition + 1
        destination_y = copyState.agent_Yposition - 1

        # Check if the destination cell is within bounds and available
        if (
                destination_x < copyState.floor.rows and destination_y >= 0 and
                copyState.floor.checkValueInCell(destination_x, copyState.agent_Yposition, "-1") == False and
                copyState.floor.checkValueInCell(copyState.agent_Xposition, destination_y, "-1") == False and
                copyState.floor.checkValueInCell(destination_x, destination_y, "-1") == False
        ):
            old_x, old_y = copyState.agent_Xposition, copyState.agent_Yposition
            copyState.agent_Xposition, copyState.agent_Yposition = destination_x, destination_y

            # Remove value "A1" from the old cell
            copyState.floor.removeFromCell(old_x, old_y, "A1")

            # Add value "A1" to the new cell
            copyState.floor.appendToCell(copyState.agent_Xposition, copyState.agent_Yposition, "A1")
            return copyState
        return None

    def moveNW(self,current_agent):
        copyState = copy.deepcopy(self)
        copyState.setPrevious(self)

        destination_y = copyState.agent_Yposition - 1
        destination_x = copyState.agent_Xposition - 1

        # Check if the destination cell is within bounds and available
        if (
                destination_x >= 0 and destination_y >= 0 and
                copyState.floor.checkValueInCell(destination_x, copyState.agent_Yposition, "-1") == False and
                copyState.floor.checkValueInCell(copyState.agent_Xposition, destination_y, "-1") == False and
                copyState.floor.checkValueInCell(destination_x, destination_y, "-1") == False
        ):
            old_x, old_y = copyState.agent_Xposition, copyState.agent_Yposition
            copyState.agent_Xposition, copyState.agent_Yposition = destination_x, destination_y

            # Remove value "A1" from the old cell
            copyState.floor.removeFromCell(old_x, old_y, "A1")

            # Add value "A1" to the new cell
            copyState.floor.appendToCell(copyState.agent_Xposition, copyState.agent_Yposition, "A1")
            return copyState
        return None


class Task:
    def __init__(self,x,y,floor):
        self.floor = floor
        self.destinationX = x
        self.destinationY = y

    def set_task(self,x,y):
        if floor[x][y].isWall == False:
            self.destinationX = x
            self.destinationY = y
        else:
            print("Cannot set a task destination at a wall or an obstacle")