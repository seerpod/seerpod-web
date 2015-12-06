"""Contains exceptions that will be thrown bu seerpod."""

__author__ = 'tarunkumar'


class SeerpodAPIBaseException(Exception):
    """Base class for Details API exceptions."""

    def __init__(self, message, response_data=None):
        super(SeerpodAPIBaseException, self).__init__(message)
        self.response_data = response_data


class InvalidAuthenticationCode(SeerpodAPIBaseException):
    """Raised if authentication code is invalid."""


class AuthenticationCodeExpired(SeerpodAPIBaseException):
    """Raised if authentication code is expired."""


