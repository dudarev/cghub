from django import template


register = template.Library()


@register.filter
def without_header(value):
    """
    Remove xml header like this:
    <?xml version="1.0" encoding="ASCII" standalone="yes"?>
    """
    if value is None:
        return u''
    if value.find('<?') == 0:
        start = value.find('?>')
        if start != -1:
            return value[start + 2:]
    return value
