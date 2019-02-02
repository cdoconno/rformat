"""bench.py: utilities for time tracking and benchmarking"""

from functools import wraps
from time import time as tm
import resource

DEFAULT_TIMING_FMT = "@timecall: {0} took {1} seconds" 
DEFAULT_MEMORY_FMT = "@trackmem: {0} start: {1} end: {2} used: {3} {4}" 

def timethis(timing_fmt=DEFAULT_TIMING_FMT, verbose=True):
    """
    Parameterized decorator for tracking time of a function call
    """
    def decorator(func):
        @wraps(func)
        def time_call(*args, **kwargs):
            t1 = tm()
            result = func(*args, **kwargs)
            t2 = tm()
            d = t2-t1
            if verbose:
                print(timing_fmt.format(func.func_name, d))
            return result
        return time_call
    return decorator


def trackmem(print_fmt=DEFAULT_MEMORY_FMT, verbose=True, unit="MB"):
    """
    Paramaterized decorator for tracking memory usage of a function calls via resource module
    
    Note that there has not been any specific review of how gargage collection affects this profiling
    """
    def decorator(func):
        @wraps(func)
        def memtrack_call(*args, **kwargs):
            m1 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            result = func(*args, **kwargs)
            m2 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            usage = m2-m1
            cv = size([m1, m2, usage], unit)
            if verbose:
                print(print_fmt.format(func.func_name, cv[0], cv[1], cv[2], unit.upper()))
            return result
        return memtrack_call
    return decorator
            

def timethis_returnstats(func):
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


def size(values, unit):
    converted = []
    u = unit.lower()
    UNITS = ('b','kb','mb','gb')
    if u not in UNITS:
        raise ValueError("Must provide unit as one of %s" % list(UNITS))
    for v in values:
        if u == 'b':
            cv = v
        elif u == 'kb':
            cv = v / 1024.0
        elif u == 'mb':
            cv = v / 1024 / 1024.0
        elif u == 'gb':
            cv = v / 1024 / 1024 / 1024.0
        else:
            raise ValueError("case not handled for unit")
        converted.append(cv)
    return converted

