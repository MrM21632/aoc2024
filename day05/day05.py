import collections
from typing import Dict, List, Set, Tuple


def read_file(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines

def construct_rules_graph(rules_file: str) -> Tuple[Dict[int, Set[int]], Dict[int, int]]:
    # Defaultdict allows us to correctly handle the deepest child nodes
    # (i.e., who have no children themselves) down the line.
    graph = collections.defaultdict(set)

    lines = read_file(rules_file)
    for line in lines:
        values = line.split('|')
        first, second = int(values[0]), int(values[1])
        graph[first].add(second)
    return graph

def construct_updates(updates_file: str) -> List[List[int]]:
    lines = read_file(updates_file)
    result = []
    for line in lines:
        result.append(list(map(int, line.split(','))))
    return result

def group_updates(graph: Dict[int, Set[int]], updates: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
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

def fix_update(graph: Dict[int, Set[int]], update: List[int]) -> List[int]:
    for i, page in enumerate(update[:-1]):
        errors = graph[page].intersection(update[i + 1:])
        if errors:
            update[i:] = list(errors) + [x for x in update[i:] if x not in errors]
            return fix_update(graph, update)
    return update

def get_sum_of_middles(rules_file: str, updates_file: str) -> int:
    graph = construct_rules_graph(rules_file)
    updates = construct_updates(updates_file)

    correct, _ = group_updates(graph, updates)
    total = sum(c[len(c) // 2] for c in correct)
    return total

def get_sum_of_fixed_middles(rules_file: str, updates_file: str) -> int:
    graph = construct_rules_graph(rules_file)
    updates = construct_updates(updates_file)

    _, incorrect = group_updates(graph, updates)
    total = 0
    for i in incorrect:
        corrected = fix_update(graph, i)
        total += corrected[len(corrected) // 2]
    return total


if __name__ == '__main__':
    print('===== DAY 5, PUZZLE 1 =====')
    print('The test input result is ', get_sum_of_middles('test_input_rules.txt', 'test_input_updates.txt'))
    print('The main input result is ', get_sum_of_middles('input_rules.txt', 'input_updates.txt'))

    print('\n\n===== DAY 5, PUZZLE 2 =====')
    print('The test input result is ', get_sum_of_fixed_middles('test_input_rules.txt', 'test_input_updates.txt'))
    print('The main input result is ', get_sum_of_fixed_middles('input_rules.txt', 'input_updates.txt'))
