"""Manage a resultset that rformatter will understand"""

class resultSet(object):
    def __init__(self, results):
        self.results = results

    def dump(self):
        print("self.results: %s" % self.results)


if __name__ == "__main__":
    r = resultSet([1, 2, 3])
    r.dump()

    