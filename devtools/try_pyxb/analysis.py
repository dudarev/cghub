# ./analysis.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2012-08-06 22:22:08.575529 by PyXB version 1.1.5-DEV
# Namespace AbsentNamespace0

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:0393ed34-dffc-11e1-a8aa-0026c7825912')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import common

Namespace = pyxb.namespace.CreateAbsentNamespace()
Namespace.configureCategories(['typeBinding', 'elementBinding'])
ModuleRecord = Namespace.lookupModuleRecordByUID(_GenerationUID, create_if_missing=True)
ModuleRecord._setModule(sys.modules[__name__])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.
    
    @kw default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
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
STD_ANON.ace = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'ace', tag=u'ace')
STD_ANON.tab = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'tab', tag=u'tab')
STD_ANON.bam = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'bam', tag=u'bam')
STD_ANON.fasta = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'fasta', tag=u'fasta')
STD_ANON.wig = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'wig', tag=u'wig')
STD_ANON.bed = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'bed', tag=u'bed')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_ (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_, enum_prefix=None)
STD_ANON_.MD5 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'MD5', tag=u'MD5')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration)

# Complex type CTD_ANON with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ANALYSIS_LINK uses Python identifier ANALYSIS_LINK
    __ANALYSIS_LINK = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ANALYSIS_LINK'), 'ANALYSIS_LINK', '__AbsentNamespace0_CTD_ANON_ANALYSIS_LINK', True)

    
    ANALYSIS_LINK = property(__ANALYSIS_LINK.value, __ANALYSIS_LINK.set, None, None)


    _ElementMap = {
        __ANALYSIS_LINK.name() : __ANALYSIS_LINK
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
    
    # Element NAME uses Python identifier NAME
    __NAME = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'NAME'), 'NAME', '__AbsentNamespace0_CTD_ANON__NAME', True)

    
    NAME = property(__NAME.value, __NAME.set, None, u'Synonym Names additional to or in place of short_name. For example genbank,\n                                    gecoll accession.version.')

    
    # Attribute short_name uses Python identifier short_name
    __short_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'short_name'), 'short_name', '__AbsentNamespace0_CTD_ANON__short_name', pyxb.binding.datatypes.string)
    
    short_name = property(__short_name.value, __short_name.set, None, u' Short name for standard reference assembly. The Home Archive shall implement\n                                  further business rules governing the usage of short_name in conjunction with or in lieu of\n                                  explicit references. ')


    _ElementMap = {
        __NAME.name() : __NAME
    }
    _AttributeMap = {
        __short_name.name() : __short_name
    }



# Complex type AlignmentProcessingType with content type ELEMENT_ONLY
class AlignmentProcessingType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AlignmentProcessingType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element PIPELINE uses Python identifier PIPELINE
    __PIPELINE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PIPELINE'), 'PIPELINE', '__AbsentNamespace0_AlignmentProcessingType_PIPELINE', False)

    
    PIPELINE = property(__PIPELINE.value, __PIPELINE.set, None, None)

    
    # Element DIRECTIVES uses Python identifier DIRECTIVES
    __DIRECTIVES = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DIRECTIVES'), 'DIRECTIVES', '__AbsentNamespace0_AlignmentProcessingType_DIRECTIVES', False)

    
    DIRECTIVES = property(__DIRECTIVES.value, __DIRECTIVES.set, None, None)


    _ElementMap = {
        __PIPELINE.name() : __PIPELINE,
        __DIRECTIVES.name() : __DIRECTIVES
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'AlignmentProcessingType', AlignmentProcessingType)


