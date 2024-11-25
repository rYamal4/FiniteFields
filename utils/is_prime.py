import math


def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


def is_prime_power(n):
    if n < 1:
        return False
    for k in range(1, int(math.log2(n)) + 1):
        p = round(n ** (1 / k))
        if p ** k == n and is_prime(p):
            return p
    return -1