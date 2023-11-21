import floor
from level1 import Level1

class Level4(Level1):
    def __init__(self):
        super.__init__()

        self.agent_Xposition = None
        self.agent_Yposition = None

        self.keys = {}  # save position of keys for each rooms with a dictionary
        self.doors = {} # save positions of room doors
        self.agents = {} # initial positions of agents
        self.rooms = 0

    def floor_rep(self):
        rep = (tuple(self.agents), tuple(self.keys))
        return rep

    def getInputFile(self, filePath):
        with open(filePath, "r") as file:
            lines = file.readlines()

        rows, cols = map(int, lines[0].strip().split(','))
        self.floor = floor.Floor(rows, cols)

        for i in range(2, len(lines)):
            row_values = list(map(str, lines[i].strip().split(',')))
            for j in range(cols):
                if str(row_values[j]).__contains__("A"): # agent
                    agent_no = row_values[j][1]
                    self.agents[agent_no] = (i - 2, j)
                elif str(row_values[j]) == "T1":
                    self.goal_Xposition = i - 2
                    self.goal_Yposition = j
                elif str(row_values[j].__contains__("K")): # key
                    key_no = row_values[j][1]
                    self.keys[key_no] = (i - 2, j)
                elif str(row_values[j].__contains__("D")): # door
                    door_no = row_values[j][1]
                    self.doors[door_no] = (i - 2, j)
                    self.rooms+=1
                self.floor.appendToCell(i - 2, j, row_values[j])  # set value for the board cell

    def solve(self):
        path = self.bfs.BFS_Level2(self)[1]
        if path is None:
            print("No solutions found")
            return False
        print(f"Path: {path}")
        self.bfs.visualize_path(self.floor, path)
        return True