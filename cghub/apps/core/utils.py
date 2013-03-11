import os, sys
import urllib
import traceback
import hashlib
import csv

from StringIO import StringIO
from lxml import etree, objectify
from datetime import datetime

from django.core.mail import mail_admins
from django.core.servers import basehttp
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone

from cghub.wsapi.api import request as api_request
from cghub.wsapi.api import Results
from cghub.apps.core.templatetags.search_tags import field_values


ALLOWED_ATTRIBUTES = (
        'study',
        'center_name',
        'last_modified',
        'upload_date',
        'analyte_code',
        'sample_type',
        'library_strategy',
        'disease_abbr',
        'state',
        'refassem_short_name',
    )

WSAPI_SETTINGS_LIST = (
        'CGHUB_SERVER',
        'CGHUB_ANALYSIS_ID_URI',
        'CGHUB_ANALYSIS_ATTRIBUTES_URI',
        'USE_CACHE',
        'CACHE_BACKEND',
        'CACHE_DIR',
    )


def get_filters_string(attributes):
    filter_str = ''
    for attr in ALLOWED_ATTRIBUTES:
        if attributes.get(attr):
                filter_str += '&%s=%s' % (
                    attr,
                    urllib.quote(attributes.get(attr))
                )
    return filter_str


def get_wsapi_settings():
    wsapi_settings = {}
    for name in WSAPI_SETTINGS_LIST:
        setting = getattr(settings, 'WSAPI_%s' % name, None)
        if setting != None:
            wsapi_settings[name] = setting
    return wsapi_settings


def generate_task_uuid(**d):
    """
    Generate uuid from dict
    """
    result = [str(v) for v in d.values()]
    result.sort()
    md5 = hashlib.md5(''.join(result))
    return md5.hexdigest()


def is_celery_alive():
    """
    Return 'True' if celery works properly
    """
    if 'test' in sys.argv:
        return True
    try:
        from celery.task.control import inspect
        insp = inspect()
        d = insp.stats()
        if not d:
            return False
        return True
    except Exception:
        subject = '[ucsc-cghub] ERROR: Message broker not working'
        message = traceback.format_exc()
        mail_admins(subject, message, fail_silently=True)
        return False


def get_results(ids, get_attributes=False, live_only=False):
    results = None
    results_counter = 1
    for analysis_id in ids:
        if live_only and ids[analysis_id].get('state') != 'live':
            continue
        filename = "{0}_with{1}_attributes".format(
            analysis_id,
            '' if get_attributes else 'out')
        try:
            result = Results.from_file(
                os.path.join(settings.CART_CACHE_DIR, filename),
                settings=get_wsapi_settings())
        except IOError:
            result = api_request(
                query='analysis_id={0}'.format(analysis_id),
                get_attributes=get_attributes, settings=get_wsapi_settings())
        if results is None:
            results = result
            results.Query.clear()
            results.Hits.clear()
        else:
            result.Result.set('id', u'{0}'.format(results_counter))
            # '+ 1' because the first two elements (0th and 1st) are Query and Hits
            results.insert(results_counter + 1, result.Result)
        results_counter += 1

    return results


def manifest(ids, format):
    results = get_results(ids, live_only=True)
    if not results:
        results= _empty_results()

    mfio = StringIO()
    if format == 'xml':
        mfio.write(results.tostring())
        content_type = 'text/xml'
        filename = 'manifest.xml'
    if format == 'tsv':
        parser = etree.XMLParser()
        tree = etree.XML(results.tostring(), parser)
        csvwriter = _write_manifest_csv(stringio=mfio, tree=tree)
        content_type = 'text/tsv'
        filename = 'manifest.tsv'
    mfio.seek(0)

    response = HttpResponse(basehttp.FileWrapper(mfio), content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


def metadata(ids, format):
    mfio = StringIO()
    results = get_results(ids, get_attributes=True)

    if format == 'xml':
        mfio.write(results.tostring())
        content_type = 'text/xml'
        filename = 'metadata.xml'
    if format == 'tsv':
        results.add_custom_fields()
        csvwriter = _write_metadata_csv(stringio=mfio, results=results)
        content_type = 'text/tsv'
        filename = 'metadata.tsv'

    mfio.seek(0)
    response = HttpResponse(basehttp.FileWrapper(mfio), content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


def _empty_results():
    results = Results(
        objectify.fromstring('<ResultSet></ResultSet>'),
        settings=get_wsapi_settings())
    results.set('date', timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
    results.insert(0, objectify.fromstring('<Query></Query>'))
    results.insert(1, objectify.fromstring('<Hits></Hits>'))
    results.insert(2, objectify.fromstring(
        '<ResultSummary>'
        '<downloadable_file_count>0</downloadable_file_count>'
        '<downloadable_file_size units="GB">0</downloadable_file_size>'
        '<state_count>'
        '<live>0</live>'
        '</state_count>'
        '</ResultSummary>'))
    return results


def _write_manifest_csv(stringio, tree):
    csvwriter = csv.writer(stringio, quoting=csv.QUOTE_MINIMAL, dialect='excel-tab')
    # date
    csvwriter.writerow(tree.items()[0])
    csvwriter.writerow('')
    # Result
    result = tree.find("Result")
    csvwriter.writerow([result.keys()[0]]+
                       [r.tag for r in result.iterchildren()])
    for result in tree.iterfind("Result"):
        csvwriter.writerow([result.values()[0]]+
                           [r.text for r in result.iterchildren()])
    csvwriter.writerow('')
    # ResultSummary
    summary = tree.find("ResultSummary")
    if summary is not None:
        state_count = summary.find("state_count")
        csvwriter.writerow([s.tag for s in summary.iterchildren()
                            if s.tag != "summary_count"]+
                           [s.tag for s in state_count.iterchildren()])
        csvwriter.writerow([s.text for s in summary.iterchildren()
                            if s.tag != "summary_count"]+
                           [s.text for s in state_count.iterchildren()])
    return csvwriter


def _write_metadata_csv(stringio, results):
    csvwriter = csv.writer(stringio, quoting=csv.QUOTE_MINIMAL, dialect='excel-tab')

    csvwriter.writerow([field.lower().replace(' ', '_')
                        for field, visibility in settings.TABLE_COLUMNS])
    for result in results.Result:
        fields = field_values(result)

        row = []
        for field_name, default_state in settings.TABLE_COLUMNS:
            value = fields.get(field_name, None)
            if value == None:
                continue
            row.append(value)
        csvwriter.writerow(row)
    return csvwriter
