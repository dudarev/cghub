# ./analysis.py
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2012-06-07 09:42:28.551140 by PyXB version 1.1.3
# Namespace AbsentNamespace0

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:f3135fb8-b06b-11e1-80b2-0026c7825912')

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
STD_ANON.MD5 = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'MD5', tag=u'MD5')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_ (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_, enum_prefix=None)
STD_ANON_.tab = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'tab', tag=u'tab')
STD_ANON_.bam = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'bam', tag=u'bam')
STD_ANON_.bai = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'bai', tag=u'bai')
STD_ANON_.vcf = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'vcf', tag=u'vcf')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration)

# Complex type CTD_ANON with content type EMPTY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute alias uses Python identifier alias
    __alias = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'alias'), 'alias', '__AbsentNamespace0_CTD_ANON_alias', pyxb.binding.datatypes.string)
    
    alias = property(__alias.value, __alias.set, None, u'\n                    Submitter designated name of the SRA document of this type.  At minimum alias should\n                    be unique throughout the submission of this document type.  If center_name is specified, the name should\n                    be unique in all submissions from that center of this document type.\n                ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'accession'), 'accession', '__AbsentNamespace0_CTD_ANON_accession', pyxb.binding.datatypes.string)
    
    accession = property(__accession.value, __accession.set, None, u"\n                    The document's accession as assigned by the Home Archive.\n                ")

    
    # Attribute broker_name uses Python identifier broker_name
    __broker_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'broker_name'), 'broker_name', '__AbsentNamespace0_CTD_ANON_broker_name', pyxb.binding.datatypes.string)
    
    broker_name = property(__broker_name.value, __broker_name.set, None, u'\n                    Broker authority of this document.  If not provided, then the broker is considered "direct".\n                ')

    
    # Attribute center_name uses Python identifier center_name
    __center_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'center_name'), 'center_name', '__AbsentNamespace0_CTD_ANON_center_name', pyxb.binding.datatypes.string)
    
    center_name = property(__center_name.value, __center_name.set, None, u'\n                    Owner authority of this document and namespace for submitter\'s name of this document. \n                    If not provided, then the submitter is regarded as "Individual" and document resolution\n                    can only happen within the submission.\n                ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __alias.name() : __alias,
        __accession.name() : __accession,
        __broker_name.name() : __broker_name,
        __center_name.name() : __center_name
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


# Complex type AnalysisType with content type ELEMENT_ONLY
class AnalysisType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AnalysisType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element TITLE uses Python identifier TITLE
    __TITLE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TITLE'), 'TITLE', '__AbsentNamespace0_AnalysisType_TITLE', False)

    
    TITLE = property(__TITLE.value, __TITLE.set, None, u'Title of the analyis object which will be displayed in\n                        database search results. ')

    
    # Element RUN_REF uses Python identifier RUN_REF
    __RUN_REF = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'RUN_REF'), 'RUN_REF', '__AbsentNamespace0_AnalysisType_RUN_REF', True)

    
    RUN_REF = property(__RUN_REF.value, __RUN_REF.set, None, u'One or more runs associated with the\n                        analysis.')

    
    # Element SAMPLE_REF uses Python identifier SAMPLE_REF
    __SAMPLE_REF = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SAMPLE_REF'), 'SAMPLE_REF', '__AbsentNamespace0_AnalysisType_SAMPLE_REF', True)

    
    SAMPLE_REF = property(__SAMPLE_REF.value, __SAMPLE_REF.set, None, u'One of more samples associated with the\n                        analysis.')

    
    # Element ANALYSIS_LINKS uses Python identifier ANALYSIS_LINKS
    __ANALYSIS_LINKS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ANALYSIS_LINKS'), 'ANALYSIS_LINKS', '__AbsentNamespace0_AnalysisType_ANALYSIS_LINKS', False)

    
    ANALYSIS_LINKS = property(__ANALYSIS_LINKS.value, __ANALYSIS_LINKS.set, None, u' Links to resources related to this analysis.\n                    ')

    
    # Element DESCRIPTION uses Python identifier DESCRIPTION
    __DESCRIPTION = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DESCRIPTION'), 'DESCRIPTION', '__AbsentNamespace0_AnalysisType_DESCRIPTION', False)

    
    DESCRIPTION = property(__DESCRIPTION.value, __DESCRIPTION.set, None, u'Describes the analysis in detail.')

    
    # Element FILES uses Python identifier FILES
    __FILES = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'FILES'), 'FILES', '__AbsentNamespace0_AnalysisType_FILES', False)

    
    FILES = property(__FILES.value, __FILES.set, None, u'Files associated with the\n                                        analysis.')

    
    # Element STUDY_REF uses Python identifier STUDY_REF
    __STUDY_REF = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'STUDY_REF'), 'STUDY_REF', '__AbsentNamespace0_AnalysisType_STUDY_REF', False)

    
    STUDY_REF = property(__STUDY_REF.value, __STUDY_REF.set, None, u'Establishes a relationship between the analysis and the\n                        parent study.')

    
    # Element ANALYSIS_ATTRIBUTES uses Python identifier ANALYSIS_ATTRIBUTES
    __ANALYSIS_ATTRIBUTES = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ANALYSIS_ATTRIBUTES'), 'ANALYSIS_ATTRIBUTES', '__AbsentNamespace0_AnalysisType_ANALYSIS_ATTRIBUTES', False)

    
    ANALYSIS_ATTRIBUTES = property(__ANALYSIS_ATTRIBUTES.value, __ANALYSIS_ATTRIBUTES.set, None, u'Properties and attributes of an analysis. These can be\n                        entered as free-form tag-value pairs.')

    
    # Element ANALYSIS_TYPE uses Python identifier ANALYSIS_TYPE
    __ANALYSIS_TYPE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ANALYSIS_TYPE'), 'ANALYSIS_TYPE', '__AbsentNamespace0_AnalysisType_ANALYSIS_TYPE', False)

    
    ANALYSIS_TYPE = property(__ANALYSIS_TYPE.value, __ANALYSIS_TYPE.set, None, u'The type of the analysis. ')

    
    # Attribute broker_name uses Python identifier broker_name
    __broker_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'broker_name'), 'broker_name', '__AbsentNamespace0_AnalysisType_broker_name', pyxb.binding.datatypes.string)
    
    broker_name = property(__broker_name.value, __broker_name.set, None, u'\n                    Broker authority of this document.  If not provided, then the broker is considered "direct".\n                ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'accession'), 'accession', '__AbsentNamespace0_AnalysisType_accession', pyxb.binding.datatypes.string)
    
    accession = property(__accession.value, __accession.set, None, u"\n                    The document's accession as assigned by the Home Archive.\n                ")

    
    # Attribute center_name uses Python identifier center_name
    __center_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'center_name'), 'center_name', '__AbsentNamespace0_AnalysisType_center_name', pyxb.binding.datatypes.string)
    
    center_name = property(__center_name.value, __center_name.set, None, u'\n                    Owner authority of this document and namespace for submitter\'s name of this document. \n                    If not provided, then the submitter is regarded as "Individual" and document resolution\n                    can only happen within the submission.\n                ')

    
    # Attribute analysis_date uses Python identifier analysis_date
    __analysis_date = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'analysis_date'), 'analysis_date', '__AbsentNamespace0_AnalysisType_analysis_date', pyxb.binding.datatypes.dateTime)
    
    analysis_date = property(__analysis_date.value, __analysis_date.set, None, u'The date when this analysis was produced. ')

    
    # Attribute analysis_center uses Python identifier analysis_center
    __analysis_center = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'analysis_center'), 'analysis_center', '__AbsentNamespace0_AnalysisType_analysis_center', pyxb.binding.datatypes.string)
    
    analysis_center = property(__analysis_center.value, __analysis_center.set, None, u'If applicable, the center name of the institution responsible\n                    for this analysis. ')

    
    # Attribute alias uses Python identifier alias
    __alias = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'alias'), 'alias', '__AbsentNamespace0_AnalysisType_alias', pyxb.binding.datatypes.string)
    
    alias = property(__alias.value, __alias.set, None, u'\n                    Submitter designated name of the SRA document of this type.  At minimum alias should\n                    be unique throughout the submission of this document type.  If center_name is specified, the name should\n                    be unique in all submissions from that center of this document type.\n                ')


    _ElementMap = {
        __TITLE.name() : __TITLE,
        __RUN_REF.name() : __RUN_REF,
        __SAMPLE_REF.name() : __SAMPLE_REF,
        __ANALYSIS_LINKS.name() : __ANALYSIS_LINKS,
        __DESCRIPTION.name() : __DESCRIPTION,
        __FILES.name() : __FILES,
        __STUDY_REF.name() : __STUDY_REF,
        __ANALYSIS_ATTRIBUTES.name() : __ANALYSIS_ATTRIBUTES,
        __ANALYSIS_TYPE.name() : __ANALYSIS_TYPE
    }
    _AttributeMap = {
        __broker_name.name() : __broker_name,
        __accession.name() : __accession,
        __center_name.name() : __center_name,
        __analysis_date.name() : __analysis_date,
        __analysis_center.name() : __analysis_center,
        __alias.name() : __alias
    }
