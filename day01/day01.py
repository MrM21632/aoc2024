import collections
import re
from typing import List


def read_file(filename: str) -> List[str]:
    with open(filename, "r") as file:
        lines = file.readlines()
    return lines

def find_sum_of_distances(input_file: str) -> int:
    first, second = [], []
    lines = read_file(input_file)

    for line in lines:
        numbers = re.split(r'\s+', line)
        first.append(int(numbers[0]))
        second.append(int(numbers[1]))
    
    first.sort()
    second.sort()
    return sum(abs(first[i] - second[i]) for i in range(len(first)))

def find_similarity_score(input_file: str) -> int:
    first, second = [], []
    lines = read_file(input_file)

    for line in lines:
        numbers = re.split(r'\s+', line)
        first.append(int(numbers[0]))
        second.append(int(numbers[1]))
    
    second_freq = collections.Counter(second)
    total = 0
    for f in first:
        if f in second_freq:
            total += (f * second_freq[f])
    return total


if __name__ == '__main__':
    print('===== DAY 1, PUZZLE 1 =====')
    print('The test input result is ', find_sum_of_distances('test_input.txt'))
    print('The main input result is ', find_sum_of_distances('input.txt'))

    print('\n\n===== DAY 1, PUZZLE 2 =====')
    print('The test input result is ', find_similarity_score('test_input.txt'))
    print('The main input result is ', find_similarity_score('input.txt'))
