"""Test views."""

from django.test import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model


class EndpointViewTests(TestCase):

    """Test endpoint for views."""

    def setUp(self):
        """Add an http client to test object."""
        super(EndpointViewTests, self).setUp()
        self.client = Client()

    def test_no_registered_endpoint(self):
        """Test view context with no endpoint.

        Test when we have no registered enpoint,
        system returns returns an empty endpoint_urls.
        """
        url = reverse('django-numerics-index')
        User = get_user_model()
        User.objects.create_user('test', 'test@test.com', 'test')

        self.client.login(username='test', password='test')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        endpoint_urls = response.context[0].get('endpoints')
        self.assertEqual(endpoint_urls, [])
