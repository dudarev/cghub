from django import forms

from django.utils import simplejson as json


class CheckInputTypeForm(forms.Form):
    filters = forms.CharField()
    attributes = forms.CharField()

    def clean(self):
        cleaned_data = super(CheckInputTypeForm, self).clean()
        filters = self.cleaned_data.get('filters')
        attributes = self.cleaned_data.get('attributes')
        if filters:
            try:
                filters = json.loads(filters)
            except:
                raise forms.ValidationError("Validation error in filters")
        try:
            attributes = json.loads(attributes)
        except:
            raise forms.ValidationError("Validation error in attributes")
        return self.cleaned_data
