"""Response objects for endpoints.

Endpoint objects must return one of those objects as responses.

New repsonse types should make sure that they are not subclass of an existing
response type. Otherwise response type check would fail for those specific
cases.
"""
import json

from django.http import HttpResponse

from djangonumerics.exceptions import ResponseException
from djangonumerics.forms import LabelResponseForm
from djangonumerics.forms import NumberResponseForm


class BaseResponse:

    """Base response object for numeric endpoint responses."""

    code = 'base'
    form_class = None

    def set_data(self, data):
        """Validate and set given data to object."""
        form = self.form_class(data)
        if form.is_valid():
            self.data = form.cleaned_data
        else:
            raise ResponseException('Cannot parse answer.',
                                    {'data': data,
                                     'errors': form.errors})

    def response(self):
        """Return a json serializable object."""
        raise NotImplementedError

    def to_http_response(self):
        """Convert the endpoint response to HttpResponse object."""
        return HttpResponse(json.dumps(self.response()),
                            content_type='application/json')


class BaseBasicResponse(BaseResponse):

    """Response Object for Label From JSON Data widget."""

    code = 'basebasic'
    form_class = None

    def __init__(self, value, postfix=''):
        """Initializer."""
        self.set_data({'value': value, 'postfix': postfix})

    def response(self):
        """Return response object."""
        return {'postfix': self.data['postfix'],
                'data': {
                    'value': self.data['value']}}


class LabelResponse(BaseBasicResponse):

    """Response Object for Label From JSON Data widget."""

    code = 'label'
    form_class = LabelResponseForm


class NumberResponse(LabelResponse):

    """Response Object for Number from JSON data widget."""

    code = 'number'
    form_class = NumberResponseForm
