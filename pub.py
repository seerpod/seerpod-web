import random, string
import tornado.ioloop
import tornadoredis

from util import *

cnt = 1

def sample_data():
    global cnt
    data = []
    num_resto = len(get_resto())
    i = random.randint(1, num_resto)
    cnt = cnt + 1
    data.append({
                 'id': i, 
                 'cnt' : cnt
                })
    return data

def callback():
    data = sample_data()
    print data
    c.publish('user', data)
 
#milliseconds
interval_ms = 2 * 1000
main_loop = tornado.ioloop.IOLoop.instance()
scheduler = tornado.ioloop.PeriodicCallback(callback,interval_ms, io_loop = main_loop)
#start your period timer
scheduler.start()
#start your loop
main_loop.start()
