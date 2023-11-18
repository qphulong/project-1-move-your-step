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
                    self.agent_Yposition = i-2
                    self.agent_Xposition = j
                self.floor.appendToCell(i-2, j, row_values[j]) #set value for the board cell

    def printSelf(self):
        print("Agent Y: "+str(self.agent_Yposition))
        print("Agent X: "+str(self.agent_Xposition))
        self.floor.printSelf()

    def moveN(self):
        copy = Level1(self)

        if self.agent_Yposition > 0 and self.floor.checkValueInCell(self.agent_Yposition-1, self.agent_Xposition, "-1")==False:
            old_y, old_x = self.agent_Yposition, self.agent_Xposition
            self.agent_Yposition -= 1
            self.floor.removeFromCell(old_y, old_x, "A1")
            self.floor.appendToCell(self.agent_Yposition, self.agent_Xposition, "A1")
            return copy
        return None
    
    def moveS(self):
        copy = Level1(self)

        if self.agent_Yposition < self.floor.rows - 1 and self.floor.checkValueInCell(self.agent_Yposition + 1, self.agent_Xposition, "-1") == False:
            old_y, old_x = self.agent_Yposition, self.agent_Xposition
            self.agent_Yposition += 1
            self.floor.removeFromCell(old_y, old_x, "A1")
            self.floor.appendToCell(self.agent_Yposition, self.agent_Xposition, "A1")
            return copy
        return None

    def moveE(self):
        copy = Level1(self)

        if self.agent_Xposition < self.floor.cols - 1 and self.floor.checkValueInCell(self.agent_Yposition, self.agent_Xposition + 1, "-1") == False:
            old_y, old_x = self.agent_Yposition, self.agent_Xposition
            self.agent_Xposition += 1
            self.floor.removeFromCell(old_y, old_x, "A1")
            self.floor.appendToCell(self.agent_Yposition, self.agent_Xposition, "A1")
            return copy
        return None

    def moveW(self):
        copy = Level1(self)

        if self.agent_Xposition > 0 and self.floor.checkValueInCell(self.agent_Yposition, self.agent_Xposition - 1, "-1") == False:
            old_y, old_x = self.agent_Yposition, self.agent_Xposition
            self.agent_Xposition -= 1
            self.floor.removeFromCell(old_y, old_x, "A1")
            self.floor.appendToCell(self.agent_Yposition, self.agent_Xposition, "A1")
            return copy
        return None

    def moveNE(self):
        copy = Level1(self)

        destination_y = self.agent_Yposition - 1
        destination_x = self.agent_Xposition + 1

        # Check if the destination cell is within bounds and available
        if (
            destination_y >= 0 and destination_x < self.floor.cols and
            self.floor.checkValueInCell(destination_y, self.agent_Xposition, "-1") == False and
            self.floor.checkValueInCell(self.agent_Yposition, destination_x, "-1") == False and
            self.floor.checkValueInCell(destination_y, destination_x, "-1") == False
        ):
            old_y, old_x = self.agent_Yposition, self.agent_Xposition
            self.agent_Yposition, self.agent_Xposition = destination_y, destination_x

            # Remove value "A1" from the old cell
            self.floor.removeFromCell(old_y, old_x, "A1")

            # Add value "A1" to the new cell
            self.floor.appendToCell(self.agent_Yposition, self.agent_Xposition, "A1")
            return copy
        return None

    
    def moveSE(self):
        copy = Level1(self)

        destination_y = self.agent_Yposition + 1
        destination_x = self.agent_Xposition + 1

        # Check if the destination cell is within bounds and available
        if (
            destination_y < self.floor.rows and destination_x < self.floor.cols and
            self.floor.checkValueInCell(destination_y, self.agent_Xposition, "-1") == False and
            self.floor.checkValueInCell(self.agent_Yposition, destination_x, "-1") == False and
            self.floor.checkValueInCell(destination_y, destination_x, "-1") == False
        ):
            old_y, old_x = self.agent_Yposition, self.agent_Xposition
            self.agent_Yposition, self.agent_Xposition = destination_y, destination_x

            # Remove value "A1" from the old cell
            self.floor.removeFromCell(old_y, old_x, "A1")

            # Add value "A1" to the new cell
            self.floor.appendToCell(self.agent_Yposition, self.agent_Xposition, "A1")
            return copy
        return None


    def moveSW(self):
        copy = Level1(self)

        destination_y = self.agent_Yposition + 1
        destination_x = self.agent_Xposition - 1

        # Check if the destination cell is within bounds and available
        if (
            destination_y < self.floor.rows and destination_x >= 0 and
            self.floor.checkValueInCell(destination_y, self.agent_Xposition, "-1") == False and
            self.floor.checkValueInCell(self.agent_Yposition, destination_x, "-1") == False and
            self.floor.checkValueInCell(destination_y, destination_x, "-1") == False
        ):
            old_y, old_x = self.agent_Yposition, self.agent_Xposition
            self.agent_Yposition, self.agent_Xposition = destination_y, destination_x

            # Remove value "A1" from the old cell
            self.floor.removeFromCell(old_y, old_x, "A1")

            # Add value "A1" to the new cell
            self.floor.appendToCell(self.agent_Yposition, self.agent_Xposition, "A1")
            return copy
        return None


    def moveNW(self):
        copy = Level1(self)

        destination_y = self.agent_Yposition - 1
        destination_x = self.agent_Xposition - 1

        # Check if the destination cell is within bounds and available
        if (
            destination_y >= 0 and destination_x >= 0 and
            self.floor.checkValueInCell(destination_y, self.agent_Xposition, "-1") == False and
            self.floor.checkValueInCell(self.agent_Yposition, destination_x, "-1") == False and
            self.floor.checkValueInCell(destination_y, destination_x, "-1") == False
        ):
            old_y, old_x = self.agent_Yposition, self.agent_Xposition
            self.agent_Yposition, self.agent_Xposition = destination_y, destination_x

            # Remove value "A1" from the old cell
            self.floor.removeFromCell(old_y, old_x, "A1")

            # Add value "A1" to the new cell
            self.floor.appendToCell(self.agent_Yposition, self.agent_Xposition, "A1")
            return copy
        return None

    def successors(self):
        if user_input == '1':
            m.moveSW()
        elif user_input == '2':
            m.moveS()
        elif user_input == '3':
            m.moveSE()
        elif user_input == '4':
            m.moveW()
        elif user_input == '6':
            m.moveE()
        elif user_input == '7':
            m.moveNW()
        elif user_input == '8':
            m.moveN()
        elif user_input == '9':
            m.moveNE()
        successors = [self.moveE(),self.moveW(),self.moveN(),self.moveS(),self.moveSW(),self.moveSE(),self.moveNE(),self.moveNW()]
        return successors

    
    def __del__(self):
        pass


#Duoi nay la test code
m = Level1()
m.getInputFile("input//input1-level1.txt")

while True:
    m.printSelf()  # Print the table each loop
    user_input = input("Enter 1 to move SW, 2 to move S, 3 to move SE, 4 to move W, 6 to move E, 7 to move NW, 8 to move N, 9 to move NE, or 'q' to quit: ")

    if user_input == 'q':
        break  # Exit the loop if the user enters 'q'
    elif user_input in {'1', '2', '3', '4', '6', '7', '8', '9'}:
        # Move the agent based on user input
        if user_input == '1':
            m.moveSW()
        elif user_input == '2':
            m.moveS()
        elif user_input == '3':
            m.moveSE()
        elif user_input == '4':
            m.moveW()
        elif user_input == '6':
            m.moveE()
        elif user_input == '7':
            m.moveNW()
        elif user_input == '8':
            m.moveN()
        elif user_input == '9':
            m.moveNE()
    else:
        print("Invalid input. Please enter 1, 2, 3, 4, 6, 7, 8, 9, or 'q'.")

