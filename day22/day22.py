import collections
from typing import List


PRUNE_MOD = 16777216  # Note that this is a power of two!
ITERATIONS = 2000


def read_file(filename: str) -> List[int]:
    with open(filename, 'r') as file:
        secret_numbers = [int(l.strip()) for l in file.readlines()]
    return secret_numbers


def get_next_secret_number(number: int) -> int:
    number ^= (number << 6)    # Multiply by 64
    number &= (PRUNE_MOD - 1)  # Modulo 2^24
    number ^= (number >> 5)    # Divide by 32
    number &= (PRUNE_MOD - 1)
    number ^= (number << 11)   # Multiply by 2048
    return number & (PRUNE_MOD - 1)

def simulate_secnum_generation(input_file: str) -> int:
    secret_numbers = read_file(input_file)

    result = 0
    for number in secret_numbers:
        for _ in range(ITERATIONS):
            number = get_next_secret_number(number)
        result += number
    return result

def maximize_bananas(input_file: str) -> int:
    secret_numbers = read_file(input_file)

    # prices: Price history for each trader
    # changes: Price change history for each trader
    prices, changes = [], []
    for number in secret_numbers:
        p, c = [], []
        # Get prices for each secret number, including the very first
        for _ in range(ITERATIONS):
            p.append(number % 10)
            number = get_next_secret_number(number)
        p.append(number % 10)
        # Get changes in price over time
        for i in range(1, len(p)):
            c.append(p[i] - p[i - 1])
        prices.append(p)
        changes.append(c)
    
    # Maps a trend (i.e., quadruple of price changes) to the total bananas we
    # can earn from this trend
    trend_to_earnings = collections.Counter()
    for i, cl in enumerate(changes):
        # Note: Trends will net the same amount no matter when we find them
        seen = set()
        for j in range(3, len(cl)):
            trend = tuple(cl[j - 3:j + 1])
            if trend not in seen:
                # j + 1 because the lists are staggered
                trend_to_earnings[trend] += prices[i][j + 1]
                seen.add(trend)
    return max(trend_to_earnings.values())


if __name__ == '__main__':
    print('===== DAY 22, PUZZLE 1 =====')
    print('The test input result is ', simulate_secnum_generation('test_input1.txt'))  # 37327623
    print('The main input result is ', simulate_secnum_generation('input.txt'))

    print('\n\n===== DAY 22, PUZZLE 2 =====')
    print('The test input result is ', maximize_bananas('test_input2.txt'))  # 23
    print('The main input result is ', maximize_bananas('input.txt'))
