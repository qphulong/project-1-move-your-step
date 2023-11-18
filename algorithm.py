import tkinter as tk

class DFS:
    def DFS(self, start):
        visited = set()
        current_path = [start]
        frontier = [start]

        while frontier:
            current_state = frontier.pop()

            if current_state is None:
                continue

            current_path.append(current_state)

            #check goal

            if current_state not in visited:
                visited.add(current_state)

                successors = current_state.successors()

                # Explore neighbors in reverse order to maintain LIFO behavior
                for successor in successors:
                    if current_state is not None and current_state not in visited:
                        frontier.append(successor)

        return current_path


    def visualize_path(self, root, path, cell_size):
        canvas = tk.Canvas(root, width=len(path[0]) * cell_size, height=len(path) * cell_size)
        canvas.pack()

        for i in range(len(path)):
            for j in range(len(path[0])):
                x1 = j * cell_size
                y1 = i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=("yellow" if path[i][j] == '1' else "black" if path[i][j] == '-1' else "white"),
                    outline="grey"
                )

                text_x = x1 + cell_size // 2
                text_y = y1 + cell_size // 2

                canvas.create_text(text_x, text_y,
                                   text=(path[i][j] if path[i][j].__contains__("A") or path[i][j] == "T1" else ""),
                                   fill=("blue" if path[i][j] == "T1" else "red" if path[i][j].__contains__(
                                       "A") else "white"),
                                   font=("Arial", 25))

