import pytest
import sys
import collections
import types

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

    @pytest.mark.parametrize("values", [
        [100],
        [100.1],
        ["foo"],
    ], scope="class")
    def test_normalize_row_raises_type_error_for_incorrect_value_types(self, values):
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
    @pytest.mark.parametrize("value1,headers1,order_map1", [
       ([[1, 2, 3]], ['a', 'b', 'c'], None), # list
    ], scope="class")
    def test_can_create_result_set(self, value1, headers1, order_map1):
        rs = resultset.ResultSet(value1, headers1, order_map1)
        assert isinstance(rs, resultset.ResultSet)

    def test_result_set_generate_rows_is_a_generator_after_init(self):
        rs = resultset.ResultSet([[1, 2, 3]], ['a', 'b', 'c'], None)
        assert type(rs.generate_rows) is types.GeneratorType

    @pytest.mark.parametrize("gen,genheaders,order_map_gen", [
       ((row for row in [[1, 2, 3]]), ['a', 'b', 'c'], None), # list
       ((row for row in [(1, 2, 3)]), ['a', 'b', 'c'], None), # tuple
       ((row for row in [{'a': 1, 'b': 2, 'c': 3}]), ['a', 'b', 'c'] , {0:'a', 1:'b', 2:'c'}), # test dict
    ], scope="class")
    def test_result_set_can_take_a_generator_on_initialization(self, gen, genheaders, order_map_gen):
        assert type(gen) is types.GeneratorType
        rs = resultset.ResultSet(gen, genheaders, order_map_gen)
        assert type(rs.generate_rows) is types.GeneratorType

    @pytest.mark.parametrize("value2,headers2,order_map2", [
       ([[1, 2, 3]], ['a', 'b', 'c'], None), # list
       ((row for row in [[1, 2, 3]]), ['a', 'b', 'c'], None), # list
    ], scope="class")
    def test_result_set_add_row_sets_rowcount_on_intilization(self, value2, headers2, order_map2):
        rs = resultset.ResultSet(value2, headers2, order_map2)
        assert rs.row_count == 1

    @pytest.mark.parametrize("value3,headers3,order_map3", [
       ([[1, 2, 3], [4, 5, 6]], ['a', 'b', 'c'], None), # list
    ], scope="class")
    def test_result_set_add_row_sets_rowcount_on_intilization_w_mutlirow_set(self, value3, headers3, order_map3):
        rs = resultset.ResultSet(value3, headers3, order_map3)
        assert rs.row_count == 2

    @pytest.mark.parametrize("value4,headers4,order_map4", [
       ([[1, 2, 3], [4, 5, 6]], ['a', 'b', 'c'], None), # list
    ], scope="class")
    def test_result_set_add_row_works_and_increments_rowcount(self, value4, headers4, order_map4):
        rs = resultset.ResultSet(value4, headers4, order_map4)
        assert rs.row_count == 2
        #r = resultset.Row([6, 7, 8], rs.rowdef)
        rs.addrow([6, 7, 8])
        assert rs.row_count == 3
        assert list(rs.rows[2].data) == [6, 7, 8] # also tests that list() preserves ordering of tuple by prop name

    @pytest.mark.parametrize("value5,headers5,order_map5", [
       ([[1, 2]], ['a', 'b', 'c'], None), # list
    ], scope="class")
    def test_result_set_add_row_onfail_tracks_errors_and_increments_errorcount(self, value5, headers5, order_map5):
        rs = resultset.ResultSet(value5, headers5, order_map5)
        assert rs.row_count == 0
        assert rs.error_count == 1
        rs.addrow([6, 7, 8])
        rs.addrow([9, 10])
        assert rs.row_count == 1
        assert rs.error_count == 2
        assert list(rs.rows[0].data) == [6, 7, 8]
        assert type(rs.errors) is list
        assert rs.errors == [[1,2],[9,10]]


    @pytest.mark.parametrize("test_order_map,ordered_map_keys", [
        ({'0': {}, '1': {}}, [0.0, 1.0]),   # str keys proper order
        ({'1': {}, '0': {}}, [0.0, 1.0]),   # str keys out of order
        ({'1': {}, '0.0': {}}, [0.0, 1.0]), # str keys w decimals out of order
        ({1: {}, '0.0': {}}, [0.0, 1.0]),   # mixed keys w decimals out of order
        ({1: {}, 0: {}}, [0.0, 1.0]),       # int keys out of order
        ({1: {}, 0.0: {}}, [0.0, 1.0]),     # int and float keys out of order
        ({-1: {}, 0.0: {}}, [-1.0, 0.0]),   # int and float with negatives being first
        ({-1.0: {}, -1.5: {}}, [-1.5, -1.0]), # negatives floats larger negative first
        ({'1':{}, '11':{}, '2':{}, '20':{}}, [1.0, 2.0, 11.0, 20.0]), # str keys to ensure 11 not ordered before 2 like strings
        ({"-1": {}, "0.0": {}}, [-1.0, 0.0]), # strings with negatives being first
        ({-1e-5: {}, 0.0: {}, 1e-5: {}, "1e5":{}}, [-0.00001, 0.0, 0.00001, 100000.0]), # scientific notitation and float mix with negative sci notation
    ], scope="class")
    def test_result_sort_order_map_sorts_dict_by_int_keys(self, test_order_map, ordered_map_keys):
        assert type(resultset.ResultSet._sort_order_map) is types.FunctionType # function exists
        assert resultset.ResultSet._sort_order_map(test_order_map).keys() == ordered_map_keys


        





class TestResults(object):
    @pytest.mark.parametrize("value1,headers1,order_map1", [
       ([[1, 2, 3]], ['a', 'b', 'c'], None), # list
    ], scope="class")
    def test_can_create_result_set(self, value1, headers1, order_map1):
        rs = resultset.ResultSet(value1, headers1, order_map1)
        results = resultset.Results([rs])
        assert isinstance(results, resultset.Results)

    @pytest.mark.parametrize("rs,config", [
        (resultset.ResultSet([[1, 2, 3]], ['a', 'b', 'c'], None), -1),
        (resultset.ResultSet([[1, 2, 3]], ['a', 'b', 'c'], None), []),
        (resultset.ResultSet([[1, 2, 3]], ['a', 'b', 'c'], None), "failstring"),
    ], scope="class")
    def test_manage_config_raises_type_error_when_opts_not_dict(self, rs, config):
        with pytest.raises(TypeError):
            resultset.Results([rs], config)

    @pytest.mark.parametrize("rs1,config1", [
        (resultset.ResultSet([[1, 2, 3]], ['a', 'b', 'c'], None), {"test": True}),
    ], scope="class")
    def test_manage_config_sets_self_config(self, rs1, config1):
        result = resultset.Results([rs1], config1)
        assert result.config == {"test": True}






