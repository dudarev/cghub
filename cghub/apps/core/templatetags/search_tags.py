import urllib
import datetime

from django import template
from django.utils.http import urlencode
from django.utils.html import escape
from django.utils import timezone
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import Context
from django.template.loader import select_template

from cghub.apps.core.filters_storage import ALL_FILTERS, DATE_FILTERS_HTML_IDS
from cghub.apps.core.attributes import (
                COLUMN_NAMES, DATE_ATTRIBUTES, SORT_BY_ATTRIBUTES,
                CART_SORT_ATTRIBUTES)


register = template.Library()


DEFAULT_CULUMN_STYLE = {
        'width': 100,
        'align': 'left',
        'default_state': 'visible'
}


def period_from_query(query):
    """
    examples:
    '[NOW-2DAY TO NOW]' -> '2013/02/25 - 2013/02/27'
    '[NOW-5DAY TO NOW-2]' -> '2013/02/22 - 2013/02/25'
    """
    query = urllib.unquote(query)
    try:
        start, stop = query[1:-1].split(' TO ')
        for c in ('NOW', 'DAY', '-',):
            start = start.replace(c, '')
            stop = stop.replace(c, '')
        start = timezone.now() - datetime.timedelta(int(start))
        start = datetime.datetime.strftime(start, '%Y/%m/%d')
        if not stop:
            stop = timezone.now()
        else:
            stop = timezone.now() - datetime.timedelta(int(stop))
        stop = datetime.datetime.strftime(stop, '%Y/%m/%d')
        period = '%s - %s' % (start, stop)
    except ValueError:
        return ''
    return period


@register.filter
def file_size(value):
    """
    Transform number of bytes to value in KB, MB or GB
    123456 -> 123,46 KB
    """
    try:
        bytes = int(value)
    except ValueError:
        return ''
    if bytes >= 1073741824:
        return ('%.2f GB' % round(bytes / 1073741824., 2))
    if bytes >= 1048576:
        return ('%.2f MB' % round(bytes / 1048576., 2))
    if bytes >= 1024:
        return ('%.2f KB' % round(bytes / 1024., 2))
    return '%d Bytes' % bytes


@register.filter
def only_date(value):
    """
    Extracts date string from datetime string.
    """
    return unicode(value).split('T')[0]


@register.simple_tag
def get_name_by_code(filter_section, code):
    """
    If name for such code does not exist return the code.
    """
    try:
        if filter_section == "sample_type":
            raise Exception('Use get_sample_type_by_code tag for sample types.')
        else:
            return ALL_FILTERS[filter_section]['filters'][code]
    except KeyError:
        return code


@register.simple_tag
def get_sample_type_by_code(code, format):
    code = str(code)
    if len(code) == 1:
        code = '0' + code

    try:
        if format == 'full':
            return ALL_FILTERS['sample_type']['filters'][code]
        elif format == 'shortcut':
            return ALL_FILTERS['sample_type']['shortcuts'][code]
        else:
            raise Exception('Unknown format for sample type.')
    except KeyError:
        return code


@register.simple_tag
def render_filters():
    t = select_template(['filters.html', ])
    content = t.render(Context({
        'all_filters': ALL_FILTERS,
        'date_ids': DATE_FILTERS_HTML_IDS,
    }))
    return content


@register.simple_tag
def filter_link(request, attribute, value):
    """
    Generates a link based on request.path and `value` for `attribute`.
    If this attribute did not exist it is specified.
    If this attribute was specified before, it is replaced with a new value.
    If the value is empty - remove the link.
    Other attributes are preserved.
    """
    data = {}
    for k in request.GET:
        if k not in ('offset',):
            data[k] = request.GET[k]
    if value:
        data[attribute] = value
    elif attribute in data:
        # in this case value is '' or False etc. and the key exists -
        # remove it
        del data[attribute]
    return request.path + u'?' + urlencode(data)


def remove_dashes(value):
    if not value:
        return ''
    while value.find('-') == 0:
        value = value[1:]
    return value


