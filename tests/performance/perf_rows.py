import sys
import resource
import copy

from rformat import resultset
from rformat.utils import bench

# TEST DATA GENERATED WITH https://www.json-generator.com
# Copy this into 1k, 10k, 100k, 1M, 10M rows - not unue
BASE_ROW = {"_id":"5c5523a7c21ba304d62c15fd","index":1,"guid":"f5402b2e-6dcd-44dc-a4cf-6fbce63ab9e5","isActive":False,"balance":"$2,170.84","picture":"http://placehold.it/32x32","age":40,"eyeColor":"brown","name":"Cantrell Rose","gender":"male","company":"UNIWORLD","email":"cantrellrose@uniworld.com","phone":"+1 (929) 572-2875","address":"997 Will Place, Gibbsville, South Carolina, 6970","about":"Consequat laboris commodo sint laboris non occaecat officia qui quis ullamco non. Ut in officia aliquip aliqua proident Lorem tempor sit. Cupidatat quis veniam esse fugiat. Aute aute id quis et commodo culpa. Nulla culpa do magna culpa. Dolor ullamco ea culpa laborum ullamco eiusmod velit veniam culpa veniam proident duis qui. Consectetur veniam esse qui aliqua reprehenderit anim exercitation incididunt.\r\n","registered":"2017-06-23T06:03:16 +05:00","latitude":61.890363,"longitude":-87.979366} # noqa
KEYS = BASE_ROW.keys()
ORDER_MAP = {}
for i, v in enumerate(KEYS):
    ORDER_MAP.setdefault(i, v)


@bench.timethis()
@bench.trackmem()
def gen_1k():
    one_k = BASE_ROW * (10**3)
    rs = resultset.ResultSet([one_k], None, ORDER_MAP) # noqa


@bench.timethis()
@bench.trackmem()
def gen_10k():
    ten_k = BASE_ROW * (10**4)
    rs = resultset.ResultSet([ten_k], None, ORDER_MAP) # noqa


@bench.timethis()
@bench.trackmem()
def gen_100k():
    hun_k = BASE_ROW * (10**3)
    rs = resultset.ResultSet([hun_k], None, ORDER_MAP) # noqa


@bench.timethis()
@bench.trackmem()
def list_1m():
    one_m = [BASE_ROW] * (10**6)
    rsl = resultset.ResultSet(one_m, None, ORDER_MAP)
    print("1ml %s" % rsl)
    inspect_rs(rsl)


@bench.timethis()
@bench.trackmem()
def gen_1m():
    one_m = (copy.copy(BASE_ROW) for _ in xrange(10**6))
    rsg = resultset.ResultSet(one_m, None, ORDER_MAP)
    print("1mg %s" % rsg)
    inspect_rs(rsg)


@bench.timethis()
@bench.trackmem()
def list_10m():
    ten_m = [BASE_ROW] * (10**7)
    rs = resultset.ResultSet(ten_m, None, ORDER_MAP)
    print("1ml %s" % rs)
    inspect_rs(rs)


@bench.timethis()
@bench.trackmem()
def gen_10m():
    ten_m = (copy.copy(BASE_ROW) for _ in xrange(10**7))
    rs = resultset.ResultSet(ten_m, None, ORDER_MAP) # noqa


def inspect_rs(rs):
    print("rs rows length %s" % len(rs.rows))


if __name__ == '__main__':
    # only run one at at time
    #
    # gen_1k()
    # gen_10k()
    # gen_100k()
    # list_1m()
    gen_1m()
    # gen_10m()
    # list_10m()
    print("done")
