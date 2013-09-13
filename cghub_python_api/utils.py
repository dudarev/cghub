import time

import urllib2


def urlopen(url, format='xml', max_attempts=5, sleep_time=1):
    """
    Wrapper for urllib2.urlopen.
    Retry getting answer from server if URLError raised (limited number of attempts).

    :param url: url
    :param format: 'xml' or 'json'
    :param max_attempts: maximum count of attempts to retrieve answer after URLError raised
    :param sleep_time: time between attempts, seconds
    """

    FORMAT_CHOICES = {
        'xml': 'text/xml',
        'json': 'application/json',
    }

    error_msg = ''
    for i in range(max_attempts):
        try:
            req = urllib2.Request(url, headers={
                    'Accept':  FORMAT_CHOICES.get(format, FORMAT_CHOICES['xml'])})
            return urllib2.urlopen(req)
        except urllib2.URLError as e:
            try:
                if e.getcode() == 400:
                    raise urllib2.URLError(u'%s: %s' % (e.msg, url))
                error_msg = e.msg
            except AttributeError:
                pass
            time.sleep(sleep_time)
    if error_msg:
        error_msg = ' (%s)' % error_msg
    raise urllib2.URLError(
            u'No response after %d attempts: %s%s' % (
                    max_attempts, url, error_msg))
