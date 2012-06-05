# ./experiment.py
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2012-06-04 20:05:10.755100 by PyXB version 1.1.3
# Namespace AbsentNamespace0

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:6f0836a4-ae67-11e1-9370-0026c7825912')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import common

Namespace = pyxb.namespace.CreateAbsentNamespace()
Namespace.configureCategories(['typeBinding', 'elementBinding'])
ModuleRecord = Namespace.lookupModuleRecordByUID(_GenerationUID, create_if_missing=True)
ModuleRecord._setModule(sys.modules[__name__])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a Python instance."""
    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement)
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=Namespace.fallbackNamespace(), location_base=location_base)
    handler = saxer.getContentHandler()
    saxer.parse(StringIO.StringIO(xml_text))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, _fallback_namespace=default_namespace)


# Atomic SimpleTypeDefinition
class STD_ANON (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON, enum_prefix=None)
STD_ANON.Base_Space = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'Base Space', tag=u'Base_Space')
STD_ANON.Color_Space = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'Color Space', tag=u'Color_Space')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_ (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_, enum_prefix=None)
STD_ANON_.phred = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'phred', tag=u'phred')
STD_ANON_.other = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'other', tag=u'other')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration)

# Complex type CTD_ANON with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element BASE_CALLER uses Python identifier BASE_CALLER
    __BASE_CALLER = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'BASE_CALLER'), 'BASE_CALLER', '__AbsentNamespace0_CTD_ANON_BASE_CALLER', False)

    
    BASE_CALLER = property(__BASE_CALLER.value, __BASE_CALLER.set, None, u'\n                                                    Name and version of the base or color calling software.\n                                                ')

    
    # Element SEQUENCE_SPACE uses Python identifier SEQUENCE_SPACE
    __SEQUENCE_SPACE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SEQUENCE_SPACE'), 'SEQUENCE_SPACE', '__AbsentNamespace0_CTD_ANON_SEQUENCE_SPACE', False)

    
    SEQUENCE_SPACE = property(__SEQUENCE_SPACE.value, __SEQUENCE_SPACE.set, None, None)


    _ElementMap = {
        __BASE_CALLER.name() : __BASE_CALLER,
        __SEQUENCE_SPACE.name() : __SEQUENCE_SPACE
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_ with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element SAMPLE_DESCRIPTOR uses Python identifier SAMPLE_DESCRIPTOR
    __SAMPLE_DESCRIPTOR = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SAMPLE_DESCRIPTOR'), 'SAMPLE_DESCRIPTOR', '__AbsentNamespace0_CTD_ANON__SAMPLE_DESCRIPTOR', False)

    
    SAMPLE_DESCRIPTOR = property(__SAMPLE_DESCRIPTOR.value, __SAMPLE_DESCRIPTOR.set, None, u'\n                              Pick a sample to associate this experiment with.  \n                              The sample may be an individual or a pool, depending on how it is specified.\n                            ')

    
    # Element SPOT_DESCRIPTOR uses Python identifier SPOT_DESCRIPTOR
    __SPOT_DESCRIPTOR = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SPOT_DESCRIPTOR'), 'SPOT_DESCRIPTOR', '__AbsentNamespace0_CTD_ANON__SPOT_DESCRIPTOR', False)

    
    SPOT_DESCRIPTOR = property(__SPOT_DESCRIPTOR.value, __SPOT_DESCRIPTOR.set, None, u'\n                                  The SPOT_DESCRIPTOR specifies how to decode the individual reads of interest from the \n                                  monolithic spot sequence.  The spot descriptor contains aspects of the experimental design, \n                                  platform, and processing information.  There will be two methods of specification: one \n                                  will be an index into a table of typical decodings, the other being an exact specification.                                      \n                              ')

    
    # Element LIBRARY_DESCRIPTOR uses Python identifier LIBRARY_DESCRIPTOR
    __LIBRARY_DESCRIPTOR = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LIBRARY_DESCRIPTOR'), 'LIBRARY_DESCRIPTOR', '__AbsentNamespace0_CTD_ANON__LIBRARY_DESCRIPTOR', False)

    
    LIBRARY_DESCRIPTOR = property(__LIBRARY_DESCRIPTOR.value, __LIBRARY_DESCRIPTOR.set, None, u'\n                                  The LIBRARY_DESCRIPTOR specifies the origin of the material being sequenced and any treatments that the \n                                  material might have undergone that affect the sequencing result.  This specification is needed even if the platform\n                                  does not require a library construction step per se.\n                              ')

    
    # Element GAP_DESCRIPTOR uses Python identifier GAP_DESCRIPTOR
    __GAP_DESCRIPTOR = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'GAP_DESCRIPTOR'), 'GAP_DESCRIPTOR', '__AbsentNamespace0_CTD_ANON__GAP_DESCRIPTOR', False)

    
    GAP_DESCRIPTOR = property(__GAP_DESCRIPTOR.value, __GAP_DESCRIPTOR.set, None, u' The GAP_DESCRIPTOR specifies how to place the\n                                    individual tags in the spot against a notinoal reference\n                                    sequence. This information is important to interpreting the\n                                    placement of spot tags in an assembly or alignment for the\n                                    purpose of detecting structural variations and other genomic\n                                    features. ')

    
    # Element DESIGN_DESCRIPTION uses Python identifier DESIGN_DESCRIPTION
    __DESIGN_DESCRIPTION = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DESIGN_DESCRIPTION'), 'DESIGN_DESCRIPTION', '__AbsentNamespace0_CTD_ANON__DESIGN_DESCRIPTION', False)

    
    DESIGN_DESCRIPTION = property(__DESIGN_DESCRIPTION.value, __DESIGN_DESCRIPTION.set, None, u'\n                              More details about the setup and goals of the experiment as supplied by the Investigator.\n                          ')


    _ElementMap = {
        __SAMPLE_DESCRIPTOR.name() : __SAMPLE_DESCRIPTOR,
        __SPOT_DESCRIPTOR.name() : __SPOT_DESCRIPTOR,
        __LIBRARY_DESCRIPTOR.name() : __LIBRARY_DESCRIPTOR,
        __GAP_DESCRIPTOR.name() : __GAP_DESCRIPTOR,
        __DESIGN_DESCRIPTION.name() : __DESIGN_DESCRIPTION
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_2 with content type ELEMENT_ONLY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element EXPERIMENT_LINK uses Python identifier EXPERIMENT_LINK
    __EXPERIMENT_LINK = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'EXPERIMENT_LINK'), 'EXPERIMENT_LINK', '__AbsentNamespace0_CTD_ANON_2_EXPERIMENT_LINK', True)

    
    EXPERIMENT_LINK = property(__EXPERIMENT_LINK.value, __EXPERIMENT_LINK.set, None, None)


    _ElementMap = {
        __EXPERIMENT_LINK.name() : __EXPERIMENT_LINK
    }
    _AttributeMap = {
        
    }



# Complex type ExperimentType with content type ELEMENT_ONLY
class ExperimentType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ExperimentType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element PROCESSING uses Python identifier PROCESSING
    __PROCESSING = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PROCESSING'), 'PROCESSING', '__AbsentNamespace0_ExperimentType_PROCESSING', False)

    
    PROCESSING = property(__PROCESSING.value, __PROCESSING.set, None, None)

    
    # Element PLATFORM uses Python identifier PLATFORM
    __PLATFORM = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PLATFORM'), 'PLATFORM', '__AbsentNamespace0_ExperimentType_PLATFORM', False)

    
    PLATFORM = property(__PLATFORM.value, __PLATFORM.set, None, u'\n                      The PLATFORM record selects which sequencing platform and platform-specific runtime parameters.  \n                      This will be determined by the Center.\n                    ')

    
    # Element TITLE uses Python identifier TITLE
    __TITLE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TITLE'), 'TITLE', '__AbsentNamespace0_ExperimentType_TITLE', False)

    
    TITLE = property(__TITLE.value, __TITLE.set, None, u'\n                        Short text that can be used to call out experiment records in searches or in displays.\n                        This element is technically optional but should be used for all new records.\n                      ')

    
    # Element EXPERIMENT_LINKS uses Python identifier EXPERIMENT_LINKS
    __EXPERIMENT_LINKS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'EXPERIMENT_LINKS'), 'EXPERIMENT_LINKS', '__AbsentNamespace0_ExperimentType_EXPERIMENT_LINKS', False)

    
    EXPERIMENT_LINKS = property(__EXPERIMENT_LINKS.value, __EXPERIMENT_LINKS.set, None, u'\n\t\t\t  Links to resources related to this experiment or experiment set (publication, datasets, online databases).\n\t\t      ')

    
    # Element DESIGN uses Python identifier DESIGN
    __DESIGN = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DESIGN'), 'DESIGN', '__AbsentNamespace0_ExperimentType_DESIGN', False)

    
    DESIGN = property(__DESIGN.value, __DESIGN.set, None, None)

    
    # Element STUDY_REF uses Python identifier STUDY_REF
    __STUDY_REF = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'STUDY_REF'), 'STUDY_REF', '__AbsentNamespace0_ExperimentType_STUDY_REF', False)

    
    STUDY_REF = property(__STUDY_REF.value, __STUDY_REF.set, None, u'\n                        The STUDY_REF descriptor establishes the relationship of the experiment to the parent\n                        study.  This can either be the accession of an existing archived study record, or\n                        a reference to a new study record in the same submission (which does not yet have an\n                        accession).\n                      ')

    
    # Element EXPERIMENT_ATTRIBUTES uses Python identifier EXPERIMENT_ATTRIBUTES
    __EXPERIMENT_ATTRIBUTES = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'EXPERIMENT_ATTRIBUTES'), 'EXPERIMENT_ATTRIBUTES', '__AbsentNamespace0_ExperimentType_EXPERIMENT_ATTRIBUTES', False)

    
    EXPERIMENT_ATTRIBUTES = property(__EXPERIMENT_ATTRIBUTES.value, __EXPERIMENT_ATTRIBUTES.set, None, u'\n                       Properties and attributes of the experiment.  These can be entered as free-form \n                       tag-value pairs. \n                    ')

    
    # Attribute expected_number_runs uses Python identifier expected_number_runs
    __expected_number_runs = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'expected_number_runs'), 'expected_number_runs', '__AbsentNamespace0_ExperimentType_expected_number_runs', pyxb.binding.datatypes.positiveInteger)
    
    expected_number_runs = property(__expected_number_runs.value, __expected_number_runs.set, None, u'\n                     Number of runs expected to be submitted  for this experiment. \n                  ')

    
    # Attribute expected_number_spots uses Python identifier expected_number_spots
    __expected_number_spots = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'expected_number_spots'), 'expected_number_spots', '__AbsentNamespace0_ExperimentType_expected_number_spots', pyxb.binding.datatypes.positiveInteger)
    
    expected_number_spots = property(__expected_number_spots.value, __expected_number_spots.set, None, u'\n                       DEPRECATED. Number of spots expected to be submitted  for this experiment. \n                     ')

    
    # Attribute broker_name uses Python identifier broker_name
    __broker_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'broker_name'), 'broker_name', '__AbsentNamespace0_ExperimentType_broker_name', pyxb.binding.datatypes.string)
    
    broker_name = property(__broker_name.value, __broker_name.set, None, u'\n                    Broker authority of this document.  If not provided, then the broker is considered "direct".\n                ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'accession'), 'accession', '__AbsentNamespace0_ExperimentType_accession', pyxb.binding.datatypes.string)
    
    accession = property(__accession.value, __accession.set, None, u"\n                    The document's accession as assigned by the Home Archive.\n                ")

    
    # Attribute alias uses Python identifier alias
    __alias = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'alias'), 'alias', '__AbsentNamespace0_ExperimentType_alias', pyxb.binding.datatypes.string)
    
    alias = property(__alias.value, __alias.set, None, u'\n                    Submitter designated name of the SRA document of this type.  At minimum alias should\n                    be unique throughout the submission of this document type.  If center_name is specified, the name should\n                    be unique in all submissions from that center of this document type.\n                ')

    
    # Attribute expected_number_reads uses Python identifier expected_number_reads
    __expected_number_reads = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'expected_number_reads'), 'expected_number_reads', '__AbsentNamespace0_ExperimentType_expected_number_reads', pyxb.binding.datatypes.positiveInteger)
    
    expected_number_reads = property(__expected_number_reads.value, __expected_number_reads.set, None, u'\n                      DEPRECATED. Number of reads expected to be submitted  for this experiment. \n                    ')

    
    # Attribute center_name uses Python identifier center_name
    __center_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'center_name'), 'center_name', '__AbsentNamespace0_ExperimentType_center_name', pyxb.binding.datatypes.string)
    
    center_name = property(__center_name.value, __center_name.set, None, u'\n                    Owner authority of this document and namespace for submitter\'s name of this document. \n                    If not provided, then the submitter is regarded as "Individual" and document resolution\n                    can only happen within the submission.\n                ')


    _ElementMap = {
        __PROCESSING.name() : __PROCESSING,
        __PLATFORM.name() : __PLATFORM,
        __TITLE.name() : __TITLE,
        __EXPERIMENT_LINKS.name() : __EXPERIMENT_LINKS,
        __DESIGN.name() : __DESIGN,
        __STUDY_REF.name() : __STUDY_REF,
        __EXPERIMENT_ATTRIBUTES.name() : __EXPERIMENT_ATTRIBUTES
    }
    _AttributeMap = {
        __expected_number_runs.name() : __expected_number_runs,
        __expected_number_spots.name() : __expected_number_spots,
        __broker_name.name() : __broker_name,
        __accession.name() : __accession,
        __alias.name() : __alias,
        __expected_number_reads.name() : __expected_number_reads,
        __center_name.name() : __center_name
    }
Namespace.addCategoryObject('typeBinding', u'ExperimentType', ExperimentType)


# Complex type CTD_ANON_3 with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element QUALITY_SCORER uses Python identifier QUALITY_SCORER
    __QUALITY_SCORER = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'QUALITY_SCORER'), 'QUALITY_SCORER', '__AbsentNamespace0_CTD_ANON_3_QUALITY_SCORER', False)

    
    QUALITY_SCORER = property(__QUALITY_SCORER.value, __QUALITY_SCORER.set, None, u'\n                                                    Name and version of the quality scoring software.\n                                                ')

    
    # Element MULTIPLIER uses Python identifier MULTIPLIER
    __MULTIPLIER = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'MULTIPLIER'), 'MULTIPLIER', '__AbsentNamespace0_CTD_ANON_3_MULTIPLIER', False)

    
    MULTIPLIER = property(__MULTIPLIER.value, __MULTIPLIER.set, None, u'\n                                                    DEPRECATED.\n                                                ')

    
    # Element NUMBER_OF_LEVELS uses Python identifier NUMBER_OF_LEVELS
    __NUMBER_OF_LEVELS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'NUMBER_OF_LEVELS'), 'NUMBER_OF_LEVELS', '__AbsentNamespace0_CTD_ANON_3_NUMBER_OF_LEVELS', False)

    
    NUMBER_OF_LEVELS = property(__NUMBER_OF_LEVELS.value, __NUMBER_OF_LEVELS.set, None, u'\n                                                    DEPRECATED.  Number of distinct values possible with this scoring system.\n                                                ')

    
    # Attribute qtype uses Python identifier qtype
    __qtype = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'qtype'), 'qtype', '__AbsentNamespace0_CTD_ANON_3_qtype', STD_ANON_)
    
    qtype = property(__qtype.value, __qtype.set, None, None)


    _ElementMap = {
        __QUALITY_SCORER.name() : __QUALITY_SCORER,
        __MULTIPLIER.name() : __MULTIPLIER,
        __NUMBER_OF_LEVELS.name() : __NUMBER_OF_LEVELS
    }
    _AttributeMap = {
        __qtype.name() : __qtype
    }



# Complex type CTD_ANON_4 with content type ELEMENT_ONLY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element EXPERIMENT_ATTRIBUTE uses Python identifier EXPERIMENT_ATTRIBUTE
    __EXPERIMENT_ATTRIBUTE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'EXPERIMENT_ATTRIBUTE'), 'EXPERIMENT_ATTRIBUTE', '__AbsentNamespace0_CTD_ANON_4_EXPERIMENT_ATTRIBUTE', True)

    
    EXPERIMENT_ATTRIBUTE = property(__EXPERIMENT_ATTRIBUTE.value, __EXPERIMENT_ATTRIBUTE.set, None, None)


    _ElementMap = {
        __EXPERIMENT_ATTRIBUTE.name() : __EXPERIMENT_ATTRIBUTE
    }
    _AttributeMap = {
        
    }



# Complex type ExperimentSetType with content type ELEMENT_ONLY
class ExperimentSetType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ExperimentSetType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element EXPERIMENT uses Python identifier EXPERIMENT
    __EXPERIMENT = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'EXPERIMENT'), 'EXPERIMENT', '__AbsentNamespace0_ExperimentSetType_EXPERIMENT', True)

    
    EXPERIMENT = property(__EXPERIMENT.value, __EXPERIMENT.set, None, None)


    _ElementMap = {
        __EXPERIMENT.name() : __EXPERIMENT
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ExperimentSetType', ExperimentSetType)


# Complex type CTD_ANON_5 with content type ELEMENT_ONLY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element BASE_CALLS uses Python identifier BASE_CALLS
    __BASE_CALLS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'BASE_CALLS'), 'BASE_CALLS', '__AbsentNamespace0_CTD_ANON_5_BASE_CALLS', False)

    
    BASE_CALLS = property(__BASE_CALLS.value, __BASE_CALLS.set, None, None)

    
    # Element PIPELINE uses Python identifier PIPELINE
    __PIPELINE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PIPELINE'), 'PIPELINE', '__AbsentNamespace0_CTD_ANON_5_PIPELINE', False)

    
    PIPELINE = property(__PIPELINE.value, __PIPELINE.set, None, u'\n                                        Generic processing pipeline specification.\n                                    ')

    
    # Element DIRECTIVES uses Python identifier DIRECTIVES
    __DIRECTIVES = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DIRECTIVES'), 'DIRECTIVES', '__AbsentNamespace0_CTD_ANON_5_DIRECTIVES', False)

    
    DIRECTIVES = property(__DIRECTIVES.value, __DIRECTIVES.set, None, u'\n                                        Processing directives tell the Sequence Read Archive how to treat the input data, if any treatment is requested.\n                                    ')

    
    # Element QUALITY_SCORES uses Python identifier QUALITY_SCORES
    __QUALITY_SCORES = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'QUALITY_SCORES'), 'QUALITY_SCORES', '__AbsentNamespace0_CTD_ANON_5_QUALITY_SCORES', True)

    
    QUALITY_SCORES = property(__QUALITY_SCORES.value, __QUALITY_SCORES.set, None, u'\n                                        DEPRECATED.  THis is instead a  property of the run to load.  Basecalling software and version will be called out in\n                                        new branch PIPELINE.\n                                    ')


    _ElementMap = {
        __BASE_CALLS.name() : __BASE_CALLS,
        __PIPELINE.name() : __PIPELINE,
        __DIRECTIVES.name() : __DIRECTIVES,
        __QUALITY_SCORES.name() : __QUALITY_SCORES
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_6 with content type EMPTY
class CTD_ANON_6 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'accession'), 'accession', '__AbsentNamespace0_CTD_ANON_6_accession', pyxb.binding.datatypes.string)
    
    accession = property(__accession.value, __accession.set, None, u'\n                    Identifies a record by its accession.  The scope of resolution is the entire Archive.\n                ')

    
    # Attribute refcenter uses Python identifier refcenter
    __refcenter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refcenter'), 'refcenter', '__AbsentNamespace0_CTD_ANON_6_refcenter', pyxb.binding.datatypes.string)
    
    refcenter = property(__refcenter.value, __refcenter.set, None, u'\n                    The center namespace of the attribute "refname". When absent, the namespace is assumed to be the current submission.\n                ')

    
    # Attribute refname uses Python identifier refname
    __refname = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refname'), 'refname', '__AbsentNamespace0_CTD_ANON_6_refname', pyxb.binding.datatypes.string)
    
    refname = property(__refname.value, __refname.set, None, u'\n                    Identifies a record by name that is known within the namespace defined by attribute "refcenter"\n                    Use this field when referencing an object for which an accession has not yet been issued.\n                ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __accession.name() : __accession,
        __refcenter.name() : __refcenter,
        __refname.name() : __refname
    }



EXPERIMENT = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'EXPERIMENT'), ExperimentType)
Namespace.addCategoryObject('elementBinding', EXPERIMENT.name().localName(), EXPERIMENT)

EXPERIMENT_SET = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'EXPERIMENT_SET'), ExperimentSetType, documentation=u'\n      An EXPERMENT_SET is a container for a set of experiments and a common namespace.\n    ')
Namespace.addCategoryObject('elementBinding', EXPERIMENT_SET.name().localName(), EXPERIMENT_SET)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'BASE_CALLER'), pyxb.binding.datatypes.string, scope=CTD_ANON, documentation=u'\n                                                    Name and version of the base or color calling software.\n                                                '))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SEQUENCE_SPACE'), STD_ANON, scope=CTD_ANON))
CTD_ANON._GroupModel = pyxb.binding.content.GroupAll(
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, u'SEQUENCE_SPACE')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, u'BASE_CALLER')), min_occurs=1L, max_occurs=1L)
    )
CTD_ANON._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SAMPLE_DESCRIPTOR'), common.SampleDescriptorType, scope=CTD_ANON_, documentation=u'\n                              Pick a sample to associate this experiment with.  \n                              The sample may be an individual or a pool, depending on how it is specified.\n                            '))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SPOT_DESCRIPTOR'), common.SpotDescriptorType, scope=CTD_ANON_, documentation=u'\n                                  The SPOT_DESCRIPTOR specifies how to decode the individual reads of interest from the \n                                  monolithic spot sequence.  The spot descriptor contains aspects of the experimental design, \n                                  platform, and processing information.  There will be two methods of specification: one \n                                  will be an index into a table of typical decodings, the other being an exact specification.                                      \n                              '))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LIBRARY_DESCRIPTOR'), common.LibraryDescriptorType, scope=CTD_ANON_, documentation=u'\n                                  The LIBRARY_DESCRIPTOR specifies the origin of the material being sequenced and any treatments that the \n                                  material might have undergone that affect the sequencing result.  This specification is needed even if the platform\n                                  does not require a library construction step per se.\n                              '))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'GAP_DESCRIPTOR'), common.GapDescriptorType, scope=CTD_ANON_, documentation=u' The GAP_DESCRIPTOR specifies how to place the\n                                    individual tags in the spot against a notinoal reference\n                                    sequence. This information is important to interpreting the\n                                    placement of spot tags in an assembly or alignment for the\n                                    purpose of detecting structural variations and other genomic\n                                    features. '))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DESIGN_DESCRIPTION'), pyxb.binding.datatypes.string, scope=CTD_ANON_, documentation=u'\n                              More details about the setup and goals of the experiment as supplied by the Investigator.\n                          '))
CTD_ANON_._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, u'DESIGN_DESCRIPTION')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, u'SAMPLE_DESCRIPTOR')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, u'LIBRARY_DESCRIPTOR')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, u'SPOT_DESCRIPTOR')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, u'GAP_DESCRIPTOR')), min_occurs=0L, max_occurs=1L)
    )
CTD_ANON_._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'EXPERIMENT_LINK'), common.LinkType, scope=CTD_ANON_2))
CTD_ANON_2._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, u'EXPERIMENT_LINK')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_2._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_2._GroupModel, min_occurs=1L, max_occurs=None)



ExperimentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PROCESSING'), CTD_ANON_5, scope=ExperimentType))

ExperimentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PLATFORM'), common.PlatformType, scope=ExperimentType, documentation=u'\n                      The PLATFORM record selects which sequencing platform and platform-specific runtime parameters.  \n                      This will be determined by the Center.\n                    '))

ExperimentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TITLE'), pyxb.binding.datatypes.string, scope=ExperimentType, documentation=u'\n                        Short text that can be used to call out experiment records in searches or in displays.\n                        This element is technically optional but should be used for all new records.\n                      '))

ExperimentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'EXPERIMENT_LINKS'), CTD_ANON_2, scope=ExperimentType, documentation=u'\n\t\t\t  Links to resources related to this experiment or experiment set (publication, datasets, online databases).\n\t\t      '))

ExperimentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DESIGN'), CTD_ANON_, scope=ExperimentType))

ExperimentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'STUDY_REF'), CTD_ANON_6, scope=ExperimentType, documentation=u'\n                        The STUDY_REF descriptor establishes the relationship of the experiment to the parent\n                        study.  This can either be the accession of an existing archived study record, or\n                        a reference to a new study record in the same submission (which does not yet have an\n                        accession).\n                      '))

ExperimentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'EXPERIMENT_ATTRIBUTES'), CTD_ANON_4, scope=ExperimentType, documentation=u'\n                       Properties and attributes of the experiment.  These can be entered as free-form \n                       tag-value pairs. \n                    '))
ExperimentType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ExperimentType._UseForTag(pyxb.namespace.ExpandedName(None, u'TITLE')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ExperimentType._UseForTag(pyxb.namespace.ExpandedName(None, u'STUDY_REF')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ExperimentType._UseForTag(pyxb.namespace.ExpandedName(None, u'DESIGN')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ExperimentType._UseForTag(pyxb.namespace.ExpandedName(None, u'PLATFORM')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ExperimentType._UseForTag(pyxb.namespace.ExpandedName(None, u'PROCESSING')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ExperimentType._UseForTag(pyxb.namespace.ExpandedName(None, u'EXPERIMENT_LINKS')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(ExperimentType._UseForTag(pyxb.namespace.ExpandedName(None, u'EXPERIMENT_ATTRIBUTES')), min_occurs=0L, max_occurs=1L)
    )
ExperimentType._ContentModel = pyxb.binding.content.ParticleModel(ExperimentType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'QUALITY_SCORER'), pyxb.binding.datatypes.string, scope=CTD_ANON_3, documentation=u'\n                                                    Name and version of the quality scoring software.\n                                                '))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'MULTIPLIER'), pyxb.binding.datatypes.double, scope=CTD_ANON_3, documentation=u'\n                                                    DEPRECATED.\n                                                '))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'NUMBER_OF_LEVELS'), pyxb.binding.datatypes.int, scope=CTD_ANON_3, documentation=u'\n                                                    DEPRECATED.  Number of distinct values possible with this scoring system.\n                                                '))
CTD_ANON_3._GroupModel = pyxb.binding.content.GroupAll(
    pyxb.binding.content.ParticleModel(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, u'QUALITY_SCORER')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, u'NUMBER_OF_LEVELS')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, u'MULTIPLIER')), min_occurs=0L, max_occurs=1L)
    )
CTD_ANON_3._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_3._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'EXPERIMENT_ATTRIBUTE'), common.AttributeType, scope=CTD_ANON_4))
CTD_ANON_4._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, u'EXPERIMENT_ATTRIBUTE')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_4._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_4._GroupModel, min_occurs=1L, max_occurs=None)



ExperimentSetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'EXPERIMENT'), ExperimentType, scope=ExperimentSetType))
ExperimentSetType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ExperimentSetType._UseForTag(pyxb.namespace.ExpandedName(None, u'EXPERIMENT')), min_occurs=1, max_occurs=None)
    )
ExperimentSetType._ContentModel = pyxb.binding.content.ParticleModel(ExperimentSetType._GroupModel, min_occurs=1L, max_occurs=1L)



CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'BASE_CALLS'), CTD_ANON, scope=CTD_ANON_5))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PIPELINE'), common.PipelineType, scope=CTD_ANON_5, documentation=u'\n                                        Generic processing pipeline specification.\n                                    '))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DIRECTIVES'), common.SequencingDirectivesType, scope=CTD_ANON_5, documentation=u'\n                                        Processing directives tell the Sequence Read Archive how to treat the input data, if any treatment is requested.\n                                    '))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'QUALITY_SCORES'), CTD_ANON_3, scope=CTD_ANON_5, documentation=u'\n                                        DEPRECATED.  THis is instead a  property of the run to load.  Basecalling software and version will be called out in\n                                        new branch PIPELINE.\n                                    '))
CTD_ANON_5._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, u'BASE_CALLS')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, u'QUALITY_SCORES')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, u'PIPELINE')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, u'DIRECTIVES')), min_occurs=0L, max_occurs=1L)
    )
CTD_ANON_5._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_5._GroupModel, min_occurs=1, max_occurs=1)
