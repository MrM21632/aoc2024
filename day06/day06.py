import collections
from typing import List, Tuple


DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # U, R, D, L
FREE = '.'
WALL = '#'


def read_file(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines

def construct_grid(input_file: str) -> List[List[int]]:
    lines = read_file(input_file)
    return [list(l.strip()) for l in lines]

def get_starting_location_of_guard(grid: List[List[int]], m: int, n: int) -> Tuple[int, int]:
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '^':  # The guard always starts facing north (U)
                return i, j
    return -1, -1

def get_visited_cells(input_file: str) -> int:
    grid = construct_grid(input_file)
    m, n = len(grid), len(grid[0])
    x, y = get_starting_location_of_guard(grid, m, n)
    
    queue = collections.deque([(x, y, 0)])
    visited = set()
    while queue:
        r, c, d = queue.popleft()
        visited.add((r, c))
        nr, nc = r + DIRS[d][0], c + DIRS[d][1]
        if not (0 <= nr < m and 0 <= nc < n):
            continue
        if grid[nr][nc] == WALL:
            queue.append((r, c, d + (1 if d < 3 else -3)))
        else:
            queue.append((nr, nc, d))

    return len(visited)

def count_cells_that_produce_loop(input_file: str) -> int:
    grid = construct_grid(input_file)
    m, n = len(grid), len(grid[0])
    x, y = get_starting_location_of_guard(grid, m, n)

    def run(i, j):
        queue = collections.deque([(i, j, 0)])
        visited = set()
        while queue:
            r, c, d = queue.popleft()
            if (r, c, d) in visited:
                return True
            visited.add((r, c, d))
            nr, nc = r + DIRS[d][0], c + DIRS[d][1]
            if not (0 <= nr < m and 0 <= nc < n):
                continue
            if grid[nr][nc] == WALL:
                queue.append((r, c, d + (1 if d < 3 else -3)))
            else:
                queue.append((nr, nc, d))
        return False
    
    total = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == FREE:
                prev = grid[r][c]
                grid[r][c] = WALL
                looped = run(x, y)
                if looped:
                    total += 1
                grid[r][c] = prev
    return total


if __name__ == '__main__':
    print('===== DAY 6, PUZZLE 1 =====')
    print('The test input result is ', get_visited_cells('test_input.txt'))
    print('The main input result is ', get_visited_cells('input.txt'))

    print('\n\n===== DAY 6, PUZZLE 2 =====')
    print('The test input result is ', count_cells_that_produce_loop('test_input.txt'))
    print('The main input result is ', count_cells_that_produce_loop('input.txt'))
