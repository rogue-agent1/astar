#!/usr/bin/env python3
"""A* pathfinding on a grid. '#'=wall, '.'=open, 'S'=start, 'E'=end."""
import sys, heapq
grid = [list(l.rstrip()) for l in (open(sys.argv[1]) if len(sys.argv)>1 else sys.stdin)]
start = end = None
for r, row in enumerate(grid):
    for c, ch in enumerate(row):
        if ch == 'S': start = (r, c)
        elif ch == 'E': end = (r, c)
if not start or not end: sys.exit("Need S and E in grid")
def h(a, b): return abs(a[0]-b[0]) + abs(a[1]-b[1])
pq, came, gscore = [(h(start,end), 0, start)], {}, {start: 0}
while pq:
    _, g, cur = heapq.heappop(pq)
    if cur == end:
        path, n = [], cur
        while n in came: path.append(n); n = came[n]
        path.append(start)
        for r, c in reversed(path):
            if grid[r][c] not in 'SE': grid[r][c] = '*'
        for row in grid: print(''.join(row))
        print(f"Path length: {len(path)}")
        sys.exit(0)
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = cur[0]+dr, cur[1]+dc
        if 0<=nr<len(grid) and 0<=nc<len(grid[0]) and grid[nr][nc]!='#':
            ng = g + 1
            if ng < gscore.get((nr,nc), float('inf')):
                gscore[(nr,nc)] = ng; came[(nr,nc)] = cur
                heapq.heappush(pq, (ng+h((nr,nc),end), ng, (nr,nc)))
print("No path found")
