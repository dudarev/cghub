import re

from django import forms
from django.conf import settings


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
        unvalidated_ids = []
        id_pattern = re.compile(
                    '^[0-9abcdef]{8}-[0-9abcdef]{4}-[0-9abcdef]{4}-'
                    '[0-9abcdef]{4}-[0-9abcdef]{12}$')
        legacy_sample_id_pattern = re.compile('^[A-Z]{2,8}-.{10,30}$')
        for i in text.split():
            id = i.strip()
            if not id:
                continue
            if id not in raw_ids:
                raw_ids.append(id)

        if upload:
            for i in upload.read().split():
                id = i.strip()
                if not id:
                    continue
                if id not in raw_ids:
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
            elif id not in unvalidated_ids:
                unvalidated_ids.append(id)

        if (len(ids) > settings.MAX_ITEMS_IN_QUERY or
                    len(legacy_sample_ids) > settings.MAX_ITEMS_IN_QUERY):
            raise forms.ValidationError('Max count of ids that can be '
                'submitted at once limited by %d' % settings.MAX_ITEMS_IN_QUERY)

        if not ids and not legacy_sample_ids:
            raise forms.ValidationError('No valid ids was found')

        data['raw_ids'] = raw_ids
        data['ids'] = ids
        data['legacy_sample_ids'] = legacy_sample_ids
        data['unvalidated_ids'] = unvalidated_ids

        return data


class AnalysisIDsForm(forms.Form):
    ids = forms.CharField(
                    widget=forms.Textarea,
                    label='Space separated list of analysis ids')

    def clean(self):
        data = self.cleaned_data
        ids = data.get('ids')

        if not ids or ids.isspace():
            raise forms.ValidationError('No analysis_ids found')

        id_pattern = re.compile(
                    '^[0-9abcdef]{8}-[0-9abcdef]{4}-[0-9abcdef]{4}-'
                    '[0-9abcdef]{4}-[0-9abcdef]{12}$')

        cleaned_ids = []

        for i in ids.split():
            id = i.strip()
            if not id:
                continue
            if id_pattern.match(id) and id not in cleaned_ids:
                cleaned_ids.append(id)

        data['ids'] = cleaned_ids

        return data
