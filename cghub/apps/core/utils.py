import os, sys
import urllib
import traceback
import hashlib
import csv

from StringIO import StringIO
from lxml import etree, objectify

from django.core.mail import mail_admins
from django.core.servers import basehttp
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone

from cghub.wsapi.api import request as api_request
from cghub.wsapi.api import Results
from cghub.apps.core.templatetags.search_tags import field_values
from cghub.apps.core.filters_storage import ALL_FILTERS


ALLOWED_ATTRIBUTES = ALL_FILTERS.keys()

DATE_ATTRIBUTES = (
        'last_modified',
        'upload_date',
    )

WSAPI_SETTINGS_LIST = (
        'CGHUB_SERVER',
        'CGHUB_ANALYSIS_ID_URI',
        'CGHUB_ANALYSIS_FULL_URI',
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


def get_default_query():
    """
    Taking in mind settings.DEFAULT_FILTERS returns query string.
    For example:
    DEFAULT_FILTERS = {
        'study': ('phs000178', '*Other_Sequencing_Multiisolate'),
        'state': ('live',),
        'upload_date': '[NOW-7DAY TO NOW]',
    }
    result should be:
    upload_date=[NOW-7DAY+TO+NOW]&study=(phs000178+OR+*Other_Sequencing_Multiisolate)&state=(live)
    """
    filters_list = []
    DEFAULT_FILTERS = settings.DEFAULT_FILTERS
    for f in DEFAULT_FILTERS:
        if f in ALLOWED_ATTRIBUTES:
            if f in DATE_ATTRIBUTES:
                filters_list.append('%s=%s' % (f, DEFAULT_FILTERS[f]))
            else:
                allowed_keys = ALL_FILTERS[f]['filters'].keys()
                filters_list.append('%s=(%s)' % (
                        f,
                        ' OR '.join([v for v in DEFAULT_FILTERS[f] if v in allowed_keys])
                ))
    return '&'.join(filters_list).replace(' ', '+')


def get_wsapi_settings():
    wsapi_settings = {}
    for name in WSAPI_SETTINGS_LIST:
        setting = getattr(settings, 'WSAPI_%s' % name, None)
        if setting != None:
            wsapi_settings[name] = setting
    return wsapi_settings


def generate_task_analysis_id(**d):
    """
    Generate analysis_id from dict
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
    """
    Join xml files with specified ids.
    If file exists in cache, it will be used, otherwise, file will be downloaded.
    """
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


def manifest(ids):
    results = get_results(ids, live_only=True)
    if not results:
        results= _empty_results()
    mfio = _stream_with_xml(results)
    response = HttpResponse(basehttp.FileWrapper(mfio), content_type='text/xml')
    response['Content-Disposition'] = 'attachment; filename=manifest.xml'
    return response


def metadata(ids):
    results = get_results(ids, get_attributes=True)
    mfio = _stream_with_xml(results)
    response = HttpResponse(basehttp.FileWrapper(mfio), content_type='text/xml')
    response['Content-Disposition'] = 'attachment; filename=metadata.xml'
    return response


def summary(ids):
    results = get_results(ids, get_attributes=True)
    results.add_custom_fields()
    mfio = _write_summary_tsv(results)
    response = HttpResponse(basehttp.FileWrapper(mfio), content_type='text/tsv')
    response['Content-Disposition'] = 'attachment; filename=summary.tsv'
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


def _stream_with_xml(results):
    stringio = StringIO()
    parser = etree.XMLParser()
    tree = etree.XML(results.tostring(), parser)
    stringio.write(etree.tostring(tree, pretty_print=True))
    stringio.seek(0)
    return stringio


def _write_summary_tsv(results):
    stringio = StringIO()
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

    stringio.seek(0)
    return stringio
