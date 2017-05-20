from time import time
from functools import wraps
from collections import defaultdict
import sys


def print_error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def deprecated_1(func):
    print_error("Function {} is deprecated".format(func.__name__))
    return func


def deprecated_2(func):
    @wraps(func)
    def inner(*args, **kwargs):
        print_error("Function {} is deprecated and will be removed "
                    "in the next release".format(func.__name__))
        return func(*args, **kwargs)

    return inner


def deprecated_3(func):
    @wraps(func)
    def inner(*args, **kwargs):
        deprecated_3.calls[func.__name__] += 1
        print_error("Function {} is deprecated and will be removed "
                    "in the next release. Execution number: {}".format(
            func.__name__,
            deprecated_3.calls[func.__name__],
        ))
        return func(*args, **kwargs)

    return inner
deprecated_3.calls = defaultdict(int)


def my_timeit(func):
    @wraps(func)
    def inner(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        print("Execution time {}: {:.2e} ms".format(
            func.__name__,
            100 * (time() - start_time),
        ))
        return result

    return inner


@deprecated_1
@deprecated_2
@deprecated_3
@my_timeit
def f():
    pass

f()
f()
f()
f()
print(deprecated_3.calls[f.__name__])
