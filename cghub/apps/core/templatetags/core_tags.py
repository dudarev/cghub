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
    """
    Shows messages from session or from context
    """
    messages = []
    if 'request' in context:
        session = context['request'].session
        if session and 'messages' in session and session['messages']:
            messages = [
                    {'id': i, 'level': message['level'], 'content': message['content']}
                    for i, message in session['messages'].iteritems()]
            # remove messages that should be shown only once
            messages_to_remove = [i for i, message in
                    session['messages'].iteritems() if message.get('once')]
            if messages_to_remove:
                for i in messages_to_remove:
                    del session['messages'][i]
                session.save()
    if 'notifications' in context:
        for message in context['notifications']:
            messages.append(message)
    if not messages:
        return ''
    return render_to_string(
            'core/messages.html',
            {'messages': messages})
