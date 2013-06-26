from django import forms
from django.utils.translation import ugettext_lazy as _


class BatchSearchForm(forms.Form):
    text = forms.CharField(required=False, widget=forms.Textarea, label=_('Space separated ids'))
    upload = forms.FileField(required=False, label=_('Or select file'))

    def clean(self):
        cleaned_data = super(BatchSearchForm, self).clean()
        cl_upload = cleaned_data.get("upload")
        cl_text = cleaned_data.get("text")

        if not cl_upload and (not cl_text or cl_text.isspace()):
            raise forms.ValidationError("All fields are empty")

        return cleaned_data
