import tkinter as tk

class SquareDrawer:
    def __init__(self, master):
        self.master = master
        master.title("Simple Square Drawer")

        # Canvas to draw the square
        self.canvas = tk.Canvas(master, width=200, height=200)
        self.canvas.pack()

        # Button to trigger square drawing
        draw_button = tk.Button(master, text="Draw Square", command=self.draw_square)
        draw_button.pack()

    def draw_square(self):
        # Coordinates for the square (top-left and bottom-right)
        x1, y1 = 50, 50
        x2, y2 = 150, 150

        # Draw the square on the canvas
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="blue")

# Create the main window
root = tk.Tk()
app = SquareDrawer(root)
root.mainloop()
