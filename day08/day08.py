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

def find_antinodes_and_harmonics(input_file: str) -> Tuple[int, int]:
    grid = get_grid(input_file)
    m, n = len(grid), len(grid[0])
    node_positions = find_nodes(grid)

    valid = lambda r, c: 0 <= r < m and 0 <= c < n
    antinodes, harmonics = set(), set()
    for positions in node_positions.values():
        for (ax, ay), (bx, by) in itertools.combinations(positions, 2):
            harmonics.update([(ax, ay), (bx, by)])
            # Positions are naturally ordered, which makees the math simpler
            cx, cy = ax - (bx - ax), ay - (by - ay)
            dx, dy = bx + (bx - ax), by + (by - ay)

            if valid(cx, cy):
                antinodes.add((cx, cy))
            while valid(cx, cy):
                harmonics.add((cx, cy))
                cx -= (bx - ax)
                cy -= (by - ay)

            if valid(dx, dy):
                antinodes.add((dx, dy))
            while valid(dx, dy):
                harmonics.add((dx, dy))
                dx += (bx - ax)
                dy += (by - ay)
    return len(antinodes), len(harmonics)


if __name__ == '__main__':
    input_results = find_antinodes_and_harmonics('input.txt')
    test_input_results = find_antinodes_and_harmonics('test_input.txt')

    print('===== DAY 8, PUZZLE 1 =====')
    print('The test input result is ', test_input_results[0])
    print('The main input result is ', input_results[0])

    print('\n\n===== DAY 8, PUZZLE 2 =====')
    print('The test input result is ', test_input_results[1])
    print('The main input result is ', input_results[1])