# Complex type CTD_ANON_2 with content type ELEMENT_ONLY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element DE_NOVO_ASSEMBLY uses Python identifier DE_NOVO_ASSEMBLY
    __DE_NOVO_ASSEMBLY = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DE_NOVO_ASSEMBLY'), 'DE_NOVO_ASSEMBLY', '__AbsentNamespace0_CTD_ANON_2_DE_NOVO_ASSEMBLY', False)

    
    DE_NOVO_ASSEMBLY = property(__DE_NOVO_ASSEMBLY.value, __DE_NOVO_ASSEMBLY.set, None, u' A placement of sequences including trace, SRA, GI records into a multiple alignment from which a\n                  consensus is computed. This branch will be further specified in the future. ')

    
    # Element ABUNDANCE_MEASUREMENT uses Python identifier ABUNDANCE_MEASUREMENT
    __ABUNDANCE_MEASUREMENT = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ABUNDANCE_MEASUREMENT'), 'ABUNDANCE_MEASUREMENT', '__AbsentNamespace0_CTD_ANON_2_ABUNDANCE_MEASUREMENT', False)

    
    ABUNDANCE_MEASUREMENT = property(__ABUNDANCE_MEASUREMENT.value, __ABUNDANCE_MEASUREMENT.set, None, u' A track of read placement coverage used to measure abundance of a library with respect to a\n                  reference. This branch will be further specified in the future. ')

    
    # Element SEQUENCE_ANNOTATION uses Python identifier SEQUENCE_ANNOTATION
    __SEQUENCE_ANNOTATION = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SEQUENCE_ANNOTATION'), 'SEQUENCE_ANNOTATION', '__AbsentNamespace0_CTD_ANON_2_SEQUENCE_ANNOTATION', False)

    
    SEQUENCE_ANNOTATION = property(__SEQUENCE_ANNOTATION.value, __SEQUENCE_ANNOTATION.set, None, u' Per sequence annotation of named attributes and values. Example: Processed sequencing data for\n                  submission to dbEST without assembly. Reads have already been submitted to one of the sequence read archives in\n                  raw form. The fasta data submitted under this analysis object result from the following treatments, which may\n                  serve to filter reads from the raw dataset: - sequencing adapter removal - low quality trimming - poly-A tail\n                  removal - strand orientation - contaminant removal This branch will be further specified in the future. ')

    
    # Element REFERENCE_ALIGNMENT uses Python identifier REFERENCE_ALIGNMENT
    __REFERENCE_ALIGNMENT = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'REFERENCE_ALIGNMENT'), 'REFERENCE_ALIGNMENT', '__AbsentNamespace0_CTD_ANON_2_REFERENCE_ALIGNMENT', False)

    
    REFERENCE_ALIGNMENT = property(__REFERENCE_ALIGNMENT.value, __REFERENCE_ALIGNMENT.set, None, u' A multiple alignment of short reads against a reference substrate. ')


    _ElementMap = {
        __DE_NOVO_ASSEMBLY.name() : __DE_NOVO_ASSEMBLY,
        __ABUNDANCE_MEASUREMENT.name() : __ABUNDANCE_MEASUREMENT,
        __SEQUENCE_ANNOTATION.name() : __SEQUENCE_ANNOTATION,
        __REFERENCE_ALIGNMENT.name() : __REFERENCE_ALIGNMENT
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_3 with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element PROCESSING uses Python identifier PROCESSING
    __PROCESSING = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PROCESSING'), 'PROCESSING', '__AbsentNamespace0_CTD_ANON_3_PROCESSING', False)

    
    PROCESSING = property(__PROCESSING.value, __PROCESSING.set, None, u' Identify the tools and processing steps used to produce the sequence annotations. ')


    _ElementMap = {
        __PROCESSING.name() : __PROCESSING
    }
    _AttributeMap = {
        
    }



# Complex type AnalysisType with content type ELEMENT_ONLY
class AnalysisType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AnalysisType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ANALYSIS_ATTRIBUTES uses Python identifier ANALYSIS_ATTRIBUTES
    __ANALYSIS_ATTRIBUTES = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ANALYSIS_ATTRIBUTES'), 'ANALYSIS_ATTRIBUTES', '__AbsentNamespace0_AnalysisType_ANALYSIS_ATTRIBUTES', False)

    
    ANALYSIS_ATTRIBUTES = property(__ANALYSIS_ATTRIBUTES.value, __ANALYSIS_ATTRIBUTES.set, None, u' Properties and attributes of an analysis. These can be entered as free-form tag-value pairs. For\n            certain studies, submitters may be asked to follow a community established ontology when describing the work. ')

    
    # Element DATA_BLOCK uses Python identifier DATA_BLOCK
    __DATA_BLOCK = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DATA_BLOCK'), 'DATA_BLOCK', '__AbsentNamespace0_AnalysisType_DATA_BLOCK', True)

    
    DATA_BLOCK = property(__DATA_BLOCK.value, __DATA_BLOCK.set, None, u' One or more blocks of data and associated file(s). Each data block may be a partition of the overall\n              analysis object. ')

    
    # Element TARGETS uses Python identifier TARGETS
    __TARGETS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TARGETS'), 'TARGETS', '__AbsentNamespace0_AnalysisType_TARGETS', False)

    
    TARGETS = property(__TARGETS.value, __TARGETS.set, None, u' SRA object(s) targeted for analysis. Run - One or more runs that are assembled, aligned, or analyzed.\n            Sample - All the sequencing data for this sample are being assembled, aligned, or analyzed. Experiment - All the\n            sequencing data for this experiment are being assembled, aligned, or analyzed. Study - All the sequencing data for this\n            study are being assembled, aligned, or analyzed. ')

    
    # Element DESCRIPTION uses Python identifier DESCRIPTION
    __DESCRIPTION = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DESCRIPTION'), 'DESCRIPTION', '__AbsentNamespace0_AnalysisType_DESCRIPTION', False)

    
    DESCRIPTION = property(__DESCRIPTION.value, __DESCRIPTION.set, None, u' Describes the contents of the analysis objects, their relationship with one another, the target\n            objects, and their place in the overall study. ')

    
    # Element TITLE uses Python identifier TITLE
    __TITLE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TITLE'), 'TITLE', '__AbsentNamespace0_AnalysisType_TITLE', False)

    
    TITLE = property(__TITLE.value, __TITLE.set, None, u' Title of the analyis object which will be displayed in short form in the Analysis browser and in\n            database search results. ')

    
    # Element ANALYSIS_LINKS uses Python identifier ANALYSIS_LINKS
    __ANALYSIS_LINKS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ANALYSIS_LINKS'), 'ANALYSIS_LINKS', '__AbsentNamespace0_AnalysisType_ANALYSIS_LINKS', False)

    
    ANALYSIS_LINKS = property(__ANALYSIS_LINKS.value, __ANALYSIS_LINKS.set, None, u' Links to resources related to this analysis or analysis set (publication, datasets, online databases). ')

    
    # Element STUDY_REF uses Python identifier STUDY_REF
    __STUDY_REF = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'STUDY_REF'), 'STUDY_REF', '__AbsentNamespace0_AnalysisType_STUDY_REF', False)

    
    STUDY_REF = property(__STUDY_REF.value, __STUDY_REF.set, None, u' The STUDY_REF descriptor establishes the relationship of the analysis to the parent study. This can\n            either be the accession of an existing archived study record, or a reference to a new study record in the same\n            submission or same center (which does not yet have an accession). ')

    
    # Element ANALYSIS_TYPE uses Python identifier ANALYSIS_TYPE
    __ANALYSIS_TYPE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ANALYSIS_TYPE'), 'ANALYSIS_TYPE', '__AbsentNamespace0_AnalysisType_ANALYSIS_TYPE', False)

    
    ANALYSIS_TYPE = property(__ANALYSIS_TYPE.value, __ANALYSIS_TYPE.set, None, u' Supported analysis types. ')

    
    # Element IDENTIFIERS uses Python identifier IDENTIFIERS
    __IDENTIFIERS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'IDENTIFIERS'), 'IDENTIFIERS', '__AbsentNamespace0_AnalysisType_IDENTIFIERS', False)

    
    IDENTIFIERS = property(__IDENTIFIERS.value, __IDENTIFIERS.set, None, u'List of primary and alternate identifiers including those records replacing or replaced by this record. ')

    
    # Attribute analysis_date uses Python identifier analysis_date
    __analysis_date = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'analysis_date'), 'analysis_date', '__AbsentNamespace0_AnalysisType_analysis_date', pyxb.binding.datatypes.dateTime)
    
    analysis_date = property(__analysis_date.value, __analysis_date.set, None, u' The ISO date when this analysis was produced. ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'accession'), 'accession', '__AbsentNamespace0_AnalysisType_accession', pyxb.binding.datatypes.string)
    
    accession = property(__accession.value, __accession.set, None, u" The document's accession as assigned by the Home Archive. ")

    
    # Attribute broker_name uses Python identifier broker_name
    __broker_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'broker_name'), 'broker_name', '__AbsentNamespace0_AnalysisType_broker_name', pyxb.binding.datatypes.string)
    
    broker_name = property(__broker_name.value, __broker_name.set, None, u' Broker authority of this document. If not provided, then the broker is considered "direct". ')

    
    # Attribute alias uses Python identifier alias
    __alias = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'alias'), 'alias', '__AbsentNamespace0_AnalysisType_alias', pyxb.binding.datatypes.string)
    
    alias = property(__alias.value, __alias.set, None, u' Submitter designated name of the SRA document of this type. At minimum alias should be unique\n                    throughout the submission of this document type. If center_name is specified, the name should be unique in all\n                    submissions from that center of this document type. ')

    
    # Attribute center_name uses Python identifier center_name
    __center_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'center_name'), 'center_name', '__AbsentNamespace0_AnalysisType_center_name', pyxb.binding.datatypes.string)
    
    center_name = property(__center_name.value, __center_name.set, None, u' Owner authority of this document and namespace for submitter\'s name of this document. If not\n                    provided, then the submitter is regarded as "Individual" and document resolution can only happen within the\n                    submission. ')

    
    # Attribute analysis_center uses Python identifier analysis_center
    __analysis_center = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'analysis_center'), 'analysis_center', '__AbsentNamespace0_AnalysisType_analysis_center', pyxb.binding.datatypes.string)
    
    analysis_center = property(__analysis_center.value, __analysis_center.set, None, u' Use SRA center_name. If applicable, the center name of the institution responsible for this analysis. ')


    _ElementMap = {
        __ANALYSIS_ATTRIBUTES.name() : __ANALYSIS_ATTRIBUTES,
        __DATA_BLOCK.name() : __DATA_BLOCK,
        __TARGETS.name() : __TARGETS,
        __DESCRIPTION.name() : __DESCRIPTION,
        __TITLE.name() : __TITLE,
        __ANALYSIS_LINKS.name() : __ANALYSIS_LINKS,
        __STUDY_REF.name() : __STUDY_REF,
        __ANALYSIS_TYPE.name() : __ANALYSIS_TYPE,
        __IDENTIFIERS.name() : __IDENTIFIERS
    }
    _AttributeMap = {
        __analysis_date.name() : __analysis_date,
        __accession.name() : __accession,
        __broker_name.name() : __broker_name,
        __alias.name() : __alias,
        __center_name.name() : __center_name,
        __analysis_center.name() : __analysis_center
    }
