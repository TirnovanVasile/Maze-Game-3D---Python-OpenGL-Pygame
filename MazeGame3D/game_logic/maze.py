import random

def generate_maze(size):
    grid = [[1] * size for _ in range(size)]

    def walk(x, z):
        grid[z][x] = 0
        dirs = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(dirs)
        for dx, dz in dirs:
            nx, nz = x + dx, z + dz
            if 0 < nx < size and 0 < nz < size and grid[nz][nx] == 1:
                grid[z + dz // 2][x + dx // 2] = 0
                walk(nx, nz)

    walk(1, 1)
    return grid
