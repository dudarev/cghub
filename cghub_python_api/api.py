import urllib2
import ijson

from xml.dom import pulldom
from xml.etree import ElementTree

from .utils import urlopen


DATE_ATTRIBUTES = ('last_modified', 'upload_date', 'published_date',)


class NonExistent(object):
    """
    Object returns None for not existent attributes
    instead of rising AttributeError.
    """

    exist = False

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        return None


class Result(object):
    """
    Wrapper for ElementTree object.
    Allows to access to tree nodes using attributes.

    Usage example:
    result = Result(tree)
    print result.analysis_id
    print result['analysis_id']
    print result['filename.0']
    print result['filename.1']

    If requested node was not found, will be returned NonExistent object.
    To check is requested node exists can be used 'exist' attribute.
    result.files.exist == True
    result.badattr.exist == False
    """

    API_SOLR = 'sorl'
    API_WSAPI = 'wsapi'

    def __init__(self, tree):
        """
        :param tree: ElementTree object
        """
        self.tree = tree
        if self.tree.find('analysis_id') is None:
            self.api = self.API_SOLR
        else:
            self.api = self.API_WSAPI

    def get_node(self, attr, index):
        if self.api == self.API_WSAPI:
            nodes = self.tree.findall('.//%s' % attr)
        else:
            nodes = self.tree.findall(".//*[@name='%s']" % attr)
            # open arrays
            if len(nodes) == 1 and nodes[0].tag == 'arr':
                nodes = nodes[0].findall('.//*')
        if len(nodes) < index + 1:
            return NonExistent()
        nodes[index].exist = True
        return nodes[index]

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        return self.get_node(attr, 0)

    def __getitem__(self, path):
        if '.' in path:
            try:
                attr, index = path.split('.')
                index = int(index)
            except ValueError:
                return NonExistent()
        else:
            attr = path
            index = 0
        return self.get_node(attr, index)


class BaseRequest(object):
    """
    CGHub API base class
    """

    FORMAT_XML = 'xml'
    FORMAT_JSON = 'json'

    def __init__(self,
            query, offset=0, limit=None, sort_by=None,
            server_url=None, uri=None, fields=None, format=FORMAT_XML):
        """
        :param query: a dict with query to send to the server
        :param offset: how many results should be skipped
        :param limit: how many records output should have
        :param sort_by: the attribute by which the results should be sorted (use '-' for reverse)
        :param server_url: server url where API works
        :param uri: uri that will be used to access data on API server
        :param fields: list of fields will be returned in result (used only in SOLRRequest)
        :param format: format of requested data ('xml' or 'json')
        """
        self.query = query
        self.server_url = server_url
        self.uri = uri
        self.offset = offset
        self.limit = limit
        self.sort_by = sort_by
        self.fields = fields
        self.format = format

    def get_source_file(self, url):
        """
        Can be overridden for testing purposes
        """
        return urlopen(url, format=self.format)

    def patch_input_data(self):
        """
        Here can be changed self.server_url, self.uri and other input data
        """
        pass

    def patch_result(self, result, result_xml):
        """
        Can be overriden to add custom fields to results, etc.
        """
        return result

    def call(self):
        """
        Makes a request to cghub server.
        Returns generator that returns Result objects.
        """
        raise NotImplementedError()

    def escape_query_value(self, key, value):
        val = urllib2.unquote(str(value)).replace('\-', '-')
        if key not in DATE_ATTRIBUTES:
            val = val.replace(' ', '+').replace('+OR+', ' OR ')
        return urllib2.quote(val)

    def build_query(self):
        """
        Builds query to access to cghub server.
        """
        raise NotImplementedError()


class WSAPIRequest(BaseRequest):
    """
    Allow to access to cghub data by query.

    Usage example:
    request = Request(query={
            'analysis_id': '017a4d4e-9f4b-4904-824e-060fde3ca223'})
    for result in request.call():
        print result.state
    """

    CGHUB_SERVER = 'https://192.35.223.223'
    CGHUB_ANALYSIS_ID_URI = '/cghub/metadata/analysisId'
    CGHUB_ANALYSIS_DETAIL_URI = '/cghub/metadata/analysisDetail'
    CGHUB_ANALYSIS_FULL_URI = '/cghub/metadata/analysisFull'
    FORMAT_XML = 'xml'
    FORMAT_JSON = 'json'

    def __init__(self,
                query, offset=0, limit=None, sort_by=None,
                server_url=CGHUB_SERVER, uri=CGHUB_ANALYSIS_DETAIL_URI,
                fields=None, format=FORMAT_XML):
        """
        :param query: a dict with query to send to the server
        :param offset: how many results should be skipped
        :param limit: how many records output should have
        :param sort_by: the attribute by which the results should be sorted (use '-' for reverse)
        :param server_url: server url where WSAPI works
        :param uri: uri that will be used to access data on WSAPI server
        :param fields: list of fields will be returned in result (used only in SOLRRequest)
        :param format: format of requested data from wsapi server ('xml' or 'json')
        """
        self.query = query
        self.server_url = server_url
        self.uri = uri
        self.offset = offset
        self.limit = limit
        self.sort_by = sort_by
        self.format = format

    def call(self):
        """
        Makes a request to cghub server.
        Returns generator that returns Result objects.
        """
        self.patch_input_data()
        query = self.build_query()
        url = '%s%s' % (self.server_url, self.uri)
        if query:
            url = '%s?%s' % (url, query)
        xml = self.get_source_file(url)
        if self.format == self.FORMAT_JSON:
            results = ijson.items(xml, 'result_set.results.item')
            for result in results:
                yield self.patch_result(result, None)
        else:
            # http://docs.python.org/dev/library/xml.dom.pulldom.html
            doc = pulldom.parse(xml)
            for event, node in doc:
                if event == pulldom.START_ELEMENT:
                    if node.tagName == 'Result':
                        doc.expandNode(node)
                        # convert to python object
                        # http://docs.python.org/2/library/xml.etree.elementtree.html
                        result_xml = node.toxml(encoding='utf-8')
                        tree = ElementTree.fromstring(result_xml)
                        result = Result(tree)
                        yield self.patch_result(result, result_xml)
                    elif node.tagName == 'Hits':
                        doc.expandNode(node)
                        tree = ElementTree.fromstring(node.toxml())
                        self.hits = int(tree.text)

    def build_query(self):
        """
        Builds query to access to cghub server.
        """
        parts = []
        for key, value in self.query.iteritems():
            if isinstance(value, list) or isinstance(value, tuple):
                value_str = '+OR+'.join([
                        self.escape_query_value(key, v) for v in value])
                value_str = '(%s)' % value_str
            else:
                value_str = self.escape_query_value(key, value)
            parts.append('='.join([key, value_str]))
        if self.offset:
            parts.append('='.join(['start', str(self.offset)]))
        if self.limit:
            parts.append('='.join(['rows', str(self.limit)]))
        if self.sort_by:
            if self.sort_by[0] == '-':
                parts.append('='.join([
                        'sort_by',
                        '%s:desc' % urllib2.quote(self.sort_by[1:])]))
            else:
                parts.append('='.join([
                        'sort_by',
                        '%s:asc' % urllib2.quote(self.sort_by)]))
        return '&'.join(parts)


