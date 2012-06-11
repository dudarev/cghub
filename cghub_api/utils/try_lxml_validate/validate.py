xml_file = "../../tests/test_data/aliquot_id.xml"

file_schema_experiment = "../data/schemas/SRA.experiment.xsd"
file_schema_analysis = "../data/schemas/SRA.analysis.xsd"
file_schema_run = "../data/schemas/SRA.run.xsd"

from lxml import etree

doc = etree.parse(open(xml_file, 'r'))

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

print "Validating experiment_xml:"
validate_schema(file_schema_experiment, doc, './/EXPERIMENT_SET')

print "Validating analysis_xml:"
validate_schema(file_schema_analysis, doc, './/ANALYSIS_SET')

print "Validating run_xml:"
validate_schema(file_schema_run, doc, './/RUN_SET')
