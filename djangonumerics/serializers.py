"""Builtin Serilizers objects. for numerics mixin.

This Class Serializes current user and endpoint object to create
endpoint url.
"""

from django.contrib.auth import get_user_model

from djangonumerics.api import get_endpoint
from djangonumerics.api import get_endpoint_by_name
from djangonumerics.utils import encrypt
from djangonumerics.utils import decrypt

from cryptography.fernet import InvalidToken


class SerializerException(Exception):

    """Raised if Serializer cannot deserialize given string."""


class DebugSerializer:

    """Debug serializer.

    This is default serializer. Serialized urls will be human readable.
    """

    SEPARATOR = "/"

    def serialize(self, user, endpoint):
        """Serialize to username/endpoint_name."""
        return '{username}{seperator}{endpoint_name}'.format(
            username=user.username,
            seperator=self.SEPARATOR,
            endpoint_name=endpoint.name)

    def deserialize(self, st):
        """Deserialize url."""
        s_index = st.find(self.SEPARATOR)
        if s_index == -1:
            raise SerializerException('Invalid endpoint string')

        username = st[:s_index]
        endpoint_name = st[s_index + 1:]

        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise SerializerException('User does not exist')
        endpoint = get_endpoint_by_name(endpoint_name)
        if not endpoint:
            raise SerializerException('Endpoint does not exist')
        return user, endpoint


class BasicSerializer:

    """Basic serializer."""

    SEPARATOR = '/'

    def serialize(self, user, endpoint):
        """serialize to user_pk|endpointcode."""
        return '{user_pk}{seperator}{endpoint_code}'.format(
            user_pk=user.pk,
            seperator=self.SEPARATOR,
            endpoint_code=endpoint.code)

    def deserialize(self, st):
        """Deserialize url."""
        [user_pk, endpoint_code] = st.split(self.SEPARATOR)
        User = get_user_model()
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            raise SerializerException('User does not exist')
        endpoint = get_endpoint(endpoint_code)
        if not endpoint:
            raise SerializerException('Endpoint does not exist')
        return user, endpoint


class CryptoSerializer:

    """Serialize with cryptography."""

    def serialize(self, user, endpoint):
        """Serialize using fernet encryption."""
        return encrypt((user.pk, endpoint.code))

    def deserialize(self, st):
        """Deserialize url."""
        try:
            (user_pk, endpoint_code) = decrypt(st)
        except InvalidToken:
            raise SerializerException('Invalid token. Cannot deserialize.')
        User = get_user_model()
        try:
            user = User.objects.get(pk=user_pk)

        except User.DoesNotExist:
            raise SerializerException('User does not exist')
        endpoint = get_endpoint(endpoint_code)
        if not endpoint:
            raise SerializerException('Endpoint does not exist')
        return user, endpoint
