from typing import List


def read_file(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines

def construct_grid(filename: str) -> List[List[str]]:
    lines = read_file(filename)
    return [list(line.strip()) for line in lines]

def find_word(
    grid: List[List[str]],
    word: str,
    index: int,
    m: int,
    n: int,
    x: int,
    y: int,
    dx: int,
    dy: int,
) -> bool:
    if index == len(word):
        return True
    if (0 <= x < m and 0 <= y < n) and grid[x][y] == word[index]:
        return find_word(grid, word, index + 1, m, n, x + dx, y + dy, dx ,dy)
    return False

def find_all_occurrences(input_file: str, word: str) -> int:
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    grid = construct_grid(input_file)
    m, n = len(grid), len(grid[0])

    total = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == word[0]:
                for dx, dy in dirs:
                    if find_word(grid, word, 0, m, n, i, j, dx, dy):
                        total += 1
    return total

def find_all_x_mases(input_file: str) -> int:
    """
    .....
    .x.x.
    ..A..
    .x.x.

    The following configurations must hold for an X-MAS:
    - The position of each 'x' must be a valid index in the grid
    - For each 'x', the diametric opposite 'x' must be the correct letter. i.e., if the 'x' we're looking
    at is an 'M', its diametric opposite 'x' must be an 'S'

    This means that, for each 'A' we find in the grid (call its coordinates (i, j)), we need to check
    for the following:
    - (i - 1, j - 1), (i - 1, j + 1), (i + 1, j - 1), and (i + 1, j + 1) are all valid indexes in the
    grid.
    - (grid[i - 1][j - 1] == 'M' and grid[i + 1][j + 1] == 'S') or
    (grid[i - 1][j - 1] == 'S' and grid[i + 1][j + 1] == 'M')
    - (grid[i - 1][j + 1] == 'M' and grid[i + 1][j - 1] == 'S') or
    (grid[i - 1][j + 1] == 'S' and grid[i + 1][j - 1] == 'M')
    """
    dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    grid = construct_grid(input_file)
    m, n = len(grid), len(grid[0])

    total = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 'A':
                if all(0 <= i + dx < m and 0 <= j + dy < n for dx, dy in dirs) and (
                    (grid[i - 1][j - 1] == 'M' and grid[i + 1][j + 1] == 'S') or
                    (grid[i - 1][j - 1] == 'S' and grid[i + 1][j + 1] == 'M')
                ) and (
                    (grid[i - 1][j + 1] == 'M' and grid[i + 1][j - 1] == 'S') or
                    (grid[i - 1][j + 1] == 'S' and grid[i + 1][j - 1] == 'M')
                ):
                    total += 1
    return total


if __name__ == '__main__':
    print('===== DAY 4, PUZZLE 1 =====')
    print('The test input result is ', find_all_occurrences('test_input.txt', 'XMAS'))
    print('The main input result is ', find_all_occurrences('input.txt', 'XMAS'))

    print('\n\n===== DAY 4, PUZZLE 2 =====')
    print('The test input result is ', find_all_x_mases('test_input.txt'))
    print('The main input result is ', find_all_x_mases('input.txt'))
