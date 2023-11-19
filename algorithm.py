import tkinter as tk
from graphical import root

class BFS:
    def BFS_Level1(self, start):
        visited = set()
        current_path = []
        frontier = [start] #queue

        found = False

        while frontier:
            current_state = frontier.pop(0)

            if current_state is None:
                continue

            #check goal
            if current_state.checkGoal():
                current_path.append((current_state.agent_Xposition, current_state.agent_Yposition))
                previous = current_state.previous

                while previous is not None:
                    current_path.append((previous.agent_Xposition, previous.agent_Yposition))
                    previous = previous.previous
                found = True
                break

            if current_state.floor_rep() not in visited:
                visited.add(current_state.floor_rep())

                successors = current_state.successors()

                # Explore neighbors in reverse order to maintain LIFO behavior
                for successor in successors:
                    if successor is not None and successor.floor_rep() not in visited:
                        frontier.append(successor)

        if found == False:
            current_path = None

        return (found,current_path)

    #ở level 2 kh đảm bảo sẽ tìm được goal ở những nơi có thể đến (những nơi không nằm ở trong các phòng phải dùng chìa khoá để mở vào)
    #bfs ở level này sẽ với mục đích đầu tiên là thu thập chìa khoá và khám phá thế giới
    def BFS_Level2(self, start):
        level1 = self.BFS_Level1(start)
        if level1[0] == True: #nếu không cần vào các phòng mà đã tìm được level1
            return level1



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
                    fill=("black" if floor.table[i][j].checkValue("-1") else "green" if (i,j) in path else "white"),
                    outline="grey"  # Specify the color of the border (here, "grey")
                )

                text_x = x1 + cell_size // 2
                text_y = y1 + cell_size // 2

                canvas.create_text(text_x, text_y,
                                   text=(floor.table[i][j].getValue() if floor.table[i][j].checkValue("A1") or floor.table[i][
                                       j].checkValue("T1") else "")
                                   , fill=(
                        "blue" if floor.table[i][j].checkValue("T1") else "red" if floor.table[i][j].checkValue("A1") else "white")
                                   , font=("Arial", 25))

        root.mainloop()

