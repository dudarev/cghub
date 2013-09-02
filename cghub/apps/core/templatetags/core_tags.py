from django import template
from django.template.loader import render_to_string


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


@register.simple_tag(takes_context=True)
def messages(context):
    if 'request' not in context:
        return ''
    session = context['request'].session
    if not session or 'messages' not in session or not session['messages']:
        return u''
    messages = session['messages']
    messages = [
            {'id': i, 'level': message['level'], 'content': message['content']}
            for i, message in session['messages'].iteritems()]
    return render_to_string(
            'core/messages.html',
            {'messages': messages})
