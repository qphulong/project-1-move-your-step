import copy
from enum import Enum, auto

import numpy as np

import floor

from algorithm import Algorithm


class GOAL(Enum):
    KEY = 1
    ROOM = 2
    FLOOR = 3
    FINAL_GOAL = 4
    UNDEFINED = 5


class Level4:
    def __init__(self):

        self.keys = {}  # save position of keys for each rooms with a dictionary
        self.doors = {}  # save positions of room doors
        self.agents = {}  # positions of agents
        self.goals = {}  # pos of goals
        self.stairs = {}

        self.floors = {}  # list of floors
        self.obtained_keys = []  # list of obtained keys (Save room numbers)
        self.rooms = 0  # count number of rooms
        self.visited_rooms = {}  # whether a room is visited

        self.currentGoal = None  # there are many goals, from smaller to the biggest (T1)

        self.previous = None

        self.moves = {}  # number of moves for each agent

        self.algo = Algorithm()

    def __lt__(self, other):
        if isinstance(other, Level4):
            return self.moves[1] < other.moves[1]

    def __eq__(self, other):
        return self.moves[1] < other.moves[1]

    def setPrevious(self, prev, agent):
        self.previous = prev

        self.moves[agent] += 1

    # mở cửa phòng
    def open_door(self, room_no, goal):
        res = self.AStar(self, self.keys[room_no])
        path = res[1][1]  # tìm đường đến key
        last_state = res[1][0]  # tìm state mới nhất

        res = self.AStar(last_state, self.doors[room_no])
        last_state = res[1][0]  # tìm state mới nhất
        path.__add__(res[1][1])  # tìm đường đến door

        # nhớ tính tới vụ chìa khoá ở trên lầu => phải cho nó đi xuống

        final = self.AStar(last_state, goal)[1]

        self.visited_rooms[room_no] = True

        return final

    def heuristic_lvl4(self, current_agent):
        x = self.agents[current_agent].x
        y = self.agents[current_agent].y

        goal_x = self.goals[current_agent].x
        goal_y = self.goals[current_agent].y

        point1 = np.array((x, y, 0))
        point2 = np.array((goal_x, goal_y, 0))
        dist = np.linalg.norm(point1 - point2)

        floor_diff = abs(self.agents[current_agent].floor - self.goals[current_agent].floor)

        return floor_diff + dist

    def __hash__(self):
        return hash(self.floor_rep())

    def floor_rep(self):
        rep = tuple([tuple(self.agents), tuple(self.obtained_keys)])
        return rep

    class Pos():
        def __init__(self, floor, x, y):
            self.floor = floor
            self.x = x
            self.y = y

        def __eq__(self, other):
            return self.floor == other.floor and self.x == other.x and self.y == other.y

    def getInputFile(self, filePath):
        with open(filePath, "r") as file:
            lines = file.readlines()

        rows, cols = map(int, lines[0].strip().split(','))
        current_floor = 0

        for i in range(1, len(lines)):
            self.floor = floor.Floor(rows, cols)
            if lines[i].__contains__("floor"):
                current_floor += 1
                self.floors[current_floor] = floor.Floor(rows, cols)
            else:
                row_values = list(map(str, lines[i].strip().split(',')))
                for j in range(cols):

                    pos = self.Pos(current_floor, i - 2, j)

                    if str(row_values[j]).__contains__("A"):  # agent
                        agent_no = int(row_values[j][1])
                        self.agents[agent_no] = pos
                        self.moves[agent_no] = 0
                    elif str(row_values[j]).__contains__("T"):
                        goal_no = int(row_values[j][1])
                        self.goals[goal_no] = pos
                    elif str(row_values[j]).__contains__("K"):  # key
                        key_no = int(row_values[j][1])
                        self.keys[key_no] = pos
                    elif str(row_values[j]).__contains__("D"):  # door
                        door_no = int(row_values[j][1])
                        self.doors[door_no] = pos
                        self.rooms += 1
                    elif str(row_values[j]) == "UP" or str(row_values[j]) == "DO":
                        if str(row_values[j]) == "UP":
                            self.stairs[(current_floor, current_floor + 1)] = pos
                        else:
                            self.stairs[(current_floor, current_floor - 1)] = pos

                    self.floors[current_floor].appendToCell(i - 2, j, row_values[j])  # set value for the board cell

    def move(self):
        _current_floor = 1

        def goUp(_current_floor):
            _current_floor += 1

        def goDown(_current_floor):
            _current_floor -= 1

    def solve(self):
        path = self.algo.discover_floor(self, 1, 1, self.goals[1])
        if path is None:
            print("No solutions found")
            return False
        print(f"Path: {path}")
        self.algo.visualize_path(self.floor, path)
        return True

    def checkGoal(self, goal=None):
        if goal is None:
            return self.agents[1].x == self.goals[1].x and self.agents[1].y == self.goals[1].y \
                and self.agents[1].floor == self.goals[1].floor
        else:
            return self.agents[1].x == goal.x and self.agents[1].y == goal.y \
                and self.agents[1].floor == goal.floor

    def checkKey(self):
        current_floor = self.floors[self.agents[1].floor]

        x = self.agents[1].x
        y = self.agents[1].y

        if current_floor[x][y].isKey == True:
            self.obtained_keys.append(current_floor[x][y][len(current_floor[x][y]) - 1][1])  # thêm số phòng

    def moveUp(self, current_agent):
        copyState = copy.deepcopy(self)
        copyState.setPrevious(self, current_agent)

        current_floor = copyState.agents[current_agent].floor
        old_x = copyState.agents[current_agent].x
        old_y = copyState.agents[current_agent].y

        x = copyState.stairs[(current_floor + 1, current_floor)].x
        y = copyState.stairs[(current_floor + 1, current_floor)].y

        copyState.floors[current_floor + 1].removeFromCell(old_x, old_y, "A1")
        copyState.floors[current_floor + 1].appendToCell(x, y, "A1")
        copyState.agents[current_agent] = self.Pos(current_floor+1,x,y)

    def moveDown(self, current_agent):
        copyState = copy.deepcopy(self)
        copyState.setPrevious(self, current_agent)

        current_floor = copyState.agents[current_agent].floor
        old_x = copyState.agents[current_agent].x
        old_y = copyState.agents[current_agent].y

        x = copyState.stairs[(current_floor - 1, current_floor)].x
        y = copyState.stairs[(current_floor - 1, current_floor)].y

        copyState.floors[current_floor - 1].removeFromCell(old_x, old_y, "A1")
        copyState.floors[current_floor - 1].appendToCell(x, y, "A1")
        copyState.agents[current_agent] = self.Pos(current_floor-1,x,y)

    def moveN(self, current_agent):
        copyState = copy.deepcopy(self)
        copyState.setPrevious(self, current_agent)

        current_floor = copyState.agents[current_agent].floor
        x = copyState.agents[current_agent].x
        y = copyState.agents[current_agent].y
        if x > 0 and copyState.floors[current_floor].checkValueInCell(x - 1,
                                                                      y, "-1") == False and copyState.floors[
            current_floor].getCell(x - 1, y).isAgent() == False:
            old_x, old_y = x, y
            x -= 1
            copyState.floors[current_floor].removeFromCell(old_x, old_y, "A1")
            copyState.floors[current_floor].appendToCell(x, y, "A1")
            copyState.agents[current_agent]=self.Pos(current_floor,x,y)
            return copyState
        return None

    def moveS(self, current_agent):
        copyState = copy.deepcopy(self)
        copyState.setPrevious(self, current_agent)

        current_floor = copyState.agents[current_agent].floor
        x = copyState.agents[current_agent].x
        y = copyState.agents[current_agent].y
        if y < copyState.floors[current_floor].rows - 1 and copyState.floors[current_floor].checkValueInCell(
                x + 1, y, "-1") == False and copyState.floors[current_floor].getCell(x + 1, y).isAgent() == False:
            old_x, old_y = x, y
            x += 1
            copyState.floors[current_floor].removeFromCell(old_x, old_y, "A1")
            copyState.floors[current_floor].appendToCell(x, y, "A1")
            copyState.agents[current_agent]=self.Pos(current_floor,x,y)
            return copyState
        return None

    def moveE(self, current_agent):
        copyState = copy.deepcopy(self)
        copyState.setPrevious(self, current_agent)

        current_floor = copyState.agents[current_agent].floor
        x = copyState.agents[current_agent].x
        y = copyState.agents[current_agent].y
        if y < copyState.floors[current_floor].cols - 1 and copyState.floors[current_floor].checkValueInCell(
                x, y + 1, "-1") == False and copyState.floors[current_floor].getCell(x, y + 1).isAgent() == False:
            old_x, old_y = x, y
            y += 1
            copyState.floors[current_floor].removeFromCell(old_x, old_y, "A1")
            copyState.floors[current_floor].appendToCell(x, y, "A1")
            copyState.agents[current_agent]=self.Pos(current_floor,x,y)
            return copyState
        return None

    def moveW(self, current_agent):
        copyState = copy.deepcopy(self)
        copyState.setPrevious(self, current_agent)

        current_floor = copyState.agents[current_agent].floor
        x = copyState.agents[current_agent].x
        y = copyState.agents[current_agent].y
        if y > 0 and copyState.floors[current_floor].checkValueInCell(x, y - 1, "-1") == False and copyState.floors[
            current_floor].getCell(x, y - 1).isAgent() == False == False:
            old_x, old_y = x, y
            y -= 1
            copyState.floors[current_floor].removeFromCell(old_x, old_y, "A1")
            copyState.floors[current_floor].appendToCell(x, y, "A1")
            copyState.agents[current_agent]=self.Pos(current_floor,x,y)
            return copyState
        return None

    def moveNE(self, current_agent):
        copyState = copy.deepcopy(self)
        copyState.setPrevious(self, current_agent)

        current_floor = copyState.agents[current_agent].floor
        x = copyState.agents[current_agent].x
        y = copyState.agents[current_agent].y

        destination_x = x - 1
        destination_y = y + 1

        # Check if the destination cell is within bounds and available
        if (
                destination_x >= 0 and destination_y < copyState.floors[current_floor].cols and
                copyState.floors[current_floor].checkValueInCell(destination_x, y, "-1") == False and
                copyState.floors[current_floor].checkValueInCell(x, destination_y, "-1") == False and
                copyState.floors[current_floor].checkValueInCell(destination_x, destination_y, "-1") == False and
                copyState.floors[current_floor].getCell(destination_x, y).isAgent() == False == False and
                copyState.floors[current_floor].getCell(x, destination_y).isAgent() == False == False and
                copyState.floors[current_floor].getCell(destination_x, destination_y).isAgent() == False == False
        ):
            old_x, old_y = x, y
            x, y = destination_x, destination_y

            # Remove value "A1" from the old cell
            copyState.floors[current_floor].removeFromCell(old_x, old_y, "A1")

            # Add value "A1" to the new cell
            copyState.floors[current_floor].appendToCell(x, y, "A1")
            copyState.agents[current_agent]=self.Pos(current_floor,x,y)
            return copyState
        return None

    def moveSE(self, current_agent):
        copyState = copy.deepcopy(self)
        copyState.setPrevious(self, current_agent)

        current_floor = copyState.agents[current_agent].floor
        x = copyState.agents[current_agent].x
        y = copyState.agents[current_agent].y
        destination_y = y + 1
        destination_x = x + 1

        # Check if the destination cell is within bounds and available
        if (
                destination_x < copyState.floors[current_floor].rows and destination_y < copyState.floors[
            current_floor].cols and
                copyState.floors[current_floor].checkValueInCell(destination_x, y, "-1") == False and
                copyState.floors[current_floor].checkValueInCell(x, destination_y, "-1") == False and
                copyState.floors[current_floor].checkValueInCell(destination_x, destination_y, "-1") == False and
                copyState.floors[current_floor].getCell(destination_x, y).isAgent() == False == False and
                copyState.floors[current_floor].getCell(x, destination_y).isAgent() == False == False and
                copyState.floors[current_floor].getCell(destination_x, destination_y).isAgent() == False == False
        ):
            old_x, old_y = x, y
            x, y = destination_x, destination_y

            # Remove value "A1" from the old cell
            copyState.floors[current_floor].removeFromCell(old_x, old_y, "A1")

            # Add value "A1" to the new cell
            copyState.floors[current_floor].appendToCell(x, y, "A1")
            copyState.agents[current_agent]=self.Pos(current_floor,x,y)
            return copyState
        return None

    def moveSW(self, current_agent):
        copyState = copy.deepcopy(self)
        copyState.setPrevious(self, current_agent)

        current_floor = copyState.agents[current_agent].floor
        x = copyState.agents[current_agent].x
        y = copyState.agents[current_agent].y
        destination_x = x + 1
        destination_y = y - 1

        # Check if the destination cell is within bounds and available
        if (
                destination_x < copyState.floors[current_floor].rows and destination_y >= 0 and
                copyState.floors[current_floor].checkValueInCell(destination_x, y, "-1") == False and
                copyState.floors[current_floor].checkValueInCell(x, destination_y, "-1") == False and
                copyState.floors[current_floor].checkValueInCell(destination_x, destination_y, "-1") == False
                and copyState.floors[current_floor].getCell(destination_x, y).isAgent() == False == False and
                copyState.floors[current_floor].getCell(x, destination_y).isAgent() == False == False and
                copyState.floors[current_floor].getCell(destination_x, destination_y).isAgent() == False == False
        ):
            old_x, old_y = x, y
            x, y = destination_x, destination_y

            # Remove value "A1" from the old cell
            copyState.floors[current_floor].removeFromCell(old_x, old_y, "A1")

            # Add value "A1" to the new cell
            copyState.floors[current_floor].appendToCell(x, y, "A1")
            copyState.agents[current_agent]=self.Pos(current_floor,x,y)
            return copyState
        return None

    def moveNW(self, current_agent):
        copyState = copy.deepcopy(self)
        copyState.setPrevious(self, current_agent)

        current_floor = copyState.agents[current_agent].floor
        x = copyState.agents[current_agent].x
        y = copyState.agents[current_agent].y
        destination_y = y - 1
        destination_x = x - 1

        # Check if the destination cell is within bounds and available
        if (
                destination_x >= 0 and destination_y >= 0 and
                copyState.floors[current_floor].checkValueInCell(destination_x, y, "-1") == False and
                copyState.floors[current_floor].checkValueInCell(x, destination_y, "-1") == False and
                copyState.floors[current_floor].checkValueInCell(destination_x, destination_y, "-1") == False
                and copyState.floors[current_floor].getCell(destination_x, y).isAgent() == False == False and
                copyState.floors[current_floor].getCell(x, destination_y).isAgent() == False == False and
                copyState.floors[current_floor].getCell(destination_x, destination_y).isAgent() == False == False
        ):
            old_x, old_y = x, y
            x, y = destination_x, destination_y

            # Remove value "A1" from the old cell
            copyState.floors[current_floor].removeFromCell(old_x, old_y, "A1")

            # Add value "A1" to the new cell
            copyState.floors[current_floor].appendToCell(x, y, "A1")
            copyState.agents[current_agent]=self.Pos(current_floor,x,y)
            return copyState
        return None

    def successors(self, current_agent):
        successors = [self.moveE(current_agent), self.moveW(current_agent), self.moveN(current_agent),
                      self.moveS(current_agent), self.moveSW(current_agent), self.moveSE(current_agent),
                      self.moveNE(current_agent), self.moveNW(current_agent)]
        return successors


class Task:
    def __init__(self, x, y, floor):
        self.floor = floor
        self.destinationX = x
        self.destinationY = y

    def set_task(self, x, y):
        if floor[x][y].isWall == False:
            self.destinationX = x
            self.destinationY = y
        else:
            print("Cannot set a task destination at a wall or an obstacle")