Namespace.addCategoryObject('typeBinding', u'AnalysisType', AnalysisType)


# Complex type CTD_ANON_4 with content type ELEMENT_ONLY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ANALYSIS_ATTRIBUTE uses Python identifier ANALYSIS_ATTRIBUTE
    __ANALYSIS_ATTRIBUTE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ANALYSIS_ATTRIBUTE'), 'ANALYSIS_ATTRIBUTE', '__AbsentNamespace0_CTD_ANON_4_ANALYSIS_ATTRIBUTE', True)

    
    ANALYSIS_ATTRIBUTE = property(__ANALYSIS_ATTRIBUTE.value, __ANALYSIS_ATTRIBUTE.set, None, None)


    _ElementMap = {
        __ANALYSIS_ATTRIBUTE.name() : __ANALYSIS_ATTRIBUTE
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_5 with content type ELEMENT_ONLY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element FILES uses Python identifier FILES
    __FILES = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'FILES'), 'FILES', '__AbsentNamespace0_CTD_ANON_5_FILES', False)

    
    FILES = property(__FILES.value, __FILES.set, None, u' Actual run data are contained in one of the files listed in the submission manifest. Each data\n                    block is represented by one SRF file, one SFF file, one compressed fastq file, or one compressed tar archive\n                    file. ')

    
    # Attribute serial uses Python identifier serial
    __serial = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'serial'), 'serial', '__AbsentNamespace0_CTD_ANON_5_serial', pyxb.binding.datatypes.integer)
    
    serial = property(__serial.value, __serial.set, None, u'Specifies the order in which analysis files should be loaded, if needed.')

    
    # Attribute member uses Python identifier member
    __member = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'member'), 'member', '__AbsentNamespace0_CTD_ANON_5_member', pyxb.binding.datatypes.string)
    
    member = property(__member.value, __member.set, None, u'Member name of the fraction of the analysis file that should be loaded for this data block. Used\n                  for sample multiplexed studies where the analysis data has been demultiplexed by the submitter. ')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__AbsentNamespace0_CTD_ANON_5_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'Data block name, for use in mapping multiple analysis files to a single analysis object. This\n                  attribute is not needed if there is only one analysis file loaded for the analysis object. ')


    _ElementMap = {
        __FILES.name() : __FILES
    }
    _AttributeMap = {
        __serial.name() : __serial,
        __member.name() : __member,
        __name.name() : __name
    }



