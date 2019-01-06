"""bench.py: utilities for time tracking and benchmarking"""

from functools import wraps
from time import time as tm

def timethis(func):
    @wraps(func)
    def time_call(*args, **kwargs):
        t1 = tm()
        result = func(*args, **kwargs)
        t2 = tm()
        print("@timecall: %s took %s seconds" % (func.func_name, str(t2-t1)))
        return result
    return time_call
