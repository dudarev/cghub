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
        raw_ids = []
        ids = []
        legacy_sample_ids = []
        id_pattern = re.compile(
                    '[0-9abcdef]{8}-[0-9abcdef]{4}-[0-9abcdef]{4}-'
                    '[0-9abcdef]{4}-[0-9abcdef]{12}')
        legacy_sample_id_pattern = re.compile(
                    '[0-9A-Z]{4}-[0-9A-Z]{2}-[0-9A-Z]{4}-[0-9A-Z]{3}-'
                    '[0-9A-Z]{3}-[0-9A-Z]{4}-[0-9A-Z]{2}')
        for i in text.split():
            id = i.strip()
            if not id:
                continue
            raw_ids.append(id)

        if upload:
            for i in upload.read().split():
                id = i.strip()
                if not id:
                    continue
                raw_ids.append(id)

        for id in raw_ids:
            if id_pattern.match(id):
                if id not in ids:
                    ids.append(id)
                continue
            elif legacy_sample_id_pattern.match(id):
                if id not in legacy_sample_ids:
                    legacy_sample_ids.append(id)
                continue
            raise forms.ValidationError('"%s" not mutch any id pattern' % id)

        data['ids'] = ids
        data['legacy_sample_ids'] = legacy_sample_ids

        return data
