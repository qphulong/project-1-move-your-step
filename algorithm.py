import heapq
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
                if successor is not None and successor.floor_rep() not in visited and successor not in frontier:
                    frontier.append(successor)

        if found == False:
            current_path = None

        return (found, current_path)

    def AStar(self, start, current_agent, goal=None):
        visited = set()
        current_path = []
        frontier = []  # queue
        heapq.heappush(frontier, (0, start))  # priority queue based on moves

        found = False
        current_state = None

        while frontier:
            current_state = heapq.heappop(frontier)[1]  # get starts

            if current_state is None:
                continue

            visited.add(current_state.floor_rep())

            # check goal
            if current_state.checkGoal(goal):
                current_path.append((current_state.agent_Xposition, current_state.agent_Yposition))
                previous = current_state.previous

                while previous is not None:
                    current_path.append((previous.agent_Xposition, previous.agent_Yposition))
                    previous = previous.previous
                found = True
                break

            successors = current_state.successors(current_agent)

            for successor in successors:
                if successor is None:
                    continue

                total_cost = successor.moves[current_agent] + successor.heuristic_lvl4(current_agent)
                print(total_cost)
                if successor.floor_rep not in visited and not any(successor == s for _, s in frontier):
                    heapq.heappush(frontier, (total_cost, successor))
                elif any(total_cost < cost for cost, s in frontier if tuple(s.puzzle) == tuple(successor.puzzle)):
                    # if in frontier already but higher path cost
                    frontier.remove(successor)
                    heapq.heappush(frontier, (total_cost, successor))  # replace with lower path cost

        if found == False:
            current_path = None

        return (found, (current_state, current_path))

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
            path = self.AStar(level4, 1, goal)

            # kiếm trong những đường có thể đi không có
            if path is None:
                current_cost = -1
                returned_path = None

                for i in range(level4.obtained_keys):  # duyệt tất cả mọi key đã lấy cho phòng ở tầng này
                    room = heapq.heappop(level4.obtained_keys)

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
