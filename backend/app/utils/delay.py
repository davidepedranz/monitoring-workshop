import functools
import os
import random
import time


def random_delay(min_delay: float, max_delay: float):
    """
    Decorator to add a random delay before executing the function.
    The delay is applied ONLY if the environment variable RANDOM_DELAY is set.
    :param min_delay: Min delay in seconds.
    :param max_delay: Max delay in seconds.
    :return: Decorator.
    """
    assert min_delay >= 0
    assert min_delay <= max_delay

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if os.environ.get("RANDOM_DELAY") is not None:
                wait = random.uniform(min_delay, max_delay)
                time.sleep(wait)
            return f(*args, **kwargs)

        return wrapper

    return decorator


def rare_delay(delay: float, probability: float):
    """
    Decorator to add a fixed random delay before executing the function
    with a given probability. The delay is applied ONLY if the environment
    variable RARE_DELAY is set.
    :return: Decorator.
    """
    assert probability >= 0
    assert probability <= 1

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if os.environ.get("RARE_DELAY") is not None:
                number = random.random()
                if probability >= number:
                    time.sleep(delay)
            return f(*args, **kwargs)

        return wrapper

    return decorator
