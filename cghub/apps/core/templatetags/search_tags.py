import urllib
from django import template
from django.utils.http import urlencode
from django.utils.html import escape
from django.template import Context
from django.template.loader import select_template

from cghub.apps.core.filters_storage import ALL_FILTERS, DATE_FILTERS_HTML_IDS

register = template.Library()


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
        'date_ids': DATE_FILTERS_HTML_IDS
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


@register.simple_tag
def applied_filters(request):
    applied_filters = {
        'center_name': request.GET.get('center_name'),
        'last_modified': request.GET.get('last_modified'),
        'analyte_code': request.GET.get('analyte_code'),
        'sample_type': request.GET.get('sample_type'),
        'library_strategy': request.GET.get('library_strategy'),
        'disease_abbr': request.GET.get('disease_abbr'),
        'q': request.GET.get('q'),
    }

    if not any(applied_filters.values()):
        return 'No applied filters'

    filtered_by_str = 'Applied filter(s): <ul>'

    # query is mentioned first
    if applied_filters.get('q', None):
        # Text query from search input
        filtered_by_str += '<li>Text query: "' + applied_filters['q'] + '"</li>'

    for f in applied_filters:
        if not applied_filters[f]:
            continue

        filters = applied_filters[f]

        if f == 'q':
            continue

        # Date filters differ from other filters, they should be parsed differently
        if f == 'last_modified':
            filtered_by_str += '<li id="time-filter-applied" data="' + filters + '">Uploaded '
            filtered_by_str += ALL_FILTERS[f]['filters'][filters]['filter_name'].lower() + '</li>'
            continue

        # Parsing other applied filters, e.g. u'(SARC OR STAD)'
        title = ALL_FILTERS[f]['title'][3:]
        filters = filters[1:-1].split(' OR ')
        filters_str = ''
        for value in filters:
            # do not put abbreviation in parenthesis if it is the same
            if ALL_FILTERS[f]['filters'][value] == value:
                filters_str += ', %s' % (value)
            else:
                filters_str += ', %s (%s)' % (ALL_FILTERS[f]['filters'][value], value)

        filtered_by_str += '<li>%s: %s</li>' % (title, filters_str[2:])

    filtered_by_str += '</ul>'
    return filtered_by_str


@register.simple_tag
def sort_link(request, attribute, link_anchor):
    """
    Generates a link based on request.path and `order` direction for `attribute`
    Specifies sort `direction`: '-' (DESC) or '' (ASC)
    
    """
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

    if direction_label:
        if direction_label == 'up':
            sorting_arrow = "&nbsp;&uarr;"
        if direction_label == 'down':
            sorting_arrow = "&nbsp;&darr;"
    else:
        sorting_arrow = direction_label
    
    path = request.path or '/search/'
    href = escape(path + '?' + urllib.urlencode(data))
    return '<a class="sort-link" href="%(href)s">%(link_anchor)s%(sorting_arrow)s</a>' % {
        'link_anchor': link_anchor,
        'sorting_arrow': sorting_arrow,
        'href': href}