# Complex type CTD_ANON_6 with content type ELEMENT_ONLY
class CTD_ANON_6 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element STANDARD uses Python identifier STANDARD
    __STANDARD = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'STANDARD'), 'STANDARD', '__AbsentNamespace0_CTD_ANON_6_STANDARD', False)

    
    STANDARD = property(__STANDARD.value, __STANDARD.set, None, u' Short name for the standard reference assembly used in the alignment. This should\n                              resolve into community accepted collection of reference sequences. ')

    
    # Element CUSTOM uses Python identifier CUSTOM
    __CUSTOM = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'CUSTOM'), 'CUSTOM', '__AbsentNamespace0_CTD_ANON_6_CUSTOM', False)

    
    CUSTOM = property(__CUSTOM.value, __CUSTOM.set, None, u' A list of ad-hoc reference sequences identified by database link. ')


    _ElementMap = {
        __STANDARD.name() : __STANDARD,
        __CUSTOM.name() : __CUSTOM
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_7 with content type ELEMENT_ONLY
class CTD_ANON_7 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element PROCESSING uses Python identifier PROCESSING
    __PROCESSING = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PROCESSING'), 'PROCESSING', '__AbsentNamespace0_CTD_ANON_7_PROCESSING', False)

    
    PROCESSING = property(__PROCESSING.value, __PROCESSING.set, None, u' Identify the tools and processing steps used to produce the de novo assembly. ')


    _ElementMap = {
        __PROCESSING.name() : __PROCESSING
    }
    _AttributeMap = {
        
    }



# Complex type DefaultProcessingType with content type ELEMENT_ONLY
class DefaultProcessingType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DefaultProcessingType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element PIPELINE uses Python identifier PIPELINE
    __PIPELINE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PIPELINE'), 'PIPELINE', '__AbsentNamespace0_DefaultProcessingType_PIPELINE', False)

    
    PIPELINE = property(__PIPELINE.value, __PIPELINE.set, None, None)


    _ElementMap = {
        __PIPELINE.name() : __PIPELINE
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'DefaultProcessingType', DefaultProcessingType)


# Complex type CTD_ANON_8 with content type ELEMENT_ONLY
class CTD_ANON_8 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element PROCESSING uses Python identifier PROCESSING
    __PROCESSING = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PROCESSING'), 'PROCESSING', '__AbsentNamespace0_CTD_ANON_8_PROCESSING', False)

    
    PROCESSING = property(__PROCESSING.value, __PROCESSING.set, None, u' Identify the tools and processing steps used to produce the reference alignment, and\n                        specify directives used to load and interpret the data supplied by the submitter. ')

    
    # Element SEQ_LABELS uses Python identifier SEQ_LABELS
    __SEQ_LABELS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SEQ_LABELS'), 'SEQ_LABELS', '__AbsentNamespace0_CTD_ANON_8_SEQ_LABELS', False)

    
    SEQ_LABELS = property(__SEQ_LABELS.value, __SEQ_LABELS.set, None, None)

    
    # Element ASSEMBLY uses Python identifier ASSEMBLY
    __ASSEMBLY = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ASSEMBLY'), 'ASSEMBLY', '__AbsentNamespace0_CTD_ANON_8_ASSEMBLY', False)

    
    ASSEMBLY = property(__ASSEMBLY.value, __ASSEMBLY.set, None, u' Specification of the reference collection of sequences used in the alignment. ')

    
    # Element RUN_LABELS uses Python identifier RUN_LABELS
    __RUN_LABELS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'RUN_LABELS'), 'RUN_LABELS', '__AbsentNamespace0_CTD_ANON_8_RUN_LABELS', False)

    
    RUN_LABELS = property(__RUN_LABELS.value, __RUN_LABELS.set, None, u'Mapping between the run (read group) labels used in the alignment data file, and the runs in\n                        the Archive. This is optional when SRA runs are reffered by accession in submitted data. ')


    _ElementMap = {
        __PROCESSING.name() : __PROCESSING,
        __SEQ_LABELS.name() : __SEQ_LABELS,
        __ASSEMBLY.name() : __ASSEMBLY,
        __RUN_LABELS.name() : __RUN_LABELS
    }
    _AttributeMap = {
        
    }



# Complex type AnalysisFileType with content type EMPTY
class AnalysisFileType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AnalysisFileType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute checksum_method uses Python identifier checksum_method
    __checksum_method = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'checksum_method'), 'checksum_method', '__AbsentNamespace0_AnalysisFileType_checksum_method', STD_ANON_, required=True)
    
    checksum_method = property(__checksum_method.value, __checksum_method.set, None, u' Checksum method used. ')

    
    # Attribute checksum uses Python identifier checksum
    __checksum = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'checksum'), 'checksum', '__AbsentNamespace0_AnalysisFileType_checksum', pyxb.binding.datatypes.string, required=True)
    
    checksum = property(__checksum.value, __checksum.set, None, u' Checksum of the file. ')

    
    # Attribute filename uses Python identifier filename
    __filename = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'filename'), 'filename', '__AbsentNamespace0_AnalysisFileType_filename', pyxb.binding.datatypes.string, required=True)
    
    filename = property(__filename.value, __filename.set, None, u'The name or relative pathname of an analysis file. The actual file name extension is irrelevant so long as\n          the filetype is correctly indicated, and in the case of binary files the correct magic number is embedded in the file. ')

    
    # Attribute filetype uses Python identifier filetype
    __filetype = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'filetype'), 'filetype', '__AbsentNamespace0_AnalysisFileType_filetype', STD_ANON, required=True)
    
    filetype = property(__filetype.value, __filetype.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __checksum_method.name() : __checksum_method,
        __checksum.name() : __checksum,
        __filename.name() : __filename,
        __filetype.name() : __filetype
    }
Namespace.addCategoryObject('typeBinding', u'AnalysisFileType', AnalysisFileType)


# Complex type CTD_ANON_9 with content type ELEMENT_ONLY
class CTD_ANON_9 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element SEQUENCE uses Python identifier SEQUENCE
    __SEQUENCE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SEQUENCE'), 'SEQUENCE', '__AbsentNamespace0_CTD_ANON_9_SEQUENCE', True)

    
    SEQUENCE = property(__SEQUENCE.value, __SEQUENCE.set, None, u'Sequences which are labeled by Accession.version are optional in the\n                              list')


    _ElementMap = {
        __SEQUENCE.name() : __SEQUENCE
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_10 with content type ELEMENT_ONLY
class CTD_ANON_10 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element PROCESSING uses Python identifier PROCESSING
    __PROCESSING = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PROCESSING'), 'PROCESSING', '__AbsentNamespace0_CTD_ANON_10_PROCESSING', False)

    
    PROCESSING = property(__PROCESSING.value, __PROCESSING.set, None, u' Identify the tools and processing steps used to produce the abundance measurements\n                        (coverage tracks). ')


    _ElementMap = {
        __PROCESSING.name() : __PROCESSING
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_11 with content type ELEMENT_ONLY
class CTD_ANON_11 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element DESCRIPTION uses Python identifier DESCRIPTION
    __DESCRIPTION = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DESCRIPTION'), 'DESCRIPTION', '__AbsentNamespace0_CTD_ANON_11_DESCRIPTION', False)

    
    DESCRIPTION = property(__DESCRIPTION.value, __DESCRIPTION.set, None, u' Description of how the reference assembly was obtained especially when it is a\n                                    derivative of existing standards')

    
    # Element REFERENCE_SOURCE uses Python identifier REFERENCE_SOURCE
    __REFERENCE_SOURCE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'REFERENCE_SOURCE'), 'REFERENCE_SOURCE', '__AbsentNamespace0_CTD_ANON_11_REFERENCE_SOURCE', True)

    
    REFERENCE_SOURCE = property(__REFERENCE_SOURCE.value, __REFERENCE_SOURCE.set, None, u' A pointer to reference sequences using one of the Link mechanisms. ')


    _ElementMap = {
        __DESCRIPTION.name() : __DESCRIPTION,
        __REFERENCE_SOURCE.name() : __REFERENCE_SOURCE
    }
    _AttributeMap = {
        
    }



