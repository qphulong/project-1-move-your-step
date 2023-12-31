import heapq
import tkinter as tk
from graphical import root
import numpy as np
from PIL import Image, ImageGrab
import platform
import os
import subprocess
import psutil


class Algorithm:
    def heuristic_Level1(self, current_state, goal_x, goal_y):
        return np.sqrt((current_state.agent_Xposition - goal_x) ** 2 + (current_state.agent_Yposition - goal_y) ** 2)

    def AStar_Level1(self, start): # astar
        visited = set()
        current_path = []
        frontier = []  # queue

        goal_x = start.goal_Xposition
        goal_y = start.goal_Yposition

        heapq.heappush(frontier,
                       (self.heuristic_Level1(start, goal_x, goal_y) + 0, start))  # priority queue based on moves

        found = False

        while frontier:

            current_state = heapq.heappop(frontier)[1]

            if current_state is None:
                continue

            visited.add(current_state.floor_rep())

            # check goal
            if current_state.checkGoal():
                current_path.append((current_state.agent_Xposition, current_state.agent_Yposition))
                previous = current_state.previous

                while previous is not None:
                    current_path.append((previous.agent_Xposition, previous.agent_Yposition))
                    previous = previous.previous
                found = True
                break

            successors = current_state.successors()

            for successor in successors:
                if successor is None:
                    continue

                total_cost = successor.moves + self.heuristic_Level1(successor, goal_x, goal_y)

                if tuple(successor.floor_rep()) not in visited and not any(
                        successor == s for _, s in frontier
                ):
                    heapq.heappush(frontier, (total_cost, successor))
                elif any(
                        total_cost < cost
                        for cost, s in frontier
                        if s.floor_rep() == successor.floor_rep()
                ):
                    # if in frontier already but higher path cost
                    frontier = [
                        (cost, s)
                        for cost, s in frontier
                        if s.floor_rep() != successor.floor_rep()
                    ]
                    heapq.heappush(
                        frontier, (total_cost, successor)
                    )  # replace with lower path cost

        if found == False:
            current_path = None

        return (found, current_path)

    def BFS_Level1(self, start):  # bfs
        visited = set()
        current_path = []
        frontier = []  # queue
        frontier.append(start)

        goal_x = start.goal_Xposition
        goal_y = start.goal_Yposition

        found = False

        while frontier:

            current_state = frontier.pop(0)

            if current_state is None:
                continue

            visited.add(current_state.floor_rep())

            # check goal
            if current_state.checkGoal():
                current_path.append((current_state.agent_Xposition, current_state.agent_Yposition))
                previous = current_state.previous

                while previous is not None:
                    current_path.append((previous.agent_Xposition, previous.agent_Yposition))
                    previous = previous.previous
                found = True
                break

            successors = current_state.successors()

            for successor in successors:
                if successor is None:
                    continue

                if tuple(successor.floor_rep()) not in visited:
                    frontier.append(successor)

        if found == False:
            current_path = None

        return (found, current_path)

    def UCS_Level1(self, start): # ucs
        visited = set()
        current_path = []
        frontier = []  # queue

        goal_x = start.goal_Xposition
        goal_y = start.goal_Yposition

        heapq.heappush(frontier,
                       (0, start))  # priority queue based on moves

        found = False

        while frontier:

            current_state = heapq.heappop(frontier)[1]

            if current_state is None:
                continue

            visited.add(current_state.floor_rep())

            # check goal
            if current_state.checkGoal():
                current_path.append((current_state.agent_Xposition, current_state.agent_Yposition))
                previous = current_state.previous

                while previous is not None:
                    current_path.append((previous.agent_Xposition, previous.agent_Yposition))
                    previous = previous.previous
                found = True
                break

            successors = current_state.successors()

            for successor in successors:
                if successor is None:
                    continue


                if tuple(successor.floor_rep()) not in visited and not any(
                        successor == s for _, s in frontier
                ):
                    heapq.heappush(frontier, (successor.moves, successor))
                elif any(
                        successor.moves < cost
                        for cost, s in frontier
                        if s.floor_rep() == successor.floor_rep()
                ):
                    # if in frontier already but higher path cost
                    frontier = [
                        (cost, s)
                        for cost, s in frontier
                        if s.floor_rep() != successor.floor_rep()
                    ]
                    heapq.heappush(
                        frontier, (successor.moves, successor)
                    )  # replace with lower path cost

        if found == False:
            current_path = None

        return (found, current_path)

    # mở cửa phòng
    def open_door(self, room_no, level4, goal):
        res = self.AStar(level4, level4.keys[room_no])
        path = res[1][1]  # tìm đường đến key
        last_state = res[1][0]  # tìm state mới nhất

        res = self.AStar(last_state, level4.doors[room_no])
        last_state = res[1][0]  # tìm state mới nhất
        path.__add__(res[1][1])  # tìm đường đến door

        # nhớ tính tới vụ chìa khoá ở trên lầu => phải cho nó đi xuống

        final = self.AStar(last_state, goal)[1]

        return final

    # nếu không phải floor chứa goal (T1 hoặc tìm key) thì đi tìm đường lên (hoặc xuống)
    # nếu floor chứa goal thì làm giống level 2
    def discover_floor(self, level4, floor, goal_floor, goal):
        if goal_floor == floor:
            path = self.AStar(level4, 1, goal)[1][1]

            # kiếm trong những đường có thể đi không có
            if path is None:
                print("Finding with keys")

                current_cost = -1
                returned_path = None

                print(len(level4.obtained_keys))

                for i in range(len(level4.obtained_keys)):  # duyệt tất cả mọi key đã lấy cho phòng ở tầng này
                    room = level4.obtained_keys.pop(0)

                    open_door = level4.open_door(room, goal)
                    path = open_door[1]
                    cost = open_door[0].moves

                    if path is not None:
                        if cost < current_cost:
                            current_cost = cost
                            returned_path = path

                if returned_path is not None:
                    return returned_path  # tìm được goal khi vào phòng

                # nếu không tìm được goal khi vào phòng
                # phải đi tìm chìa khoá
            else:  # tìm được đến goal
                return path
        else:  # ở tầng khác
            next_floor = None

            if floor > goal_floor:
                next_floor = floor - 1
            else:
                next_floor = floor + 1

            return self.discover_floor(level4, next_floor, goal_floor, goal)

    def visualize_path(self, start_x, start_y, goal_x, goal_y, floor, path):
        board_size = 30  # Define the size of the board
        cell_size = 20  # Define the size of each cell in pixels

        canvas = tk.Canvas(root, width=board_size * cell_size, height=board_size * cell_size)
        canvas.pack()

        score = tk.Label(root, font=('Arial', 25), text='Score: '+str(len(path)), fg='Black')
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


def export_heatmap(Tkroot):
    x = Tkroot.winfo_rootx()
    y = Tkroot.winfo_rooty()
    width = Tkroot.winfo_width()
    height = Tkroot.winfo_height()
    screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    screenshot.save("heatmap.png")

    image_folder = os.path.dirname(os.path.abspath("heatmap.png"))

    operating_system = platform.system()
    if operating_system == "Darwin":
        subprocess.run(["open", image_folder])  # Opens the folder in Windows File Explorer
    elif operating_system == "Windows":
        subprocess.run(["explorer", image_folder])  # Opens the folder in Windows File Explorer

def get_memory_usage():
    # Get memory usage in bytes
    memory_info = psutil.Process().memory_info()
    memory_usage = memory_info.rss  # Get Resident Set Size (memory used)

    # Convert bytes to megabytes for readability
    memory_usage_mb = memory_usage / (1024 * 1024)
    return memory_usage_mb