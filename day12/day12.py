import collections
from typing import List, Set, Tuple, TypeAlias


Pair: TypeAlias = Tuple[int, int]


DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def read_file(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        contents = file.readlines()
    return contents

def parse_grid(input_file: str) -> List[List[str]]:
    lines = read_file(input_file)
    return [list(line.strip()) for line in lines]

def find_regions(grid: List[List[str]]) -> List[Set[Pair]]:
    m, n = len(grid), len(grid[0])
    is_valid = lambda r, c: 0 <= r < m and 0 <= c < n

    def flood_fill(sr, sc):
        region = set([(sr, sc)])
        queue = collections.deque([(sr, sc)])

        plant = grid[sr][sc]
        while queue:
            r, c = queue.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if is_valid(nr, nc) and (nr, nc) not in region and grid[nr][nc] == plant:
                    region.add((nr, nc))
                    queue.append((nr, nc))
        return region
    
    regions = []
    filled = set()
    for i in range(m):
        for j in range(n):
            if (i, j) in filled:
                continue
            region = flood_fill(i, j)
            filled |= region
            regions.append(region)
    return regions

def compute_perimeter(region: Set[Pair]) -> int:
    result = 0
    for r, c in region:
        for dr, dc in DIRS:
            if (r + dr, c + dc) not in region:
                result += 1
    return result

def count_sides(region: Set[Pair]) -> int:
    perimeter = set()
    for r, c in region:
        for dr, dc in DIRS:
            if (r + dr, c + dc) not in region:
                perimeter.add((r, c))
    
    sides = 0
    while perimeter:
        r, c = perimeter.pop()
        sides += 1

        for dr, dc in [(1, 0), (0, 1)]:
            if (r + dr, c + dc) in perimeter:
                perimeter.remove((r + dr, c + dc))
    return sides

def get_price_of_fencing(input_file: str, part2: bool = False) -> int:
    grid = parse_grid(input_file)
    regions = find_regions(grid)

    total_price = 0
    for region in regions:
        total_price += len(region) * (count_sides(region) if part2 else compute_perimeter(region))
    return total_price


if __name__ == '__main__':
    print('===== DAY 12, PUZZLE 1 =====')
    print('The test input result is ', get_price_of_fencing('test_input.txt'))
    print('The main input result is ', get_price_of_fencing('input.txt'))

    print('\n\n===== DAY 12, PUZZLE 2 =====')
    print('The test input result is ', get_price_of_fencing('test_input.txt', True))
    print('The main input result is ', get_price_of_fencing('input.txt', True))
