import heapq
import sys
from typing import List, Tuple


START = 'S'
END = 'E'
EMPTY = '.'
WALL = '#'

DIRS = [
    # East (0), South (1), West (2), North (3)
    (0, 1), (1, 0), (0, -1), (-1, 0),
]

MOVE_SCORE = 1
TURN_SCORE = 1000


cw = lambda i: (i + 1) % 4
ccw = lambda i: (i + 3) % 4


def read_file(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        content = file.readlines()
    return content

def parse_grid(input_file: str) -> List[List[str]]:
    lines = read_file(input_file)
    return [list(line.strip()) for line in lines]

def find_start_and_end_points(grid: List[List[str]]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    start, end = None, None
    m, n = len(grid), len(grid[0])

    for i in range(m):
        for j in range(n):
            if grid[i][j] == START:
                start = (i, j)
            if grid[i][j] == END:
                end = (i, j)
    return start, end


def dijkstra(grid: List[List[str]], starts: List[Tuple[int, int, int]]) -> dict:
    m, n = len(grid), len(grid[0])
    is_valid = lambda r, c: 0 <= r < m and 0 <= c < n

    distances = dict()
    heap = []
    for r, c, d in starts:
        distances[(r, c, d)] = 0
        heapq.heappush(heap, (0, r, c, d))

    while heap:
        dist, r, c, d = heapq.heappop(heap)
        if distances[(r, c, d)] < dist:
            continue

        # Account for turns
        for nd in (cw(d), ccw(d)):
            if (r, c, nd) not in distances or distances[(r, c, nd)] > dist + 1000:
                distances[(r, c, nd)] = dist + 1000
                heapq.heappush(heap, (dist + 1000, r, c, nd))
        
        # Handle moving
        dr, dc = DIRS[d]
        nr, nc = r + dr, c + dc
        if is_valid(nr, nc) and grid[nr][nc] != WALL and (
            (nr, nc, d) not in distances or
            distances[(nr, nc, d)] > dist + 1
        ):
            distances[(nr, nc, d)] = dist + 1
            heapq.heappush(heap, (dist + 1, nr, nc, d))
    return distances


def find_minimum_score(input_file: str) -> int:
    grid = parse_grid(input_file)
    (sr, sc), (er, ec) = find_start_and_end_points(grid)

    distances = dijkstra(grid, [(sr, sc, 0)])
    best_distance = sys.maxsize
    for d in range(4):
        if (er, ec, d) in distances:
            best_distance = min(best_distance, distances[(er, ec, d)])
    return best_distance


if __name__ == '__main__':
    print('===== DAY 16, PUZZLE 1 =====')
    print('The first test input result is ', find_minimum_score('test_input1.txt'))   # 7036
    print('The second test input result is ', find_minimum_score('test_input2.txt'))  # 11048
    print('The main input result is ', find_minimum_score('input.txt'))

    print('\n\n===== DAY 16, PUZZLE 2 =====')
    # print('The first test input result is ', get_sum_of_coords('test_input1.txt'))
    # print('The second test input result is ', get_sum_of_coords('test_input2.txt'))
    # print('The main input result is ', get_sum_of_coords('input.txt'))
