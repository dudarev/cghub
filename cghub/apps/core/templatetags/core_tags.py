from django import template


register = template.Library()


@register.filter
def file_size(value):
    """
    Transform number of bytes to value in KB, MB or GB
    123456 -> 123.46 KB
    """
    try:
        bytes = int(value)
    except ValueError:
        return ''
    if bytes >= 1000000000:
        return '%.2f GB' % round(bytes / 1000000000., 2)
    if bytes >= 1000000:
        return '%.2f MB' % round(bytes / 1000000., 2)
    if bytes >= 1000:
        return '%.2f KB' % round(bytes / 1000., 2)
    return '%d Bytes' % bytes
     
