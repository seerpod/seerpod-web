#!/usr/bin/env python
# set this export DYLD_LIBRARY_PATH=/usr/local/mysql/lib/
__author__ = 'tarunkumar'

import os.path
import datetime
import torndb
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.gen
from tornado import gen
import error_codes
from tornado.options import define, options
import httplib
import base
import business_contact_api
import count_encoder
import business_api
import authenticator


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    @property
    def biz_api(self):
        return business_api.BusinessApi(self.db)

    @property
    def biz_contact_api(self):
        return business_contact_api.BusinessContacts(self.db)

    @property
    def redis_db(self):
        return self.application.redis_db

    def write_error(self, status_code, **kwargs):
        data = {}
        data['error_code'] = status_code
        data['message'] = kwargs.get('reason')
        self.write(data)


class AuthLoginHandler(BaseHandler):

    @gen.coroutine
    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')

        if not password or not email:
            self.write_error(status_code=error_codes.INVALID_ARGUMENTS,
                             reason='Invalid request, password or email not passed')
            self.set_status(400)
            return

        user = self.biz_contact_api.get_user_detail_from_email(email)

        if not user:
            self.write_error(status_code=error_codes.INVALID_EMAIL,
                             reason='Invalid email, %s not found' % email)
            self.set_status(400)
            return

        if password == user.password:
            authentication_code = authenticator.generate_authentication_code(user)
            data = {'authentication_code': authentication_code}
            self.write(data)
        else:
            self.set_status(400)
            self.write_error(status_code=error_codes.INVALID_PASSWORD,
                             reason='Invalid Password for email %s' % email)


class SignupHandler(BaseHandler):

    @gen.coroutine
    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')

        if not password or not email:
            self.write_error(status_code=error_codes.INVALID_ARGUMENTS,
                             reason='Invalid request, password or email not passed')
            self.set_status(400)
            return

        user = self.biz_contact_api.get_user_detail_from_email(email)

        if user:
            self.write_error(status_code=error_codes.EMAIL_ALREADY_EXIST,
                             reason='Email %s already exists' % email)
            self.set_status(400)
            return

        user = self.biz_contact_api.create_business_account(email, password,  self.get_argument('email'),
                                                    self.get_argument('first_name'), self.get_argument('last_name'))

        self.write({'authentication_code': authenticator.generate_authentication_code(user)})


class HomeHandler(BaseHandler):

    def get(self):
        self.render("home.html")

    def get_yelp_data(self, id):
        # TODO(we need to use actual api, to get these reviews, we cannot store it our db),
        #  returning just random numbers for now

        return 100+(13+id % 2) * id, 3+id % 2

    def post(self):
        address = self.get_argument('user-address', None)
        no_template = self.get_argument('render-template', None)
        if not address:
            self.set_status(400)
            self.write_error(status_code=error_codes.INVALID_ARGUMENTS ,
                             reason='Please pass address')
            return

        if address:
            # TODO(TARUN) - Get nearest businesses based on location(currently I am not using location field)
            businesses = self.biz_api.get_businesses_near_address(address)

            for b in businesses:
                 # Decorate restaurants with yelp reviews and availability
                review_count, rating = self.get_yelp_data(b.id)
                b.review_count = review_count
                b['created_on'] = None
                b.rating = rating
                b.occupancy = self.biz_api.get_business_vacancy(b.id, b.capacity)
                b.street_address = '%s %s, %s %s' % (b.street_number, b.street_name, b.city, b.state)
                self.redis_db.hset('users_%d' % b['id'], 'user', 1)
            if no_template:
                self.write({'businesses': businesses})
            else:
                self.render("search.html", address=address, businesses=businesses)


class BusinessDetailHandler(BaseHandler):

    def get(self):
        biz_id = self.get_argument("id", None)
        detail = self.biz_api.get_business_detail(biz_id)

        if not detail:
            self.write_error(status_code=error_codes.INVAID_BUSINESS_ID,
                             reason='Business id %s does not exists' % biz_id)
            return

        detail.pop('created_on', None)
        self.write({'data': detail})


class CountHandler(BaseHandler):

    def post(self):
        params = self.get_argument('c')

        if params:
            encoded_restaurant_count = params[0]
            biz_id, time_stamp, count = count_encoder.get_count_from_encoded_count_request(
                encoded_restaurant_count)

            ts = datetime.datetime.fromtimestamp(float(time_stamp))
            command = "INSERT INTO business_counter (biz_id, time_stamp, count) VALUES (%s, '%s', %s)" % (
                biz_id, ts, count)
            self.db.execute(command)

    def get(self):
        biz_id = self.get_argument('id')

        if not biz_id:
            self.write_error(status_code=error_codes.INVALID_ARGUMENTS,
                             reason='Business id not passed')
            return
        count = self.biz_api.get_business_count(biz_id)

        if count:
            self.write({'count': count})
        else:
            self.write_error(status_code=error_codes.INVAID_BUSINESS_ID,
                             reason='Invalid business id %s' % biz_id)


class CountNextHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super(CountNextHandler, self).__init__(*args, **kwargs)
        self.listen()

    @tornado.gen.engine
    def listen(self):
        #self.client = tornadoredis.Client()
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


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(base.Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
