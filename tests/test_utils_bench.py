import pytest
import sys
import time
import re
import uuid

from rformat.utils import bench

@bench.timethis_returnstats
def foo(x):
    time.sleep(.001)
    return x

@bench.timethis()
def foo2(x):
    time.sleep(.001)
    return x

@bench.timethis(verbose=False)
def foo3(x):
    time.sleep(.001)
    return x


class TestBenchmarking(object):
    def test_bench_as_decorator_returnstats_returns_a_tuple_on_single_assignment(self):
        _ = foo(x=10)
        assert type(_) is tuple

    def test_bench_as_decorator_timethis_returnstatus_prints_timing_info_to_stdout(self, capsys):
        """ capsys variable is a pytest function to capture system error and output
        """
        _, __ = foo(x=10)
        captured_stdouterr = capsys.readouterr()
        timefoo_stdout_regex = re.compile(r"@timecall: foo took (\d+\.\d+) seconds")
        assert timefoo_stdout_regex.match(captured_stdouterr.out) is not None

    def test_bench_as_decorator_timethis_returnstats_can_return_the_metrics_as_dict(self):
        _, timing = foo(x=10) # this will throw warning in pylint but not an issue
        assert type(timing) is dict

    @pytest.mark.parametrize("prop,prop_type", [
        ("duration", float),
        ("func_name", str),
    ], scope="class")
    def test_bench_as_decorator_timethis_returnstats_dict_has_properties(self, prop, prop_type):
        _, timing = foo(x=10) # this will throw warning in pylint for each paramaterized test
        assert type(timing[prop]) is prop_type


    def test_bench_as_decorator_timethis_does_not_return_a_tuple_on_single_assignment(self):
        _ = foo2(x=10)
        assert type(_) is not tuple

    def test_bench_as_decorator_timethis_prints_timing_info_to_stdout(self, capsys):
        """ capsys variable is a pytest function to capture system error and output
        """
        _ = foo2(x=10)
        captured_stdouterr = capsys.readouterr()
        timefoo_stdout_regex = re.compile(r"@timecall: foo2 took (\d+\.\d+) seconds")
        assert timefoo_stdout_regex.match(captured_stdouterr.out) is not None

    def test_bench_as_decorator_timethis_does_not_print_timing_info_to_stdout_when_verbose_false(self, capsys):
        """ capsys variable is a pytest function to capture system error and output
        """
        _ = foo3(x=10)
        captured_stdouterr = capsys.readouterr()
        timefoo_stdout_regex = re.compile(r"@timecall: foo3 took (\d+\.\d+) seconds")
        assert timefoo_stdout_regex.match(captured_stdouterr.out) is None

    def test_bench_as_decorator_timethis_does_print_timing_info_to_stdout_when_verbose_true(self, capsys):
        """ capsys variable is a pytest function to capture system error and output
        """
        @bench.timethis(verbose=True)
        def foo4(x):
            time.sleep(.001)
            return x
        _ = foo4(x=10)
        captured_stdouterr = capsys.readouterr()
        timefoo_stdout_regex = re.compile(r"@timecall: foo4 took (\d+\.\d+) seconds")
        assert timefoo_stdout_regex.match(captured_stdouterr.out) is not None

    def test_bench_as_decorator_timethis_does_print_timing_info_to_stdout_in_non_default(self, capsys):
        """ capsys variable is a pytest function to capture system error and output
        """
        @bench.timethis(timing_fmt="Took {1} seconds", verbose=True)
        def foo4(x):
            time.sleep(.001)
            return x
        _ = foo4(x=10)
        captured_stdouterr = capsys.readouterr()
        timefoo_stdout_regex = re.compile(r"Took (\d+\.\d+) seconds")
        assert timefoo_stdout_regex.match(captured_stdouterr.out) is not None


class TestBenchmarkMemory(object):

    def test_bench_as_decorator_trackmem_does_print_timing_info_to_stdout_in_non_default(self, capsys):
        """ capsys variable is a pytest function to capture system error and output
        """
        @bench.trackmem(verbose=True)
        def foo_mem(numrows):
            rows = []
            for _ in xrange(numrows):
                rows.append({'a': str(uuid.uuid4()), 'b': str(uuid.uuid4()), 'c': str(uuid.uuid4())})
            return rows
        _ = foo_mem(10**3)
        captured_stdouterr = capsys.readouterr()
        trackmemfoo_stdout_regex = re.compile(r"@trackmem: foo_mem start: (\d+\.\d+) end: (\d+\.\d+) used: (\d+\.\d+) (B|KB|MB|GB)")
        assert trackmemfoo_stdout_regex.match(captured_stdouterr.out) is not None


@pytest.mark.parametrize("size_value", [
    0,
    0.1
])
def test_size_raises_type_error_when_passed_non_iterable_value(size_value):
    with pytest.raises(TypeError):
      _ = bench.size(size_value, "GB")

@pytest.mark.parametrize("size_value1", [
    "1",      # single string is iterable, so will try and be converted and raise typeerror
    ["2048", "4096"],
    [2048, "4096"],
])
def test_size_raises_type_error_when_passed_interable_nonconverteable_objects(size_value1):
    with pytest.raises(TypeError):
      _ = bench.size(size_value1, "GB")


def test_size_raises_value_error_when_not_provided_valid_unit():
    with pytest.raises(ValueError):
      _ = bench.size([2048], "k")


@pytest.mark.parametrize("values,unit,converted", [
    ([2048, 4096], "B", [2048, 4096]),
    ([2048, 4096], "b", [2048, 4096]),
    ([2048, 4096], "Kb", [2, 4]),     # test case on unit mixed
    ([2048, 4096], "KB", [2, 4]),     # test case on unit caps
    ([2048, 4096], "kb", [2, 4]),     # test case on unit lower
    ([1048576], "MB", [1]),           
    ([-10485760], "mb", [-10]),       # test negative returns negative
    ([524288], "Mb", [0.5]),          # test fractional
    ([107374182400], "GB", [100]),    # test large (for memory)
])
def test_conversions_are_accurate(values, unit, converted):
    cv = bench.size(values, unit)
    assert cv == converted



