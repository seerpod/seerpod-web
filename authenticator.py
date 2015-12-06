"""Module for decoding the restaurant count and updating for real time discounting"""

__author__ = 'tarunkumar'

import base64
import hashlib
import time

import business_contact_api
import seerpod_exceptions

# Authentication code will expire will after 30 days(in seconds)
EXPIRE_TIME_LIMIT = 30*24*60*60


def generate_authentication_code(user):
    """Encodes user verification request using user profile ID as pub key."""

    salt = 'd9!1l@39#c3'

    expire_timestamp = time.time() + EXPIRE_TIME_LIMIT
    # Make a string which depends on restaurant id
    # Same encoding mechanism will be used in seerpod hardware

    composite_string = "%s%s%s" % (user.id, user.password, salt)

    str_hex = hashlib.md5(composite_string).hexdigest()
    decoded_str = str(user.owner_email_id) + str(user.id) + "_" + str(expire_timestamp) + "_" + str_hex

    # Encoded string will be a multiple line string, if it is greater
    # than maximum bin size of 76. Browser strips the newline character
    # in the url.
    encoded = base64.encodestring(decoded_str).strip().replace('\n', '')
    return encoded


def authenticate_user(authentication_code):
    """Authenticate user based on code."""

    for suffix in ('', '=', '=='):
        attempt = authentication_code + suffix
        decoded = base64.decodestring(attempt)
        fields = decoded.split('_')

        email, user_id, time_stamp, str_hex = fields

        if time_stamp < time.time():
            # Authentication Code Expired
            raise seerpod_exceptions.AuthenticationCodeExpired('Authentication code expired',
                                                               response_data=authentication_code)
        user = None #business_contact_api.BusinessContacts().get_user_detail_from_email(email)

        if not user:
            continue

        if attempt == generate_authentication_code(
                user.id, time_stamp, user.owner_email_id, user.password):
            return user

    # Invalid authentication code
    raise seerpod_exceptions.InvalidAuthenticationCode('Invalid Authentication code',
                                                       response_data=authentication_code)

