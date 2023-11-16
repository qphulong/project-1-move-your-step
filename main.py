# import tkinter as tk

# class SquareDrawer:
#     def __init__(self, master):
#         self.master = master
#         master.title("Simple Square Drawer")

#         # Canvas to draw the square
#         self.canvas = tk.Canvas(master, width=200, height=200)
#         self.canvas.pack()

#         # Button to trigger square drawing
#         draw_button = tk.Button(master, text="Draw Square", command=self.draw_square)
#         draw_button.pack()

#     def draw_square(self):
#         # Coordinates for the square (top-left and bottom-right)
#         x1, y1 = 50, 50
#         x2, y2 = 150, 150

#         # Draw the square on the canvas
#         self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="blue")

# # Create the main window
# root = tk.Tk()
# app = SquareDrawer(root)
# root.mainloop()

import floor
import tkinter as tk

root = tk.Tk()
root.title("Move Your Step")

# input này để test thử
m = int(input("Input m: "))
n = int(input("Input n: "))


map = [[0 for _ in range(n)] for _ in range(m)]

for i in range (0,m):
    for j in range (0, n):
        map[i][j]=input(f"Insert for {i},{j}: ")

board_size = 8  # Define the size of the board
cell_size = 50  # Define the size of each cell in pixels

canvas = tk.Canvas(root, width=board_size*cell_size, height=board_size*cell_size)
canvas.pack()

# Draw the board
for i in range(board_size):
    for j in range(board_size):
        x1 = j * cell_size
        y1 = i * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size

        canvas.create_rectangle(x1, y1, x2, y2, fill=("black" if map[i][j] == "1" else "white"))

        text_x = x1 + cell_size // 2
        text_y = y1 + cell_size // 2
        canvas.create_text(text_x, text_y, text=("T" if map[i][j] == "T" else "A" if map[i][j] == "A" else ""), fill=("blue" if map[i][j] == "T" else "red" if map[i][j] == "A" else "white"), font=("Arial", 10))

# Run the Tkinter main loop
root.mainloop()