from typing import Dict, List, Tuple


def read_file(filename: str) -> Tuple[Dict[str, int], Dict[str, Tuple[str, str, str]]]:
    with open(filename, 'r') as file:
        lines = [l.strip() for l in file.readlines() if l.strip()]
    
    initial_values = dict()
    gates = dict()
    for line in lines:
        if '->' in line:
            chunks = line.split()  # in1 OP in2 -> out
            gates[chunks[4]] = (chunks[1], chunks[0], chunks[2])
        else:
            wire, value = line.split(': ')
            initial_values[wire] = int(value)
    return gates, initial_values


def perform_operation(op: str, in1: int, in2: int) -> int:
    match op:
        case 'AND':
            return in1 & in2
        case 'OR':
            return in1 | in2
        case 'XOR':
            return in1 ^ in2
        case _:
            return 0  # Should be unreachable


def simulate_gates(input_file: str) -> int:
    gates, initial_values = read_file(input_file)

    while gates:
        solvable = [
            (k, v) for k, v in gates.items()
            if v[1] in initial_values and v[2] in initial_values
        ]

        for s in solvable:
            v = s[1]
            initial_values[s[0]] = perform_operation(
                v[0], initial_values[v[1]], initial_values[v[2]],
            )
            del gates[s[0]]
    
    final_wire_values = [(k, v) for k, v in initial_values.items() if k.startswith('z')]
    result = 0
    for key, value in final_wire_values:
        shift = int(key[1:])
        result |= (value << shift)
    return result


if __name__ == '__main__':
    print('===== DAY 24, PUZZLE 1 =====')
    print('The test input result is ', simulate_gates('test_input1.txt'))  # 4
    print('The test input result is ', simulate_gates('test_input2.txt'))  # 2024
    print('The main input result is ', simulate_gates('input.txt'))

    print('\n\n===== DAY 24, PUZZLE 2 =====')
    # print('The test input result is ', simulate_gates('test_input1.txt'))
    # print('The test input result is ', simulate_gates('test_input2.txt'))
    # print('The main input result is ', simulate_gates('input.txt'))
