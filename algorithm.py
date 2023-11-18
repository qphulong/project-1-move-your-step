import tkinter as tk
from graphical import root

class BFS:
    def BFS(self, start):
        visited = set()
        current_path = []
        frontier = [start] #queue

        while frontier:
            current_state = frontier.pop(0)

            if current_state is None:
                continue

            current_path.append((current_state.agent_Xposition, current_state.agent_Yposition))

            #check goal
            if current_state.checkGoal():
                break

            if current_state not in visited:
                visited.add(current_state)

                successors = current_state.successors()

                # Explore neighbors in reverse order to maintain LIFO behavior
                for successor in successors:
                    if successor is not None and successor not in visited:
                        frontier.append(successor)

        return current_path


    def visualize_path(self, floor, path):
        board_size = 8  # Define the size of the board
        cell_size = 50  # Define the size of each cell in pixels

        canvas = tk.Canvas(root, width=board_size * cell_size, height=board_size * cell_size)
        canvas.pack()

        # Draw the board
        for i in range(floor.rows):
            for j in range(floor.cols):
                x1 = j * cell_size
                y1 = i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=("black" if floor.table[i][j] == "-1" else "red" if (i,j) in path else "white"),
                    outline="grey"  # Specify the color of the border (here, "grey")
                )

                text_x = x1 + cell_size // 2
                text_y = y1 + cell_size // 2

                canvas.create_text(text_x, text_y,
                                   text=(floor.table[i][j] if floor.table[i][j].__contains__("A") or floor.table[i][
                                       j] == "T1" else "")
                                   , fill=(
                        "blue" if floor.table[i][j] == "T1" else "red" if floor.table[i][j].__contains__(
                            "A") else "white")
                                   , font=("Arial", 25))

        root.mainloop()

