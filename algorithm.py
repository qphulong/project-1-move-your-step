def DFS(start):
    visited = set()
    frontier = [start]

    while frontier:
        current_state = frontier.pop()

        if tuple(current_state.floor.table) not in visited:
            visited.add(current_state.floor.table)

            successors = current_state.successors()

            # Explore neighbors in reverse order to maintain LIFO behavior
            for successor in successors:
                if tuple(successor.floor.table) not in visited:
                    frontier.append(successor)