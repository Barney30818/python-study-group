import asyncio
import itertools
import time

from primes import is_prime, NUMBERS

async def spin(msg: str) -> None:
    for char in itertools.cycle(r'\|/-'):
        status = f'\r{char} {msg}'
        print(status, flush=True, end='')
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError: # asyncio.CancelledError is raised when the cancel method is called on the Task controlling this coroutine.
            break
    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')

async def slow() -> int:
    await asyncio.sleep(3)
    # time.sleep(3)
    # for n in NUMBERS:
    #     is_prime(n)
    return 42

def main() -> None:  # The only regular function defined in this program, the others are coroutines.
    result = asyncio.run(supervisor())  # Start the event loop → main function will stay blocked.
    print(f'Answer: {result}')

async def supervisor() -> int:
    spinner = asyncio.create_task(spin('thinking!'))  # asyncio.create_task schedules the eventual execution of spin, immediately returning an instance of asyncio.Task.
    print(f'spinner object: {spinner}')
    result = await slow()  # Call slow, blocking supervisor
    spinner.cancel()  # Raises a CancelledError
    return result

if __name__ == '__main__':
    main()