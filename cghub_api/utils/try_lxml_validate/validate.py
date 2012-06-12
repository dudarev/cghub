import sys
from optparse import OptionParser

XML_FILE = "../../tests/test_data/aliquot_id.xml"

FILE_SCHEMA_EXPERIMENT = "../data/schemas/SRA.experiment.xsd"
FILE_SCHEMA_ANALYSIS = "../data/schemas/SRA.analysis.xsd"
FILE_SCHEMA_RUN = "../data/schemas/SRA.run.xsd"

from lxml import etree

def validate_schema(schema_file, doc, element_path):

    xmlschema_doc = etree.parse(open(schema_file, 'r'))
    xmlschema = etree.XMLSchema(xmlschema_doc)

    e = doc.findall(element_path)[0]
    is_valid = xmlschema.validate(e)

    if not is_valid:
        try:
            xmlschema.assertValid(e)
        except Exception, e:
            print 'Error: %s' % e
    else:
        print "Valid"

def validate(xml_file):

    if not xml_file:
        xml_file = XML_FILE

    try:
        doc = etree.parse(open(xml_file, 'r'))
    except IOError, e:
        print e
        return

    print "Validating experiment_xml:"
    validate_schema(FILE_SCHEMA_EXPERIMENT, doc, './/EXPERIMENT_SET')

    print "Validating analysis_xml:"
    validate_schema(FILE_SCHEMA_ANALYSIS, doc, './/ANALYSIS_SET')

    print "Validating run_xml:"
    validate_schema(FILE_SCHEMA_RUN, doc, './/RUN_SET')

def main():

    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file", default=None,
                      help="specify file to validate")
    (opts, args) = parser.parse_args(sys.argv)

    validate(opts.file)

if __name__ == "__main__":
    main()
