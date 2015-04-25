"""Tests for djangonumerics.responses."""
import json
from djangonumerics import exceptions
from djangonumerics import responses
from tests.base import BaseTestCase


class LabelResponseTestCase(BaseTestCase):

    """Tests for LabelResponse."""

    def test_valid_data(self):
        """Test valid data."""
        response = responses.LabelResponse('value', 'postfix')
        resp = json.loads(response.to_http_response().content.decode('utf-8'))
        expected_resp = {'data': {'value': 'value'}, 'postfix': 'postfix'}
        self.assertEqual(resp, expected_resp)

    def test_valid_number_data(self):
        """Test valid number data.

        This is testing if number data is being converting to str in json.
        """
        response = responses.LabelResponse(12.3, 'postfix')
        resp = json.loads(response.to_http_response().content.decode('utf-8'))
        expected_resp = {'data': {'value': '12.3'}, 'postfix': 'postfix'}
        self.assertEqual(resp, expected_resp)

    def test_valid_no_postfix(self):
        """Test valid data with no postfix."""
        response = responses.LabelResponse('value')
        resp = json.loads(response.to_http_response().content.decode('utf-8'))
        expected_resp = {'data': {'value': 'value'}, 'postfix': ''}
        self.assertEqual(resp, expected_resp)


class NumberResponseTestCase(BaseTestCase):

    """Tests for NumberResponse."""

    def test_valid_data(self):
        """Test valid data."""
        response = responses.NumberResponse(12.3, 'postfix')
        resp = json.loads(response.to_http_response().content.decode('utf-8'))
        expected_resp = {'data': {'value': 12.3}, 'postfix': 'postfix'}
        self.assertEqual(resp, expected_resp)

    def test_valid_str_data(self):
        """Test valid number data.

        This is testing if str data is being parsed to number in json.
        """
        response = responses.NumberResponse('12.3', 'postfix')
        resp = json.loads(response.to_http_response().content.decode('utf-8'))
        expected_resp = {'data': {'value': 12.3}, 'postfix': 'postfix'}
        self.assertEqual(resp, expected_resp)

    def test_valid_no_postfix(self):
        """Test valid data with no postfix."""
        response = responses.NumberResponse(12.3)
        resp = json.loads(response.to_http_response().content.decode('utf-8'))
        expected_resp = {'data': {'value': 12.3}, 'postfix': ''}
        self.assertEqual(resp, expected_resp)

    def test_invalid_data(self):
        """Test valid number data.

        This is testing if str data is being parsed to number in json.
        """
        with self.assertRaises(exceptions.ResponseException) as e:
            responses.NumberResponse('invalid', 'postfix')
        expected_args = ('Cannot parse answer.',
                         {'data': {'value': 'invalid',
                                   'postfix': 'postfix'},
                          'errors': {'value': ['Enter a number.']}})

        self.assertEqual(e.exception.args, expected_args)
