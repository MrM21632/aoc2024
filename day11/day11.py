import functools
from typing import List


def read_file(filename: str) -> str:
    with open(filename, 'r') as file:
        contents = file.read()
    return contents

def construct_arrangement(input_file) -> List[int]:
    contents = read_file(input_file)
    return list(map(int, contents.strip().split()))

def perform_blinks(input_file: str, blinks: int) -> int:
    stones = construct_arrangement(input_file)

    @functools.lru_cache(None)
    def blink(stone: int, blinks_left: int) -> int:
        if blinks_left == 0:
            return 1
        
        result = 0
        if stone == 0:
            result += blink(1, blinks_left - 1)
        elif len(str(stone)) & 1:  # Odd length
            result += blink(stone * 2024, blinks_left - 1)
        else:
            stone_str = str(stone)
            stone_str_len = len(stone_str) // 2
            result += blink(int(stone_str[:stone_str_len]), blinks_left - 1)
            result += blink(int(stone_str[stone_str_len:]), blinks_left - 1)
        return result

    return sum(blink(s, blinks) for s in stones)



if __name__ == '__main__':
    print('===== DAY 9, PUZZLE 1 =====')
    print('The test input result is ', perform_blinks('test_input.txt', 25))
    print('The main input result is ', perform_blinks('input.txt', 25))

    print('\n\n===== DAY 9, PUZZLE 2 =====')
    print('The test input result is ', perform_blinks('test_input.txt', 75))
    print('The main input result is ', perform_blinks('input.txt', 75))
