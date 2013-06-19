from django import forms


class BatchSearchForm(forms.Form):
    file = forms.FileField(required=False)
    text = forms.CharField(required=False, widget=forms.Textarea)
