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
        self.registers[0] = self.registers[0] // (2 ** self.get_operand_value(operand))
        self.instruction_pointer += 2
    
    def bdv(self, operand: int) -> None:
        self.registers[1] = self.registers[0] // (2 ** self.get_operand_value(operand))
        self.instruction_pointer += 2
    
    def cdv(self, operand: int) -> None:
        self.registers[2] = self.registers[0] // (2 ** self.get_operand_value(operand))
        self.instruction_pointer += 2
    
    def bxl(self, operand: int) -> None:
        self.registers[1] ^= operand
        self.instruction_pointer += 2
    
    def bxc(self, operand: int) -> None:
        self.registers[1] ^= self.registers[2]
        self.instruction_pointer += 2
    
    def bst(self, operand: int) -> None:
        self.registers[1] = self.get_operand_value(operand) % 8
        self.instruction_pointer += 2
    
    def jnz(self, operand: int) -> None:
        if self.registers[0] == 0:
            self.instruction_pointer += 2
        else:
            self.instruction_pointer = operand
    
    def out(self, operand: int) -> None:
        self.output.append(str(self.get_operand_value(operand) % 8))
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


def execute_program(input_file: str) -> str:
    computer = get_computer(input_file)
    return computer.run()


if __name__ == '__main__':
    print('===== DAY 17, PUZZLE 1 =====')
    # 4,6,3,5,6,3,5,2,1,0
    print('The first test input result is ', execute_program('test_input.txt'))
    print('The main input result is ', execute_program('input.txt'))

    print('\n\n===== DAY 17, PUZZLE 2 =====')
    print('The first test input result is ', execute_program('test_input.txt'))
    print('The main input result is ', execute_program('input.txt'))
