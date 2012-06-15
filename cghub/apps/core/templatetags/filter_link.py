import urllib
from django import template


register = template.Library()


@register.simple_tag
def filter_link(request, attribute, value):
    """
    Generates a link based on request.path and `value` for `attribute`.
    If this attribute did not existed it is specified.
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
    return request.path + '?' + urllib.urlencode(data)
