__author__ = 'tarunkumar'

"""Module for decoding the restaurant count and updating for real time discounting"""

import base64
import hashlib


def encode_restaurant_count_request(rest_id, time_stamp, count):
    """Encodes user verification request using user profile ID as pub key."""

    # Example encoded string = MV8xNDM5MDk2NDEwLjNfMjNkODRkOGFjNDc3YTEzYjRiMTFkMjY4OGYxZTBhZGFfMjM0
    salt = 'c9!1k@47!b3'

    # Make a string which depends on restaurant id
    # Same encoding mechanism will be used in seerpod hardware

    composite_string = "%s%s" % (rest_id, salt)

    str_hex = hashlib.md5(composite_string).hexdigest()
    decoded_str = str(rest_id) + "_" + str(time_stamp) + "_" + str_hex + '_' + str(count)

    # Encoded string will be a multiple line string, if it is greater
    # than maximum bin size of 76. Browser strips the newline character
    # in the url.
    encoded = base64.encodestring(decoded_str).strip().replace('\n', '')
    return encoded


def get_count_from_encoded_count_request(encoded_string):
    """Extracts restaurant id and count from the request."""

    try:
        decoded = base64.decodestring(encoded_string)
        fields = decoded.split('_')
        rest_id, time_stamp, str_hex, count = fields

        # If this request is valid return this
        if encoded_string == encode_restaurant_count_request(rest_id, time_stamp, count):
            return rest_id, time_stamp, count
    except:
        return None, None, None
