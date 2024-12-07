import re
from typing import List, Callable


ADD = lambda x, y: x + y
MULTIPLY = lambda x, y: x * y
CONCAT = lambda x, y: int(f'{x}{y}')


def read_file(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines

def get_equations(input_file: str) -> List[List[int]]:
    lines = read_file(input_file)
    result = []
    for line in lines:
        result.append(list(map(int, re.split(r'\D+', line.strip()))))
    return result

def has_solution(
    operators: List[Callable[[int, int], int]],
    target: int,
    total: int,
    remaining: List[int],
) -> bool:
    if not remaining:
        return total == target
    if total > target:
        return False
    
    for op in operators:
        if has_solution(operators, target, op(total, remaining[0]), remaining[1:]):
            return True
    return False

def check_solvability(input_file: str, part2: bool = False) -> int:
    equations = get_equations(input_file)
    operators = [ADD, MULTIPLY]
    if part2:
        operators.append(CONCAT)

    result = 0
    for equ in equations:
        if has_solution(operators, equ[0], equ[1], equ[2:]):
            result += equ[0]
    return result


if __name__ == '__main__':
    print('===== DAY 7, PUZZLE 1 =====')
    print('The test input result is ', check_solvability('test_input.txt'))
    print('The main input result is ', check_solvability('input.txt'))

    print('\n\n===== DAY 7, PUZZLE 2 =====')
    print('The test input result is ', check_solvability('test_input.txt', True))
    print('The main input result is ', check_solvability('input.txt', True))
