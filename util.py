import simplejson
import tornadoredis
import random, string

c = tornadoredis.Client()
c.connect()

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

def sample_data():
    data = []
    for  i in range(5):
        dic = {}
        dic["id"] = i
        dic["name"] = randomword(10)
        dic['cnt'] = 1
        data.append(dic)
    json = simplejson.dumps(data)
    return json
 
