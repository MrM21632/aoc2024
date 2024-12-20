import collections
from typing import Set, Tuple, TypeAlias


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


def get_path(filename: str) -> Tuple[Set[Pair], Pair, Pair]:
    with open(filename, 'r') as file:
        lines = [l for l in file.readlines() if l.strip()]

    # Key observation: There's only one path from S to E. We don't need a full
    # grid structure, just the points along the path.
    path = set()
    start, end = None, None
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c in [EMPTY, START, END]:
                path.add((i, j))
                if c == START:
                    start = (i, j)
                if c == END:
                    end = (i, j)
    return path, start, end


def traverse(path: Set[Pair], start: Pair, end: Pair) -> Tuple[dict, set]:
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
            if (nr, nc) not in visited and (nr, nc) in path:
                queue.append((d + 1, nr, nc))
    return distances, visited


def find_best_time_saves(input_file: str, limit: int, part2: bool = False) -> int:
    path, start, end = get_path(input_file)
    distances, visited = traverse(path, start, end)

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
    print('The test input result is ', find_best_time_saves('test_input.txt', 10))  # 10
    print('The main input result is ', find_best_time_saves('input.txt', 100))

    print('\n\n===== DAY 20, PUZZLE 2 =====')
    print('The test input result is ', find_best_time_saves('test_input.txt', 50, True))  # 285
    print('The main input result is ', find_best_time_saves('input.txt', 100, True))