@register.simple_tag
def applied_filters(request):
    applied_filters = {
        'study': request.GET.get('study'),
        'center_name': request.GET.get('center_name'),
        'upload_date': request.GET.get('upload_date'),
        'last_modified': request.GET.get('last_modified'),
        'analyte_code': request.GET.get('analyte_code'),
        'sample_type': request.GET.get('sample_type'),
        'library_strategy': request.GET.get('library_strategy'),
        'disease_abbr': request.GET.get('disease_abbr'),
        'platform': request.GET.get('platform'),
        'state': request.GET.get('state'),
        'refassem_short_name': request.GET.get('refassem_short_name'),
        'q': request.GET.get('q'),
    }

    if not any(applied_filters.values()):
        return 'No applied filters'

    filtered_by_str = 'Applied filter(s): <ul>'

    # query is mentioned first
    if applied_filters.get('q', None):
        # Text query from search input
        filtered_by_str += '<li data-name="q" data-filters="' + applied_filters['q'] + \
                    '"><b>Text query</b>: "' + applied_filters['q'] + '"</li>'

    for f in applied_filters:
        if not applied_filters[f]:
            continue

        filters = applied_filters[f]

        if f == 'q':
            continue

        # Date filters differ from other filters, they should be parsed differently
        if f in ('last_modified', 'upload_date',):
            applied_filter = ALL_FILTERS[f]['filters'].get(filters)
            if applied_filter:
                filter_name = applied_filter['filter_name']
            else:
                filter_name = period_from_query(filters)
            if f == 'last_modified':
                filtered_by_str += '<li data-name="' + f + '" data-filters="' + \
                                        filters + '"><b>Modified</b>: '
            else:
                filtered_by_str += '<li data-name="' + f + '" data-filters="' + \
                                        filters + '"><b>Uploaded</b>: '
            filtered_by_str += filter_name.lower() + '</li>'
            continue

        # Parsing other applied filters, e.g. u'(SARC OR STAD)'
        title = ALL_FILTERS[f]['title'][3:]
        filters = filters[1:-1].split(' OR ')
        filters_str = ''

        # Filters by assembly can use complex queries
        if f == 'refassem_short_name':
            for value in ALL_FILTERS[f]['filters']:
                options = value.split(' OR ')
                for option in options:
                    if option not in filters:
                        break
                else:
                    filters_str += ', <span>%s</span>' % (
                            remove_dashes(ALL_FILTERS[f]['filters'].get(value)))
            filtered_by_str += '<li data-name="' + f + '" data-filters="' + \
                    '&amp;'.join(filters) + '"><b>%s</b>: %s</li>' % (
                                                title, filters_str[2:])
            continue

        for value in filters:
            # do not put abbreviation in parenthesis if it is the same
            # or if the filter type is state
            if ALL_FILTERS[f]['filters'].get(value) == value or f == 'state':
                filters_str += ', <span>%s </span>' % (
                        remove_dashes(ALL_FILTERS[f]['filters'].get(value)))
            else:
                filters_str += ', <span>%s (%s)</span>' % (
                        remove_dashes(ALL_FILTERS[f]['filters'].get(value)),
                        value)
        filtered_by_str += '<li data-name="' + f + '" data-filters="' + \
                    '&amp;'.join(filters) + '"><b>%s</b>: %s</li>' % (
                                                title, filters_str[2:])

    filtered_by_str += '</ul>'
    return filtered_by_str


@register.simple_tag
def sort_link(request, attribute, link_anchor):
    """
    Generates a link based on request.path and `order` direction for `attribute`
    Specifies sort `direction`: '-' (DESC) or '' (ASC)
    """
    if request.path == reverse('cart_page'):
        # allow sorting in cart only by CART_SORT_ATTRIBUTES
        if attribute not in CART_SORT_ATTRIBUTES:
            return ('<a href="#" onclick="return false;">%s</a>' % link_anchor)
    elif request.path == reverse('batch_search_page'):
        # disable sorting on batch search results page
        return ('<a href="#" onclick="return false;">%s</a>' % link_anchor)
    elif attribute not in SORT_BY_ATTRIBUTES:
        # allow sorting on search page only by SORT_BY_ATTRIBUTES
        return ('<a href="#" onclick="return false;">%s</a>' % link_anchor)

    data = {}
    for k in request.GET:
        if k not in ('offset',):
            data[k] = request.GET[k]
    if 'sort_by' in data and attribute in data['sort_by']:
        # for current sort change NEXT possible order
        if data['sort_by'].startswith('-'):
            data['sort_by'] = data['sort_by'][1:]
            direction_label = 'up'
        else:
            data['sort_by'] = '-' + data['sort_by']
            direction_label = 'down'
    else:
        # for all other use default order (ASC)
        data['sort_by'] = attribute
        direction_label = ''

    sorting_arrow = direction_label
    if direction_label:
        triangle = '<span class="{0}-triangle"></span>'
        if direction_label == 'up':
            sorting_arrow = triangle.format('up')
        if direction_label == 'down':
            sorting_arrow = triangle.format('down')

    path = request.path or reverse('search_page')
    href = escape(path + '?' + urllib.urlencode(data))
    return ('<a class="sort-link" href="%(href)s" '
        'title="click to sort by %(link_anchor)s">%(link_anchor)s%(sorting_arrow)s</a>' % {
        'link_anchor': link_anchor,
        'sorting_arrow': sorting_arrow,
        'href': href})


