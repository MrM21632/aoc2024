import functools
import itertools
from typing import List


KEYPAD_POSITIONS = {
    '0': (3, 1), 'A': (3, 2),
    '1': (2, 0), '2': (2, 1), '3': (2, 2),
    '4': (1, 0), '5': (1, 1), '6': (1, 2),
    '7': (0, 0), '8': (0, 1), '9': (0, 2),
}
DIRPAD_POSITIONS = {
    '^': (0, 1), 'A': (0, 2),
    '<': (1, 0), 'v': (1, 1), '>': (1, 2),
}
DIRS = {
    '^': (-1, 0), 'v': (1, 0),
    '<': (0, -1), '>': (0, 1),
}


def get_codes(filename: str) -> List[int]:
    with open(filename, 'r') as file:
        codes = [l.strip() for l in file.readlines()]
    return codes


@functools.lru_cache(None)
def compute_complexity(robots: int, robot_id: int, curr_key: str, dest_key: str) -> int:
    pad = KEYPAD_POSITIONS if robot_id == 0 else DIRPAD_POSITIONS

    (cr, cc), (dr, dc) = pad[curr_key], pad[dest_key]
    delta_r, delta_c = dr - cr, dc - cc
    if robot_id == robots - 1:
        return abs(delta_r) + abs(delta_c) + 1
    
    sequence = []
    sequence.extend(['^' if delta_r < 0 else 'v'] * abs(delta_r))
    sequence.extend(['<' if delta_c < 0 else '>'] * abs(delta_c))
    if not sequence:
        return 1
    
    candidates = []
    for perm in set(itertools.permutations(sequence)):
        r, c = cr, cc
        steps = 0
        for i, key in enumerate(perm):
            steps += compute_complexity(robots, robot_id + 1, 'A' if i == 0 else perm[i - 1], key)
            d = DIRS[key]
            r, c = r + d[0], c + d[1]
            if (r, c) not in pad.values():
                break
        else:
            steps += compute_complexity(robots, robot_id + 1, perm[-1], 'A')
            candidates.append(steps)
    return min(candidates)


def get_complexity_of_codes(input_file: str, robots: int) -> int:
    codes = get_codes(input_file)

    total_complexity = 0
    for code in codes:
        complexity = compute_complexity(robots, 0, 'A', code[0])
        for i in range(1, len(code)):
            complexity += compute_complexity(robots, 0, code[i - 1], code[i])
        total_complexity += (complexity * int(code[:-1]))
    return total_complexity


if __name__ == "__main__":
    print('===== DAY 20, PUZZLE 1 =====')
    print('The test input result is ', get_complexity_of_codes('test_input.txt', 3))  # 126384
    print('The main input result is ', get_complexity_of_codes('input.txt', 3))

    print('\n\n===== DAY 20, PUZZLE 2 =====')
    print('The test input result is ', get_complexity_of_codes('test_input.txt', 26))
    print('The main input result is ', get_complexity_of_codes('input.txt', 26))
