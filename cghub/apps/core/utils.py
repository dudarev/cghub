import os
import threading
import socket
import csv
import codecs
import errno

from gzip import GzipFile
from cStringIO import StringIO

from django.conf import settings

from .filters_storage import Filters


def get_filters_dict(filters):
    """
    Removes illegal filters from dict.
    """
    filters_dict = {}
    for attr in Filters.ALL_FILTERS.keys():
        if filters.get(attr):
            filters_dict[attr] = filters[attr]
    return filters_dict


def query_dict_to_str(query):
    """
    Transform query dict to string.
    Example:
    query_dict_to_str({'analysis_id': ['123', '345']})
    ->
    'analysis_id=(123 OR 345)'
    """
    parts = []
    for key, value in query.iteritems():
        if isinstance(value, list) or isinstance(value, tuple):
            value_str = ' OR '.join([v for v in value])
            value_str = '(%s)' % value_str.replace('+', ' ')
        else:
            value_str = str(value).replace('+', ' ')
        parts.append('='.join([key, value_str]))
    return '&'.join(parts)


def paginator_params(request):
    """
    Returns offset, limit.
    :param request: django Request object
    """
    offset = request.GET.get('offset')
    offset = offset and offset.isdigit() and int(offset) or 0
    limit = request.GET.get('limit')
    if limit and limit.isdigit():
        limit = int(limit) or settings.DEFAULT_PAGINATOR_LIMIT
    elif settings.PAGINATOR_LIMIT_COOKIE in request.COOKIES:
        limit = str(request.COOKIES[settings.PAGINATOR_LIMIT_COOKIE])
        limit = limit.isdigit() and int(limit) or settings.DEFAULT_PAGINATOR_LIMIT
    else:
        limit = settings.DEFAULT_PAGINATOR_LIMIT
    return offset, limit


def add_message(request, level, content):
    """
    Adds message to messages pool stored in session.
    :request: Request object
    :level: error, success or info
    :content: message content
    """
    messages = request.session.get('messages', {})
    if not messages:
        message_id = 1
    else:
        message_id = sorted(messages.keys())[-1] + 1
    messages[message_id] = {'level': level, 'content': content}
    request.session['messages'] = messages
    request.session.modified = True


def makedirs_group_write(path):
    "create a directory, including missing parents, ensuring it has group write permissions"
    old_mask = os.umask(0002)
    try:
        try: 
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e
    finally:
        os.umask(old_mask)


def generate_tmp_file_name():
    """
    Returns filename in next format:
    pid-threadId-host.tmp
    """
    return '{pid}-{thread}-{host}.tmp'.format(
                    pid=os.getpid(), thread=threading.current_thread().name,
                    host=socket.gethostname())


class CSVUnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


class Gzipper(object):
    """
    Text stream compressor.
    """

    def __init__(self, filename=None, compress=False):
        self.compress = compress
        if not self.compress:
            self.buffer = ''
        else:
            self.io = StringIO()
            self.zipfile = GzipFile(filename, mode='wb', fileobj=self.io)

    def read(self):
        if not self.compress:
            result = self.buffer
            self.buffer = ''
            return result
        self.zipfile.flush()
        self.io.seek(0)
        line = self.io.read()
        self.io.seek(0)
        self.io.truncate()
        return line

    def write(self, l):
        if not self.compress:
            self.buffer += l
        else:
            self.zipfile.write(l)

    def close(self):
        if not self.compress:
            return self.buffer
        self.zipfile.close()
        self.io.seek(0)
        return self.io.read()
