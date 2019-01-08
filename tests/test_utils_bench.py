import pytest
import sys
import time
import re

from rformat.utils import bench

@bench.timethis
def foo(x):
    time.sleep(.001)
    return x


class TestBenchmarking(object):
    def test_bench_as_decorator_returns_a_tuple_on_single_assignment(self):
        _ = foo(x=10)
        assert type(_) is tuple

    def test_bench_as_decorator_timethis_prints_timing_info_to_stdout(self, capsys):
        """ capsys variable is a pytest function to capture system error and output
        """
        _, __ = foo(x=10)
        captured_stdouterr = capsys.readouterr()
        timefoo_stdout_regex = re.compile(r"@timecall: foo took (\d+\.\d+) seconds")
        assert timefoo_stdout_regex.match(captured_stdouterr.out) is not None

    def test_bench_as_decorator_timethis_can_return_the_metrics_as_dict(self):
        _, timing = foo(x=10) # this will throw warning in pylint but not an issue
        assert type(timing) is dict

    @pytest.mark.parametrize("prop,prop_type", [
        ("duration", float),
        ("func_name", str),
    ], scope="class")
    def test_bench_as_decorator_timethis_dict_has_properties(self, prop, prop_type):
        _, timing = foo(x=10) # this will throw warning in pylint for each paramaterized test
        assert type(timing[prop]) is prop_type