# Complex type AnalysisSetType with content type ELEMENT_ONLY
class AnalysisSetType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AnalysisSetType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ANALYSIS uses Python identifier ANALYSIS
    __ANALYSIS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ANALYSIS'), 'ANALYSIS', '__AbsentNamespace0_AnalysisSetType_ANALYSIS', True)

    
    ANALYSIS = property(__ANALYSIS.value, __ANALYSIS.set, None, None)


    _ElementMap = {
        __ANALYSIS.name() : __ANALYSIS
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'AnalysisSetType', AnalysisSetType)


# Complex type CTD_ANON_12 with content type EMPTY
class CTD_ANON_12 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute seq_label uses Python identifier seq_label
    __seq_label = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'seq_label'), 'seq_label', '__AbsentNamespace0_CTD_ANON_12_seq_label', pyxb.binding.datatypes.string)
    
    seq_label = property(__seq_label.value, __seq_label.set, None, u' This is how Reference Sequence is labeled in submission file(s). It is equivalent\n                                  to SQ label in BAM. Optional when submitted file uses INSDC accession.version')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'accession'), 'accession', '__AbsentNamespace0_CTD_ANON_12_accession', pyxb.binding.datatypes.token, required=True)
    
    accession = property(__accession.value, __accession.set, None, u' Accession.version with version being mandatory ')

    
    # Attribute gi uses Python identifier gi
    __gi = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'gi'), 'gi', '__AbsentNamespace0_CTD_ANON_12_gi', pyxb.binding.datatypes.integer)
    
    gi = property(__gi.value, __gi.set, None, u' NCBI - assigned gi ')

    
    # Attribute data_block_name uses Python identifier data_block_name
    __data_block_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'data_block_name'), 'data_block_name', '__AbsentNamespace0_CTD_ANON_12_data_block_name', pyxb.binding.datatypes.string)
    
    data_block_name = property(__data_block_name.value, __data_block_name.set, None, u' An optional attrtibute matching DATA_BLOCK/@name for a particular data file. This\n                                  is only needed when the same reference sequence has different labeling in the submission. ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __seq_label.name() : __seq_label,
        __accession.name() : __accession,
        __gi.name() : __gi,
        __data_block_name.name() : __data_block_name
    }



# Complex type AlignmentDirectivesType with content type ELEMENT_ONLY
class AlignmentDirectivesType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AlignmentDirectivesType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element alignment_includes_unaligned_reads uses Python identifier alignment_includes_unaligned_reads
    __alignment_includes_unaligned_reads = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'alignment_includes_unaligned_reads'), 'alignment_includes_unaligned_reads', '__AbsentNamespace0_AlignmentDirectivesType_alignment_includes_unaligned_reads', False)

    
    alignment_includes_unaligned_reads = property(__alignment_includes_unaligned_reads.value, __alignment_includes_unaligned_reads.set, None, u' Whether the reference alignment includes unaligned reads. ')

    
    # Element alignment_marks_duplicate_reads uses Python identifier alignment_marks_duplicate_reads
    __alignment_marks_duplicate_reads = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'alignment_marks_duplicate_reads'), 'alignment_marks_duplicate_reads', '__AbsentNamespace0_AlignmentDirectivesType_alignment_marks_duplicate_reads', False)

    
    alignment_marks_duplicate_reads = property(__alignment_marks_duplicate_reads.value, __alignment_marks_duplicate_reads.set, None, u' Whether the reference alignment identifies reads that appear to be duplicates. ')

    
    # Element alignment_includes_failed_reads uses Python identifier alignment_includes_failed_reads
    __alignment_includes_failed_reads = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'alignment_includes_failed_reads'), 'alignment_includes_failed_reads', '__AbsentNamespace0_AlignmentDirectivesType_alignment_includes_failed_reads', False)

    
    alignment_includes_failed_reads = property(__alignment_includes_failed_reads.value, __alignment_includes_failed_reads.set, None, u" Whether the reference alignment includes all reads regardless of whether they fail the instrument\n            vendor's quality check. ")


    _ElementMap = {
        __alignment_includes_unaligned_reads.name() : __alignment_includes_unaligned_reads,
        __alignment_marks_duplicate_reads.name() : __alignment_marks_duplicate_reads,
        __alignment_includes_failed_reads.name() : __alignment_includes_failed_reads
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'AlignmentDirectivesType', AlignmentDirectivesType)


