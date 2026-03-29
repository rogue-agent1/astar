import argparse, heapq

def astar(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    def h(a, b): return abs(a[0]-b[0]) + abs(a[1]-b[1])
    open_set = [(h(start, end), 0, start, [start])]
    visited = set()
    while open_set:
        _, cost, pos, path = heapq.heappop(open_set)
        if pos == end: return path, cost
        if pos in visited: continue
        visited.add(pos)
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = pos[0]+dr, pos[1]+dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 1 and (nr,nc) not in visited:
                new_cost = cost + 1
                heapq.heappush(open_set, (new_cost + h((nr,nc), end), new_cost, (nr,nc), path + [(nr,nc)]))
    return [], -1

def main():
    p = argparse.ArgumentParser(description="A* pathfinding")
    p.add_argument("--demo", action="store_true")
    p.add_argument("--size", type=int, default=10)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()
    if args.demo:
        import random; random.seed(args.seed)
        n = args.size
        grid = [[1 if random.random() < 0.25 else 0 for _ in range(n)] for _ in range(n)]
        grid[0][0] = grid[n-1][n-1] = 0
        path, cost = astar(grid, (0,0), (n-1,n-1))
        path_set = set(path)
        for r in range(n):
            row = ""
            for c in range(n):
                if (r,c) in path_set: row += "·"
                elif grid[r][c] == 1: row += "█"
                else: row += " "
            print(row)
        print(f"Cost: {cost}, Path length: {len(path)}")
    else: p.print_help()

if __name__ == "__main__":
    main()
