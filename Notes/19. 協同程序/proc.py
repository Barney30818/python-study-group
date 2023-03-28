import sys
from time import perf_counter
from typing import NamedTuple
from multiprocessing import Process, SimpleQueue, cpu_count
from multiprocessing import queues

from primes import is_prime, NUMBERS

class PrimeResult(NamedTuple):
    n: int
    prime: bool
    elapsed: float

JobQueue = queues.SimpleQueue[int]  # Send numbers to the processes that will do the work
ResultQueue = queues.SimpleQueue[PrimeResult]  # Collect the results in main

def check(n: int) -> PrimeResult:
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n, res, perf_counter() - t0)

def worker(jobs: JobQueue, results: ResultQueue) -> None:
    while n := jobs.get():
        results.put(check(n))  # Enqueue PrimeResult
    results.put(PrimeResult(0, False, 0.0))  # Let the main loop know that this worker is done.

def start_jobs(
    procs: int, jobs: JobQueue, results: ResultQueue  # Compute the prime checks in parallel.
) -> None:
    for n in NUMBERS:
        jobs.put(n)  # Enqueue the numbers to be checked in jobs.
    for _ in range(procs):
        proc = Process(target=worker, args=(jobs, results))  # Fork a child process for each worker.
        proc.start()  # Start each child process.
        jobs.put(0)  # Enqueue one 0 for each process, to terminate them

def main() -> None:
    if len(sys.argv) < 2:
        procs = cpu_count()
    else:
        procs = int(sys.argv[1])

    print(f'Checking {len(NUMBERS)} numbers with {procs} processes:')
    t0 = perf_counter()
    jobs: JobQueue = SimpleQueue()
    results: ResultQueue = SimpleQueue()
    start_jobs(procs, jobs, results)  # Start proc processes to consume jobs and post results.
    checked = report(procs, results)  # Retrieve the results and display them.
    elapsed = perf_counter() - t0
    print(f'{checked} checks in {elapsed:.2f}s')

def report(procs: int, results: ResultQueue) -> int:
    checked = 0
    procs_done = 0
    while procs_done < procs:
        n, prime, elapsed = results.get()
        if n == 0:
            procs_done += 1
        else:
            checked += 1
            label = 'P' if prime else ' '
            print(f'{n:16}  {label} {elapsed:9.6f}s')
    return checked

if __name__ == '__main__':
    main()