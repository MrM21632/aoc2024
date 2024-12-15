from typing import List, Tuple


TOTAL_ROWS = 103
TOTAL_COLS = 101
ITERATIONS = 100


def read_file(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        contents = file.readlines()
    return contents

def parse_robot_details(input_file: str) -> List[List[Tuple[int, int]]]:
    contents = read_file(input_file)

    result = []  # [(pr, pc), (vr, vc)]
    for detail in contents:
        result.append([
            tuple(map(int, reversed(d.split('=')[1].split(','))))
            for d in detail.strip().split(' ')
        ])
    return result

def compute_final_positions(input_file: str) -> int:
    details = parse_robot_details(input_file)

    quadrants = [0] * 4
    for d in details:
        pr, pc = d[0]
        vr, vc = d[1]
        dr, dc = pr + (vr * ITERATIONS), pc + (vc * ITERATIONS)
        dr, dc = dr % TOTAL_ROWS, dc % TOTAL_COLS

        if dr == TOTAL_ROWS // 2 or dc == TOTAL_COLS // 2:
            continue
        if dr < TOTAL_ROWS // 2 and dc < TOTAL_COLS // 2:
            quadrants[0] += 1
        elif dr > TOTAL_ROWS // 2 and dc < TOTAL_COLS // 2:
            quadrants[1] += 1
        elif dr < TOTAL_ROWS // 2 and dc > TOTAL_COLS // 2:
            quadrants[2] += 1
        else:
            quadrants[3] += 1
    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]


if __name__ == '__main__':
    print('===== DAY 14, PUZZLE 1 =====')
    # This will not match the test answer because we're now working with the full grid
    print('The test input result is ', compute_final_positions('test_input.txt'))
    print('The main input result is ', compute_final_positions('input.txt'))

    print('\n\n===== DAY 14, PUZZLE 2 =====')
    print('The test input result is ', compute_final_positions('test_input.txt'))
    print('The main input result is ', compute_final_positions('input.txt'))
