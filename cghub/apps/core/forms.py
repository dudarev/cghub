from django import forms

from django.utils import simplejson as json


class SelectedFilesForm(forms.Form):
    """
    Checks that clicking at 'Add all files' sends the right
    format to the form - format that can be loaded to json.
    """
    filters = forms.CharField()
    attributes = forms.CharField()

    def clean(self):
        filters = self.cleaned_data.get('filters')
        attributes = self.cleaned_data.get('attributes')
        try:
            filters = json.loads(filters)
        except TypeError, ValueError:
            raise forms.ValidationError("Validation error in filters")
        try:
            attributes = json.loads(attributes)
        except TypeError, ValueError:
            raise forms.ValidationError("Validation error in attributes")
        return self.cleaned_data
