import collections
import functools
from typing import List, Tuple


class TrieNode:
    def __init__(self):
        self.is_end = False
        self.children = [None] * 26

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        curr = self.root
        for c in word:
            index = ord(c) - ord('a')
            if not curr.children[index]:
                curr.children[index] = TrieNode()
            curr = curr.children[index]
        curr.is_end = True


def get_stripes_and_towels(filename: str) -> Tuple[List[str], List[str]]:
    with open(filename, 'r') as file:
        lines = [l.strip() for l in file.readlines() if l.strip()]
    
    stripes = lines[0].split(', ')
    return stripes, lines[1:]


def is_towel_possible(towel: str, stripes: List[str]) -> bool:
    stripeset = set(stripes)
    queue = collections.deque([0])
    seen = set()

    while queue:
        start = queue.popleft()
        if start == len(towel):
            return True
        
        for end in range(start + 1, len(towel) + 1):
            if end in seen:
                continue
            if towel[start:end] in stripeset:
                queue.append(end)
                seen.add(end)

    return False

# Disgustingly memory-inefficient; will chew up RAM like there's no tomorrow
# TODO: Look into making this solution use memory space more efficiently, if it's even possible.
def count_ways_trie(towel: str, stripes: List[str]) -> List[str]:
    memo = dict()
    trie = Trie()
    for stripe in stripes:
        trie.insert(stripe)
    
    for start in range(len(towel), -1, -1):
        valid = []
        curr = trie.root

        for end in range(start, len(towel)):
            char = towel[end]
            index = ord(char) - ord('a')
            if not curr.children[index]:
                break
            curr = curr.children[index]

            if curr.is_end:
                word = towel[start:end + 1]
                if end == len(towel) - 1:
                    valid.append(word)
                else:
                    next_sentences = memo.get(end + 1, [])
                    for sentence in next_sentences:
                        valid.append(f"{word} {sentence}")
        memo[start] = valid
    
    return memo.get(0, [])


def count_possible_towels(input_file: str) -> int:
    stripes, towels = get_stripes_and_towels(input_file)

    result = 0
    for towel in towels:
        result += (1 if is_towel_possible(towel, stripes) else 0)
    return result

def count_ways_to_make_towels(input_file: str) -> int:
    stripes, towels = get_stripes_and_towels(input_file)

    # result = 0
    # for towel in towels:
    #     result += len(count_ways_trie(towel, stripes))
    # return result
    @functools.lru_cache(None)
    def count_ways(towel: str):
        if not towel:
            return 1
        return sum(
            count_ways(towel[len(stripe):])
            for stripe in stripes
            if towel.startswith(stripe)
        )
    
    return sum(count_ways(towel) for towel in towels)


if __name__ == '__main__':
    print('===== DAY 19, PUZZLE 1 =====')
    print('The test input result is ', count_possible_towels('test_input.txt'))  # 6
    print('The main input result is ', count_possible_towels('input.txt'))

    print('\n\n===== DAY 19, PUZZLE 2 =====')
    print('The test input result is ', count_ways_to_make_towels('test_input.txt'))  # 16
    print('The main input result is ', count_ways_to_make_towels('input.txt'))
