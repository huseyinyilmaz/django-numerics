"""Base module for all tests."""
from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase

from djangonumerics import api
from djangonumerics import responses


class BaseTestCase(TestCase):

    """Base test class for view tests."""

    USERNAME = 'username'
    PASSWORD = 'password'
    EMAIL = 'email@test.com'

    def setUp(self):
        """Add an http client to test object."""
        super(BaseTestCase, self).setUp()
        self.client = Client()

    def _empty_dict(self, d):
        """Empty given dict.

        We have references to existing dict methods so we cannot replace it
        with a new one. Those references will still be bound to old instance.
        """
        for key in list(d.keys()):
            del d[key]

    def tearDown(self):
        """Reset registered endpoints."""
        self._empty_dict(api._CODE_ENDPOINT_MAP)
        self._empty_dict(api._NAME_ENDPOINT_MAP)
        self._empty_dict(api._CACHE)

    def label_endpoint(self, user):
        """mock label endpoint."""
        return responses.LabelResponse('label_val', 'postfix_label')

    def number_endpoint(self, user):
        """mock number endpoint."""
        return responses.NumberResponse(3, 'postfix_number')

    def create_user(self):
        """Create a new user."""
        User = get_user_model()
        User.objects.create_user(self.USERNAME,
                                 self.EMAIL,
                                 self.PASSWORD)
        return User.objects.get(username=self.USERNAME)
