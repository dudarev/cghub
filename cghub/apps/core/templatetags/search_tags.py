import urllib
from django import template
from django.utils.http import urlencode


register = template.Library()


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
        data[k] = request.GET[k]
    if value:
        data[attribute] = value
    elif data.has_key(attribute):
        # in this case value is '' or False etc. and the key exists -
        # remove it
        del data[attribute]
    return request.path + u'?' + urlencode(data)


@register.simple_tag
def applied_filters(request):
    filters = {'center_name': request.GET.get('center_name'),
               'last_modified': request.GET.get('last_modified'),
               'analyte_code': request.GET.get('analyte_code'),
               'sample_type': request.GET.get('sample_type'),
               'library_strategy': request.GET.get('library_strategy'),
               'disease_abbr': request.GET.get('disease_abbr'),
               }
    filters_human = {'center_name': 'center',
               'last_modified': 'date',
               'analyte_code': 'experiment type',
               'sample_type': 'sample type',
               'library_strategy': 'run type',
               'disease_abbr': 'desease',
               }
    if any(filters.values()):
        filtered_by_str = "Filtered by "
        for f in filters:
            if filters[f]:
                filtered_by_str += "{0}: {1}, ".format(filters_human[f], filters[f])
    else:
        return 'Filtered by nothing.'
    # replace the last comma with a period.
    return filtered_by_str[:-2] + '.'


@register.simple_tag
def sort_link(request, attribute, link_anchor):
    """
    Generates a link based on request.path and `order` direction for `attribute`
    Specifies sort `direction`: '-' (DESC) or '' (ASC)
    
    """
    data = {}
    for k in request.GET:
        data[k] = request.GET[k]
    
    if data.has_key('sort_by') and attribute in data['sort_by']:
        # for current sort change NEXT possible order
        if data['sort_by'].startswith('-'):
            data['sort_by'] = data['sort_by'][1:]
            direction_label = ' DESC'
        else:
            data['sort_by'] = '-' + data['sort_by']
            direction_label = ' ASC'
    else:
        # for all other use default order (ASC)
        data['sort_by'] = attribute
        direction_label = ''
    
    href = request.path + '?' + urllib.urlencode(data)
    return '<a href="%(href)s">%(link_anchor)s%(direction_label)s</a>' % {
        'link_anchor': link_anchor,
        'direction_label': direction_label,
        'href': href}
