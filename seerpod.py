#!/usr/bin/env python
# set this export DYLD_LIBRARY_PATH=/usr/local/mysql/lib/
__author__ = 'tarunkumar'

import os.path
import torndb
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import datetime
import count_encoder


from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("mysql_host", default="dev.cisege0e6wes.us-west-2.rds.amazonaws.com:3306", help="seerpod database host")
define("mysql_database", default="seerpod", help="seerpod database name")
define("mysql_user", default="root", help="seerpod database user")
define("mysql_password", default="5eerp0d1nc", help="seerpod database password")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/count", CountHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)

        # Have one global connection to the blog DB across all handlers
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)


class HomeHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.render("home.html")

    def get_yelp_data(self, id):
        # TODO(we need to use actual api, to get these reviews, we cannot store it our db),
        #  returning just random numbers for now

        return 100+(13+id % 2) * id, 3+id % 2

    def get_restaurant_vacancy(self, id, capacity):

        query = "SELECT count FROM restaurant_count where restaurant_id=%s ORDER BY time_stamp DESC LIMIT 1" % id
        restaurant_count = self.db.query(query)[0]

        occupancy_percent = restaurant_count.get('count', 0)*100.0/capacity

        return int(occupancy_percent)

    def post(self):
        address = self.get_argument("user-address", None)

        if address:
            # TODO(TARUN) - Get nearest restaurants based on location(currently I am not using location field)
            restaurants = self.db.query("SELECT * FROM restaurants")

            for r in restaurants:
                 # Decorate restaurants with yelp reviews and availability
                review_count, rating = self.get_yelp_data(r.id)
                r.review_count = review_count
                r.rating = rating
                r.occupancy = self.get_restaurant_vacancy(r.id, r.capacity)

            self.render("search.html", address=address, restaurants=restaurants)


class CountHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get(self):
        params = self.get_arguments('c')

        if params and params[0]:
            encoded_restaurant_count = params[0]
            rest_id, time_stamp, count = count_encoder.get_count_from_encoded_count_request(
                encoded_restaurant_count)

            ts = datetime.datetime.fromtimestamp(float(time_stamp))
            command = "INSERT INTO restaurant_count (restaurant_id, time_stamp, count) VALUES (%s, '%s', %s)" % (
                rest_id, ts, count)
            self.db.execute(command)

        self.render("home.html")


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
