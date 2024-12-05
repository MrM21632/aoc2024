import collections
from typing import Dict, List, Tuple


def read_file(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines

def construct_rules_graph(rules_file: str) -> Dict[int, List[int]]:
    # Defaultdict allows us to correctly handle the deepest child nodes
    # (i.e., who have no children themselves) down the line.
    graph = collections.defaultdict(list)

    lines = read_file(rules_file)
    for line in lines:
        values = line.split('|')
        graph[int(values[0])].append(int(values[1]))
    return graph

def construct_updates(updates_file: str) -> List[List[int]]:
    lines = read_file(updates_file)
    result = []
    for line in lines:
        result.append(list(map(int, line.split(','))))
    return result

def group_updates(graph: Dict[int, List[int]], updates: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
    correct, incorrect = [], []
    for u in updates:
        valid = True
        for i in range(len(u) - 1):
            if any(x not in graph[u[i]] for x in u[i + 1:]):
                valid = False
                break
        if valid:
            correct.append(u)
        else:
            incorrect.append(u)
    return correct, incorrect

def get_sum_of_middles(rules_file: str, updates_file: str) -> int:
    graph = construct_rules_graph(rules_file)
    updates = construct_updates(updates_file)

    correct, _ = group_updates(graph, updates)
    total = 0
    for c in correct:
        if len(c) % 2 == 0:
            total += c[len(c) // 2 - 1]
        else:
            total += c[len(c) // 2]
    return total

def get_sum_of_fixed_middles(rules_file: str, updates_file: str) -> int:
    graph = construct_rules_graph(rules_file)
    updates = construct_updates(updates_file)

    _, incorrect = group_updates(graph, updates)
    total = 0
    for i in incorrect:
        # TODO: Correctly order the list, find its middle
        pass
    return total


if __name__ == '__main__':
    print('===== DAY 5, PUZZLE 1 =====')
    print('The test input result is ', get_sum_of_middles('test_input_rules.txt', 'test_input_updates.txt'))
    print('The main input result is ', get_sum_of_middles('input_rules.txt', 'input_updates.txt'))

    print('\n\n===== DAY 5, PUZZLE 2 =====')
    print('The test input result is ', get_sum_of_fixed_middles('test_input_rules.txt', 'test_input_updates.txt'))
    print('The main input result is ', get_sum_of_fixed_middles('input_rules.txt', 'input_updates.txt'))