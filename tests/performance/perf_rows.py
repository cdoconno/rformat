import sys
import resource 

from rformat import resultset 
from rformat.utils import bench

# TEST DATA GENERATED WITH https://www.json-generator.com
# Copy this into 1k, 10k, 100k, 1M, 10M rows - not unue
BASE_ROWS = [
 {"_id":"5c5523a7c21ba304d62c15fd","index":1,"guid":"f5402b2e-6dcd-44dc-a4cf-6fbce63ab9e5","isActive":False,"balance":"$2,170.84","picture":"http://placehold.it/32x32","age":40,"eyeColor":"brown","name":"Cantrell Rose","gender":"male","company":"UNIWORLD","email":"cantrellrose@uniworld.com","phone":"+1 (929) 572-2875","address":"997 Will Place, Gibbsville, South Carolina, 6970","about":"Consequat laboris commodo sint laboris non occaecat officia qui quis ullamco non. Ut in officia aliquip aliqua proident Lorem tempor sit. Cupidatat quis veniam esse fugiat. Aute aute id quis et commodo culpa. Nulla culpa do magna culpa. Dolor ullamco ea culpa laborum ullamco eiusmod velit veniam culpa veniam proident duis qui. Consectetur veniam esse qui aliqua reprehenderit anim exercitation incididunt.\r\n","registered":"2017-06-23T06:03:16 +05:00","latitude":61.890363,"longitude":-87.979366},
 {"_id":"5c5523a7ab635ed5dc44aadc","index":2,"guid":"f4241cb6-46ce-451f-9fd4-6217d5716c95","isActive":False,"balance":"$3,646.43","picture":"http://placehold.it/32x32","age":36,"eyeColor":"green","name":"Jane Terry","gender":"female","company":"ENERVATE","email":"janeterry@enervate.com","phone":"+1 (875) 496-2707","address":"537 Thornton Street, Marbury, Alaska, 3733","about":"Lorem ea ad do commodo anim tempor mollit ut do officia cillum consectetur aute. Labore aute sit amet nisi ex. Est dolor ad commodo excepteur aliquip eu labore amet laboris elit amet in sit in. Dolore tempor consequat minim irure et sunt ullamco. Adipisicing fugiat excepteur aliquip officia voluptate. Ea reprehenderit amet irure nisi aliqua adipisicing dolore amet sint laborum mollit ut esse.\r\n","registered":"2014-06-14T02:17:41 +05:00","latitude":-67.722381,"longitude":-93.697106},
 {"_id":"5c5523a7e7497fe6c61a1ef0","index":3,"guid":"c8209769-d46e-4598-9538-db7f21d8f21a","isActive":False,"balance":"$3,310.42","picture":"http://placehold.it/32x32","age":30,"eyeColor":"blue","name":"Merritt Ellis","gender":"male","company":"EMPIRICA","email":"merrittellis@empirica.com","phone":"+1 (960) 452-2226","address":"248 Commercial Street, Nash, Colorado, 457","about":"Nisi voluptate velit id commodo sint nostrud commodo exercitation aute reprehenderit. Cupidatat Lorem consequat aliquip adipisicing et reprehenderit nostrud. Eu exercitation tempor ut ut ea id magna ipsum. Est quis esse fugiat laborum cupidatat. Quis laborum excepteur consectetur cillum ullamco cupidatat laborum eiusmod consectetur sit amet laborum.\r\n","registered":"2014-03-24T09:20:57 +05:00","latitude":-9.130929,"longitude":140.156949},
 {"_id":"5c5523a7c1e978def3cdb9a2","index":4,"guid":"1d1618bf-6b8d-4f51-b174-5aba8e7bcb8d","isActive":False,"balance":"$2,787.63","picture":"http://placehold.it/32x32","age":20,"eyeColor":"blue","name":"Kinney Peck","gender":"male","company":"SENSATE","email":"kinneypeck@sensate.com","phone":"+1 (951) 480-3145","address":"649 Sunnyside Avenue, Fairmount, Louisiana, 1036","about":"Voluptate veniam dolor aliquip eiusmod reprehenderit. Ad sint et excepteur voluptate quis non occaecat. Sint non dolor tempor ea ad enim consequat sunt culpa. Cillum voluptate mollit aute minim in ut culpa nulla. Fugiat aliquip duis irure reprehenderit magna nisi dolor velit nostrud anim labore enim duis reprehenderit. Ullamco mollit veniam sint ut nostrud voluptate magna. Elit anim ad proident adipisicing dolore nostrud consectetur.\r\n","registered":"2019-01-23T04:19:04 +06:00","latitude":13.321486,"longitude":11.100136},
 {"_id":"5c5523a7b996bc995ce2c765","index":5,"guid":"be04a898-e366-4b16-820f-d32fbefdca7c","isActive":False,"balance":"$2,489.57","picture":"http://placehold.it/32x32","age":38,"eyeColor":"green","name":"Sharon York","gender":"female","company":"OPTICALL","email":"sharonyork@opticall.com","phone":"+1 (836) 572-2154","address":"127 Hemlock Street, Fairview, Kentucky, 6105","about":"Laborum consectetur velit ut consectetur elit nulla nulla cillum exercitation id. Voluptate ea sit culpa id magna sint sit ut irure deserunt. Do do Lorem consequat eiusmod. Deserunt et irure sint do est irure sunt amet ea magna tempor exercitation consectetur. Consectetur excepteur duis ea aliqua ut irure culpa irure consectetur non enim.\r\n","registered":"2017-07-24T08:06:46 +05:00","latitude":-53.887751,"longitude":-117.745987},
 {"_id":"5c5523a7c21ba304d62c15fd","index":1,"guid":"f5402b2e-6dcd-44dc-a4cf-6fbce63ab9e5","isActive":False,"balance":"$2,170.84","picture":"http://placehold.it/32x32","age":40,"eyeColor":"brown","name":"Cantrell Rose","gender":"male","company":"UNIWORLD","email":"cantrellrose@uniworld.com","phone":"+1 (929) 572-2875","address":"997 Will Place, Gibbsville, South Carolina, 6970","about":"Consequat laboris commodo sint laboris non occaecat officia qui quis ullamco non. Ut in officia aliquip aliqua proident Lorem tempor sit. Cupidatat quis veniam esse fugiat. Aute aute id quis et commodo culpa. Nulla culpa do magna culpa. Dolor ullamco ea culpa laborum ullamco eiusmod velit veniam culpa veniam proident duis qui. Consectetur veniam esse qui aliqua reprehenderit anim exercitation incididunt.\r\n","registered":"2017-06-23T06:03:16 +05:00","latitude":61.890363,"longitude":-87.979366},
 {"_id":"5c5523a7ab635ed5dc44aadc","index":2,"guid":"f4241cb6-46ce-451f-9fd4-6217d5716c95","isActive":False,"balance":"$3,646.43","picture":"http://placehold.it/32x32","age":36,"eyeColor":"green","name":"Jane Terry","gender":"female","company":"ENERVATE","email":"janeterry@enervate.com","phone":"+1 (875) 496-2707","address":"537 Thornton Street, Marbury, Alaska, 3733","about":"Lorem ea ad do commodo anim tempor mollit ut do officia cillum consectetur aute. Labore aute sit amet nisi ex. Est dolor ad commodo excepteur aliquip eu labore amet laboris elit amet in sit in. Dolore tempor consequat minim irure et sunt ullamco. Adipisicing fugiat excepteur aliquip officia voluptate. Ea reprehenderit amet irure nisi aliqua adipisicing dolore amet sint laborum mollit ut esse.","registered":"2014-06-14T02:17:41 +05:00","latitude":-67.722381,"longitude":-93.697106},
 {"_id":"5c5523a7e7497fe6c61a1ef0","index":3,"guid":"c8209769-d46e-4598-9538-db7f21d8f21a","isActive":False,"balance":"$3,310.42","picture":"http://placehold.it/32x32","age":30,"eyeColor":"blue","name":"Merritt Ellis","gender":"male","company":"EMPIRICA","email":"merrittellis@empirica.com","phone":"+1 (960) 452-2226","address":"248 Commercial Street, Nash, Colorado, 457","about":"Nisi voluptate velit id commodo sint nostrud commodo exercitation aute reprehenderit. Cupidatat Lorem consequat aliquip adipisicing et reprehenderit nostrud. Eu exercitation tempor ut ut ea id magna ipsum. Est quis esse fugiat laborum cupidatat. Quis laborum excepteur consectetur cillum ullamco cupidatat laborum eiusmod consectetur sit amet laborum.\r\n","registered":"2014-03-24T09:20:57 +05:00","latitude":-9.130929,"longitude":140.156949},
 {"_id":"5c5523a7c1e978def3cdb9a2","index":4,"guid":"1d1618bf-6b8d-4f51-b174-5aba8e7bcb8d","isActive":False,"balance":"$2,787.63","picture":"http://placehold.it/32x32","age":20,"eyeColor":"blue","name":"Kinney Peck","gender":"male","company":"SENSATE","email":"kinneypeck@sensate.com","phone":"+1 (951) 480-3145","address":"649 Sunnyside Avenue, Fairmount, Louisiana, 1036","about":"Voluptate veniam dolor aliquip eiusmod reprehenderit. Ad sint et excepteur voluptate quis non occaecat. Sint non dolor tempor ea ad enim consequat sunt culpa. Cillum voluptate mollit aute minim in ut culpa nulla. Fugiat aliquip duis irure reprehenderit magna nisi dolor velit nostrud anim labore enim duis reprehenderit. Ullamco mollit veniam sint ut nostrud voluptate magna. Elit anim ad proident adipisicing dolore nostrud consectetur","registered":"2019-01-23T04:19:04 +06:00","latitude":13.321486,"longitude":11.100136},
 {"_id":"5c5523a7b996bc995ce2c765","index":5,"guid":"be04a898-e366-4b16-820f-d32fbefdca7c","isActive":False,"balance":"$2,489.57","picture":"http://placehold.it/32x32","age":38,"eyeColor":"green","name":"Sharon York","gender":"female","company":"OPTICALL","email":"sharonyork@opticall.com","phone":"+1 (836) 572-2154","address":"127 Hemlock Street, Fairview, Kentucky, 6105","about":"Laborum consectetur velit ut consectetur elit nulla nulla cillum exercitation id. Voluptate ea sit culpa id magna sint sit ut irure deserunt. Do do Lorem consequat eiusmod. Deserunt et irure sint do est irure sunt amet ea magna tempor exercitation consectetur. Consectetur excepteur duis ea aliqua ut irure culpa irure consectetur non enim.\r\n","registered":"2017-07-24T08:06:46 +05:00","latitude":-53.887751,"longitude":-117.745987}
]
KEYS = BASE_ROWS[0].keys()
ORDER_MAP = {}
for i, v in enumerate(KEYS):
    ORDER_MAP.setdefault(i, v)

one_k = BASE_ROWS * (10**3 / 10)
ten_k = BASE_ROWS * (10**4 / 10)
hun_k = BASE_ROWS * (10**5 / 10)
one_m = BASE_ROWS * (10**6 / 10)
ten_m = BASE_ROWS * (10**7 / 10)


@bench.timethis
def gen_1k():
    rs = resultset.ResultSet([one_k], None, ORDER_MAP)

@bench.timethis
def gen_10k():
    rs = resultset.ResultSet([ten_k], None, ORDER_MAP)

@bench.timethis
def gen_100k():
    rs = resultset.ResultSet([hun_k], None, ORDER_MAP)

@bench.timethis
def gen_1m():
    rs = resultset.ResultSet([one_m], None, ORDER_MAP)

@bench.timethis
def gen_10m():
    rs = resultset.ResultSet([ten_m], None, ORDER_MAP)


if __name__=='__main__':
    gen_1k()
    gen_10k()
    gen_100k()
    gen_1m()
    gen_10m()
    print("done")

