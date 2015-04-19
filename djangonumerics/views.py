"""View implementations for numeric source."""
import json
import logging
from django.http import Http404
from django.http import HttpResponse
from django.views.generic import View
from django.conf import settings
from djangonumerics.api import get_endpoint_url
from djangonumerics.api import get_endpoints
from djangonumerics.api import get_serializer
from djangonumerics.forms import EndPointForm
from djangonumerics.exceptions import ResponseException
from djangonumerics.responses import LabelResponse
from djangonumerics.responses import NumberResponse

from djangonumerics.serializers import SerializerException
from django.shortcuts import render
from django.core.cache import cache
logger = logging.getLogger()


class IndexView(View):

    """List endpoints view."""

    def get(self, request):
        """get method."""
        endpoints = get_endpoints(request.user)
        view_name = getattr(settings,
                            'DJANGO_NUMERICS_VIEW',
                            'djangonumerics/index.html')
        return render(self.request, view_name,
                      {'endpoints': endpoints,
                       'LabelResponse': LabelResponse,
                       'NumberResponse': NumberResponse})


class BaseView(View):

    """View for numeric endpoints.

    If an endpoint is provided
    """

    def get(self, request, code):
        """get handler."""
        enabled = getattr(settings,
                          'DJANGO_NUMERICS_ENABLED',
                          True)
        if not enabled:
            raise Http404()

        serializer = get_serializer()
        try:
            user, endpoint = serializer.deserialize(code)
            self.user = user
            self.endpoint = endpoint
        except SerializerException:
            logger.exception('Cannot deserialize')
            raise Http404()
        return self.process(code, user, endpoint)


class EndpointView(BaseView):

    """numeric source interface."""

    form_class = EndPointForm

    def process(self, code, user, endpoint):
        """Return result for given endpoint."""
        response_body = endpoint.cache_timeout and cache.get(code)
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
                    cache.set(code,
                              response_body,
                              endpoint.cache_timeout)
            except ResponseException as e:
                logger.exception('Could not return a response')
                response_body = json.dumps({'success': False,
                                            'errors': e.args})

        return HttpResponse(response_body,
                            content_type='application/json')


class HelpView(BaseView):

    """Endpoint for given help page."""

    def process(self, code, user, endpoint):
        """Return help page as httpresponse."""
        view_name = getattr(settings,
                            'DJANGO_NUMERICS_HELP_VIEW',
                            'djangonumerics/help.html')

        return render(self.request, view_name,
                      {'code': code,
                       'user': user,
                       'endpoint': endpoint,
                       'endpoint_response_class': str(endpoint.response_type),
                       'label_response_class': str(LabelResponse),
                       'number_response_class': str(NumberResponse.code),
                       'endpoint_url': get_endpoint_url(user, endpoint)})
