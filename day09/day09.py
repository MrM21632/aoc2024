from typing import List


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
        block_size = int(c)
        if on_empty_block:
            result.extend([-1] * block_size)
        else:
            result.extend([curr_file_id] * block_size)
            curr_file_id += 1
        on_empty_block = not on_empty_block
    return result

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


if __name__ == '__main__':
    print('===== DAY 9, PUZZLE 1 =====')
    print('The test input result is ', defrag_disk('test_input.txt'))
    print('The main input result is ', defrag_disk('input.txt'))

    print('\n\n===== DAY 9, PUZZLE 2 =====')  # TODO
    print('The test input result is ', defrag_disk('test_input.txt'))
    print('The main input result is ', defrag_disk('input.txt'))