Namespace.addCategoryObject('typeBinding', u'AnalysisType', AnalysisType)


# Complex type CTD_ANON_ with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ANALYSIS_ATTRIBUTE uses Python identifier ANALYSIS_ATTRIBUTE
    __ANALYSIS_ATTRIBUTE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ANALYSIS_ATTRIBUTE'), 'ANALYSIS_ATTRIBUTE', '__AbsentNamespace0_CTD_ANON__ANALYSIS_ATTRIBUTE', True)

    
    ANALYSIS_ATTRIBUTE = property(__ANALYSIS_ATTRIBUTE.value, __ANALYSIS_ATTRIBUTE.set, None, None)


    _ElementMap = {
        __ANALYSIS_ATTRIBUTE.name() : __ANALYSIS_ATTRIBUTE
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_2 with content type EMPTY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType

    _ElementMap = {
        
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_3 with content type EMPTY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'accession'), 'accession', '__AbsentNamespace0_CTD_ANON_3_accession', pyxb.binding.datatypes.string)
    
    accession = property(__accession.value, __accession.set, None, u'\n                    Identifies a record by its accession.  The scope of resolution is the entire Archive.\n                ')

    
    # Attribute label uses Python identifier label
    __label = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'label'), 'label', '__AbsentNamespace0_CTD_ANON_3_label', pyxb.binding.datatypes.string)
    
    label = property(__label.value, __label.set, None, u'A label associating the sample with BAM (@RG/ID or @RG/SM) or VCF file samples.')

    
    # Attribute refname uses Python identifier refname
    __refname = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refname'), 'refname', '__AbsentNamespace0_CTD_ANON_3_refname', pyxb.binding.datatypes.string)
    
    refname = property(__refname.value, __refname.set, None, u'\n                    Identifies a record by name that is known within the namespace defined by attribute "refcenter"\n                    Use this field when referencing an object for which an accession has not yet been issued.\n                ')

    
    # Attribute refcenter uses Python identifier refcenter
    __refcenter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refcenter'), 'refcenter', '__AbsentNamespace0_CTD_ANON_3_refcenter', pyxb.binding.datatypes.string)
    
    refcenter = property(__refcenter.value, __refcenter.set, None, u'\n                    The center namespace of the attribute "refname". When absent, the namespace is assumed to be the current submission.\n                ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __accession.name() : __accession,
        __label.name() : __label,
        __refname.name() : __refname,
        __refcenter.name() : __refcenter
    }



