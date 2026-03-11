#!/usr/bin/env python3
"""astar — A* pathfinding on a 2D grid with visualization. Zero deps."""
import heapq

def astar(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    def h(a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])
    open_set = [(h(start, goal), 0, start)]
    came_from = {}
    g_score = {start: 0}
    visited = set()
    while open_set:
        _, cost, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        if current in visited:
            continue
        visited.add(current)
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = current[0]+dr, current[1]+dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 1:
                new_cost = g_score[current] + 1
                nb = (nr, nc)
                if new_cost < g_score.get(nb, float('inf')):
                    g_score[nb] = new_cost
                    came_from[nb] = current
                    heapq.heappush(open_set, (new_cost + h(nb, goal), new_cost, nb))
    return None

def visualize(grid, path):
    path_set = set(path) if path else set()
    for r, row in enumerate(grid):
        line = ""
        for c, cell in enumerate(row):
            if (r, c) == path[0] if path else False:
                line += "S "
            elif (r, c) == path[-1] if path else False:
                line += "G "
            elif (r, c) in path_set:
                line += "· "
            elif cell == 1:
                line += "█ "
            else:
                line += "  "
        print(line)

def main():
    grid = [
        [0,0,0,0,0,0,0,0,0,0],
        [0,1,1,1,0,0,0,1,0,0],
        [0,0,0,1,0,1,0,1,0,0],
        [0,0,0,0,0,1,0,0,0,0],
        [0,1,1,1,1,1,0,1,1,0],
        [0,0,0,0,0,0,0,0,0,0],
    ]
    start, goal = (0, 0), (5, 9)
    path = astar(grid, start, goal)
    if path:
        print(f"Path found ({len(path)} steps):")
        visualize(grid, path)
    else:
        print("No path found!")

if __name__ == "__main__":
    main()
