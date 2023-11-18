import floor
from algorithm import BFS
import copy

class Level1:
    def __init__(self):
        self.floor = None
        self.agent_Xposition = None
        self.agent_Yposition = None
        self.goal_Xposition = None
        self.goal_Yposition = None

        self.bfs = BFS()
        self.previous = None

    def __hash__(self):
        tuple_array = [tuple(inner_list) for inner_list in self.floor.table]

        hashed = tuple(set(tuple_array))
        return hash(hashed)
        
    def getInputFile(self,filePath):
        with open (filePath, "r") as file:
            lines = file.readlines()
        
        rows, cols = map(int, lines[0].strip().split(','))
        self.floor=floor.Floor(rows, cols)
        
        for i in range(2, len(lines)):
            row_values = list(map(str, lines[i].strip().split(',')))
            for j in range(cols):
                if str(row_values[j])=="A1":
                    self.agent_Xposition = i-2
                    self.agent_Yposition = j
                elif str(row_values[j])=="T1":
                    self.goal_Xposition = i-2
                    self.goal_Yposition = j
                self.floor.appendToCell(i-2, j, row_values[j]) #set value for the board cell


    def printSelf(self):
        print("Agent X: "+str(self.agent_Xposition))
        print("Agent Y: "+str(self.agent_Yposition))
        self.floor.printSelf()

    def checkGoal(self):
        return self.agent_Xposition == self.goal_Xposition and self.agent_Yposition == self.goal_Yposition

    def setPrevious(self,prev):
        self.previous = prev

    def moveN(self):
        copyState = copy.deepcopy(self)
        copyState.setPrevious(self)

        if self.agent_Xposition > 0 and self.floor.checkValueInCell(self.agent_Xposition-1, self.agent_Yposition, "-1")==False:
            old_x, old_y = self.agent_Yposition, self.agent_Xposition
            self.agent_Xposition -= 1
            self.floor.removeFromCell(old_x, old_y, "A1")
            self.floor.appendToCell(self.agent_Xposition, self.agent_Yposition, "A1")
            return copyState
        return None
    
    def moveS(self):
        copyState = copy.deepcopy(self)
        copyState.setPrevious(self)

        if copyState.agent_Xposition < copyState.floor.rows - 1 and copyState.floor.checkValueInCell(copyState.agent_Xposition + 1, copyState.agent_Yposition, "-1") == False:
            old_x, old_y = copyState.agent_Xposition, copyState.agent_Yposition
            copyState.agent_Xposition += 1
            copyState.floor.removeFromCell(old_x, old_y, "A1")
            copyState.floor.appendToCell(copyState.agent_Xposition, copyState.agent_Yposition, "A1")
            return copyState
        return None

    def moveE(self):
        copyState = copy.deepcopy(self)
        copyState.setPrevious(self)

        if copyState.agent_Yposition < copyState.floor.cols - 1 and copyState.floor.checkValueInCell(copyState.agent_Xposition, copyState.agent_Yposition + 1, "-1") == False:
            old_x, old_y = copyState.agent_Xposition, copyState.agent_Yposition
            copyState.agent_Yposition += 1
            copyState.floor.removeFromCell(old_x, old_y, "A1")
            copyState.floor.appendToCell(copyState.agent_Xposition, copyState.agent_Yposition, "A1")
            return copyState
        return None

    def moveW(self):
        copyState = copy.deepcopy(self)
        copyState.setPrevious(self)

        if copyState.agent_Yposition > 0 and copyState.floor.checkValueInCell(copyState.agent_Xposition, copyState.agent_Yposition - 1, "-1") == False:
            old_x, old_y = copyState.agent_Xposition, copyState.agent_Yposition
            copyState.agent_Yposition -= 1
            copyState.floor.removeFromCell(old_x, old_y, "A1")
            copyState.floor.appendToCell(copyState.agent_Xposition, copyState.agent_Yposition, "A1")
            return copyState
        return None

    def moveNE(self):
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

    
    def moveSE(self):
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


    def moveSW(self):
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


    def moveNW(self):
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

    def successors(self):
        successors = [self.moveE(),self.moveW(),self.moveN(),self.moveS(),self.moveSW(),self.moveSE(),self.moveNE(),self.moveNW()]
        return successors

    
    def __del__(self):
        pass

    def solve(self):
        path = self.bfs.BFS(self)
        self.bfs.visualize_path(self,path,8,50)



