from time import perf_counter
from typing import NamedTuple

from primes import is_prime, NUMBERS

class Result(NamedTuple):  # Returns a Result tuple with the boolean value of the is_prime call and the elapsed time.
    prime: bool
    elapsed: float

def check(n: int) -> Result:  # Computes the elapsed time to return a Result.
    t0 = perf_counter()
    prime = is_prime(n)
    return Result(prime, perf_counter() - t0)

def main() -> None:
    print(f'Checking {len(NUMBERS)} numbers sequentially:')
    t0 = perf_counter()
    for n in NUMBERS:
        prime, elapsed = check(n)
        label = 'P' if prime else ' '
        print(f'{n:16}  {label} {elapsed:9.6f}s')

    elapsed = perf_counter() - t0  # Compute and display the total elapsed time.
    print(f'Total time: {elapsed:.2f}s')

if __name__ == '__main__':
    main()