from level1 import Level1


class Level2(Level1):
    def __init__(self):
        super.__init__()
        self.keys = {} # save position of a key with a dictionary
        self.rooms = 0
    def solve(self):
        path = self.bfs.BFS_Level2(self)[1]
        if path is None:
            print("No solutions found")
            return False
        print(f"Path: {path}")
        self.bfs.visualize_path(self.floor,path)
        return True