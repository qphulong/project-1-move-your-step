import floor
from algorithm import Algorithm
import copy
import tkinter as tk

class Level1:
    def __init__(self):
        self.floor = None
        self.agent_Xposition = None
        self.agent_Yposition = None
        self.goal_Xposition = None
        self.goal_Yposition = None

        self.algo = Algorithm()

        self.previous = None

        self.moves = 0

    def __hash__(self):
        return hash(self.floor_rep())

    def __lt__(self, other):
        return self.moves < other.moves

    def floor_rep(self):
        rep = (self.agent_Xposition, self.agent_Yposition)
        return rep

    def getInputFile(self, filePath):
        with open(filePath, "r") as file:
            lines = file.readlines()

        rows, cols = map(int, lines[0].strip().split(","))
        self.floor = floor.Floor(rows, cols)

        for i in range(2, len(lines)):
            row_values = list(map(str, lines[i].strip().split(",")))
            for j in range(cols):
                if str(row_values[j]) == "A1":
                    self.agent_Xposition = i - 2
                    self.agent_Yposition = j
                elif str(row_values[j]) == "T1":
                    self.goal_Xposition = i - 2
                    self.goal_Yposition = j
                self.floor.appendToCell(
                    i - 2, j, row_values[j]
                )  # set value for the board cell

    def printSelf(self):
        print("Agent X: " + str(self.agent_Xposition))
        print("Agent Y: " + str(self.agent_Yposition))
        self.floor.printSelf()

    def checkGoal(self):
        return (
            self.agent_Xposition == self.goal_Xposition
            and self.agent_Yposition == self.goal_Yposition
        )

    def setPrevious(self, prev):
        self.previous = prev
        self.moves = prev.moves + 1

    def moveN(self):
        copyState = copy.copy(self)
        copyState.setPrevious(self)

        if (
            copyState.agent_Xposition > 0
            and copyState.floor.checkValueInCell(
                copyState.agent_Xposition - 1, copyState.agent_Yposition, "-1"
            )
            == False
        ):
            old_x, old_y = copyState.agent_Xposition, copyState.agent_Yposition
            copyState.agent_Xposition -= 1
            copyState.floor.removeFromCell(old_x, old_y, "A1")
            copyState.floor.appendToCell(
                copyState.agent_Xposition, copyState.agent_Yposition, "A1"
            )
            return copyState
        return None

    def moveS(self):
        copyState = copy.copy(self)
        copyState.setPrevious(self)

        if (
            copyState.agent_Xposition < copyState.floor.rows - 1
            and copyState.floor.checkValueInCell(
                copyState.agent_Xposition + 1, copyState.agent_Yposition, "-1"
            )
            == False
        ):
            old_x, old_y = copyState.agent_Xposition, copyState.agent_Yposition
            copyState.agent_Xposition += 1
            copyState.floor.removeFromCell(old_x, old_y, "A1")
            copyState.floor.appendToCell(
                copyState.agent_Xposition, copyState.agent_Yposition, "A1"
            )
            return copyState
        return None

    def moveE(self):
        copyState = copy.copy(self)
        copyState.setPrevious(self)

        if (
            copyState.agent_Yposition < copyState.floor.cols - 1
            and copyState.floor.checkValueInCell(
                copyState.agent_Xposition, copyState.agent_Yposition + 1, "-1"
            )
            == False
        ):
            old_x, old_y = copyState.agent_Xposition, copyState.agent_Yposition
            copyState.agent_Yposition += 1
            copyState.floor.removeFromCell(old_x, old_y, "A1")
            copyState.floor.appendToCell(
                copyState.agent_Xposition, copyState.agent_Yposition, "A1"
            )
            return copyState
        return None

    def moveW(self):
        copyState = copy.copy(self)
        copyState.setPrevious(self)

        if (
            copyState.agent_Yposition > 0
            and copyState.floor.checkValueInCell(
                copyState.agent_Xposition, copyState.agent_Yposition - 1, "-1"
            )
            == False
        ):
            old_x, old_y = copyState.agent_Xposition, copyState.agent_Yposition
            copyState.agent_Yposition -= 1
            copyState.floor.removeFromCell(old_x, old_y, "A1")
            copyState.floor.appendToCell(
                copyState.agent_Xposition, copyState.agent_Yposition, "A1"
            )
            return copyState
        return None

    def moveNE(self):
        copyState = copy.copy(self)
        copyState.setPrevious(self)

        destination_x = copyState.agent_Xposition - 1
        destination_y = copyState.agent_Yposition + 1

        # Check if the destination cell is within bounds and available
        if (
            destination_x >= 0
            and destination_y < copyState.floor.cols
            and copyState.floor.checkValueInCell(
                destination_x, copyState.agent_Yposition, "-1"
            )
            == False
            and copyState.floor.checkValueInCell(
                copyState.agent_Xposition, destination_y, "-1"
            )
            == False
            and copyState.floor.checkValueInCell(destination_x, destination_y, "-1")
            == False
        ):
            old_x, old_y = copyState.agent_Xposition, copyState.agent_Yposition
            copyState.agent_Xposition, copyState.agent_Yposition = (
                destination_x,
                destination_y,
            )

            # Remove value "A1" from the old cell
            copyState.floor.removeFromCell(old_x, old_y, "A1")

            # Add value "A1" to the new cell
            copyState.floor.appendToCell(
                copyState.agent_Xposition, copyState.agent_Yposition, "A1"
            )
            return copyState
        return None

    def moveSE(self):
        copyState = copy.copy(self)
        copyState.setPrevious(self)

        destination_y = copyState.agent_Yposition + 1
        destination_x = copyState.agent_Xposition + 1

        # Check if the destination cell is within bounds and available
        if (
            destination_x < copyState.floor.rows
            and destination_y < copyState.floor.cols
            and copyState.floor.checkValueInCell(
                destination_x, copyState.agent_Yposition, "-1"
            )
            == False
            and copyState.floor.checkValueInCell(
                copyState.agent_Xposition, destination_y, "-1"
            )
            == False
            and copyState.floor.checkValueInCell(destination_x, destination_y, "-1")
            == False
        ):
            old_x, old_y = copyState.agent_Xposition, copyState.agent_Yposition
            copyState.agent_Xposition, copyState.agent_Yposition = (
                destination_x,
                destination_y,
            )

            # Remove value "A1" from the old cell
            copyState.floor.removeFromCell(old_x, old_y, "A1")

            # Add value "A1" to the new cell
            copyState.floor.appendToCell(
                copyState.agent_Xposition, copyState.agent_Yposition, "A1"
            )
            return copyState
        return None

    def moveSW(self):
        copyState = copy.copy(self)
        copyState.setPrevious(self)

        destination_x = copyState.agent_Xposition + 1
        destination_y = copyState.agent_Yposition - 1

        # Check if the destination cell is within bounds and available
        if (
            destination_x < copyState.floor.rows
            and destination_y >= 0
            and copyState.floor.checkValueInCell(
                destination_x, copyState.agent_Yposition, "-1"
            )
            == False
            and copyState.floor.checkValueInCell(
                copyState.agent_Xposition, destination_y, "-1"
            )
            == False
            and copyState.floor.checkValueInCell(destination_x, destination_y, "-1")
            == False
        ):
            old_x, old_y = copyState.agent_Xposition, copyState.agent_Yposition
            copyState.agent_Xposition, copyState.agent_Yposition = (
                destination_x,
                destination_y,
            )

            # Remove value "A1" from the old cell
            copyState.floor.removeFromCell(old_x, old_y, "A1")

            # Add value "A1" to the new cell
            copyState.floor.appendToCell(
                copyState.agent_Xposition, copyState.agent_Yposition, "A1"
            )
            return copyState
        return None

    def moveNW(self):
        copyState = copy.copy(self)
        copyState.setPrevious(self)

        destination_y = copyState.agent_Yposition - 1
        destination_x = copyState.agent_Xposition - 1

        # Check if the destination cell is within bounds and available
        if (
            destination_x >= 0
            and destination_y >= 0
            and copyState.floor.checkValueInCell(
                destination_x, copyState.agent_Yposition, "-1"
            )
            == False
            and copyState.floor.checkValueInCell(
                copyState.agent_Xposition, destination_y, "-1"
            )
            == False
            and copyState.floor.checkValueInCell(destination_x, destination_y, "-1")
            == False
        ):
            old_x, old_y = copyState.agent_Xposition, copyState.agent_Yposition
            copyState.agent_Xposition, copyState.agent_Yposition = (
                destination_x,
                destination_y,
            )

            # Remove value "A1" from the old cell
            copyState.floor.removeFromCell(old_x, old_y, "A1")

            # Add value "A1" to the new cell
            copyState.floor.appendToCell(
                copyState.agent_Xposition, copyState.agent_Yposition, "A1"
            )
            return copyState
        return None

    def successors(self):
        successors = [
            self.moveE(),
            self.moveW(),
            self.moveN(),
            self.moveS(),
            self.moveSW(),
            self.moveSE(),
            self.moveNE(),
            self.moveNW(),
        ]
        return successors

    def __del__(self):
        pass

    def visualize_path(self, start_x, start_y, goal_x, goal_y, floor, path):

        root = tk.Tk()
        board_size = 30  # Define the size of the board
        cell_size = 20  # Define the size of each cell in pixels

        canvas = tk.Canvas(root, width=board_size * cell_size, height=board_size * cell_size)
        canvas.pack()

        score = tk.Label(root, font=('Arial', 25), text='Score: '+str(len(path)-1), fg='Black')
        score.place(x=floor.cols*13, y=floor.rows*23)

        # Draw the board
        for i in range(floor.rows):
            for j in range(floor.cols):
                x1 = j * cell_size
                y1 = i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=(
                        "black" if floor.table[i][j].checkValue("-1") else "green" if (i, j) in path else "white"),
                    outline="grey"  # Specify the color of the border (here, "grey")
                )

                text_x = x1 + cell_size // 2
                text_y = y1 + cell_size // 2

                canvas.create_text(text_x, text_y,
                                   text=(
                                       "A1" if i == start_x and j == start_y else "T1" if i == goal_x and j == goal_y else "")
                                   , fill=(
                        "blue" if i == goal_x and j == goal_y else "red" if i == start_x and j == start_y else "white")
                                   , font=("Arial", 10))

        # export_heatmap(root)
        root.mainloop()

    def solve(self,num):
        if num == 1: path = self.algo.AStar_Level1(self)[1]
        if num == 2: path = self.algo.UCS_Level1(self)[1]
        if num == 3: path = self.algo.BFS_Level1(self)[1]
        start_x = self.agent_Xposition
        start_y = self.agent_Yposition
        goal_x = self.goal_Xposition
        goal_y = self.goal_Yposition
        if path is None:
            print("No solutions found")
            return False
        print(f"Path: {path}")
        self.visualize_path(start_x, start_y, goal_x, goal_y, self.floor, path)
        return True


# myLevel1 = Level1()
# myLevel1.getInputFile("input//input5-level1.txt")
# myLevel1.solve()