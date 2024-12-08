import collections
import itertools
from typing import Dict, List, Tuple


def read_file(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines

def get_grid(input_file: str) -> List[List[str]]:
    lines = read_file(input_file)
    return [list(line.strip()) for line in lines]

def find_nodes(grid: List[List[str]]) -> Dict[str, List[Tuple[int, int]]]:
    result = collections.defaultdict(list)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != '.':
                result[grid[i][j]].append((i, j))
    return result

def find_antinodes(input_file: str) -> int:
    grid = get_grid(input_file)
    m, n = len(grid), len(grid[0])
    node_positions = find_nodes(grid)

    valid = lambda r, c: 0 <= r < m and 0 <= c < n
    antinodes = set()
    for positions in node_positions.values():
        for (ax, ay), (bx, by) in itertools.combinations(positions, 2):
            cx, cy = ax - (bx - ax), ay - (by - ay)
            if valid(cx, cy):
                antinodes.add((cx, cy))
            dx, dy = bx + (bx - ax), by + (by - ay)
            if valid(dx, dy):
                antinodes.add((dx, dy))
    return len(antinodes)

def find_harmonics(input_file: str) -> int:
    grid = get_grid(input_file)
    m, n = len(grid), len(grid[0])
    node_positions = find_nodes(grid)

    valid = lambda r, c: 0 <= r < m and 0 <= c < n
    harmonics = set()
    for positions in node_positions.values():
        for (ax, ay), (bx, by) in itertools.combinations(positions, 2):
            harmonics.update([(ax, ay), (bx, by)])
            cx, cy = ax - (bx - ax), ay - (by - ay)
            while valid(cx, cy):
                harmonics.add((cx, cy))
                cx -= (bx - ax)
                cy -= (by - ay)
            dx, dy = bx + (bx - ax), by + (by - ay)
            while valid(dx, dy):
                harmonics.add((dx, dy))
                dx += (bx - ax)
                dy += (by - ay)
    return len(harmonics)


if __name__ == '__main__':
    print('===== DAY 8, PUZZLE 1 =====')
    print('The test input result is ', find_antinodes('test_input.txt'))
    print('The main input result is ', find_antinodes('input.txt'))

    print('\n\n===== DAY 8, PUZZLE 2 =====')
    print('The test input result is ', find_harmonics('test_input.txt'))
    print('The main input result is ', find_harmonics('input.txt'))