class SOLRRequest(BaseRequest):
    """
    Allow to access to cghub data by query.

    Usage example:
    request = Request(query={
            'analysis_id': '017a4d4e-9f4b-4904-824e-060fde3ca223'})
    for result in request.call():
        print result.state
    """

    CGHUB_SERVER = 'http://127.0.0.1:8983'
    CGHUB_SEARCH_URI = '/solr/select/'
    FORMAT_XML = 'xml'
    FORMAT_JSON = 'json'

    def __init__(self,
                query, offset=0, limit=None, sort_by=None,
                server_url=CGHUB_SERVER, uri=CGHUB_SEARCH_URI,
                fields=None, format=FORMAT_XML):
        """
        :param query: a dict with query to send to the server
        :param offset: how many results should be skipped
        :param limit: how many records output should have
        :param sort_by: the attribute by which the results should be sorted (use '-' for reverse)
        :param server_url: server url where WSAPI works
        :param uri: uri that will be used to access data on WSAP
        :param format: format of requested data from solr server ('xml' or 'json')
        """
        self.query = query
        self.server_url = server_url
        self.uri = uri
        self.offset = offset
        self.limit = limit
        self.sort_by = sort_by
        self.fields = fields
        self.format = format

    def call(self):
        """
        Makes a request to cghub server.
        Returns generator that returns Result objects.
        """
        self.patch_input_data()
        query = self.build_query()
        url = '%s%s' % (self.server_url, self.uri)
        if query:
            url = '%s?%s' % (url, query)
        xml = self.get_source_file(url)
        if self.format == self.FORMAT_JSON:
            results = ijson.items(xml, 'response.docs.item')
            for result in results:
                yield self.patch_result(result, None)
        else:
            # http://docs.python.org/dev/library/xml.dom.pulldom.html
            doc = pulldom.parse(xml)
            for event, node in doc:
                if event == pulldom.START_ELEMENT:
                    if node.tagName == 'doc':
                        doc.expandNode(node)
                        # convert to python object
                        # http://docs.python.org/2/library/xml.etree.elementtree.html
                        result_xml = node.toxml(encoding='utf-8')
                        tree = ElementTree.fromstring(result_xml)
                        result = Result(tree)
                        yield self.patch_result(result, result_xml)
                    elif node.tagName == 'result':
                        self.hits = int(node.getAttribute('numFound'))

    def build_query(self):
        """
        Builds query to access to cghub server.
        """
        parts = []
        for key, value in self.query.iteritems():
            if isinstance(value, list) or isinstance(value, tuple):
                value_str = '+OR+'.join([
                        self.escape_query_value(key, v) for v in value])
                value_str = '(%s)' % value_str
            else:
                value_str = self.escape_query_value(key, value)
            parts.append(urllib2.quote(':').join([key, value_str]))
        if len(parts):
            parts = ['q=%s' % '+'.join(parts)]
        else:
            parts = ['q=*%s*' % urllib2.quote(':')]
        if self.offset:
            parts.append('='.join(['start', str(self.offset)]))
        if self.limit:
            parts.append('='.join(['rows', str(self.limit)]))
        else:
            parts.append('rows=1000000')
        if self.sort_by:
            if self.sort_by[0] == '-':
                parts.append('='.join([
                        'sort',
                        '%s+desc' % urllib2.quote(self.sort_by[1:])]))
            else:
                parts.append('='.join([
                        'sort',
                        '%s+asc' % urllib2.quote(self.sort_by)]))
        if self.fields:
            parts.append('='.join([
                        'fl',
                        ','.join(
                            [urllib2.quote(f) for f in self.fields])]))
        if self.format == self.FORMAT_JSON:
            parts.append('wt=json')
        return '&'.join(parts)
