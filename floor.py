
import tkinter as tk
from graphical import root

class Cell:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.values = []

    def appendValue(self, value):
        self.values.append(value)

    def removeValue(self, value):
        self.values.remove(value)
        
    def checkValue(self, value):
        return value in self.values

    def calculateManhattanFrom(self, Cell):
        return abs(self.x - Cell.x) + abs(self.y - Cell.y)

    def getValue(self):
        return self.values[len(self.values)-1]
    
    def isWall(self):
        return "-1" in self.values

    def isAgent(self):
        return any('A' in value for value in self.values)

    def isGoal(self):
        return "T1" in self.values

    def isKey(self):
        return any('K' in value for value in self.values)

    def isDoor(self):
        return any('D' in value for value in self.values)

    def __del__(self):
        pass

class Floor:
    def __init__(self,rows,cols):
        self.rows=rows
        self.cols=cols
        self.table = [[Cell(i, j) for j in range(cols)] for i in range(rows)]

    def appendToCell(self, row, col, value):
        self.table[row][col].appendValue(value)

    def removeFromCell(self, row, col, value):
        if self.table[row][col].checkValue(value):
            self.table[row][col].removeValue(value)

    def checkValueInCell(self, row, col, value):
        return self.table[row][col].checkValue(value)
    
    def getCell(self, row, col):
        return self.table[row][col]


    # cai function nay de debug trong console thoi
    def printSelf(self):
        board_size = 8  # Define the size of the board
        cell_size = 50  # Define the size of each cell in pixels

        canvas = tk.Canvas(root, width=board_size * cell_size, height=board_size * cell_size)
        canvas.pack()

        # Draw the board
        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j * cell_size
                y1 = i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=("black" if self.table[i][j] == "-1" else "white"),
                    outline="grey"  # Specify the color of the border (here, "grey")
                )

                text_x = x1 + cell_size // 2
                text_y = y1 + cell_size // 2

                canvas.create_text(text_x, text_y,
                                   text=(self.table[i][j] if self.table[i][j].checkValue() or self.table[i][j] == "T1" else "")
                                   , fill=(
                        "blue" if self.table[i][j] == "T1" else "red" if self.table[i][j].__contains__("A") else "white")
                                   , font=("Arial", 25))

        root.mainloop()
