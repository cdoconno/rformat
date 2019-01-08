"""bench.py: utilities for time tracking and benchmarking"""

from functools import wraps
from time import time as tm

def timethis(func):
    """
    this decorator changes the function signature of `func` passed in
    returns a tuple where the first item is the normal result and the second is a dictionary of timing info
    """
    @wraps(func)
    def time_call(*args, **kwargs):
        t1 = tm()
        result = func(*args, **kwargs)
        t2 = tm()
        d = t2-t1
        print("@timecall: %s took %s seconds" % (func.func_name, d))
        return result, {'func_name': func.func_name, 'duration': d}
    return time_call