@register.simple_tag
def table_header(request):
    """
    Return table header ordered according to settings.TABLE_COLUMNS
    """
    html = ''
    for field_name in settings.TABLE_COLUMNS:
        col_name = COLUMN_NAMES.get(field_name, None)
        if col_name is None:
            continue
        col_style = settings.COLUMN_STYLES.get(field_name, DEFAULT_CULUMN_STYLE)
        html += '<th data-width="{width}" data-ds="{defaultstate}" id="id-col-{col_name}">{link}</th>'.format(
                    width=col_style['width'],
                    defaultstate=col_style['default_state'],
                    col_name=col_name,
                    link=sort_link(request, col_name, field_name))
    return html


def get_result_attr(result, attr):
    try:
        if attr in DATE_ATTRIBUTES:
            return only_date(result[attr])
        return result[attr] or ' '
    except KeyError:
        pass
    return ' '


def field_values(result, humanize_files_size=True):
    files_size = get_result_attr(result, 'files_size')
    if humanize_files_size:
        files_size = file_size(files_size)
    return {
        'Assembly': get_result_attr(result, 'refassem_short_name'),
        'Barcode': get_result_attr(result, 'legacy_sample_id'),
        'Center': get_result_attr(result, 'center_name'),
        'Center Name': get_name_by_code(
            'center_name',
            get_result_attr(result, 'center_name')),
        'Checksum': get_result_attr(result, 'checksum'),
        'Disease': get_result_attr(result, 'disease_abbr'),
        'Disease Name': get_name_by_code(
            'disease_abbr',
            get_result_attr(result, 'disease_abbr')),
        'Experiment Type': get_name_by_code(
            'analyte_code',
            get_result_attr(result, 'analyte_code')),
        'Filename': get_result_attr(result, 'filename'),
        'Files Size': files_size,
        'Modified': get_result_attr(result, 'last_modified'),
        'Library Type': get_result_attr(result, 'library_strategy'),
        'Platform': get_result_attr(result, 'platform'),
        'Platform Name': get_name_by_code(
            'platform',
            get_result_attr(result, 'platform')),
        'Reason': get_result_attr(result, 'reason'),
        'Sample Accession': get_result_attr(result, 'sample_accession'),
        'Sample Type': get_sample_type_by_code(
            get_result_attr(result, 'sample_type'),
            format='shortcut'),
        'Sample Type Name': get_sample_type_by_code(
            get_result_attr(result, 'sample_type'),
            format='full'),
        'State': get_name_by_code(
            'state', get_result_attr(result, 'state')),
        'Study': get_name_by_code(
            'study', get_result_attr(result, 'study')),
        'Uploaded': get_result_attr(result, 'upload_date'),
        'Analysis Id': get_result_attr(result, 'analysis_id'),

        # additional fields for details
        'Aliquot id': get_result_attr(result, 'aliquot_id'),
        'Disease abbr': get_result_attr(result, 'disease_abbr'),
        'Published time': get_result_attr(result, 'published_date'),
        'Participant id': get_result_attr(result, 'participant_id'),
        'Sample id': get_result_attr(result, 'sample_id'),
        'TSS id': get_result_attr(result, 'tss_id'),
    }


@register.simple_tag
def table_row(result):
    """
    Return table row ordered according to settings.TABLE_COLUMNS
    """
    fields = field_values(result)
    html = ''
    for field_name in settings.TABLE_COLUMNS:
        value = fields.get(field_name, None)
        col_name = COLUMN_NAMES.get(field_name, None)
        if field_name in settings.VALUE_RESOLVERS:
            value = settings.VALUE_RESOLVERS[field_name](value)
        if value is None:
            continue
        col_style = settings.COLUMN_STYLES.get(field_name, DEFAULT_CULUMN_STYLE)
        html += '<td style="text-align: {align}" headers="id-col-{col_name}">{value}</td>'.format(
                    align=col_style['align'],
                    col_name=col_name,
                    value=value)
    return html


@register.simple_tag
def details_table(result):
    """
    Return table with details
    """
    fields = field_values(result)
    html = ''
    for field_name in settings.DETAILS_FIELDS:
        value = fields.get(field_name, None)
        col_name = COLUMN_NAMES.get(field_name, None)
        if field_name in settings.VALUE_RESOLVERS:
            value = settings.VALUE_RESOLVERS[field_name](value)
        if value is None:
            continue
        if field_name == 'Reason' and value.isspace():
            continue
        html += ('<tr><th id="id-row-{col_name}">{field_name}</th>'
                 '<td headers="id-row-{col_name}">{value}</td></tr>'.format(
                    col_name=col_name, field_name=field_name, value=value))
    return html
