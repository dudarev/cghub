from django import forms

from django.utils import simplejson as json


class SelectedItemsForm(forms.Form):
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
            for a in selected_items:
                if not isinstance(a, dict):
                    raise forms.ValidationError('selected_items has not valid value')
        return selected_items


class AllItemsForm(forms.Form):
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
