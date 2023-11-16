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

    def moveN(self):
        if self.agent_Yposition > 0 and self.floor.checkValueInCell(self.agent_Yposition-1, self.agent_Xposition, "-1")==False:
            old_y, old_x = self.agent_Yposition, self.agent_Xposition
            self.agent_Yposition -= 1
            self.floor.removeFromCell(old_y, old_x, "A1")
            self.floor.appendToCell(self.agent_Yposition, self.agent_Xposition, "A1")
    
    def moveS(self):
        if self.agent_Yposition < self.floor.rows - 1 and self.floor.checkValueInCell(self.agent_Yposition + 1, self.agent_Xposition, "-1") == False:
            old_y, old_x = self.agent_Yposition, self.agent_Xposition
            self.agent_Yposition += 1
            self.floor.removeFromCell(old_y, old_x, "A1")
            self.floor.appendToCell(self.agent_Yposition, self.agent_Xposition, "A1")

    def moveE(self):
        if self.agent_Xposition < self.floor.cols - 1 and self.floor.checkValueInCell(self.agent_Yposition, self.agent_Xposition + 1, "-1") == False:
            old_y, old_x = self.agent_Yposition, self.agent_Xposition
            self.agent_Xposition += 1
            self.floor.removeFromCell(old_y, old_x, "A1")
            self.floor.appendToCell(self.agent_Yposition, self.agent_Xposition, "A1")

    def moveW(self):
        if self.agent_Xposition > 0 and self.floor.checkValueInCell(self.agent_Yposition, self.agent_Xposition - 1, "-1") == False:
            old_y, old_x = self.agent_Yposition, self.agent_Xposition
            self.agent_Xposition -= 1
            self.floor.removeFromCell(old_y, old_x, "A1")
            self.floor.appendToCell(self.agent_Yposition, self.agent_Xposition, "A1")

    
    def moveNE(self):
        return
    
    def moveNW(self):
        return
    
    def moveSE(self):
        return
    
    def moveSW(self):
        return
    
    def __del__(self):
        pass


#Duoi nay la test code
m = Level1()
m.getInputFile("input//input1-level1.txt")
m.moveN()
m.printSelf()