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
    if bytes >= 1073741824:
        return '%.2f GB' % round(bytes / 1073741824., 2)
    if bytes >= 1048576:
        return '%.2f MB' % round(bytes / 1048576., 2)
    if bytes >= 1024:
        return '%.2f KB' % round(bytes / 1024., 2)
    return '%d Bytes' % bytes
     
