import functools
import re
from typing import List


def mul(x, y):
    return x * y

def read_file(filename: str) -> str:
    with open(filename, "r") as file:
        lines = file.readlines()
    return ''.join(lines)

def get_valid_operations(memory: str) -> List[str]:
    return re.findall(r'mul\(\d{1,3},\d{1,3}\)', memory)

def get_mul_result(input_file: str) -> int:
    memory = read_file(input_file)
    vaild_ops = get_valid_operations(memory)

    result = 0
    for op in vaild_ops:
        result += functools.reduce(
            lambda x, y: x * y,
            list(map(int, re.findall(r'\d+', op))),
        )
    return result

def get_mul_result_with_conditionals(input_file: str) -> int:
    memory = read_file(input_file)
    matches = re.finditer(r'mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\)', memory)

    result = 0
    do = True
    for match in matches:
        if match.group() == 'do()':
            do = True
        elif match.group() == 'don\'t()':
            do = False
        else:  # mul() operation
            result += (eval(match.group()) if do else 0)
    return result


if __name__ == '__main__':
    print('===== DAY 3, PUZZLE 1 =====')
    print('The test input result is ', get_mul_result('test_input.txt'))
    print('The main input result is ', get_mul_result('input.txt'))

    print('\n\n===== DAY 3, PUZZLE 2 =====')
    print('The test input result is ', get_mul_result_with_conditionals('test_input2.txt'))
    print('The main input result is ', get_mul_result_with_conditionals('input.txt'))
