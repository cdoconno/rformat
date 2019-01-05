import pytest
import sys
import collections

from rformat import resultset 

class TestRow(object):
    @pytest.mark.parametrize("it,it_type,it_headers,order_map,eqcheck", [
        ([[1,2,3]], list, ['a', 'b', 'c'], None, [1, 2, 3]), # test list
        ([(1,2,3)], tuple, ['a', 'b', 'c'], None, [1, 2, 3]), # test tuple
        ([{'a': 1, 'b': 2, 'c': 3}], dict, None, {0:'a', 1:'b', 2:'c'}, [1, 2, 3]), # test dict
        ([{'a': 1, 'c': 3, 'b': 2}], dict, None, {0:'a', 1:'b', 2:'c'}, [1, 2, 3]), # test ordering of row data doesnt matter
        ([{'a': 1, 'c': 3, 'b': 2, 'd': 4}], dict, None, {0:'a', 1:'b', 2:'c'}, [1, 2, 3]), # test extra fields in row data are filtered out
        ([{'a': 1, 'b': 2}], dict, None, {0:'a', 1:'b', 2:'c'},[1, 2, None]), # test extra fields in row data are defaulted to None
        ([[1,2,3],[4,5,6]], list, ['a', 'b', 'c'], None, [1, 2, 3]),  # test two rows
    ], scope="class")
    def test_row_creation_succeeds(self, it, it_type, it_headers, order_map, eqcheck):
        rs = resultset.ResultSet(it, it_headers, order_map)
        r = resultset.Row(it[0], rs.rowdef)
        assert list(r.data) == eqcheck # test data correct 
        assert r.data.a == 1 # test we can access data fields with dot notation
        #assert r.data.get('a', None) == 1 # test we can access data fields with get notation
        assert r.rowdef is rs.rowdef # test standalone row rowdef is reference to result set rowdef
        assert r.rowdef == rs.rowdef # test standalone row rowdef is reference to result set rowdef

    @pytest.mark.parametrize("values", [
        [100],
        [100.1],
        ["foo"],
    ], scope="class")
    def test_normalize_row_raises_type_error_for_incorrect_types(self, values):
        rs = resultset.ResultSet(values, ['a', 'b', 'c'])
        with pytest.raises(TypeError):
            resultset.Row._normalize_row(values[0], rs.rowdef)

    @pytest.mark.parametrize("value,headers,order_map", [
       ([[1, 2, 3]], ['a', 'b', 'c'], None), # list
       ([(1, 2, 3)], ['a', 'b', 'c'], None), # tuple
       ([{'a': 1, 'b': 2, 'c': 3}], ['a', 'b', 'c'] , {0:'a', 1:'b', 2:'c'}), # test dict
    ], scope="class")
    def test_normalize_row_returns_named_tuple(self, value, headers, order_map):
        rs = resultset.ResultSet(value, headers, order_map)
        r = resultset.Row._normalize_row(value[0], rs.rowdef)
        print r.a
        assert r.a == 1
        assert r.b == 2
        assert r.c == 3


class TestResultSet(object):
    pass
