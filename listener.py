import redis
import threading
from time import sleep
from random import randint

from util import *

def _get_restaurant_channels():
    r_channels = []
    for resto in get_resto():
        r_channels.append(resto['rid'])
    return r_channels

class Listener(threading.Thread):
    def __init__(self, r, channels):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)
    
    def work(self, item):
        #print item['channel'], ":", item['data']
        channel = item['channel']
        cnt = item['data']
        user_channels = r.hgetall("users_%s" % (channel))
        for user_channel, count in user_channels.items():
            d = [ {'id': channel, 'cnt': cnt}]
            r.publish(user_channel, d)
    
    def run(self):
        for item in self.pubsub.listen():
            if item['data'] == "KILL":
                self.pubsub.unsubscribe()
                print self, "unsubscribed and finished"
                break
            else:
                self.work(item)

if __name__ == "__main__":
    r = redis.Redis()
    #client = Listener(r, ['test','test1'])
    client = Listener(r, _get_restaurant_channels())
    client.start()

    cnt = 1 
    num_resto = len(_get_restaurant_channels())
    for i in range(1000):
        #resto_channel = randint(1, num_resto)
        #r.publish(resto_channel, str(cnt))
        sleep(3)
   
    for channels in _get_restaurant_channels():
        r.publish(channels, 'KILL')
