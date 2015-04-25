"""Tests for djangonumerics.serializers."""
from djangonumerics import api
from djangonumerics import responses
from djangonumerics import serializers

from tests.base import BaseTestCase


class BaseSerializerTestCase(BaseTestCase):

    """Base Test case for all serialziers.

    This class also tests Debug serializer class.
    """

    # this will be assigned on child classes
    serializer_class = serializers.DebugSerializer

    def test_valid_serialize(self):
        """Test serialize/deserialize with valid data."""
        serializer = self.serializer_class()
        endpoint_name = 'label_endpoint'
        api.register(endpoint_name,
                     self.label_endpoint,
                     responses.LabelResponse)

        user = self.create_user()
        endpoint = api.get_endpoint_by_name(endpoint_name)

        data = (user, endpoint)
        output_data = serializer.deserialize(serializer.serialize(*data))
        self.assertEqual(data, output_data)

    def test_invalid_serialize(self):
        """Test serialize/deserialize with tempered data."""
        serializer = self.serializer_class()
        endpoint_name = 'label_endpoint'
        api.register(endpoint_name,
                     self.label_endpoint,
                     responses.LabelResponse)

        user = self.create_user()
        endpoint = api.get_endpoint_by_name(endpoint_name)

        data = (user, endpoint)
        serialized_code = serializer.serialize(*data)

        tempered_code = serialized_code + 'X'
        with self.assertRaises(serializers.SerializerException):
            serializer.deserialize(tempered_code)


class BasicSerializerTestCase(BaseSerializerTestCase):

    """Tests for basic serializer."""

    serializer_class = serializers.BasicSerializer


class CryptoSerializerTestCase(BaseSerializerTestCase):

    """Tests for basic serializer."""

    serializer_class = serializers.CryptoSerializer
