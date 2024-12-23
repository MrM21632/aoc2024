import collections
from typing import Dict, Set


def read_file(filename: str) -> Dict[str, Set[str]]:
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    graph = collections.defaultdict(set)
    for line in lines:
        u, v = line.strip().split('-')
        graph[u].add(v)
        graph[v].add(u)
    return graph


def find_connected_computers(input_file: str) -> int:
    graph = read_file(input_file)

    result = set()
    for u in graph.keys():
        for v in graph[u]:
            for w in graph[v]:
                # We already know u and v, and v and w, are connected
                # Checking for u and w is enough at this point
                if u in graph[w]:
                    if u.startswith('t') or v.startswith('t') or w.startswith('t'):
                        result.add(','.join(sorted([u, v, w])))
    return len(result)

def find_password_for_largest_party(input_file: str) -> int:
    graph = read_file(input_file)

    def bohn_kerbosch(r, p, x):
        if not p and not x:
            yield r
        else:
            for v in p.copy():
                yield from bohn_kerbosch(r | {v}, p & graph[v], x & graph[v])
                p.remove(v)
                x.add(v)
    
    component, complen = None, 0
    for comp in bohn_kerbosch(set(), set(graph.keys()), set()):
        if len(comp) > complen:
            component, complen = comp, len(comp)
    
    return ','.join(sorted(list(component)))


if __name__ == '__main__':
    print('===== DAY 23, PUZZLE 1 =====')
    print('The test input result is ', find_connected_computers('test_input.txt'))  # 7
    print('The main input result is ', find_connected_computers('input.txt'))

    print('\n\n===== DAY 23, PUZZLE 2 =====')
    print('The test input result is ', find_password_for_largest_party('test_input.txt'))  # co,de,ka,ta
    print('The main input result is ', find_password_for_largest_party('input.txt'))
