import urllib2
import logging

from xml.sax import handler, parse

from django.conf import settings

from cghub.apps.cart.cache import is_cart_cache_exists
from cghub.apps.core.utils import is_celery_alive


wsapi_request_logger = logging.getLogger('wsapi.request')


class CartAttributesParser(handler.ContentHandler):
    """
    Parse AnalysisDetail file and save results to user's cart
    """

    def __init__(self, session_store, attributes, cache_files):
        self.session_store = session_store
        self.cache_files = cache_files
        self.celery_alive = is_celery_alive()
        self.cart = self.session_store.get('cart', {})
        self.current_element = ''
        self.current_dict = {}
        self.current_analysis_id = ''
        self.files_size = 0
        for i in attributes:
            self.current_dict[i] = ''
        handler.ContentHandler.__init__(self)

    def startElement(self, name, attrs):
        self.content = ''
        # assembly: analysis_xml/ANALYSIS_SET/ANALYSIS/ANALYSIS_TYPE/REFERENCE_ALIGNMENT/ASSEMBLY/STANDARD[short_name]
        if name == 'STANDARD' and 'short_name' in attrs:
            self.current_dict['assembly'] = attrs['short_name']
        self.current_element = name

    def endElement(self, name):
        # files_size
        # file_size: files/file/filesize
        if self.current_element == 'filesize':
            self.files_size += int(self.content)
        if self.current_element == 'analysis_id':
            self.current_analysis_id = self.content
        if self.current_element in self.current_dict:
            self.current_dict[self.current_element] = self.content
        self.current_element = ''
        if name == 'Result':
            self._save_to_cart()

    def characters(self, content):
        self.content += content

    def endDocument(self):
        self.session_store['cart'] = self.cart
        self.session_store.save()

    def _save_to_cart(self):
        # save file to cart
        self.current_dict['files_size'] = self.files_size
        # deep copy
        self.cart[self.current_analysis_id] = dict(self.current_dict)
        # cache file
        last_modified = self.current_dict['last_modified']
        # add task to cache file if not cached yet
        if self.cache_files and not is_cart_cache_exists(
                self.current_analysis_id, last_modified) and self.celery_alive:
            from cghub.apps.cart.tasks import cache_results_task
            cache_results_task.delay(self.current_analysis_id, last_modified)
        # reset current dict
        for i in self.current_dict:
            self.current_dict[i] = ''
        self.files_size = 0


def parse_cart_attributes(session_store, attributes, query=None,
                                    file_path=None, cache_files=True):
    """
    Receives analysisDetail file from cghub server for specified query and
    parses it using xml.sax. Reults saves to user session.

    :param session_store: django.contrib.sessions.backends.db.SessionStore object
    :param attributes: list of attributes should be obtained and saved to cart
    :param query: query to get analysisDetail file, should be specified query or file_path
    :param file_path: alternatively to receiving data from server, data can be got from file
    :cache_files: if True and file not exists in cart cache, it will be cached
    """
    if not query and not file_path:
        return
    if query:
        url = u'{0}{1}?{2}'.format(
                            settings.WSAPI_CGHUB_SERVER,
                            settings.WSAPI_CGHUB_ANALYSIS_DETAIL_URI,
                            query)
        wsapi_request_logger.info(urllib2.unquote(url))
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
    else:
        response = open(file_path, 'r')
    try:
        parse(response, CartAttributesParser(session_store, attributes, cache_files))
    except:
        session_store.save()