# Complex type CTD_ANON_13 with content type ELEMENT_ONLY
class CTD_ANON_13 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element FILE uses Python identifier FILE
    __FILE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'FILE'), 'FILE', '__AbsentNamespace0_CTD_ANON_13_FILE', True)

    
    FILE = property(__FILE.value, __FILE.set, None, None)


    _ElementMap = {
        __FILE.name() : __FILE
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_14 with content type ELEMENT_ONLY
class CTD_ANON_14 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element IDENTIFIERS uses Python identifier IDENTIFIERS
    __IDENTIFIERS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'IDENTIFIERS'), 'IDENTIFIERS', '__AbsentNamespace0_CTD_ANON_14_IDENTIFIERS', False)

    
    IDENTIFIERS = property(__IDENTIFIERS.value, __IDENTIFIERS.set, None, u' Set of reference IDs to parent study record. This block is intended to replace the use of the\n                  less structured RefNameGroup identifiers. ')

    
    # Attribute refname uses Python identifier refname
    __refname = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refname'), 'refname', '__AbsentNamespace0_CTD_ANON_14_refname', pyxb.binding.datatypes.string)
    
    refname = property(__refname.value, __refname.set, None, u' Identifies a record by name that is known within the namespace defined by attribute "refcenter"\n                    Use this field when referencing an object for which an accession has not yet been issued. ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'accession'), 'accession', '__AbsentNamespace0_CTD_ANON_14_accession', pyxb.binding.datatypes.string)
    
    accession = property(__accession.value, __accession.set, None, u' Identifies a record by its accession. The scope of resolution is the entire Archive. ')

    
    # Attribute refcenter uses Python identifier refcenter
    __refcenter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refcenter'), 'refcenter', '__AbsentNamespace0_CTD_ANON_14_refcenter', pyxb.binding.datatypes.string)
    
    refcenter = property(__refcenter.value, __refcenter.set, None, u' The center namespace of the attribute "refname". When absent, the namespace is assumed to be the\n                    current submission. ')


    _ElementMap = {
        __IDENTIFIERS.name() : __IDENTIFIERS
    }
    _AttributeMap = {
        __refname.name() : __refname,
        __accession.name() : __accession,
        __refcenter.name() : __refcenter
    }



# Complex type CTD_ANON_15 with content type ELEMENT_ONLY
class CTD_ANON_15 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element TARGET uses Python identifier TARGET
    __TARGET = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TARGET'), 'TARGET', '__AbsentNamespace0_CTD_ANON_15_TARGET', True)

    
    TARGET = property(__TARGET.value, __TARGET.set, None, u' A SRA object that is the target of the analysis records. For example, a run, sample, or sequence\n                  can be the object of the analysis. ')

    
    # Element IDENTIFIERS uses Python identifier IDENTIFIERS
    __IDENTIFIERS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'IDENTIFIERS'), 'IDENTIFIERS', '__AbsentNamespace0_CTD_ANON_15_IDENTIFIERS', True)

    
    IDENTIFIERS = property(__IDENTIFIERS.value, __IDENTIFIERS.set, None, u' Set of reference IDs to target record. This block is intended to replace the use of the less\n                  structured RefNameGroup identifiers. ')


    _ElementMap = {
        __TARGET.name() : __TARGET,
        __IDENTIFIERS.name() : __IDENTIFIERS
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_16 with content type EMPTY
class CTD_ANON_16 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute refcenter uses Python identifier refcenter
    __refcenter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refcenter'), 'refcenter', '__AbsentNamespace0_CTD_ANON_16_refcenter', pyxb.binding.datatypes.string)
    
    refcenter = property(__refcenter.value, __refcenter.set, None, u' The center namespace of the attribute "refname". When absent, the namespace is assumed to be the\n                    current submission. ')

    
    # Attribute data_block_name uses Python identifier data_block_name
    __data_block_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'data_block_name'), 'data_block_name', '__AbsentNamespace0_CTD_ANON_16_data_block_name', pyxb.binding.datatypes.anySimpleType)
    
    data_block_name = property(__data_block_name.value, __data_block_name.set, None, u' An optional attrtibute matching DATA_BLOCK/@name for a particular data file. This\n                                  is only needed when the same SRA RUN has different labeling in the submission. ')

    
    # Attribute read_group_label uses Python identifier read_group_label
    __read_group_label = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'read_group_label'), 'read_group_label', '__AbsentNamespace0_CTD_ANON_16_read_group_label', pyxb.binding.datatypes.anySimpleType)
    
    read_group_label = property(__read_group_label.value, __read_group_label.set, None, u' This is how SRA run is labeled in submission file(s). It is equivalent to read\n                                  group (RG) labeling in BAM. Optional when submitted file use SRA accessions as labels ')

    
    # Attribute refname uses Python identifier refname
    __refname = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refname'), 'refname', '__AbsentNamespace0_CTD_ANON_16_refname', pyxb.binding.datatypes.string)
    
    refname = property(__refname.value, __refname.set, None, u' Identifies a record by name that is known within the namespace defined by attribute "refcenter"\n                    Use this field when referencing an object for which an accession has not yet been issued. ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'accession'), 'accession', '__AbsentNamespace0_CTD_ANON_16_accession', pyxb.binding.datatypes.string)
    
    accession = property(__accession.value, __accession.set, None, u' Identifies a record by its accession. The scope of resolution is the entire Archive. ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __refcenter.name() : __refcenter,
        __data_block_name.name() : __data_block_name,
        __read_group_label.name() : __read_group_label,
        __refname.name() : __refname,
        __accession.name() : __accession
    }



# Complex type CTD_ANON_17 with content type ELEMENT_ONLY
class CTD_ANON_17 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element RUN uses Python identifier RUN
    __RUN = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'RUN'), 'RUN', '__AbsentNamespace0_CTD_ANON_17_RUN', True)

    
    RUN = property(__RUN.value, __RUN.set, None, None)


    _ElementMap = {
        __RUN.name() : __RUN
    }
    _AttributeMap = {
        
    }



ANALYSIS = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ANALYSIS'), AnalysisType)
Namespace.addCategoryObject('elementBinding', ANALYSIS.name().localName(), ANALYSIS)

ANALYSIS_SET = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ANALYSIS_SET'), AnalysisSetType, documentation=u' An ANALYSIS_SET is a container of analysis objects with a shared namespace. ')
Namespace.addCategoryObject('elementBinding', ANALYSIS_SET.name().localName(), ANALYSIS_SET)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ANALYSIS_LINK'), common.LinkType, scope=CTD_ANON))
CTD_ANON._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, u'ANALYSIS_LINK')), min_occurs=1, max_occurs=1)
    )
CTD_ANON._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON._GroupModel, min_occurs=1L, max_occurs=None)



CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'NAME'), common.XRefType, scope=CTD_ANON_, documentation=u'Synonym Names additional to or in place of short_name. For example genbank,\n                                    gecoll accession.version.'))
CTD_ANON_._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, u'NAME')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_._GroupModel, min_occurs=1, max_occurs=1)



AlignmentProcessingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PIPELINE'), common.PipelineType, scope=AlignmentProcessingType))

AlignmentProcessingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DIRECTIVES'), AlignmentDirectivesType, scope=AlignmentProcessingType))
AlignmentProcessingType._GroupModel = pyxb.binding.content.GroupAll(
    pyxb.binding.content.ParticleModel(AlignmentProcessingType._UseForTag(pyxb.namespace.ExpandedName(None, u'PIPELINE')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(AlignmentProcessingType._UseForTag(pyxb.namespace.ExpandedName(None, u'DIRECTIVES')), min_occurs=1, max_occurs=1)
    )
AlignmentProcessingType._ContentModel = pyxb.binding.content.ParticleModel(AlignmentProcessingType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DE_NOVO_ASSEMBLY'), CTD_ANON_7, scope=CTD_ANON_2, documentation=u' A placement of sequences including trace, SRA, GI records into a multiple alignment from which a\n                  consensus is computed. This branch will be further specified in the future. '))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ABUNDANCE_MEASUREMENT'), CTD_ANON_10, scope=CTD_ANON_2, documentation=u' A track of read placement coverage used to measure abundance of a library with respect to a\n                  reference. This branch will be further specified in the future. '))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SEQUENCE_ANNOTATION'), CTD_ANON_3, scope=CTD_ANON_2, documentation=u' Per sequence annotation of named attributes and values. Example: Processed sequencing data for\n                  submission to dbEST without assembly. Reads have already been submitted to one of the sequence read archives in\n                  raw form. The fasta data submitted under this analysis object result from the following treatments, which may\n                  serve to filter reads from the raw dataset: - sequencing adapter removal - low quality trimming - poly-A tail\n                  removal - strand orientation - contaminant removal This branch will be further specified in the future. '))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'REFERENCE_ALIGNMENT'), CTD_ANON_8, scope=CTD_ANON_2, documentation=u' A multiple alignment of short reads against a reference substrate. '))
CTD_ANON_2._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, u'DE_NOVO_ASSEMBLY')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, u'REFERENCE_ALIGNMENT')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, u'SEQUENCE_ANNOTATION')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, u'ABUNDANCE_MEASUREMENT')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_2._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_2._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PROCESSING'), DefaultProcessingType, scope=CTD_ANON_3, documentation=u' Identify the tools and processing steps used to produce the sequence annotations. '))
CTD_ANON_3._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, u'PROCESSING')), min_occurs=1L, max_occurs=1L)
    )
CTD_ANON_3._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_3._GroupModel, min_occurs=1, max_occurs=1)



AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ANALYSIS_ATTRIBUTES'), CTD_ANON_4, scope=AnalysisType, documentation=u' Properties and attributes of an analysis. These can be entered as free-form tag-value pairs. For\n            certain studies, submitters may be asked to follow a community established ontology when describing the work. '))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DATA_BLOCK'), CTD_ANON_5, scope=AnalysisType, documentation=u' One or more blocks of data and associated file(s). Each data block may be a partition of the overall\n              analysis object. '))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TARGETS'), CTD_ANON_15, scope=AnalysisType, documentation=u' SRA object(s) targeted for analysis. Run - One or more runs that are assembled, aligned, or analyzed.\n            Sample - All the sequencing data for this sample are being assembled, aligned, or analyzed. Experiment - All the\n            sequencing data for this experiment are being assembled, aligned, or analyzed. Study - All the sequencing data for this\n            study are being assembled, aligned, or analyzed. '))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DESCRIPTION'), pyxb.binding.datatypes.string, scope=AnalysisType, documentation=u' Describes the contents of the analysis objects, their relationship with one another, the target\n            objects, and their place in the overall study. '))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TITLE'), pyxb.binding.datatypes.string, scope=AnalysisType, documentation=u' Title of the analyis object which will be displayed in short form in the Analysis browser and in\n            database search results. '))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ANALYSIS_LINKS'), CTD_ANON, scope=AnalysisType, documentation=u' Links to resources related to this analysis or analysis set (publication, datasets, online databases). '))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'STUDY_REF'), CTD_ANON_14, scope=AnalysisType, documentation=u' The STUDY_REF descriptor establishes the relationship of the analysis to the parent study. This can\n            either be the accession of an existing archived study record, or a reference to a new study record in the same\n            submission or same center (which does not yet have an accession). '))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ANALYSIS_TYPE'), CTD_ANON_2, scope=AnalysisType, documentation=u' Supported analysis types. '))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'IDENTIFIERS'), common.IdentifierType, scope=AnalysisType, documentation=u'List of primary and alternate identifiers including those records replacing or replaced by this record. '))
AnalysisType._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, u'DATA_BLOCK')), min_occurs=0L, max_occurs=None)
    )
AnalysisType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, u'IDENTIFIERS')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, u'TITLE')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, u'STUDY_REF')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, u'DESCRIPTION')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, u'ANALYSIS_TYPE')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, u'TARGETS')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(AnalysisType._GroupModel_, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, u'ANALYSIS_LINKS')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, u'ANALYSIS_ATTRIBUTES')), min_occurs=0L, max_occurs=1L)
    )
AnalysisType._ContentModel = pyxb.binding.content.ParticleModel(AnalysisType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ANALYSIS_ATTRIBUTE'), common.AttributeType, scope=CTD_ANON_4))
CTD_ANON_4._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, u'ANALYSIS_ATTRIBUTE')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_4._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_4._GroupModel, min_occurs=1L, max_occurs=None)



CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'FILES'), CTD_ANON_13, scope=CTD_ANON_5, documentation=u' Actual run data are contained in one of the files listed in the submission manifest. Each data\n                    block is represented by one SRF file, one SFF file, one compressed fastq file, or one compressed tar archive\n                    file. '))
CTD_ANON_5._GroupModel = pyxb.binding.content.GroupAll(
    pyxb.binding.content.ParticleModel(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, u'FILES')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_5._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_5._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'STANDARD'), CTD_ANON_, scope=CTD_ANON_6, documentation=u' Short name for the standard reference assembly used in the alignment. This should\n                              resolve into community accepted collection of reference sequences. '))

CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'CUSTOM'), CTD_ANON_11, scope=CTD_ANON_6, documentation=u' A list of ad-hoc reference sequences identified by database link. '))
CTD_ANON_6._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, u'STANDARD')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, u'CUSTOM')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_6._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_6._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PROCESSING'), DefaultProcessingType, scope=CTD_ANON_7, documentation=u' Identify the tools and processing steps used to produce the de novo assembly. '))
CTD_ANON_7._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, u'PROCESSING')), min_occurs=1L, max_occurs=1L)
    )
CTD_ANON_7._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_7._GroupModel, min_occurs=1, max_occurs=1)



DefaultProcessingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PIPELINE'), common.PipelineType, scope=DefaultProcessingType))
DefaultProcessingType._GroupModel = pyxb.binding.content.GroupAll(
    pyxb.binding.content.ParticleModel(DefaultProcessingType._UseForTag(pyxb.namespace.ExpandedName(None, u'PIPELINE')), min_occurs=1, max_occurs=1)
    )
