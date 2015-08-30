import redis
import torndb
import simplejson
import tornadoredis
import random, string

db = torndb.Connection(host = "localhost", database = "sp", user = "root", password = "root")
c = tornadoredis.Client()
c.connect()
r = redis.Redis()

ALL_RESTO = """
SELECT rid, name FROM resto
"""

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

def sample_data():
    data = []
    for  resto in get_resto():
        dic = {}
        dic["id"] = resto['rid']
        dic["name"] = resto['name']
        dic['cnt'] = str(1)
        data.append(dic)
    json = simplejson.dumps(data)
    return json
 
def get_resto():
    return db.query(ALL_RESTO)
    

