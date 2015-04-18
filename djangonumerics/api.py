"""interface functions for django numerics."""
import logging
import hashlib
from collections import namedtuple

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.http import urlquote
from django.utils.module_loading import import_string

_CODE_ENDPOINT_MAP = {}
_NAME_ENDPOINT_MAP = {}

logger = logging.getLogger(__name__)

EndPoint = namedtuple('EndPoint', ['name',
                                   'code', 'cache_timeout', 'func',
                                   'args', 'kwargs', 'permission_func'])

# return an endpoint that is assign to given code.
get_endpoint = _CODE_ENDPOINT_MAP.get
# return the endpoint that is assign to given name
get_endpoint_by_name = _NAME_ENDPOINT_MAP.get

_DEFAULT_SERIALIZER = 'djangonumerics.serializers.DebugSerializer'
_CACHE = {}


def get_serializer():
    """Get and cache serializer from settings.

    Serializer will be initialized only once per runtime.
    """
    if 'serializer' in _CACHE:
        serializer = _CACHE['serializer']
    else:
        name = getattr(settings, 'DJANGO_NUMERICS_SERIALIZER_BACKEND',
                       _DEFAULT_SERIALIZER)
        serializer = import_string(name)()
        _CACHE['serializer'] = serializer
    return serializer


def grant_access(user, endpoint):
    """Grant permission."""
    return True


def register(name, func, args=None, kwargs=None, cache_timeout=0,
             permission_func=grant_access):
    """Register given name and function."""
    if not args:
        args = []
    if not kwargs:
        kwargs = {}
    salt = settings.DJANGO_NUMERICS_SALT
    api_hash = hashlib.md5(str((name, salt)).encode()).hexdigest()
    endpoint = EndPoint(name=name,
                        code=api_hash,
                        func=func,
                        args=args,
                        kwargs=kwargs,
                        cache_timeout=cache_timeout)
    if(api_hash in _CODE_ENDPOINT_MAP):
        logger.warn('Endpoint %s is already registered to numerics', name)
    else:
        _CODE_ENDPOINT_MAP[api_hash] = endpoint
        _NAME_ENDPOINT_MAP[name] = endpoint


def get_endpoint_url(user, endpoint):
    """Return url string for given user and endpoint."""
    serializer = get_serializer()
    data = serializer.serialize(user, endpoint)
    return '{url}?endpoint={endpoint}'.format(
        url=reverse('django-numerics-index'),
        endpoint=urlquote(data))


def get_endpoint_urls(user):
    """Return mapping of name->enpoints for given user."""
    return {endpoint.name: get_endpoint_url(user, endpoint)
            for endpoint in _CODE_ENDPOINT_MAP.values()}