DefaultProcessingType._ContentModel = pyxb.binding.content.ParticleModel(DefaultProcessingType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_8._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PROCESSING'), AlignmentProcessingType, scope=CTD_ANON_8, documentation=u' Identify the tools and processing steps used to produce the reference alignment, and\n                        specify directives used to load and interpret the data supplied by the submitter. '))

CTD_ANON_8._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SEQ_LABELS'), CTD_ANON_9, scope=CTD_ANON_8))

CTD_ANON_8._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ASSEMBLY'), CTD_ANON_6, scope=CTD_ANON_8, documentation=u' Specification of the reference collection of sequences used in the alignment. '))

CTD_ANON_8._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'RUN_LABELS'), CTD_ANON_17, scope=CTD_ANON_8, documentation=u'Mapping between the run (read group) labels used in the alignment data file, and the runs in\n                        the Archive. This is optional when SRA runs are reffered by accession in submitted data. '))
CTD_ANON_8._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(None, u'ASSEMBLY')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(None, u'RUN_LABELS')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(None, u'SEQ_LABELS')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(None, u'PROCESSING')), min_occurs=1L, max_occurs=1L)
    )
CTD_ANON_8._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_8._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SEQUENCE'), CTD_ANON_12, scope=CTD_ANON_9, documentation=u'Sequences which are labeled by Accession.version are optional in the\n                              list'))
CTD_ANON_9._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(None, u'SEQUENCE')), min_occurs=1L, max_occurs=None)
    )
CTD_ANON_9._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_9._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_10._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PROCESSING'), DefaultProcessingType, scope=CTD_ANON_10, documentation=u' Identify the tools and processing steps used to produce the abundance measurements\n                        (coverage tracks). '))
CTD_ANON_10._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(None, u'PROCESSING')), min_occurs=1L, max_occurs=1L)
    )
CTD_ANON_10._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_10._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_11._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DESCRIPTION'), pyxb.binding.datatypes.string, scope=CTD_ANON_11, documentation=u' Description of how the reference assembly was obtained especially when it is a\n                                    derivative of existing standards'))

CTD_ANON_11._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'REFERENCE_SOURCE'), common.LinkType, scope=CTD_ANON_11, documentation=u' A pointer to reference sequences using one of the Link mechanisms. '))
CTD_ANON_11._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_11._UseForTag(pyxb.namespace.ExpandedName(None, u'DESCRIPTION')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_11._UseForTag(pyxb.namespace.ExpandedName(None, u'REFERENCE_SOURCE')), min_occurs=1L, max_occurs=None)
    )
CTD_ANON_11._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_11._GroupModel, min_occurs=1, max_occurs=1)



AnalysisSetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ANALYSIS'), AnalysisType, scope=AnalysisSetType))
AnalysisSetType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AnalysisSetType._UseForTag(pyxb.namespace.ExpandedName(None, u'ANALYSIS')), min_occurs=1, max_occurs=1)
    )
AnalysisSetType._ContentModel = pyxb.binding.content.ParticleModel(AnalysisSetType._GroupModel, min_occurs=1L, max_occurs=None)



AlignmentDirectivesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'alignment_includes_unaligned_reads'), pyxb.binding.datatypes.boolean, scope=AlignmentDirectivesType, documentation=u' Whether the reference alignment includes unaligned reads. '))

AlignmentDirectivesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'alignment_marks_duplicate_reads'), pyxb.binding.datatypes.boolean, scope=AlignmentDirectivesType, documentation=u' Whether the reference alignment identifies reads that appear to be duplicates. '))

AlignmentDirectivesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'alignment_includes_failed_reads'), pyxb.binding.datatypes.boolean, scope=AlignmentDirectivesType, documentation=u" Whether the reference alignment includes all reads regardless of whether they fail the instrument\n            vendor's quality check. "))
AlignmentDirectivesType._GroupModel = pyxb.binding.content.GroupAll(
    pyxb.binding.content.ParticleModel(AlignmentDirectivesType._UseForTag(pyxb.namespace.ExpandedName(None, u'alignment_includes_unaligned_reads')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(AlignmentDirectivesType._UseForTag(pyxb.namespace.ExpandedName(None, u'alignment_marks_duplicate_reads')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(AlignmentDirectivesType._UseForTag(pyxb.namespace.ExpandedName(None, u'alignment_includes_failed_reads')), min_occurs=1L, max_occurs=1L)
    )
AlignmentDirectivesType._ContentModel = pyxb.binding.content.ParticleModel(AlignmentDirectivesType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'FILE'), AnalysisFileType, scope=CTD_ANON_13))
CTD_ANON_13._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(None, u'FILE')), min_occurs=1L, max_occurs=None)
    )
CTD_ANON_13._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_13._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_14._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'IDENTIFIERS'), common.IdentifierType, scope=CTD_ANON_14, documentation=u' Set of reference IDs to parent study record. This block is intended to replace the use of the\n                  less structured RefNameGroup identifiers. '))
CTD_ANON_14._GroupModel = pyxb.binding.content.GroupAll(
    pyxb.binding.content.ParticleModel(CTD_ANON_14._UseForTag(pyxb.namespace.ExpandedName(None, u'IDENTIFIERS')), min_occurs=0L, max_occurs=1L)
    )
CTD_ANON_14._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_14._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_15._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TARGET'), common.SraLinkType, scope=CTD_ANON_15, documentation=u' A SRA object that is the target of the analysis records. For example, a run, sample, or sequence\n                  can be the object of the analysis. '))

CTD_ANON_15._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'IDENTIFIERS'), common.IdentifierType, scope=CTD_ANON_15, documentation=u' Set of reference IDs to target record. This block is intended to replace the use of the less\n                  structured RefNameGroup identifiers. '))
CTD_ANON_15._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(None, u'TARGET')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(None, u'IDENTIFIERS')), min_occurs=0L, max_occurs=1L)
    )
CTD_ANON_15._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_15._GroupModel, min_occurs=1L, max_occurs=None)



CTD_ANON_17._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'RUN'), CTD_ANON_16, scope=CTD_ANON_17))
CTD_ANON_17._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_17._UseForTag(pyxb.namespace.ExpandedName(None, u'RUN')), min_occurs=1L, max_occurs=None)
    )
CTD_ANON_17._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_17._GroupModel, min_occurs=1, max_occurs=1)
