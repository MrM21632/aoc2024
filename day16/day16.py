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
flip = lambda i: (i + 2) % 4


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

        # Account for turns. Remember we can only turn 90 degrees CW/CCW at a time
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

    # Part 1 is literally just an application of Dijkstra's algorithm. Find the most
    # optimal path from start to target.
    distances = dijkstra(grid, [(sr, sc, 0)])
    best_distance = sys.maxsize
    for d in range(4):
        if (er, ec, d) in distances:
            best_distance = min(best_distance, distances[(er, ec, d)])
    return best_distance


def find_total_best_tiles(input_file: str) -> int:
    grid = parse_grid(input_file)
    (sr, sc), (er, ec) = find_start_and_end_points(grid)

    distances_from_start = dijkstra(grid, [(sr, sc, 0)])
    distances_from_end = dijkstra(grid, [(er, ec, d) for d in range(4)])
    best_distance = find_minimum_score(input_file)

    # Basic idea: We know the optimal path(s) from the start and target cells. We know the
    # shortest path from Part 1. If a given cell is along the best path(s), then the
    # distance to that cell from the start and target cells should add up to the shortest
    # path's distance.
    best_tiles = set()
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            for d in range(4):
                # flip() produces the opposite direction; this is because we'll be coming
                # from opposite directions between the start and target cells.
                sk, ek = (r, c, d), (r, c, flip(d))
                if sk in distances_from_start and ek in distances_from_end:
                    if distances_from_start[sk] + distances_from_end[ek] == best_distance:
                        best_tiles.add((r, c))
    return len(best_tiles)


if __name__ == '__main__':
    print('===== DAY 16, PUZZLE 1 =====')
    print('The first test input result is ', find_minimum_score('test_input1.txt'))   # 7036
    print('The second test input result is ', find_minimum_score('test_input2.txt'))  # 11048
    print('The main input result is ', find_minimum_score('input.txt'))

    print('\n\n===== DAY 16, PUZZLE 2 =====')
    print('The first test input result is ', find_total_best_tiles('test_input1.txt'))   # 45
    print('The second test input result is ', find_total_best_tiles('test_input2.txt'))  # 64
    print('The main input result is ', find_total_best_tiles('input.txt'))
