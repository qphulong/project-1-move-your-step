from enum import Enum, auto
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

        self.goal_floor = None #floor with final goals

        self.keys = {}  # save position of keys for each rooms with a dictionary
        self.doors = {} # save positions of room doors
        self.agents = {} # initial positions of agents
        self.stairs = {}

        self.floors = [] # list of floors
        self.rooms = 0

        self.currentGoal = None # there are many goals, from smaller to the biggest (T1)

    def floor_rep(self):
        rep = tuple([tuple(self.agents), tuple(self.keys), tuple(self.agents)])
        return rep

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
                    pos = (current_floor, i - 2, j)
                    if str(row_values[j]).__contains__("A"):  # agent
                        agent_no = row_values[j][1]
                        self.agents[agent_no] = pos
                    elif str(row_values[j]) == "T1":
                        self.goal_floor = current_floor
                        self.goal_Xposition = i - 2
                        self.goal_Yposition = j
                    elif str(row_values[j].__contains__("K")):  # key
                        key_no = row_values[j][1]
                        self.keys[key_no] = pos
                    elif str(row_values[j].__contains__("D")):  # door
                        door_no = row_values[j][1]
                        self.doors[door_no] = pos
                        self.rooms += 1
                    elif str(row_values[j])=="UP" or str(row_values[j])=="DOWN":
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
        path = self.bfs.BFS_Level2(self)[1]
        if path is None:
            print("No solutions found")
            return False
        print(f"Path: {path}")
        self.bfs.visualize_path(self.floor, path)
        return True



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