from __future__ import print_function
import tornado.web
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.gen
import simplejson
import pdb

from util import *

class UpdateHandler(tornado.web.RequestHandler):
    def get(self, resto, cnt):
        r.publish(resto, str(cnt))

class WebHandler(tornado.web.RequestHandler):
    def get(self):
        message = sample_data()
        for resto in get_resto():
            r.hset('users_%d' % resto['rid'], 'user', 1)
        self.render("web.html", message=message)

class WebNextHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super(WebNextHandler, self).__init__(*args, **kwargs)
        self.listen()

    @tornado.gen.engine
    def listen(self):
        self.client = tornadoredis.Client()
        self.client.connect()
        yield tornado.gen.Task(self.client.subscribe, 'user')
        self.client.listen(self.on_message)

    def on_message(self, msg):
        if msg.kind == 'message':
            self.write_message(str(msg.body))
        if msg.kind == 'disconnect':
            # Do not try to reconnect, just send a message back
            # to the client and close the client connection
            self.write_message('The connection terminated '
                               'due to a Redis server error.')
            self.close()

    def on_close(self):
        if self.client.subscribed:
            self.client.unsubscribe('user')
            self.client.disconnect()
