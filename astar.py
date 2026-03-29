#!/usr/bin/env python3
"""astar: A* pathfinding on grids and graphs."""
import heapq, math, sys

def astar_grid(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    def h(pos): return abs(pos[0]-goal[0]) + abs(pos[1]-goal[1])
    open_set = [(h(start), 0, start)]
    came_from = {}
    g_score = {start: 0}
    while open_set:
        _, g, current = heapq.heappop(open_set)
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]; path.append(current)
            return list(reversed(path))
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = current[0]+dr, current[1]+dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                ng = g + 1
                neighbor = (nr, nc)
                if ng < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = ng
                    came_from[neighbor] = current
                    heapq.heappush(open_set, (ng + h(neighbor), ng, neighbor))
    return None

def astar_graph(adj, start, goal, heuristic=None):
    if heuristic is None: heuristic = lambda n: 0
    open_set = [(heuristic(start), 0, start)]
    came_from = {}
    g_score = {start: 0}
    while open_set:
        _, g, current = heapq.heappop(open_set)
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]; path.append(current)
            return list(reversed(path))
        for neighbor, cost in adj.get(current, []):
            ng = g + cost
            if ng < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = ng
                came_from[neighbor] = current
                heapq.heappush(open_set, (ng + heuristic(neighbor), ng, neighbor))
    return None

def test():
    grid = [
        [0,0,0,0,0],
        [0,1,1,1,0],
        [0,0,0,1,0],
        [0,1,0,0,0],
        [0,0,0,0,0],
    ]
    path = astar_grid(grid, (0,0), (4,4))
    assert path is not None
    assert path[0] == (0,0)
    assert path[-1] == (4,4)
    assert all(grid[r][c] == 0 for r,c in path)
    # No path
    grid2 = [[0,1],[1,0]]
    assert astar_grid(grid2, (0,0), (1,1)) is None
    # Graph
    adj = {
        "A": [("B",1),("C",4)],
        "B": [("C",2),("D",5)],
        "C": [("D",1)],
        "D": [],
    }
    path2 = astar_graph(adj, "A", "D")
    assert path2 == ["A","B","C","D"]
    # Direct
    adj2 = {"A": [("B",1)], "B": []}
    assert astar_graph(adj2, "A", "B") == ["A", "B"]
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: astar.py test")
