from typing import List


def read_file(filename: str) -> List[str]:
    with open(filename, "r") as file:
        lines = file.readlines()
    return lines

def is_report_safe(report: List[int]) -> bool:
    incr_or_decr = report == sorted(report) or report == sorted(report, reverse=True)
    good_gaps = True
    for i in range(len(report) - 1):
        if not (1 <= abs(report[i] - report[i + 1]) <= 3):
            good_gaps = False
            break
    return incr_or_decr and good_gaps

def count_safe_reports(input_file: str) -> int:
    lines = read_file(input_file)
    total = 0

    for line in lines:
        numbers = list(map(int, line.split()))
        total += (1 if is_report_safe(numbers) else 0)
        
    return total

def count_safe_reports_with_dampening(input_file: str) -> int:
    lines = read_file(input_file)
    total = 0

    for line in lines:
        numbers = list(map(int, line.split()))
        good = False
        for i in range(len(numbers)):
            x = numbers[:i] + numbers[i + 1:]
            if is_report_safe(x):
                good = True
                break
        total += (1 if good else 0)
    return total


if __name__ == '__main__':
    print('===== DAY 1, PUZZLE 1 =====')
    print('The test input result is ', count_safe_reports('test_input.txt'))
    print('The main input result is ', count_safe_reports('input.txt'))

    print('\n\n===== DAY 1, PUZZLE 2 =====')
    print('The test input result is ', count_safe_reports_with_dampening('test_input.txt'))
    print('The main input result is ', count_safe_reports_with_dampening('input.txt'))
