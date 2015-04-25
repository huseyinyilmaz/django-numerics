"""Tests for djangonumerics.api."""

from operator import itemgetter

from tests.base import BaseTestCase
from djangonumerics import responses
from djangonumerics import api


class BaseAPITestCase(BaseTestCase):

    """Base endpoint for base api test case."""

    def always_true(self, user, endpoint):
        """permission function that always grants."""
        return True

    def always_false(self, user, endpoint):
        """permission function that always refuses."""
        return False


class RegisterTests(BaseAPITestCase):

    """Tests for register."""

    def test_valid_endpoint(self):
        """Test register call with valid endpoint."""
        name = 'label_endpoint'
        api.register(name,
                     self.label_endpoint,
                     responses.LabelResponse)
        # make sure that values code end name maps have same value.
        self.assertEqual(list(api._CODE_ENDPOINT_MAP.values()),
                         list(api._NAME_ENDPOINT_MAP.values()))
        # make sure there is only one endpoint registered
        self.assertEqual(len(api._CODE_ENDPOINT_MAP.values()), 1)
        endpoint = next(iter(api._CODE_ENDPOINT_MAP.values()))
        self.assertEqual(endpoint.name, name)
        self.assertEqual(endpoint.func, self.label_endpoint)
        self.assertEqual(endpoint.permission_func, api.grant_access)

    def test_valid_endpoint_with_permission_func(self):
        """Test register call with valid endpoint and permission function."""
        name = 'label_endpoint'
        api.register(name,
                     self.label_endpoint,
                     responses.LabelResponse,
                     permission_func=self.always_true)
        endpoint = next(iter(api._CODE_ENDPOINT_MAP.values()))
        self.assertEqual(endpoint.name, name)
        self.assertEqual(endpoint.func, self.label_endpoint)
        self.assertEqual(endpoint.permission_func, self.always_true)

    def test_valid_endpoint_register_twice_with_permission_func(self):
        """Test register call with valid endpoint and permission function.

        This time endpoint will be registered twice and it will be with
        different permission function. In that case, we will use the first one
        registered.

        """
        name = 'label_endpoint'
        api.register(name,
                     self.label_endpoint,
                     responses.LabelResponse,
                     permission_func=self.always_true)
        api.register(name,
                     self.number_endpoint,
                     responses.LabelResponse)
        endpoint = next(iter(api._CODE_ENDPOINT_MAP.values()))
        self.assertEqual(endpoint.name, name)
        self.assertEqual(endpoint.func, self.label_endpoint)
        self.assertEqual(endpoint.permission_func, self.always_true)


class GetEndPointsTests(BaseAPITestCase):

    """Tests for djangonumerics.api.get_endpoints."""

    def test_two_granted_endpoints(self):
        """Test endpoints with granted access."""
        user = self.create_user()
        api.register('label_endpoint',
                     self.label_endpoint,
                     responses.LabelResponse,
                     permission_func=self.always_true)
        api.register('number_endpoint',
                     self.number_endpoint,
                     responses.NumberResponse,
                     permission_func=self.always_true)
        endpoints = sorted(api.get_endpoints(user),
                           key=itemgetter('name'))

        expected_endpoints = [{'help_url': '/help/username/label_endpoint',
                               'name': 'label_endpoint',
                               'url': '/username/label_endpoint'},
                              {'help_url': '/help/username/number_endpoint',
                               'name': 'number_endpoint',
                               'url': '/username/number_endpoint'}]

        self.assertEqual(endpoints, expected_endpoints)

    def test_one_granted_endpoints(self):
        """Test endpoints with one granted, one denied access."""
        user = self.create_user()
        api.register('label_endpoint',
                     self.label_endpoint,
                     responses.LabelResponse,
                     permission_func=self.always_true)
        api.register('number_endpoint',
                     self.number_endpoint,
                     responses.NumberResponse,
                     permission_func=self.always_false)
        endpoints = sorted(api.get_endpoints(user),
                           key=itemgetter('name'))

        expected_endpoints = [{'help_url': '/help/username/label_endpoint',
                               'name': 'label_endpoint',
                               'url': '/username/label_endpoint'}]
        self.assertEqual(endpoints, expected_endpoints)

    def test_no_granted_endpoints(self):
        """Test endpoints with denied access."""
        user = self.create_user()
        api.register('label_endpoint',
                     self.label_endpoint,
                     responses.LabelResponse,
                     permission_func=self.always_false)
        api.register('number_endpoint',
                     self.number_endpoint,
                     responses.NumberResponse,
                     permission_func=self.always_false)
        endpoints = api.get_endpoints(user)
        expected_endpoints = []
        self.assertEqual(endpoints, expected_endpoints)
