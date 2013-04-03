import urllib2

from xml.sax import handler, parse


# + 'assembly': ['analysis_xml', 'ANALYSIS_SET', 'ANALYSIS', 'ANALYSIS_TYPE', 'REFERENCE_ALIGNMENT', 'ASSEMBLY', 'STANDARD', 'short_name'],

class CartAttributesParser(handler.ContentHandler):

    def __init__(self, session_store, attributes):
        self.session_store = session_store
        self.cart = self.session_store.get('cart', {})
        self.current_element = ''
        self.current_dict = {}
        for i in attributes:
            self.current_dict[i] = ''
        self.current_analysis_id = ''
        handler.ContentHandler.__init__(self)

    def startElement(self, name, attrs):
        self.current_element = name

    def endElement(self, name):
        self.current_element = ''

    def characters(self, content):
        if self.current_element == 'analysis_id':
            # save file to cart
            self.cart[self.current_analysis_id] = self.current_dict
            # reset current dict
            for i in self.current_dict:
                self.current_dict[i] = ''
            self.current_analysis_id = content
        if self.current_element in self.current_dict:
            self.current_dict[self.current_element] = content

    def endDocument(self):
        self.session_store['cart'] = self.cart
        self.session_store.save()


def parse_cart_attributes(session_store, attributes, url=None, file_path=None):
    if not url and not file_path:
        return
    if url:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
    else:
        response = open(file_path, 'r')
    parse(response, CartAttributesParser(session_store, attributes))
