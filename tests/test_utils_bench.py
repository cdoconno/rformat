import pytest
import sys
import time
import re

from rformat.utils import bench

class TestBenchmarking(object):
    def test_bench_decorator_timethis_prints_timing(self, capsys):
        @bench.timethis
        def foo():
            time.sleep(.001)
        foo()
        captured_stdouterr = capsys.readouterr()
        timefoo_stdout_regex = re.compile(r"@timecall: foo took (\d+\.\d+) seconds")
        assert timefoo_stdout_regex.match(captured_stdouterr.out) is not None
