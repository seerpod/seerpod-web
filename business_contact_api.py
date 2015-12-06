"""Api to access business contact model."""

__author__ = 'tarunkumar'


class BusinessContacts:

    def __init__(self, db_connector):
        self.db = db_connector

    def get_user_detail_from_email(self, email):
        user = self.db.get("SELECT * FROM business_contact WHERE owner_email_id = %s", email)
        return user

    def get_user_detail_from_id(self, user_id):
        user = self.db.get("SELECT * FROM business_contact WHERE id = %s", user_id)
        return user

    def create_business_account(self, email, password, phone_number=None, first_name=None, last_name=None):

        user = self.db.execute(
            "INSERT INTO business_contact (owner_email_id, password, phone, first_name, last_name) "
            "VALUES (%s, %s, %s, %s, %s)", email, password, phone_number, first_name, last_name)

        return self.get_user_detail_from_id(user)


