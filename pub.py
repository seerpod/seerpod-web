import random, string
import tornado.ioloop
import tornadoredis

from util import *

cnt = 1

def sample_data():
    global cnt
    data = []
    i = random.randint(1, 5)
    cnt = cnt + 1
    data.append({
                 'id': i, 
                 'name': randomword(20),
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
