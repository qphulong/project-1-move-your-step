import tkinter as tk

from graphical import root


class Floor:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.table = [[[] for _ in range(cols)] for _ in range(rows)]

    def appendToCell(self, row, col, value): #save values on the map
        self.table[row][col] = value

    def removeFromCell(self, row, col, value):
        if self.table[row][col] == value:
            self.table[row][col] = ''

    def checkValueInCell(self, row, col, value):
        return value == self.table[row][col]

    def checkGoal(self):
        return False

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
                                   text=(self.table[i][j] if self.table[i][j].__contains__("A") or self.table[i][j] == "T1" else "")
                                   , fill=(
                        "blue" if self.table[i][j] == "T1" else "red" if self.table[i][j].__contains__("A") else "white")
                                   , font=("Arial", 25))

        root.mainloop()
