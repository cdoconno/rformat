"""Manage a resultset that rformatter will understand"""

import logging
import sys
import collections

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)

class Results():
    """
    Collection of ResultSet objects that rformat functions rely on
    """
    def __init__(self):
        self.setCount = 0
        self.resultSets = []
        self.converter = None # TODO add plugin support to convert common result frameworks

class ResultSet(object):
    """
    Single set of results containing row objects
    """
    def __init__(self, results, headers=None, order_map=None):
        if order_map:
            self.order_map = self._sort_order_map(order_map)
        else:
            self.order_map = order_map
        self.headers, self.header_source = self._manageheaders(headers)
        self.rowdef = collections.namedtuple("RsRow", self.headers, verbose=False, rename=True)
        self.generate_rows = None
        self.rows = []
        self.errors = []
        self.row_count = 0
        self.error_count = 0
        self._initresults(results)
        self.initialize_rows()


    def initialize_rows(self):
        """
        Process rows from a generator object
        """
        for row in self.generate_rows:
            self.addrow(row)
        log.debug("rows: %s, rowcount: %s, errors: %s, errorcount: %s" % (self.rows, self.row_count, self.errors, self.error_count))

    def addrow(self, row):
        """
        Add a single row to resultset
        """
        try:
            self.rows.append(Row(row, self.rowdef))
            self.row_count += 1
        except:
            self.errors.append(row)
            self.error_count += 1

    def _initresults(self, results):
        """
        Determine what was type results were passed and handle accordingly.
        Supports list, generator, or iterator
        """
        try:
            self.generate_rows = (row for row in results) # generator 
        except TypeError:
            raise TypeError("ResultSet results must be iterable")

        
    def _manageheaders(self, headers):
        """
        Type checking for headers and order map provided to result set
        """
        if self.order_map != None and headers != None:
            # use headers if both are provided
            #raise TypeError("ResultSet() requires and order_map or headers, not both")
            if type(headers) != list:
                raise TypeError("ResultSet() requires headers as list when no order_map provided")
            else:
                return headers, "headers priority"
        if self.order_map == None:
            if headers == None:
                raise TypeError("ResultSet() requires headers or order_map (neither given)")
            elif type(headers) != list:
                raise TypeError("ResultSet() requires headers as list when no order_map provided")
            else:
                return headers, "headers"
        if headers == None:
            if type(self.order_map) != collections.OrderedDict:
                raise TypeError("ResultSet() requires order_map as dict with no headers. provided:  type(self.order_map)")
            else:
                return self.order_map.values(), "order_map"
    
    @staticmethod
    def _sort_order_map(order_map):
        """
        returns and ordered dict of keys based on an order_map dict with floats/ints as keys
        """
        print("order_map: %s" % order_map)
        if type(order_map) != dict:
            raise TypeError("must provide dict to define ordermapping as '{float: key_string}'. provided %s" % order_map)
        return collections.OrderedDict([(k, order_map[k]) for k in sorted(order_map.keys())])

            
    
class Row(object):
    """
    Row of data that can be initialized from tuple, list, dict
    """
    def __init__(self, values, rowdef=None):
        self.rowdef = rowdef
        self.data = self._normalize_row(values, rowdef)

    @staticmethod
    def _normalize_row(values, rowdef):
        """
        return a named tuple of values if provided bounded iterable dict, tuple, etc
        """
        tp = type(values)
        if tp == list:
            return rowdef._make(values)
        elif tp == tuple:
            return rowdef._make(values)
        elif tp == dict:
            # filtered is a new dict only the named fields of the rowdef
            filtered = { k: values.get(k, None) for k in rowdef._fields }
            return rowdef(**filtered)
        else:
            raise TypeError("must provide values as bounded iterable for new Row")



if __name__ == "__main__":
    log.info("testing logger in main")

