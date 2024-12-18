import collections
from typing import cast, List, Tuple, TypeAlias


Pair: TypeAlias = Tuple[int, int]
Grid: TypeAlias = List[List[int]]


DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
EMPTY = 0
CORRUPTED = 1


def get_grid_and_corruption_list(filename: str) -> Tuple[Grid, int, List[Pair]]:
    with open(filename, 'r') as file:
        lines = [l for l in file.readlines() if l.strip()]
    
    dim, ccount = list(map(int, lines[0].strip().split(',')))
    grid = [[EMPTY for _ in range(dim)] for _ in range(dim)]

    corrupted_cells = []
    for line in lines[1:]:
        corrupted_cells.append(tuple(map(int, line.strip().split(','))))
    
    return cast(Grid, grid), ccount, cast(List[Pair], corrupted_cells)

def corrupt_grid(grid: Grid, corruptions: List[Pair], count: int) -> Grid:
    for i in range(count):
        cx, cy = corruptions[i]
        grid[cy][cx] = CORRUPTED
    return grid


def traverse(grid: Grid, start: Pair, end: Pair) -> int:
    m, n = len(grid), len(grid[0])
    is_valid = lambda r, c: 0 <= r < m and 0 <= c < n
    queue = collections.deque([(0, start)])
    visited = set()

    while queue:
        distance, (r, c) = queue.popleft()
        if (r, c) in visited or not is_valid(r, c) or grid[r][c] == CORRUPTED:
            continue

        visited.add((r, c))
        if cast(Pair, (r, c)) == end:
            return distance

        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            queue.append((distance + 1, cast(Pair, (nr, nc))))
    return -1


def find_best_path_after_corruptions(input_file: str) -> int:
    grid, count, corruptions = get_grid_and_corruption_list(input_file)
    grid = corrupt_grid(grid, corruptions, count)

    start = cast(Pair, (0, 0))
    end = cast(Pair, (len(grid) - 1, len(grid[0]) - 1))
    return traverse(grid, start, end)

def find_first_blocking_corruption(input_file: str) -> Pair:
    grid, count, corruptions = get_grid_and_corruption_list(input_file)
    start = cast(Pair, (0, 0))
    end = cast(Pair, (len(grid) - 1, len(grid[0]) - 1))

    # We know count is fine, so start at the next one
    lo, hi = count + 1, len(corruptions)
    while lo < hi:
        mid = lo + (hi - lo) // 2

        test_grid = [row.copy() for row in grid]
        test_grid = corrupt_grid(test_grid, corruptions, mid)
        if traverse(test_grid, start, end) == -1:
            hi = mid
        else:
            lo = mid + 1

    # One before lo because it's the full count, not the exact index
    return corruptions[lo - 1]


if __name__ == '__main__':
    print('===== DAY 18, PUZZLE 1 =====')
    print('The test input result is ', find_best_path_after_corruptions('test_input.txt'))  # 22
    print('The main input result is ', find_best_path_after_corruptions('input.txt'))

    print('\n\n===== DAY 18, PUZZLE 2 =====')
    print('The test input result is ', find_first_blocking_corruption('test_input.txt'))  # (6, 1)
    print('The main input result is ', find_first_blocking_corruption('input.txt'))