# Complex type AnalysisFileType with content type ELEMENT_ONLY
class AnalysisFileType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AnalysisFileType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element CHECKLIST uses Python identifier CHECKLIST
    __CHECKLIST = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'CHECKLIST'), 'CHECKLIST', '__AbsentNamespace0_AnalysisFileType_CHECKLIST', False)

    
    CHECKLIST = property(__CHECKLIST.value, __CHECKLIST.set, None, None)

    
    # Attribute checksum uses Python identifier checksum
    __checksum = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'checksum'), 'checksum', '__AbsentNamespace0_AnalysisFileType_checksum', pyxb.binding.datatypes.string, required=True)
    
    checksum = property(__checksum.value, __checksum.set, None, u' Checksum of the file. ')

    
    # Attribute filename uses Python identifier filename
    __filename = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'filename'), 'filename', '__AbsentNamespace0_AnalysisFileType_filename', pyxb.binding.datatypes.string, required=True)
    
    filename = property(__filename.value, __filename.set, None, u'The file name. ')

    
    # Attribute filetype uses Python identifier filetype
    __filetype = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'filetype'), 'filetype', '__AbsentNamespace0_AnalysisFileType_filetype', STD_ANON_, required=True)
    
    filetype = property(__filetype.value, __filetype.set, None, u'The type of the file.')

    
    # Attribute unencrypted_checksum uses Python identifier unencrypted_checksum
    __unencrypted_checksum = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'unencrypted_checksum'), 'unencrypted_checksum', '__AbsentNamespace0_AnalysisFileType_unencrypted_checksum', pyxb.binding.datatypes.string)
    
    unencrypted_checksum = property(__unencrypted_checksum.value, __unencrypted_checksum.set, None, u'\n                                                            Checksum of unenrypted file(used in conjunction with checksum of encrypted file).\n                                                        ')

    
    # Attribute checksum_method uses Python identifier checksum_method
    __checksum_method = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'checksum_method'), 'checksum_method', '__AbsentNamespace0_AnalysisFileType_checksum_method', STD_ANON, required=True)
    
    checksum_method = property(__checksum_method.value, __checksum_method.set, None, u' Checksum method used. ')


    _ElementMap = {
        __CHECKLIST.name() : __CHECKLIST
    }
    _AttributeMap = {
        __checksum.name() : __checksum,
        __filename.name() : __filename,
        __filetype.name() : __filetype,
        __unencrypted_checksum.name() : __unencrypted_checksum,
        __checksum_method.name() : __checksum_method
    }
