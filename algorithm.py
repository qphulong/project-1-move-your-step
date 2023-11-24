import tkinter as tk
from graphical import root
import numpy as np

class Algorithm:
    def BFS_Level1(self, start):
        visited = set()
        current_path = []
        frontier = [start]  # queue

        found = False

        while frontier:
            current_state = frontier.pop(0)

            if current_state is None:
                continue

            # check goal
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

        return (found, current_path)

    # ở level 2 kh đảm bảo sẽ tìm được goal ở những nơi có thể đến (những nơi không nằm ở trong các phòng phải dùng chìa khoá để mở vào)
    # bfs ở level này sẽ với mục đích đầu tiên là thu thập chìa khoá và khám phá thế giới
    def BFS_Level2(self, start):
        level1 = self.BFS_Level1(start)
        if level1[0] == True:  # nếu không cần vào các phòng mà đã tìm được level1
            return level1

    def BFS_Level4(self, start):
        level1 = self.BFS_Level1(start)
        if level1[0] == True:  # nếu không cần vào các phòng mà đã tìm được level1
            return level1


    def heuristic_lvl4(self,current_pos,goal_pos):
        point1 = np.array(current_pos.x, current_pos.y)
        point2 = np.array(goal_pos.x, goal_pos.y)

        floor_diff = abs(current_pos.floor-goal_pos.floor)

        dist = np.linalg.norm(point1 - point2)

        return floor_diff * dist

    # nếu không phải floor chứa goal (T1 hoặc tìm key) thì đi tìm đường lên (hoặc xuống)
    # nếu floor chứa goal thì làm giống level 2
    def discover_floor(self, start, floor, level4, goal_floor, goal_pos):

        path = None
        # path = UCS
        # kiếm trong những đường có thể đi không có
        if path is None:
            if goal_floor == floor: # đang ở cùng tang voi goal hien tai, nghia la dang thieu chia khoa phong
                # tim key
            else: # khac tang thi phai tim duong len (xuong tang do)
                next_floor = None

                if floor > goal_floor:
                    next_floor = floor + 1
                else:
                    next_floor = floor - 1
            path = self.discover_floor(start, floor, level4, goal_floor, goal_pos)
            # path = BFS với goal mới
        else:
            return path # tim duoc duong di


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
                    fill=(
                        "black" if floor.table[i][j].checkValue("-1") else "green" if (i, j) in path else "white"),
                    outline="grey"  # Specify the color of the border (here, "grey")
                )

                text_x = x1 + cell_size // 2
                text_y = y1 + cell_size // 2

                canvas.create_text(text_x, text_y,
                                   text=(floor.table[i][j].getValue() if floor.table[i][j].isAgent() or
                                                                         floor.table[i][
                                                                             j].isGoal() or floor.table[i][
                                                                             j].isKey() or floor.table[i][
                                                                             j].isDoor() else "")
                                   , fill=(
                        "blue" if floor.table[i][j].isGoal() else "red" if floor.table[i][j].isAgent()
                        else "yellow" if floor.table[i][j].isKey()
                        else "orange" if floor.table[i][j].isDoor()
                        else "white")
                                   , font=("Arial", 25))

        root.mainloop()
