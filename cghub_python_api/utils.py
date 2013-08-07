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
    for i in range(max_attempts):
        try:
            req = urllib2.Request(url, headers={'Accept': format})
            return urllib2.urlopen(req)
        except urllib2.URLError:
            time.sleep(sleep_time)
    raise urllib2.URLError(
            'No response after %d attempts: %s' % (max_attempts, url))
