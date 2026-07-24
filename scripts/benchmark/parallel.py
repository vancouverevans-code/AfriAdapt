"""
Parallel benchmark generation utilities.
"""

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed


MAX_WORKERS = 4


def run_parallel(tasks, worker):
    """
    Execute benchmark tasks in parallel.

    Parameters
    ----------
    tasks
        Iterable of task dictionaries.

    worker
        Callable(task) -> result

    Returns
    -------
    list
    """

    results = []

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:

        futures = [
            executor.submit(worker, task)
            for task in tasks
        ]

        for future in as_completed(futures):

            try:
                results.append(future.result())

            except Exception as e:

                print(f"Worker failed: {e}")

    return results