import collections
from typing import List, Tuple


DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
TRAIL_START = 0
TRAIL_END = 9


def read_file(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        contents = file.readlines()
    return contents

def construct_grid(input_file: str) -> List[List[int]]:
    lines = read_file(input_file)
    return [list(map(int, l.strip())) for l in lines]

def find_trailheads(grid: List[List[int]]) -> List[Tuple[int, int]]:
    m, n = len(grid), len(grid[0])

    result = []
    for i in range(m):
        for j in range(n):
            if grid[i][j] == TRAIL_START:
                result.append((i, j))
    return result

def get_score_for_trailhead(grid: List[List[int]], start: Tuple[int, int], part2: bool) -> int:
    m, n = len(grid), len(grid[0])
    is_valid = lambda r, c: 0 <= r < m and 0 <= c < n

    queue = collections.deque([start])
    visited = set()

    score = 0
    while queue:
        r, c = queue.popleft()
        if grid[r][c] == TRAIL_END:
            score += (1 if part2 or (r, c) not in visited else 0)
            visited.add((r, c))
            continue
        
        visited.add((r, c))
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc) and (nr, nc) not in visited and grid[nr][nc] == grid[r][c] + 1:
                queue.append((nr, nc))
    return score

def compute_score_total(input_file: str, part2: bool = False) -> int:
    grid = construct_grid(input_file)
    trailheads = find_trailheads(grid)
    return sum(get_score_for_trailhead(grid, t, part2) for t in trailheads)


if __name__ == '__main__':
    print('===== DAY 10, PUZZLE 1 =====')
    print('The test input result is ', compute_score_total('test_input.txt'))
    print('The main input result is ', compute_score_total('input.txt'))

    print('\n\n===== DAY 10, PUZZLE 2 =====')
    print('The test input result is ', compute_score_total('test_input.txt', True))
    print('The main input result is ', compute_score_total('input.txt', True))