Namespace.addCategoryObject('typeBinding', u'AnalysisFileType', AnalysisFileType)


# Complex type CTD_ANON_4 with content type ELEMENT_ONLY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element FILE uses Python identifier FILE
    __FILE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'FILE'), 'FILE', '__AbsentNamespace0_CTD_ANON_4_FILE', True)

    
    FILE = property(__FILE.value, __FILE.set, None, None)


    _ElementMap = {
        __FILE.name() : __FILE
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_5 with content type EMPTY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute refcenter uses Python identifier refcenter
    __refcenter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refcenter'), 'refcenter', '__AbsentNamespace0_CTD_ANON_5_refcenter', pyxb.binding.datatypes.string)
    
    refcenter = property(__refcenter.value, __refcenter.set, None, u'\n                    The center namespace of the attribute "refname". When absent, the namespace is assumed to be the current submission.\n                ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'accession'), 'accession', '__AbsentNamespace0_CTD_ANON_5_accession', pyxb.binding.datatypes.string)
    
    accession = property(__accession.value, __accession.set, None, u'\n                    Identifies a record by its accession.  The scope of resolution is the entire Archive.\n                ')

    
    # Attribute refname uses Python identifier refname
    __refname = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refname'), 'refname', '__AbsentNamespace0_CTD_ANON_5_refname', pyxb.binding.datatypes.string)
    
    refname = property(__refname.value, __refname.set, None, u'\n                    Identifies a record by name that is known within the namespace defined by attribute "refcenter"\n                    Use this field when referencing an object for which an accession has not yet been issued.\n                ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __refcenter.name() : __refcenter,
        __accession.name() : __accession,
        __refname.name() : __refname
    }



# Complex type CTD_ANON_6 with content type EMPTY
class CTD_ANON_6 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute refcenter uses Python identifier refcenter
    __refcenter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refcenter'), 'refcenter', '__AbsentNamespace0_CTD_ANON_6_refcenter', pyxb.binding.datatypes.string)
    
    refcenter = property(__refcenter.value, __refcenter.set, None, u'\n                    The center namespace of the attribute "refname". When absent, the namespace is assumed to be the current submission.\n                ')

    
    # Attribute refname uses Python identifier refname
    __refname = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refname'), 'refname', '__AbsentNamespace0_CTD_ANON_6_refname', pyxb.binding.datatypes.string)
    
    refname = property(__refname.value, __refname.set, None, u'\n                    Identifies a record by name that is known within the namespace defined by attribute "refcenter"\n                    Use this field when referencing an object for which an accession has not yet been issued.\n                ')

    
    # Attribute label uses Python identifier label
    __label = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'label'), 'label', '__AbsentNamespace0_CTD_ANON_6_label', pyxb.binding.datatypes.string)
    
    label = property(__label.value, __label.set, None, u'A label associating the run with BAM (@RG/ID).')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'accession'), 'accession', '__AbsentNamespace0_CTD_ANON_6_accession', pyxb.binding.datatypes.string)
    
    accession = property(__accession.value, __accession.set, None, u'\n                    Identifies a record by its accession.  The scope of resolution is the entire Archive.\n                ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __refcenter.name() : __refcenter,
        __refname.name() : __refname,
        __label.name() : __label,
        __accession.name() : __accession
    }



