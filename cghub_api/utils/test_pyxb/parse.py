import time
import xml.dom.minidom

import analysis
import experiment 

xml_file = "../../tests/test_data/aliquot_id.xml"


print 'Generating binding from %s with minidom' % (xml_file,)
mt1 = time.time()
xmls = open(xml_file).read()
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

print 'parsing experiment_xml tag:'
mt6 = time.time()
analysisTag = dom.getElementsByTagName('analysis_xml')[0].firstChild
dom_instance = analysis.CreateFromDOM(analysisTag)
mt7 = time.time()
for e in dom_instance.ANALYSIS:
    print e.TITLE
print mt7 - mt6, 'seconds'
print
