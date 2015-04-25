"""Test views."""

import json
from operator import itemgetter

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import Client

from djangonumerics import api
from djangonumerics import responses

from tests.base import BaseTestCase


class IndexViewTests(BaseTestCase):

    """Test endpoint for views."""

    def setUp(self):
        """Add an http client to test object."""
        super(IndexViewTests, self).setUp()
        self.client = Client()

    def test_no_registered_endpoint(self):
        """Test view context with no endpoint.

        Test when we have no registered enpoint,
        system returns returns an empty endpoint_urls.
        """
        url = reverse('django-numerics-index')

        self.create_user()

        self.client.login(username=self.USERNAME, password=self.PASSWORD)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_registered_endpoints(self):
        """Test view context with one valid endpoint."""
        url = reverse('django-numerics-index')

        self.create_user()
        api.register('label_endpoint',
                     self.label_endpoint,
                     responses.LabelResponse)

        api.register('number_endpoint',
                     self.number_endpoint,
                     responses.NumberResponse)

        self.client.login(username=self.USERNAME, password=self.PASSWORD)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        endpoint_urls = sorted(response.context[0].get('endpoints'),
                               key=itemgetter('name'))
        expected_urls = [{'help_url': '/help/username/label_endpoint',
                          'name': 'label_endpoint',
                          'url': '/username/label_endpoint'},
                         {'help_url': '/help/username/number_endpoint',
                          'name': 'number_endpoint',
                          'url': '/username/number_endpoint'}]
        self.assertListEqual(endpoint_urls, expected_urls)

    def test_one_registered_endpoint_no_user(self):
        """Test view context with one valid endpoint.

        this time there will not be any logged in users. Default
        permission function will filter all the results. As a result,
        this request will return http404
        """
        url = reverse('django-numerics-index')

        api.register('label_endpoint',
                     self.label_endpoint,
                     responses.LabelResponse)

        api.register('number_endpoint',
                     self.number_endpoint,
                     responses.NumberResponse)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class EndpointViewTests(BaseTestCase):

    """Test for endpoint view."""

    def setUp(self):
        """Add an http client to test object."""
        super(EndpointViewTests, self).setUp()
        self.client = Client()

    def test_registered_endpoints(self):
        """Test view context with one valid endpoint."""
        User = get_user_model()
        User.objects.create_user('test', 'test@test.com', 'test')
        user = User.objects.get()

        api.register('label_endpoint',
                     self.label_endpoint,
                     responses.LabelResponse)

        url = api.get_endpoints(user)[0]['url']

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        resp_json = json.loads(response.content.decode('utf-8'))
        expected_json = {'data': {'value': 'label_val'},
                         'postfix': 'postfix_label'}
        self.assertEqual(resp_json, expected_json)

    def test_registered_endpoints_with_wrong_return_type(self):
        """Test view context with one valid endpoint."""
        User = get_user_model()
        User.objects.create_user('test', 'test@test.com', 'test')
        user = User.objects.get()

        api.register('label_endpoint',
                     self.label_endpoint,
                     responses.NumberResponse)

        url = api.get_endpoints(user)[0]['url']

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        resp_json = json.loads(response.content.decode('utf-8'))
        self.assertFalse(resp_json['success'])
