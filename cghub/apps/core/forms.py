from django import forms


class BatchSearchForm(forms.Form):
    file = forms.FileField(required=False)
    text = forms.CharField(required=False, widget=forms.Textarea)

    def clean(self):
        cleaned_data = super(BatchSearchForm, self).clean()
        cl_file = cleaned_data.get("file")
        cl_text = cleaned_data.get("text")

        if not cl_file and (not cl_text or cl_text.isspace()):
            raise forms.ValidationError("All fields are empty")

        return cleaned_data
