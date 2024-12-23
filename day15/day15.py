from typing import List, Tuple


ROBOT = '@'
WALL = '#'
BOX = 'O'
BOX_LEFT = '['
BOX_RIGHT = ']'
EMPTY = '.'
DIRS = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1),
}


def parse_grid(lines: List[str]) -> List[List[str]]:
    return [list(line.strip()) for line in lines]

def parse_wider_grid(lines: List[str]) -> List[List[str]]:
    result = []
    for line in lines:
        row = []
        for c in line:
            match c:
                case '#':
                    row.append('##')
                case '.':
                    row.append('..')
                case '@':
                    row.append('@.')
                case 'O':
                    row.append('[]')
        result.append(row)
    return result

def read_file(filename: str) -> Tuple[List[List[str]], str]:
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    grid, steps = [], []
    for line in lines:
        if '#' in line:
            grid.append(line)
        else:
            steps.append(line)
    return parse_grid(grid), ''.join(s.strip() for s in steps)

def find_robot(grid: List[List[str]]) -> Tuple[int, int]:
    m, n = len(grid), len(grid[0])
    for i in range(m):
        for j in range(n):
            if grid[i][j] == ROBOT:
                return (i, j)
    return (-1, -1)  # Should never be reached

def move(grid: List[List[str]], r: int, c: int, step: str) -> Tuple[int, int]:
    dr, dc = DIRS[step]
    nr, nc = r + dr, c + dc

    # Base cases: it's a free space, or we literally hit a wall
    if grid[nr][nc] == EMPTY:
        return (nr, nc)
    elif grid[nr][nc] == WALL:
        return (r, c)

    # We found a box! Can we move it?
    xr, xc = nr, nc
    while grid[nr][nc] == BOX:
        nr += dr
        nc += dc
    if grid[nr][nc] == EMPTY:
        # Moving the box is simple: do a swap!
        grid[xr][xc], grid[nr][nc] = grid[nr][nc], grid[xr][xc]
        return (xr, xc)
    return (r, c)

def get_sum_of_coords(input_file: str) -> int:
    grid, steps = read_file(input_file)
    m, n = len(grid), len(grid[0])
    r, c = find_robot(grid)
    grid[r][c] = EMPTY  # This space is now accessible for later on

    for s in steps:
        nr, nc = move(grid, r, c, s)
        if (r, c) != (nr, nc):
            r, c = nr, nc

    result = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] in [BOX, BOX_LEFT]:
                result += (j + 100 * i)
    return result


if __name__ == '__main__':
    print('===== DAY 15, PUZZLE 1 =====')
    print('The first test input result is ', get_sum_of_coords('test_input1.txt'))   # 2028
    print('The second test input result is ', get_sum_of_coords('test_input2.txt'))  # 10092
    print('The main input result is ', get_sum_of_coords('input.txt'))

    print('\n\n===== DAY 15, PUZZLE 2 =====')
    # print('The first test input result is ', get_sum_of_coords('test_input1.txt'))  # 9021
    # print('The main input result is ', get_sum_of_coords('input.txt'))
