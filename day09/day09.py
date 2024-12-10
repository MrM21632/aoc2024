import collections
import heapq
from typing import Dict, List, Tuple


def read_file(filename: str) -> str:
    with open(filename, 'r') as file:
        content = file.read()
    return content

def construct_disk(input_file: str) -> List[int]:
    content = read_file(input_file)
    result = []

    on_empty_block = False
    curr_file_id = 0
    for c in content:
        length = int(c)
        if on_empty_block:
            result.extend([-1] * length)
        else:
            result.extend([curr_file_id] * length)
            curr_file_id += 1
        on_empty_block = not on_empty_block
    return result

def get_groups_and_positions_on_disk(
    input_file: str,
) -> Tuple[Dict[int, Tuple[int, int]], Dict[int, List[int]]]:
    lengths = [int(c) for c in read_file(input_file)]
    files = dict()                         # File ID: (start position, length)
    empty = collections.defaultdict(list)  # length: start positions

    curr = 0
    for i, l in enumerate(lengths):
        if i & 1:
            if l > 0:
                heapq.heappush(empty[l], curr)
        else:
            files[i // 2] = (curr, l)
        curr += l
    return files, empty

def compute_checksum(disk: List[int]) -> int:
    return sum([i * v for i, v in enumerate(disk) if v != -1])

def defrag_disk(input_file: str) -> int:
    disk = construct_disk(input_file)

    # Defrag the disk by shifting memory from hi to lo as needed
    lo, hi = 0, len(disk) - 1
    while lo <= hi:
        if disk[lo] != -1:
            lo += 1
        elif disk[hi] != -1:
            disk[lo], disk[hi] = disk[hi], disk[lo]
            lo += 1
            hi -= 1
        else:
            hi -= 1
    
    return compute_checksum(disk)

def defrag_without_refrag(input_file: str) -> int:
    files, empty = get_groups_and_positions_on_disk(input_file)

    # Defrag the disk by shifting whole files to empty blocks where they can fit
    for id in sorted(files.keys(), reverse=True):
        fs, fl = files[id]
        candidates = sorted([(empty[l][0], l) for l in empty if l >= fl])
        if candidates:
            es, el = candidates[0]
            if fs > es:
                files[id] = (es, fl)
                heapq.heappop(empty[el])
                if not empty[el]:
                    del empty[el]
                
                remaining = el - fl
                if remaining:
                    heapq.heappush(empty[remaining], es + fl)
    
    return sum(
        id * (start * length + (length * (length - 1)) // 2)
        for id, (start, length) in files.items()
    )


if __name__ == '__main__':
    print('===== DAY 9, PUZZLE 1 =====')
    print('The test input result is ', defrag_disk('test_input.txt'))
    print('The main input result is ', defrag_disk('input.txt'))

    print('\n\n===== DAY 9, PUZZLE 2 =====')
    print('The test input result is ', defrag_without_refrag('test_input.txt'))
    print('The main input result is ', defrag_without_refrag('input.txt'))
