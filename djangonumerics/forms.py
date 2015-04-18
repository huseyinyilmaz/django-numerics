"""Form implementations for numerics app."""
from django import forms


class EndPointForm(forms.Form):

    """Form that will used to validate endpoint view arguments."""

    endpoint = forms.CharField()


class LabelResponseForm(forms.Form):

    """Validation Form for LabelResponse."""

    value = forms.CharField()
    postfix = forms.CharField()


class NumberResponseForm(forms.Form):

    """Validation Form for NumberResponse."""

    value = forms.FloatField()
    postfix = forms.CharField()

    def clean_value(self):
        """If value is an integer convert it to an integer field."""
        value = self.cleaned_data['value']
        # if value is integer return it in integer type.
        if value.is_integer():
            value = int(value)
        return value
