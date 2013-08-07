import urllib2

from xml.dom import pulldom
from xml.etree import ElementTree

from .utils import urlopen


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

    To access to deeper elements like filename:
    <files>
        <file>
            <filename>somefilename.txt</filename>
    can be used next syntax:
    print result['files.file.filename']
    If files node has few file nodes, can be used indexes:
    print result['files.file.0.filename']

    If requested node was not found, will be returned NonExistent object.
    To check is requested node exists can be used 'exist' attribute.
    result.files.exist == True
    result.badattr.exist == False
    """

    def __init__(self, tree):
        """
        :param tree: ElementTree object
        """
        self.tree = tree

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        if attr in self.tree.__dict__:
            return getattr(self.tree, attr)
        node = self.tree.find(attr)
        if node is None:
            return NonExistent()
        node.exist = True
        return node

    def __getitem__(self, path):
        path = path.split('.')
        nodes = [self.tree]
        for attr in path:
            if attr.isdigit():
                if len(nodes) <= int(attr):
                    return NonExistent()
                nodes = [nodes[int(attr)]]
                continue
            nodes = nodes[0].findall(attr)
            if not len(nodes):
                return NonExistent()
        nodes[0].exist = True
        return nodes[0]


class Request(object):
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

    def __init__(self,
                query, offset=0, limit=None, sort_by=None,
                server_url=CGHUB_SERVER, uri=CGHUB_ANALYSIS_DETAIL_URI):
        """
        :param query: a dict with query to send to the server
        :param offset: how many results should be skipped
        :param limit: how many records output should have
        :param sort_by: the attribute by which the results should be sorted (use '-' for reverse)
        :param server_url: server url where WSAPI works
        :param uri: uri that will be used to access data on WSAPI server
        """
        self.query = query
        self.server_url = server_url
        self.uri = uri
        self.offset = offset
        self.limit = limit
        self.sort_by = sort_by

    def get_xml_file(self, url):
        """
        Can be overridden for testing purposes
        """
        return urlopen(url)

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
        self.patch_input_data()
        query = self.build_query()
        url = '%s%s' % (self.server_url, self.uri)
        if query:
            url = '%s?%s' % (url, query)
        xml = self.get_xml_file(url)
        # http://docs.python.org/dev/library/xml.dom.pulldom.html
        doc = pulldom.parse(xml)
        for event, node in doc:
            if event == pulldom.START_ELEMENT:
                if node.tagName == 'Result':
                    doc.expandNode(node)
                    # convert to python object
                    # http://docs.python.org/2/library/xml.etree.elementtree.html
                    result_xml = node.toxml()
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
                value_str = ' OR '.join([
                        urllib2.unquote(v) for v in value])
                value_str = urllib2.quote(('(%s)' % value_str)
                            .replace('+', ' ').replace('\-', '-'))
            else:
                value_str = urllib2.quote(
                        urllib2.unquote(str(value))
                            .replace('+', ' ').replace('\-', '-'))
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
