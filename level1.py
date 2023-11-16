import floor

class Level1:
    def __init__(self):
        self.floor = None
        self.agent_Yposition = None
        self.agent_Xposition = None
        
    def getInputFile(self,filePath):
        with open (filePath, "r") as file:
            lines = file.readlines()
        
        rows, cols = map(int, lines[0].strip().split(','))
        self.floor=floor.Floor(rows, cols)
        
        for i in range(2, len(lines)):
            row_values = list(map(str, lines[i].strip().split(',')))
            for j in range(cols):
                if str(row_values[j])=="A1":
                    self.floor.appendToCell(i-2, j, "0")
                    self.agent_Yposition = i-2
                    self.agent_Xposition = j
                self.floor.appendToCell(i-2, j, row_values[j])

    def printSelf(self):
        self.floor.printSelf()
        print(self.agent_Yposition, self.agent_Xposition)
    
    def __del__(self):
        pass


#Duoi nay la test code
m = Level1()
m.getInputFile("input//input1-level1.txt")
m.floor.appendToCell(2,2,"A")
m.floor.removeFromCell(2,2,"0")
m.printSelf()