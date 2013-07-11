# -*- coding: utf-8 -*-
"""
wsapi.parsers
~~~~~~~~~~~~~~~~~~~~

xml.sax ContentHandelrs.

"""

from xml.sax import handler


class IDsParser(handler.ContentHandler):
    """
    Content handler class for xml.sax.
    Parse response to get analysis_ids.
    """

    def __init__(self, callback):
        self.callback = callback
        self.hits = 0
        handler.ContentHandler.__init__(self)

    def startElement(self, name, attrs):
        self.content = ''

    def endElement(self, name):
        if name == 'analysis_id':
            self.callback(self.content)
        elif name == 'Hits':
            self.hits = int(self.content)

    def characters(self, content):
        self.content += content


class AttributesParser(handler.ContentHandler):
    """
    Content handler class for xml.sax.
    Parse AnalysisDetail file.
    """

    def __init__(self, callback):
        self.callback = callback
        self.hits = 0
        self.current_dict = {}
        self.files_size = 0
        self.files = []
        self.current_file = {}
        handler.ContentHandler.__init__(self)

    def startElement(self, name, attrs):
        self.content = ''
        if name == 'checksum':
            self.current_file['checksum'] = {'@type': attrs['type']}
        # assembly: analysis_xml/ANALYSIS_SET/ANALYSIS/ANALYSIS_TYPE/REFERENCE_ALIGNMENT/ASSEMBLY/STANDARD[short_name]
        if name == 'STANDARD' and 'short_name' in attrs:
            self.current_dict['refassem_short_name'] = attrs['short_name']

    def endElement(self, name):
        if name == 'file':
            self.files.append(self.current_file)
            self.current_file = {}
        elif name == 'filename':
            self.current_file['filename'] = self.content
        elif name == 'checksum':
            self.current_file['checksum']['#text'] = self.content
        elif name == 'filesize':
            self.files_size += int(self.content)
            self.current_file['filesize'] = int(self.content)
        elif name == 'Result':
            self.current_dict['files_size'] = self.files_size
            self.current_dict['files'] = self.files
            self.callback(self.current_dict)
            self.files = []
            self.files_size = 0
        elif name == 'Hits':
            self.hits = int(self.content)
        else:
            self.current_dict[name] = self.content

    def characters(self, content):
        self.content += content
