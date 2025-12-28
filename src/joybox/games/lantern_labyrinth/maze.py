import random

WALL = "#"
FLOOR = "."

def generate_maze(width, height, seed=None):
    if seed is not None:
        random.seed(seed)

    grid = [[WALL for _ in range(width)] for _ in range(height)]

    def neighbors(cx, cy):
        dirs = [(2,0), (-2,0), (0,2), (0,-2)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = cx + dx, cy + dy
            if 1 <= nx < width-1 and 1 <= ny < height-1:
                yield nx, ny, dx, dy

    stack = [(1,1)]
    grid[1][1] = FLOOR

    while stack:
        x, y = stack[-1]
        carved = False

        for nx, ny, dx, dy in neighbors(x, y):
            if grid[ny][nx] == WALL:
                grid[y + dy//2][x + dx//2] = FLOOR
                grid[ny][nx] = FLOOR
                stack.append((nx, ny))
                carved = True
                break

        if not carved:
            stack.pop()

    return grid

def place_exit(grid):
    h = len(grid)
    w = len(grid[0])

    for y in range(h-2, 0, -1):
        for x in range(w-2, 0, -1):
            if grid[y][x] == FLOOR:
                grid[y][x] = "E"
                return (x, y)
            
    grid[h-2][w-2] = "E"
    return (w-2, h-2)

def place_orbs(grid, count=3):
    floors = [(x,y) for y,row in enumerate(grid) for x,ch in enumerate(row) if ch == FLOOR]
    random.shuffle(floors)
    for i in range(min(count, len(floors))):
        x,y = floors[i]
        grid[y][x] = "O"
