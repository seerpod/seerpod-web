__author__ = 'tarunkumar'

import os.path

import torndb
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.gen
from tornado.options import define, options

import redis
import seerpod


#define("port", default=8888, help="run on the given port", type=int)
#define("mysql_host", default="localhost:3306", help="seerpod database host")
#define("mysql_database", default="seerpod", help="seerpod database name")
#define("mysql_user", default="seerpod", help="seerpod database user")
#define("mysql_password", default="Datadr1ven", help="seerpod database password")

define("port", default=8888, help="run on the given port", type=int)
define("mysql_host", default="dev.cisege0e6wes.us-west-2.rds.amazonaws.com:3306", help="seerpod database host")
define("mysql_database", default="seerpod", help="seerpod database name")
define("mysql_user", default="root", help="seerpod database user")
define("mysql_password", default="5eerp0d1nc", help="seerpod database password")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", seerpod.HomeHandler),
            (r"/next", seerpod.CountNextHandler),
            (r"/count", seerpod.CountHandler),
            (r"/login", seerpod.AuthLoginHandler),
            (r"/signup", seerpod.SignupHandler),
            (r"/detail", seerpod.BusinessDetailHandler),
            (r"/search", seerpod.SearchHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "../seerpod-web/templates"),
            static_path=os.path.join(os.path.dirname(__file__), "../seerpod-web/static"),
            xsrf_cookies=False,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)

        # Have one global connection to the blog DB across all handlers
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)
        self.redis_db = redis.Redis()