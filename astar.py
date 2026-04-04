#!/usr/bin/env python3
"""astar - A* pathfinding on grids and graphs with visualization."""

import sys, json, heapq, math

def cmd_grid(args):
    """Find path on ASCII grid. # = wall, S = start, E = end."""
    path = args[0] if args else None
    diag = '--diag' in args
    if path:
        with open(path) as f:
            grid = [list(line.rstrip('\n')) for line in f]
    else:
        grid = [list(line.rstrip('\n')) for line in sys.stdin]
    rows, cols = len(grid), max(len(r) for r in grid)
    for r in grid:
        while len(r) < cols: r.append(' ')
    start = end = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S': start = (r, c)
            elif grid[r][c] == 'E': end = (r, c)
    if not start or not end:
        print("Need S (start) and E (end) on grid", file=sys.stderr); sys.exit(1)

    def h(a, b):
        return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2) if diag else abs(a[0]-b[0]) + abs(a[1]-b[1])

    def neighbors(r, c):
        dirs = [(-1,0),(1,0),(0,-1),(0,1)]
        if diag: dirs += [(-1,-1),(-1,1),(1,-1),(1,1)]
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
                cost = 1.414 if abs(dr)+abs(dc) == 2 else 1
                yield (nr, nc), cost

    open_set = [(h(start, end), 0, start)]
    came_from = {}
    g_score = {start: 0}
    visited = 0

    while open_set:
        _, g, current = heapq.heappop(open_set)
        visited += 1
        if current == end:
            path_cells = []
            n = end
            while n in came_from:
                path_cells.append(n)
                n = came_from[n]
            path_cells.append(start)
            path_cells.reverse()
            for r, c in path_cells:
                if grid[r][c] not in ('S', 'E'):
                    grid[r][c] = '·'
            print('\n'.join(''.join(r) for r in grid))
            print(f"\nPath length: {len(path_cells)} steps, cost: {g_score[end]:.1f}")
            print(f"Nodes explored: {visited}")
            return
        for nb, cost in neighbors(*current):
            ng = g_score[current] + cost
            if ng < g_score.get(nb, float('inf')):
                g_score[nb] = ng
                came_from[nb] = current
                heapq.heappush(open_set, (ng + h(nb, end), ng, nb))

    print("No path found!")
    sys.exit(1)

def cmd_graph(args):
    """A* on weighted graph: A-B:W ... START END"""
    start_node = args[-2]
    end_node = args[-1]
    edges = {}
    nodes = set()
    for a in args[:-2]:
        if ':' in a:
            edge, w = a.rsplit(':', 1)
            w = float(w)
        else:
            edge, w = a, 1
        src, dst = edge.split('-')
        edges.setdefault(src, []).append((dst, w))
        edges.setdefault(dst, []).append((src, w))
        nodes.update([src, dst])

    open_set = [(0, 0, start_node)]
    came_from = {}
    g_score = {start_node: 0}
    visited = 0

    while open_set:
        _, g, current = heapq.heappop(open_set)
        visited += 1
        if current == end_node:
            path = []
            n = end_node
            while n in came_from:
                path.append(n)
                n = came_from[n]
            path.append(start_node)
            path.reverse()
            print(f"Path: {' → '.join(path)}")
            print(f"Cost: {g_score[end_node]}")
            print(f"Nodes explored: {visited}")
            return
        for nb, cost in edges.get(current, []):
            ng = g_score[current] + cost
            if ng < g_score.get(nb, float('inf')):
                g_score[nb] = ng
                came_from[nb] = current
                heapq.heappush(open_set, (ng, ng, nb))

    print("No path found!")
    sys.exit(1)

def cmd_maze(args):
    """Generate random maze."""
    import random
    w = int(args[0]) if args else 21
    h = int(args[1]) if len(args) > 1 else w
    if w % 2 == 0: w += 1
    if h % 2 == 0: h += 1
    grid = [['#'] * w for _ in range(h)]

    def carve(r, c):
        grid[r][c] = ' '
        dirs = [(0,2),(0,-2),(2,0),(-2,0)]
        random.shuffle(dirs)
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 0 <= nr < h and 0 <= nc < w and grid[nr][nc] == '#':
                grid[r+dr//2][c+dc//2] = ' '
                carve(nr, nc)

    sys.setrecursionlimit(w * h)
    carve(1, 1)
    grid[1][0] = 'S'
    grid[h-2][w-1] = 'E'
    print('\n'.join(''.join(r) for r in grid))

CMDS = {
    'grid': (cmd_grid, '[FILE] [--diag] — pathfind on ASCII grid (S→E, # walls)'),
    'graph': (cmd_graph, 'A-B:W ... START END — shortest path on weighted graph'),
    'maze': (cmd_maze, '[W] [H] — generate random maze'),
}

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print("Usage: astar <command> [args...]")
        for n, (_, d) in sorted(CMDS.items()):
            print(f"  {n:8s} {d}")
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd not in CMDS: print(f"Unknown: {cmd}", file=sys.stderr); sys.exit(1)
    CMDS[cmd][0](sys.argv[2:])

if __name__ == '__main__':
    main()
