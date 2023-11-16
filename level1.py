import floor

class Level1:
    def __init__(self):
        self.floor = None
        
    def getInputFile(self,filePath):
        with open (filePath, "r") as file:
            lines = file.readlines()
        
        rows, cols = map(int, lines[0].strip().split(','))
        self.floor=floor.Floor(rows, cols)
        
        for i in range(2, len(lines)):
            row_values = list(map(str, lines[i].strip().split(',')))
            for j in range(cols):
                self.floor.table[i-2][j] += str(row_values[j])

    def printSelf(self):
        self.floor.printSelf()
    
    def __del__(self):
        pass
