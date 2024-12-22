number = 123
PRUNE_MOD = 16777216

for _ in range(10):
    number ^= (number << 6)   # Multiply by 64
    number &= (PRUNE_MOD - 1)
    number ^= (number >> 5)   # Divide by 32
    number &= (PRUNE_MOD - 1)
    number ^= (number << 11)  # Multiply by 2048
    number &= (PRUNE_MOD - 1)
    print(number)