# Complex type CTD_ANON_7 with content type ELEMENT_ONLY
class CTD_ANON_7 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ANALYSIS_LINK uses Python identifier ANALYSIS_LINK
    __ANALYSIS_LINK = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ANALYSIS_LINK'), 'ANALYSIS_LINK', '__AbsentNamespace0_CTD_ANON_7_ANALYSIS_LINK', True)

    
    ANALYSIS_LINK = property(__ANALYSIS_LINK.value, __ANALYSIS_LINK.set, None, None)


    _ElementMap = {
        __ANALYSIS_LINK.name() : __ANALYSIS_LINK
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_8 with content type ELEMENT_ONLY
class CTD_ANON_8 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element REFERENCE_ALIGNMENT uses Python identifier REFERENCE_ALIGNMENT
    __REFERENCE_ALIGNMENT = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'REFERENCE_ALIGNMENT'), 'REFERENCE_ALIGNMENT', '__AbsentNamespace0_CTD_ANON_8_REFERENCE_ALIGNMENT', False)

    
    REFERENCE_ALIGNMENT = property(__REFERENCE_ALIGNMENT.value, __REFERENCE_ALIGNMENT.set, None, u'')

    
    # Element SEQUENCE_ANNOTATION uses Python identifier SEQUENCE_ANNOTATION
    __SEQUENCE_ANNOTATION = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SEQUENCE_ANNOTATION'), 'SEQUENCE_ANNOTATION', '__AbsentNamespace0_CTD_ANON_8_SEQUENCE_ANNOTATION', False)

    
    SEQUENCE_ANNOTATION = property(__SEQUENCE_ANNOTATION.value, __SEQUENCE_ANNOTATION.set, None, u'Annotated sequences. ')

    
    # Element SEQUENCE_VARIATION uses Python identifier SEQUENCE_VARIATION
    __SEQUENCE_VARIATION = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SEQUENCE_VARIATION'), 'SEQUENCE_VARIATION', '__AbsentNamespace0_CTD_ANON_8_SEQUENCE_VARIATION', False)

    
    SEQUENCE_VARIATION = property(__SEQUENCE_VARIATION.value, __SEQUENCE_VARIATION.set, None, None)


    _ElementMap = {
        __REFERENCE_ALIGNMENT.name() : __REFERENCE_ALIGNMENT,
        __SEQUENCE_ANNOTATION.name() : __SEQUENCE_ANNOTATION,
        __SEQUENCE_VARIATION.name() : __SEQUENCE_VARIATION
    }
    _AttributeMap = {
        
    }



ANALYSIS_SET = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ANALYSIS_SET'), AnalysisSetType, documentation=u'A container of analysis objects. ')
Namespace.addCategoryObject('elementBinding', ANALYSIS_SET.name().localName(), ANALYSIS_SET)

ANALYSIS = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ANALYSIS'), AnalysisType)
Namespace.addCategoryObject('elementBinding', ANALYSIS.name().localName(), ANALYSIS)



AnalysisSetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ANALYSIS'), AnalysisType, scope=AnalysisSetType))
AnalysisSetType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AnalysisSetType._UseForTag(pyxb.namespace.ExpandedName(None, u'ANALYSIS')), min_occurs=1, max_occurs=1)
    )
AnalysisSetType._ContentModel = pyxb.binding.content.ParticleModel(AnalysisSetType._GroupModel, min_occurs=1L, max_occurs=None)



AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TITLE'), pyxb.binding.datatypes.string, scope=AnalysisType, documentation=u'Title of the analyis object which will be displayed in\n                        database search results. '))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'RUN_REF'), CTD_ANON_6, scope=AnalysisType, documentation=u'One or more runs associated with the\n                        analysis.'))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SAMPLE_REF'), CTD_ANON_3, scope=AnalysisType, documentation=u'One of more samples associated with the\n                        analysis.'))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ANALYSIS_LINKS'), CTD_ANON_7, scope=AnalysisType, documentation=u' Links to resources related to this analysis.\n                    '))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DESCRIPTION'), pyxb.binding.datatypes.string, scope=AnalysisType, documentation=u'Describes the analysis in detail.'))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'FILES'), CTD_ANON_4, scope=AnalysisType, documentation=u'Files associated with the\n                                        analysis.'))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'STUDY_REF'), CTD_ANON_5, scope=AnalysisType, documentation=u'Establishes a relationship between the analysis and the\n                        parent study.'))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ANALYSIS_ATTRIBUTES'), CTD_ANON_, scope=AnalysisType, documentation=u'Properties and attributes of an analysis. These can be\n                        entered as free-form tag-value pairs.'))

AnalysisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ANALYSIS_TYPE'), CTD_ANON_8, scope=AnalysisType, documentation=u'The type of the analysis. '))
AnalysisType._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, u'FILES')), min_occurs=1, max_occurs=1)
    )
AnalysisType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, u'TITLE')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, u'DESCRIPTION')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, u'STUDY_REF')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, u'SAMPLE_REF')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, u'RUN_REF')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, u'ANALYSIS_TYPE')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(AnalysisType._GroupModel_, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, u'ANALYSIS_LINKS')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(AnalysisType._UseForTag(pyxb.namespace.ExpandedName(None, u'ANALYSIS_ATTRIBUTES')), min_occurs=0L, max_occurs=1L)
    )
AnalysisType._ContentModel = pyxb.binding.content.ParticleModel(AnalysisType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ANALYSIS_ATTRIBUTE'), common.AttributeType, scope=CTD_ANON_))
CTD_ANON_._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, u'ANALYSIS_ATTRIBUTE')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_._GroupModel, min_occurs=1L, max_occurs=None)



AnalysisFileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'CHECKLIST'), CTD_ANON, scope=AnalysisFileType))
AnalysisFileType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AnalysisFileType._UseForTag(pyxb.namespace.ExpandedName(None, u'CHECKLIST')), min_occurs=0L, max_occurs=1)
    )
AnalysisFileType._ContentModel = pyxb.binding.content.ParticleModel(AnalysisFileType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'FILE'), AnalysisFileType, scope=CTD_ANON_4))
CTD_ANON_4._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, u'FILE')), min_occurs=1L, max_occurs=None)
    )
CTD_ANON_4._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_4._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ANALYSIS_LINK'), common.LinkType, scope=CTD_ANON_7))
CTD_ANON_7._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, u'ANALYSIS_LINK')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_7._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_7._GroupModel, min_occurs=1L, max_occurs=None)



CTD_ANON_8._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'REFERENCE_ALIGNMENT'), common.ReferenceSequenceType, scope=CTD_ANON_8, documentation=u''))

CTD_ANON_8._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SEQUENCE_ANNOTATION'), CTD_ANON_2, scope=CTD_ANON_8, documentation=u'Annotated sequences. '))

CTD_ANON_8._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SEQUENCE_VARIATION'), common.ReferenceSequenceType, scope=CTD_ANON_8))
CTD_ANON_8._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(None, u'REFERENCE_ALIGNMENT')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(None, u'SEQUENCE_VARIATION')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(None, u'SEQUENCE_ANNOTATION')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_8._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_8._GroupModel, min_occurs=1, max_occurs=1)
