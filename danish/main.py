import os
import sys
import json
import logging
import tornado.web
import tornado.auth
import tornado.escape
import tornado.ioloop
import logging.config
import tornado.options
import tornado.httpserver
from tornado.options import define, options

from web import *

define("port", default=8001, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler): pass

DEBUG = True
DIRNAME = os.path.dirname(__file__)
STATIC_PATH = os.path.join(DIRNAME, 'static')
TEMPLATE_PATH = os.path.join(DIRNAME, 'template')

#log linked to the standard error stream
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)-8s - %(message)s',
                    datefmt='%d/%m/%Y %Hh%Mm%Ss')
console = logging.StreamHandler(sys.stderr)

#import base64
#import uuid
#base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
COOKIE_SECRET = 'L8LwECiNRxq2N0N2eGxx9MZlrpmuMEimlydNX/vt1LM='

settings = {
    "debug": True,
            "template_path": TEMPLATE_PATH,
            "static_path"  : STATIC_PATH,
            "debug"        : DEBUG,
            "cookie_secret": COOKIE_SECRET,
            "login_url"    : "/auth/login/"
}

server_settings = {
    "xheaders" : True,
}

def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
            (r"/web",                  WebHandler),
            (r"/update/(.*)/(.*)",     UpdateHandler),
            (r"/web-next",             WebNextHandler),
            
    ], **settings)

    application.listen(options.port, **server_settings)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
