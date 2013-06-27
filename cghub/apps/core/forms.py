import re

from django import forms


class BatchSearchForm(forms.Form):
    text = forms.CharField(
                    required=False, widget=forms.Textarea,
                    label='Space separated ids')
    upload = forms.FileField(required=False, label='Or select file')

    def clean(self):
        data = self.cleaned_data
        upload = data.get('upload')
        text = data.get('text')

        if not upload and (not text or text.isspace()):
            raise forms.ValidationError('All fields are empty')

        # get list of ids
        ids = []
        id_pattern = re.compile(
                    '[0-9abcdef]{8}-[0-9abcdef]{4}-[0-9abcdef]{4}-'
                    '[0-9abcdef]{4}-[0-9abcdef]{12}')
        for i in text.split(','):
            id = i.strip()
            if not id:
                continue
            if not id_pattern.match(id):
                raise forms.ValidationError(
                                '"%s" not mutch analysis_id pattern' % id)
            if id not in ids:
                ids.append(id)

        if upload:
            for i in upload.read().split(','):
                id = i.strip()
                if not id:
                    continue
                if not id_pattern.match(id):
                    raise forms.ValidationError(
                                '"%s" not mutch analysis_id pattern' % id)
                if id not in ids:
                    ids.append(id)

        data['ids'] = ids

        return data
