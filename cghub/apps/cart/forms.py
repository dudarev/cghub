import re

from django import forms

from django.utils import simplejson as json


class SelectedFilesForm(forms.Form):
    """
    Checks that adding selected files to cart sends the right
    format to the form - format that can be loaded to json.
    """
    selected_items = forms.CharField()

    def clean_selected_items(self):
        selected_items = self.cleaned_data.get('selected_items')
        try:
            selected_items = json.loads(selected_items)
        except (TypeError, ValueError):
            raise forms.ValidationError('selected_items value is not valid json')
        if not isinstance(selected_items, list):
            raise forms.ValidationError('selected_items has not valid value')
        if selected_items:
            id_pattern = re.compile(
                    '^[0-9abcdef]{8}-[0-9abcdef]{4}-[0-9abcdef]{4}-'
                    '[0-9abcdef]{4}-[0-9abcdef]{12}$')
            for a in selected_items:
                if not id_pattern.match(str(a)):
                    raise forms.ValidationError('selected_items has not valid value')
        return selected_items


class AllFilesForm(forms.Form):
    """
    Checks that adding all files to cart sends the right
    format to the form - format that can be loaded to json.
    """
    filters = forms.CharField()

    def clean_filters(self):
        filters = self.cleaned_data.get('filters')
        try:
            filters = json.loads(filters)
        except (TypeError, ValueError):
            raise forms.ValidationError("filters value is not valid json")
        if not isinstance(filters, dict):
            raise forms.ValidationError('filters has not valid value')
        return filters
