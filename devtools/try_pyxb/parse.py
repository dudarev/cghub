import sys
from optparse import OptionParser

import time
import xml.dom.minidom

import analysis
import experiment 

XML_FILE = "../../wsapi/tests/test_data/aliquot_id.xml"

def parse(xml_file):

    if not xml_file:
        xml_file = XML_FILE

    print 'Generating binding from %s with minidom' % (xml_file,)

    try:
        xmls = open(xml_file).read()
    except IOError, e:
        print e
        return

    mt2 = time.time()
    dom = xml.dom.minidom.parseString(xmls)
    mt3 = time.time()
    print mt3 - mt2, 'seconds'
    print

    # experiment_xml tag

    print 'parsing experiment_xml tag:'
    mt4 = time.time()
    experimentTag = dom.getElementsByTagName('experiment_xml')[0].firstChild
    dom_instance = experiment.CreateFromDOM(experimentTag)
    mt5 = time.time()
    for e in dom_instance.EXPERIMENT:
        print e.TITLE
    print mt5 - mt4, 'seconds'
    print

    # analysis_xml tag

    print 'parsing analysis_xml tag:'
    mt6 = time.time()
    analysisTag = dom.getElementsByTagName('analysis_xml')[0].firstChild
    dom_instance = analysis.CreateFromDOM(analysisTag)
    mt7 = time.time()
    for e in dom_instance.ANALYSIS:
        print e.TITLE
    print mt7 - mt6, 'seconds'
    print

def main():
    
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file", default=None,
                      help="specify file to validate")
    (opts, args) = parser.parse_args(sys.argv)

    parse(opts.file)

if __name__ == "__main__":
    main()
