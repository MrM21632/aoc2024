import copy
from itertools import accumulate
from multiprocessing import Pool, cpu_count
from typing import Dict, List, Callable


class Computer:
    instruction_map: Dict[int, Callable[[int], None]]
    registers: List[int]
    instructions: List[int]
    output: List[str]
    instruction_pointer: int

    def __init__(self, registers: List[int], instructions: List[int]):
        self.instruction_map = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }
        self.instruction_pointer = 0
        self.output = []
        self.registers = registers
        self.instructions = instructions
    
    def execute_instruction(self) -> None:
        instruction, operand = (
            self.instructions[self.instruction_pointer],
            self.instructions[self.instruction_pointer + 1],
        )
        self.instruction_map[instruction](operand)
    
    def run(self) -> str:
        while self.instruction_pointer < len(self.instructions):
            self.execute_instruction()
        return ','.join(self.output)

    def get_operand_value(self, operand: int) -> int:
        if 0 <= operand < 4:
            return operand
        elif 4 <= operand < 7:
            return self.registers[operand - 4]
        else:
            return 0

    def adv(self, operand: int) -> None:
        self.registers[0] = self.registers[0] >> self.get_operand_value(operand)
        self.instruction_pointer += 2
    
    def bdv(self, operand: int) -> None:
        self.registers[1] = self.registers[0] >> self.get_operand_value(operand)
        self.instruction_pointer += 2
    
    def cdv(self, operand: int) -> None:
        self.registers[2] = self.registers[0] >> self.get_operand_value(operand)
        self.instruction_pointer += 2
    
    def bxl(self, operand: int) -> None:
        self.registers[1] ^= operand
        self.instruction_pointer += 2
    
    def bxc(self, operand: int) -> None:
        self.registers[1] ^= self.registers[2]
        self.instruction_pointer += 2
    
    def bst(self, operand: int) -> None:
        self.registers[1] = self.get_operand_value(operand) & 7
        self.instruction_pointer += 2
    
    def jnz(self, operand: int) -> None:
        if self.registers[0] == 0:
            self.instruction_pointer += 2
        else:
            self.instruction_pointer = operand
    
    def out(self, operand: int) -> None:
        self.output.append(str(self.get_operand_value(operand) & 7))
        self.instruction_pointer += 2


def get_computer(filename: str) -> Computer:
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    registers = []
    instructions = []
    for line in lines:
        if 'Register' in line:
            registers.append(int(line.strip().split(': ')[-1]))
        elif 'Program' in line:
            instructions = list(map(int, line.strip().split(': ')[-1].split(',')))
    return Computer(registers, instructions)

def reset_computer(computer: Computer, new_a: int) -> Computer:
    computer.output.clear()
    computer.instruction_pointer = 0
    computer.registers = [new_a, 0, 0]
    return computer


def execute_program(input_file: str) -> str:
    computer = get_computer(input_file)
    return computer.run()

def calculate_batch_sizes(tasks: int, workers: int):
        x, y = divmod(tasks, workers)
        return [x + (y > 0)] * y + [x] * (workers - y)
    
def build_ranges(batch_sizes: list):
    upper_bounds = [*accumulate(batch_sizes)]
    lower_bounds = [0] + upper_bounds[:-1]
    return [range(l, u) for l, u in zip(lower_bounds, upper_bounds)]

def batch_run(computer: Computer, desired: str, batch_range: range):
    for a in batch_range:
        computer = reset_computer(computer, a)
        output = computer.run()

        if output == desired:
            print(f"Found it! {a}")
            return
    print("Didn't find it :(")

def find_smallest_value_for_register(input_file: str) -> int:
    """
    Some very basic observations after analyzing and reverse-engineering the opcodes:

    These are the instructions as executed, in order, in the original program:
    B = A & 7
    B = B ^ 7
    C = C >> B
    A = A >> 3
    B = B ^ 7
    B = B ^ C
    out(B)
    jnz(0)

    Notice that we truncate A by three bits each iteration. This, combined with
    the bst operation at the beginning, means that the length of A, in bits, will
    ultimately dictate the length of our output. In order to get an output of length
    16, we need a value of A that is at least 8**15. We may also have an upper bound
    of 8**16 = 2**48, but I'm not as certain about this.
    """
    computer = get_computer(input_file)
    low_a, high_a = 8 ** (len(computer.instructions) - 1), 8 ** len(computer.instructions)
    desired = ','.join(list(map(str, computer.instructions)))
    
    total_workers = cpu_count()
    batch_sizes = calculate_batch_sizes(high_a - low_a, total_workers)
    batch_ranges = build_ranges(batch_sizes)

    with Pool(total_workers) as pool:
        _ = pool.starmap(batch_run, [(copy.deepcopy(computer), desired, r) for r in batch_ranges])
 

if __name__ == '__main__':
    print('===== DAY 17, PUZZLE 1 =====')
    # 4,6,3,5,6,3,5,2,1,0
    print('The first test input result is ', execute_program('test_input1.txt'))
    print('The main input result is ', execute_program('input.txt'))

    print('\n\n===== DAY 17, PUZZLE 2 =====')
    # 117440
    print('The first test input result is ', find_smallest_value_for_register('test_input2.txt'))
    print('The main input result is ', find_smallest_value_for_register('input.txt'))
