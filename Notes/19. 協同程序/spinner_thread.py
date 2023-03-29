import itertools
import time
from threading import Thread, Event

from primes import is_prime, NUMBERS

def spin(msg: str, done: Event) -> None:  # done → instance of threading.Event
    for char in itertools.cycle(r'\|/-'):  # itertools.cycle yields one character at a time → infinite loop
        status = f'\r{char} {msg}'
        print(status, end='', flush=True)
        if done.wait(.1):  # Returns True when the event is set by another thread
            break
    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')

def slow() -> int:
    time.sleep(3)
    # for n in NUMBERS:
    #     is_prime(n)
    return 42

def supervisor() -> int:
    done = Event()
    spinner = Thread(target=spin, args=('thinking!', done))  # Create a new Thread
    print(f'spinner object: {spinner}')  # Initial is the state of the thread, meaning it has not started
    spinner.start()  # Start the spinner thread
    result = slow()
    done.set()  # Set the Event flag to True; this will terminate the for loop inside the spin function
    spinner.join()  # Wait until the spinner thread finishes
    return result

def main() -> None:
    result = supervisor()
    print(f'Answer: {result}')

if __name__ == '__main__':
    main()