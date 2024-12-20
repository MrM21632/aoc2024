import collections
from typing import List, Tuple, TypeAlias


START = 'S'
END = 'E'
EMPTY = '.'
WALL = '#'

DIRS = [
    (0, 1), (1, 0), (0, -1), (-1, 0),
]
CHEAT_DIRS = [
    (0, 2), (2, 0), (0, -2), (-2, 0),
    # Diagonals are fine here: think of it as moving in one direction, then the other
    (1, 1), (1, -1), (-1, 1), (-1, -1),
]


Pair: TypeAlias = Tuple[int, int]
Grid: TypeAlias = List[List[str]]


def get_grid(filename: str) -> Tuple[Grid, Pair, Pair]:
    with open(filename, 'r') as file:
        lines = [l for l in file.readlines() if l.strip()]
    
    grid = [list(line.strip()) for line in lines]
    start, end = None, None
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == START:
                start = (i, j)
            if grid[i][j] == END:
                end = (i, j)
    return grid, start, end


def traverse(grid: Grid, start: Pair, end: Pair) -> Tuple[dict, set]:
    m, n = len(grid), len(grid[0])
    is_valid = lambda r, c: 0 <= r < m and 0 <= c < n

    distances = dict()
    visited = set()
    queue = collections.deque([(0, *start)])

    while queue:
        d, r, c = queue.popleft()
        if (r, c) in visited:
            continue
        distances[(r, c)] = d
        visited.add((r, c))
        if (r, c) == end:
            break

        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc) and (nr, nc) not in visited and grid[nr][nc] == EMPTY:
                queue.append((d + 1, nr, nc))
    return distances, visited


def find_best_time_saves(input_file: str, limit: int, part2: bool = False) -> int:
    grid, start, end = get_grid(input_file)
    distances, visited = traverse(grid, start, end)

    cheats = CHEAT_DIRS.copy()
    if part2:
        # Add new cheats with absolute distance between 3 and 20, inclusive
        for dr in range(-20, 21):
            for dc in range(-20, 21):
                d = abs(dr) + abs(dc)
                if 3 <= d <= 20:
                    cheats.append((dr, dc))

    total = 0
    for r, c in visited:
        base_score = distances[(r, c)]
        for dr, dc in cheats:
            nr, nc = r + dr, c + dc
            if (nr, nc) not in visited:
                continue

            new_score = distances[(nr, nc)]
            cheat_distance = abs(dr) + abs(dc)
            if new_score - base_score - cheat_distance >= limit:
                total += 1
    return total


if __name__ == '__main__':
    print('===== DAY 20, PUZZLE 1 =====')
    print('The test input result is ', find_best_time_saves('test_input.txt', 10))  # 9?
    print('The main input result is ', find_best_time_saves('input.txt', 100))

    print('\n\n===== DAY 20, PUZZLE 2 =====')
    print('The test input result is ', find_best_time_saves('test_input.txt', 50, True))  # 285?
    # print('The main input result is ', find_best_time_saves('input.txt', 100, True))
