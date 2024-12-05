import collections
from typing import Dict, List, Tuple


def read_file(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines

def construct_graph_and_indegree(rules_file: str) -> Tuple[Dict[int, List[int]], Dict[int, List[int]]]:
    # Defaultdict allows us to correctly handle the deepest child nodes
    # (i.e., who have no children themselves) down the line.
    graph = collections.defaultdict(list)
    indegree = collections.defaultdict(int)

    lines = read_file(rules_file)
    for line in lines:
        values = line.split('|')
        graph[int(values[0])].append(int(values[1]))
        indegree[int(values[1])] += 1
    return graph, indegree

def construct_updates(updates_file: str) -> List[List[int]]:
    lines = read_file(updates_file)
    result = []
    for line in lines:
        result.append(list(map(int, line.split(','))))
    return result

def get_sum_of_middles(rules_file: str, updates_file: str) -> int:
    pass


if __name__ == '__main__':
    print('===== DAY 5, PUZZLE 1 =====')
    print('The test input result is ', get_sum_of_middles('test_input_rules.txt', 'test_input_updates.txt'))
    print('The main input result is ', get_sum_of_middles('input_rules.txt', 'input_updates.txt'))

    print('\n\n===== DAY 5, PUZZLE 2 =====')
    # print('The test input result is ', find_all_x_mases('test_input.txt'))
    # print('The main input result is ', find_all_x_mases('input.txt'))