from typing import List


TOTAL_BLINKS = 25


def read_file(filename: str) -> str:
    with open(filename, 'r') as file:
        contents = file.read()
    return contents

def construct_arrangement(input_file) -> List[int]:
    contents = read_file(input_file)
    return list(map(int, contents.strip().split()))

def perform_blinks(input_file: str) -> int:
    stones = construct_arrangement(input_file)

    for _ in range(25):
        new_stones = []
        for s in stones:
            if s == 0:
                new_stones.append(1)
            elif len(str(s)) & 1:  # Odd length
                new_stones.append(s * 2024)
            else:  # Even length
                s_str = str(s)
                s_str_len = len(s_str) // 2
                new_stones.extend([int(s_str[:s_str_len]), int(s_str[s_str_len:])])
        stones = new_stones
    return len(stones)



if __name__ == '__main__':
    print('===== DAY 9, PUZZLE 1 =====')
    print('The test input result is ', perform_blinks('test_input.txt'))
    print('The main input result is ', perform_blinks('input.txt'))

    print('\n\n===== DAY 9, PUZZLE 2 =====')
    print('The test input result is ', perform_blinks('test_input.txt'))
    print('The main input result is ', perform_blinks('input.txt'))
