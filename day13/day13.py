import re
from typing import cast, List, Tuple, TypeAlias


Pair: TypeAlias = Tuple[int, int]
ClawMachine: TypeAlias = List[Pair]  # [A, B, Prize]


NUMBERS = re.compile(r"(\d+).+?(\d+)")
A_TOKENS = 3
B_TOKENS = 1
CORRECTION = 10_000_000_000_000


def read_file(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        contents = file.readlines()
    return contents

def parse_line(line: str) -> Pair:
    match = NUMBERS.search(line)
    return cast(Pair, tuple(map(int, match.groups())))

def get_claw_machines(input_file: str) -> List[ClawMachine]:
    lines = read_file(input_file)

    result = []
    for i in range(0, len(lines), 4):
        button_a = parse_line(lines[i])
        button_b = parse_line(lines[i + 1])
        prize = parse_line(lines[i + 2])
        result.append(cast(ClawMachine, [button_a, button_b, prize]))
    return result

def reach_prize(machine: ClawMachine, part2: bool = False) -> Tuple[int, int]:
    # (A button deltas), (B button deltas), (prize coords)
    (a, b), (c, d), (e, f) = machine
    if part2:
        e += CORRECTION
        f += CORRECTION

    # Cramer's Rule to the rescue. We have a system of equations that we can
    # pretty quickly solve. All we need to do is compute the following:
    # 
    #   (ed - cf) / (ad - bc)
    #   (af - be) / (ad - bc)
    # 
    # If both results are whole numbers, we're good to go.
    a_presses, rem = divmod(e * d - c * f, a * d - b * c)
    if rem:
        return (-1, -1)
    b_presses, rem = divmod(a * f - b * e, a * d - b * c)
    if rem:
        return (-1, -1)
    return (a_presses, b_presses)

def compute_total_tokens(input_file: str, part2: bool = False) -> int:
    machines = get_claw_machines(input_file)

    result = 0
    for machine in machines:
        a_presses, b_presses = reach_prize(machine, part2)
        if a_presses != -1 and b_presses != -1:
            result += (A_TOKENS * a_presses + B_TOKENS * b_presses)
    return result


if __name__ == '__main__':
    print('===== DAY 13, PUZZLE 1 =====')
    # This will not match the test answer because we're now working with the full grid
    print('The test input result is ', compute_total_tokens('test_input.txt'))
    print('The main input result is ', compute_total_tokens('input.txt'))

    print('\n\n===== DAY 13, PUZZLE 2 =====')
    print('The test input result is ', compute_total_tokens('test_input.txt', True))
    print('The main input result is ', compute_total_tokens('input.txt', True))
