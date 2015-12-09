"""Api to access business contact model."""

__author__ = 'tarunkumar'


class BusinessApi:

    def __init__(self, db_connector):
        self.db = db_connector

    def get_business_vacancy(self, id, capacity):

        biz_count = self.get_business_count(id)
        if not biz_count:
            return None

        occupancy_percent = biz_count*100.0/capacity

        return int(occupancy_percent)

    def get_business_count(self, biz_id):
        command = "select count from business_counter where biz_id=%s order by time_stamp limit 1" % (
            biz_id)
        count = self.db.query(command)

        if count:
            return count[0].get('count')

        return None

    def get_businesses_near_address(self, query_address, cuisine_type=None):

        command = "SELECT * FROM business_business"

        if cuisine_type:
            cuisine_condition = " where cuisine='%s'" % cuisine_type
            command += cuisine_condition

        restaurants = self.db.query(command)
        return restaurants

    def get_business_detail(self, id):
        biz = self.db.query("SELECT * FROM business_business where id=%s" % id)

        if biz:
            return biz[0]

        return None

