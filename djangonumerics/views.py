"""View implementations for numeric source."""
import json
import logging
from django.http import Http404
from django.http import HttpResponse
from django.views.generic import View
from django.conf import settings
from djangonumerics.api import get_endpoint_urls
from djangonumerics.api import get_serializer
from djangonumerics.forms import EndPointForm
from djangonumerics.exceptions import ResponseException
from djangonumerics.serializers import SerializerException
from django.shortcuts import render
from django.core.cache import cache
logger = logging.getLogger()


class IndexView(View):

    """numeric source interface.

    This interface lists all endpoints for current user.
    If an enpoint parameter is provided, it provides that for given interface.
    """

    form_class = EndPointForm

    def get(self, request):
        """Return endpoint list or result of given endpoint.

        If endpoint code is provided, deserializes endpoint code into
        user and endpoint and returns result of that endpoint for given user.
        If endpoint code is not provided returns return list of numeric
        endpoints for given user.
        """
        enabled = getattr(settings,
                          'DJANGO_NUMERICS_ENABLED',
                          True)
        view_name = getattr(settings,
                            'DJANGO_NUMERICS_VIEW',
                            'djangonumerics/index.html')
        if not enabled:
            raise Http404()
        form = self.form_class(request.GET)
        if form.is_valid():
            endpoint_code = form.cleaned_data['endpoint']
            serializer = get_serializer()
            try:
                user, endpoint = serializer.deserialize(endpoint_code)
            except SerializerException:
                logger.exception('Cannot deserialize')
                raise Http404()
            response_body = endpoint.cache_timeout and cache.get(endpoint_code)
            if not response_body:
                try:
                    endpoint_response = endpoint.func(user,
                                                      *endpoint.args,
                                                      **endpoint.kwargs)
                    if not type(endpoint_response) == endpoint.response_type:
                        raise ResponseException(
                            'Endpoint Response Must be {expected_type}. '
                            '{typ} found '
                            'instead. {val})'
                            .format(expected_type=endpoint.response_type,
                                    typ=type(endpoint_response),
                                    val=endpoint_response))
                    response_body = json.dumps(endpoint_response.response())
                    if endpoint.cache_timeout:
                        cache.set(endpoint_code,
                                  response_body,
                                  endpoint.cache_timeout)
                except ResponseException as e:
                    logger.exception('Could not return a response')
                    response_body = json.dumps({'success': False,
                                                'errors': e.args})
            response = HttpResponse(response_body,
                                    content_type='application/json')
        else:
            endpoint_urls = get_endpoint_urls(request.user)

            response = render(self.request, view_name,
                              {'endpoint_urls': endpoint_urls})
        return response
