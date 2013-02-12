from django import forms

from django.utils import simplejson as json


class SelectedFilesForm(forms.Form):
    """
    Checks that adding selected files to cart sends the right
    format to the form - format that can be loaded to json.
    """
    attributes = forms.CharField()
    selected_files = forms.CharField()

    def clean_attributes(self):
        attributes = self.cleaned_data.get('attributes')
        try:
            attributes = json.loads(attributes)
        except (TypeError, ValueError):
            raise forms.ValidationError('attributes value is not valid json')
        if not isinstance(attributes, dict):
            raise forms.ValidationError('attributes has not valid value')
        if len(attributes):
            for a in attributes:
                if not isinstance(attributes[a], dict):
                    raise forms.ValidationError('attributes has not valid value')
        return attributes

    def clean_selected_files(self):
        selected_files = self.cleaned_data.get('selected_files')
        try:
            selected_files = json.loads(selected_files)
        except (TypeError, ValueError):
            raise forms.ValidationError('selected_files value is not valid json')
        if not isinstance(selected_files, list):
            raise forms.ValidationError('selected_files has not valid value')
        return selected_files


class AllFilesForm(forms.Form):
    """
    Checks that adding all files to cart sends the right
    format to the form - format that can be loaded to json.
    """
    filters = forms.CharField()
    attributes = forms.CharField()

    def clean_filters(self):
        filters = self.cleaned_data.get('filters')
        try:
            filters = json.loads(filters)
        except (TypeError, ValueError):
            raise forms.ValidationError("filters value is not valid json")
        if not isinstance(filters, dict):
            raise forms.ValidationError('filters has not valid value')
        return filters

    def clean_attributes(self):
        attributes = self.cleaned_data.get('attributes')
        try:
            attributes = json.loads(attributes)
        except (TypeError, ValueError):
            raise forms.ValidationError("filters value is not valid json")
        if not isinstance(attributes, list):
            raise forms.ValidationError('filters has not valid value')
        return attributes
