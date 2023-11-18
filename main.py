import floor
import tkinter as tk

root = tk.Tk()
root.title("Move Your Step")

# Open the file in read mode
with open('input/input1-level1.txt', 'r') as file:
    size_info = file.readline().strip().split(',')
    m,n = map(int, size_info)

    # Read the second line describing the floor index
    floor_info = file.readline().strip()

    # Read the grid layout
    map = []
    for _ in range(m):
        line = file.readline().strip().split(',')
        map.append(line)

# Display the information read from the file
print(f"Number of rows: {m}")
print(f"Number of columns: {n}")
print(f"Floor Information: {floor_info}")

board_size = 8  # Define the size of the board
cell_size = 50  # Define the size of each cell in pixels

canvas = tk.Canvas(root, width=board_size*cell_size, height=board_size*cell_size)
canvas.pack()

# Draw the board
for i in range(m):
    for j in range(n):
        x1 = j * cell_size
        y1 = i * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size

        canvas.create_rectangle(x1, y1, x2, y2, fill=("black" if map[i][j] == "-1" else "white"))

        text_x = x1 + cell_size // 2
        text_y = y1 + cell_size // 2
        canvas.create_text(text_x, text_y, text=("T" if map[i][j] == "T" else "A" if map[i][j] == "A" else ""), fill=("blue" if map[i][j] == "T" else "red" if map[i][j] == "A" else "white"), font=("Arial", 10))

# Run the Tkinter main loop
root.mainloop()

