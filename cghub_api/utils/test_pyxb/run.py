# ./run.py
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2012-06-07 09:45:36.769014 by PyXB version 1.1.3
# Namespace AbsentNamespace0

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:63404904-b06c-11e1-b0b7-0026c7825912')

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
STD_ANON_.sra = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'sra', tag=u'sra')
STD_ANON_.kar = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'kar', tag=u'kar')
STD_ANON_.srf = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'srf', tag=u'srf')
STD_ANON_.sff = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'sff', tag=u'sff')
STD_ANON_.fastq = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'fastq', tag=u'fastq')
STD_ANON_.fasta = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'fasta', tag=u'fasta')
STD_ANON_.tab = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'tab', tag=u'tab')
STD_ANON_.n454_native = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'454_native', tag=u'n454_native')
STD_ANON_.n454_native_seq = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'454_native_seq', tag=u'n454_native_seq')
STD_ANON_.n454_native_qual = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'454_native_qual', tag=u'n454_native_qual')
STD_ANON_.Helicos_native = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'Helicos_native', tag=u'Helicos_native')
STD_ANON_.Illumina_native = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'Illumina_native', tag=u'Illumina_native')
STD_ANON_.Illumina_native_seq = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'Illumina_native_seq', tag=u'Illumina_native_seq')
STD_ANON_.Illumina_native_prb = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'Illumina_native_prb', tag=u'Illumina_native_prb')
STD_ANON_.Illumina_native_int = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'Illumina_native_int', tag=u'Illumina_native_int')
STD_ANON_.Illumina_native_qseq = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'Illumina_native_qseq', tag=u'Illumina_native_qseq')
STD_ANON_.Illumina_native_fastq = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'Illumina_native_fastq', tag=u'Illumina_native_fastq')
STD_ANON_.Illumina_native_scarf = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'Illumina_native_scarf', tag=u'Illumina_native_scarf')
STD_ANON_.SOLiD_native = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'SOLiD_native', tag=u'SOLiD_native')
STD_ANON_.SOLiD_native_csfasta = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'SOLiD_native_csfasta', tag=u'SOLiD_native_csfasta')
STD_ANON_.SOLiD_native_qual = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'SOLiD_native_qual', tag=u'SOLiD_native_qual')
STD_ANON_.PacBio_HDF5 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'PacBio_HDF5', tag=u'PacBio_HDF5')
STD_ANON_.bam = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'bam', tag=u'bam')
STD_ANON_.CompleteGenomics_native = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'CompleteGenomics_native', tag=u'CompleteGenomics_native')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_2 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_2._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_2, enum_prefix=None)
STD_ANON_2.phred = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value=u'phred', tag=u'phred')
STD_ANON_2.log_odds = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value=u'log-odds', tag=u'log_odds')
STD_ANON_2._InitializeFacetMap(STD_ANON_2._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_3 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_3._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_3, enum_prefix=None)
STD_ANON_3.ascii = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value=u'ascii', tag=u'ascii')
STD_ANON_3.decimal = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value=u'decimal', tag=u'decimal')
STD_ANON_3.hexadecimal = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value=u'hexadecimal', tag=u'hexadecimal')
STD_ANON_3._InitializeFacetMap(STD_ANON_3._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_4 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_4._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_4, enum_prefix=None)
STD_ANON_4.emptyString = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'!', tag='emptyString')
STD_ANON_4.emptyString_ = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'@', tag='emptyString_')
STD_ANON_4._InitializeFacetMap(STD_ANON_4._CF_enumeration)

# Complex type CTD_ANON with content type EMPTY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute refcenter uses Python identifier refcenter
    __refcenter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refcenter'), 'refcenter', '__AbsentNamespace0_CTD_ANON_refcenter', pyxb.binding.datatypes.string)
    
    refcenter = property(__refcenter.value, __refcenter.set, None, u'\n                    The center namespace of the attribute "refname". When absent, the namespace is assumed to be the current submission.\n                ')

    
    # Attribute refname uses Python identifier refname
    __refname = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refname'), 'refname', '__AbsentNamespace0_CTD_ANON_refname', pyxb.binding.datatypes.string)
    
    refname = property(__refname.value, __refname.set, None, u'\n                    Identifies a record by name that is known within the namespace defined by attribute "refcenter"\n                    Use this field when referencing an object for which an accession has not yet been issued.\n                ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'accession'), 'accession', '__AbsentNamespace0_CTD_ANON_accession', pyxb.binding.datatypes.string)
    
    accession = property(__accession.value, __accession.set, None, u'\n                    Identifies a record by its accession.  The scope of resolution is the entire Archive.\n                ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __refcenter.name() : __refcenter,
        __refname.name() : __refname,
        __accession.name() : __accession
    }



# Complex type CTD_ANON_ with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element FILE uses Python identifier FILE
    __FILE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'FILE'), 'FILE', '__AbsentNamespace0_CTD_ANON__FILE', True)

    
    FILE = property(__FILE.value, __FILE.set, None, None)


    _ElementMap = {
        __FILE.name() : __FILE
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
    
    # Element FILES uses Python identifier FILES
    __FILES = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'FILES'), 'FILES', '__AbsentNamespace0_CTD_ANON_2_FILES', False)

    
    FILES = property(__FILES.value, __FILES.set, None, u' Actual run data are contained in one of the files listed in the submission manifest. \n                                           Each data block is represented by one SRF file, one SFF file, one compressed fastq file, \n                                           or one compressed tar archive file.\n                                       ')

    
    # Attribute member_name uses Python identifier member_name
    __member_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'member_name'), 'member_name', '__AbsentNamespace0_CTD_ANON_2_member_name', pyxb.binding.datatypes.string)
    
    member_name = property(__member_name.value, __member_name.set, None, u'\n                                        Allow for an individual DATA_BLOCK to be associated with a member of a sample pool.\n                                    ')


    _ElementMap = {
        __FILES.name() : __FILES
    }
    _AttributeMap = {
        __member_name.name() : __member_name
    }



# Complex type RunSetType with content type ELEMENT_ONLY
class RunSetType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'RunSetType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element RUN uses Python identifier RUN
    __RUN = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'RUN'), 'RUN', '__AbsentNamespace0_RunSetType_RUN', True)

    
    RUN = property(__RUN.value, __RUN.set, None, None)


    _ElementMap = {
        __RUN.name() : __RUN
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'RunSetType', RunSetType)


# Complex type RunType with content type ELEMENT_ONLY
class RunType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'RunType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element PLATFORM uses Python identifier PLATFORM
    __PLATFORM = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PLATFORM'), 'PLATFORM', '__AbsentNamespace0_RunType_PLATFORM', False)

    
    PLATFORM = property(__PLATFORM.value, __PLATFORM.set, None, u'\n                            The platform block can be used to set the instrument configuration (eg read length), \n                            or to override a generic  instrument configuration defined at the level of SRA Experiment.                         \n                        ')

    
    # Element SPOT_DESCRIPTOR uses Python identifier SPOT_DESCRIPTOR
    __SPOT_DESCRIPTOR = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SPOT_DESCRIPTOR'), 'SPOT_DESCRIPTOR', '__AbsentNamespace0_RunType_SPOT_DESCRIPTOR', False)

    
    SPOT_DESCRIPTOR = property(__SPOT_DESCRIPTOR.value, __SPOT_DESCRIPTOR.set, None, u'\n                            The spot descriptor can be used to define a spot layout specific to the run, \n                            or to override a generic spot descriptor defined at the level of SRA Experiment\n                        ')

    
    # Element EXPERIMENT_REF uses Python identifier EXPERIMENT_REF
    __EXPERIMENT_REF = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'EXPERIMENT_REF'), 'EXPERIMENT_REF', '__AbsentNamespace0_RunType_EXPERIMENT_REF', False)

    
    EXPERIMENT_REF = property(__EXPERIMENT_REF.value, __EXPERIMENT_REF.set, None, u' The EXPERIMENT_REF descriptor identifies the parent experiment\n                            to which this run pertains.\n                            The Experiment object contains all the mapping information needed to decode each spot and map application reads\n                            to RUN objects.\n                        ')

    
    # Element RUN_ATTRIBUTES uses Python identifier RUN_ATTRIBUTES
    __RUN_ATTRIBUTES = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'RUN_ATTRIBUTES'), 'RUN_ATTRIBUTES', '__AbsentNamespace0_RunType_RUN_ATTRIBUTES', False)

    
    RUN_ATTRIBUTES = property(__RUN_ATTRIBUTES.value, __RUN_ATTRIBUTES.set, None, u'\n                            Properties and attributes of a RUN.  These can be entered as free-form \n                            tag-value pairs. For certain studies, submitters may be asked to follow a\n                            community established ontology when describing the work.\n                        ')

    
    # Element PROCESSING uses Python identifier PROCESSING
    __PROCESSING = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PROCESSING'), 'PROCESSING', '__AbsentNamespace0_RunType_PROCESSING', False)

    
    PROCESSING = property(__PROCESSING.value, __PROCESSING.set, None, u'\n                        Identify the processing steps used to produce the sequencing data, and specify\n                        directives used to load and interpret the data supplied by the submitter.\n                    ')

    
    # Element RUN_LINKS uses Python identifier RUN_LINKS
    __RUN_LINKS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'RUN_LINKS'), 'RUN_LINKS', '__AbsentNamespace0_RunType_RUN_LINKS', False)

    
    RUN_LINKS = property(__RUN_LINKS.value, __RUN_LINKS.set, None, u'\n                            Links to resources related to this RUN or RUN set (publication, datasets, online databases).\n                        ')

    
    # Element GAP_DESCRIPTOR uses Python identifier GAP_DESCRIPTOR
    __GAP_DESCRIPTOR = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'GAP_DESCRIPTOR'), 'GAP_DESCRIPTOR', '__AbsentNamespace0_RunType_GAP_DESCRIPTOR', False)

    
    GAP_DESCRIPTOR = property(__GAP_DESCRIPTOR.value, __GAP_DESCRIPTOR.set, None, u'\n                        The gap descriptor can be used to define a spot tag gaps and orientation specific to the run, \n                        or to override a generic gap descriptor defined at the level of SRA Experiment\n                    ')

    
    # Element DATA_BLOCK uses Python identifier DATA_BLOCK
    __DATA_BLOCK = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DATA_BLOCK'), 'DATA_BLOCK', '__AbsentNamespace0_RunType_DATA_BLOCK', False)

    
    DATA_BLOCK = property(__DATA_BLOCK.value, __DATA_BLOCK.set, None, u'\n                                 Convenience partition for processing large datasets.         \n                             ')

    
    # Element RUN_TYPE uses Python identifier RUN_TYPE
    __RUN_TYPE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'RUN_TYPE'), 'RUN_TYPE', '__AbsentNamespace0_RunType_RUN_TYPE', False)

    
    RUN_TYPE = property(__RUN_TYPE.value, __RUN_TYPE.set, None, u'The type of the run. ')

    
    # Attribute instrument_name uses Python identifier instrument_name
    __instrument_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'instrument_name'), 'instrument_name', '__AbsentNamespace0_RunType_instrument_name', pyxb.binding.datatypes.string)
    
    instrument_name = property(__instrument_name.value, __instrument_name.set, None, u'\n                        Center-assigned name or id of the instrument used in the run.\n                    ')

    
    # Attribute run_date uses Python identifier run_date
    __run_date = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'run_date'), 'run_date', '__AbsentNamespace0_RunType_run_date', pyxb.binding.datatypes.dateTime)
    
    run_date = property(__run_date.value, __run_date.set, None, u'\n                        ISO date when the run took place.  \n                    ')

    
    # Attribute center_name uses Python identifier center_name
    __center_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'center_name'), 'center_name', '__AbsentNamespace0_RunType_center_name', pyxb.binding.datatypes.string)
    
    center_name = property(__center_name.value, __center_name.set, None, u'\n                    Owner authority of this document and namespace for submitter\'s name of this document. \n                    If not provided, then the submitter is regarded as "Individual" and document resolution\n                    can only happen within the submission.\n                ')

    
    # Attribute broker_name uses Python identifier broker_name
    __broker_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'broker_name'), 'broker_name', '__AbsentNamespace0_RunType_broker_name', pyxb.binding.datatypes.string)
    
    broker_name = property(__broker_name.value, __broker_name.set, None, u'\n                    Broker authority of this document.  If not provided, then the broker is considered "direct".\n                ')

    
    # Attribute alias uses Python identifier alias
    __alias = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'alias'), 'alias', '__AbsentNamespace0_RunType_alias', pyxb.binding.datatypes.string)
    
    alias = property(__alias.value, __alias.set, None, u'\n                    Submitter designated name of the SRA document of this type.  At minimum alias should\n                    be unique throughout the submission of this document type.  If center_name is specified, the name should\n                    be unique in all submissions from that center of this document type.\n                ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'accession'), 'accession', '__AbsentNamespace0_RunType_accession', pyxb.binding.datatypes.string)
    
    accession = property(__accession.value, __accession.set, None, u"\n                    The document's accession as assigned by the Home Archive.\n                ")

    
    # Attribute run_center uses Python identifier run_center
    __run_center = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'run_center'), 'run_center', '__AbsentNamespace0_RunType_run_center', pyxb.binding.datatypes.string)
    
    run_center = property(__run_center.value, __run_center.set, None, u'\n                        If applicable, the name of the contract sequencing center that executed the run.\n                        Example: 454MSC.\n                    ')


    _ElementMap = {
        __PLATFORM.name() : __PLATFORM,
        __SPOT_DESCRIPTOR.name() : __SPOT_DESCRIPTOR,
        __EXPERIMENT_REF.name() : __EXPERIMENT_REF,
        __RUN_ATTRIBUTES.name() : __RUN_ATTRIBUTES,
        __PROCESSING.name() : __PROCESSING,
        __RUN_LINKS.name() : __RUN_LINKS,
        __GAP_DESCRIPTOR.name() : __GAP_DESCRIPTOR,
        __DATA_BLOCK.name() : __DATA_BLOCK,
        __RUN_TYPE.name() : __RUN_TYPE
    }
    _AttributeMap = {
        __instrument_name.name() : __instrument_name,
        __run_date.name() : __run_date,
        __center_name.name() : __center_name,
        __broker_name.name() : __broker_name,
        __alias.name() : __alias,
        __accession.name() : __accession,
        __run_center.name() : __run_center
    }
Namespace.addCategoryObject('typeBinding', u'RunType', RunType)


# Complex type CTD_ANON_3 with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element PIPELINE uses Python identifier PIPELINE
    __PIPELINE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PIPELINE'), 'PIPELINE', '__AbsentNamespace0_CTD_ANON_3_PIPELINE', False)

    
    PIPELINE = property(__PIPELINE.value, __PIPELINE.set, None, None)

    
    # Element DIRECTIVES uses Python identifier DIRECTIVES
    __DIRECTIVES = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DIRECTIVES'), 'DIRECTIVES', '__AbsentNamespace0_CTD_ANON_3_DIRECTIVES', False)

    
    DIRECTIVES = property(__DIRECTIVES.value, __DIRECTIVES.set, None, None)


    _ElementMap = {
        __PIPELINE.name() : __PIPELINE,
        __DIRECTIVES.name() : __DIRECTIVES
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_4 with content type ELEMENT_ONLY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element RUN_LINK uses Python identifier RUN_LINK
    __RUN_LINK = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'RUN_LINK'), 'RUN_LINK', '__AbsentNamespace0_CTD_ANON_4_RUN_LINK', True)

    
    RUN_LINK = property(__RUN_LINK.value, __RUN_LINK.set, None, None)


    _ElementMap = {
        __RUN_LINK.name() : __RUN_LINK
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
    
    # Element READ_LABEL uses Python identifier READ_LABEL
    __READ_LABEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'READ_LABEL'), 'READ_LABEL', '__AbsentNamespace0_CTD_ANON_5_READ_LABEL', True)

    
    READ_LABEL = property(__READ_LABEL.value, __READ_LABEL.set, None, u'\n                                                        The READ_LABEL can associate a certain file to a certain read_label defined in the SPOT_DESCRIPTOR.\n                                                        For example, the file "slide1_F3.csfasta" can be associated with read labeled F3 (the first forward read in a mate pair).\n                                                        The FILE may contain data from multiple READ_LABELs.\n                                                    ')

    
    # Attribute quality_scoring_system uses Python identifier quality_scoring_system
    __quality_scoring_system = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'quality_scoring_system'), 'quality_scoring_system', '__AbsentNamespace0_CTD_ANON_5_quality_scoring_system', STD_ANON_2)
    
    quality_scoring_system = property(__quality_scoring_system.value, __quality_scoring_system.set, None, u'\n                                                    How the input data are scored for quality.  \n                                                ')

    
    # Attribute quality_encoding uses Python identifier quality_encoding
    __quality_encoding = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'quality_encoding'), 'quality_encoding', '__AbsentNamespace0_CTD_ANON_5_quality_encoding', STD_ANON_3)
    
    quality_encoding = property(__quality_encoding.value, __quality_encoding.set, None, u'\n                                                    Character used in representing the minimum quality value.  Helps specify how to decode text rendering of quality data.\n                                                ')

    
    # Attribute checksum uses Python identifier checksum
    __checksum = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'checksum'), 'checksum', '__AbsentNamespace0_CTD_ANON_5_checksum', pyxb.binding.datatypes.string)
    
    checksum = property(__checksum.value, __checksum.set, None, u'\n                                                    Checksum of uncompressed file.\n                                                ')

    
    # Attribute unencrypted_checksum uses Python identifier unencrypted_checksum
    __unencrypted_checksum = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'unencrypted_checksum'), 'unencrypted_checksum', '__AbsentNamespace0_CTD_ANON_5_unencrypted_checksum', pyxb.binding.datatypes.string)
    
    unencrypted_checksum = property(__unencrypted_checksum.value, __unencrypted_checksum.set, None, u'\n                                                            Checksum of unenrypted file(used in conjunction with checksum of encrypted file).\n                                                        ')

    
    # Attribute filetype uses Python identifier filetype
    __filetype = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'filetype'), 'filetype', '__AbsentNamespace0_CTD_ANON_5_filetype', STD_ANON_, required=True)
    
    filetype = property(__filetype.value, __filetype.set, None, u' The run data file model.')

    
    # Attribute ascii_offset uses Python identifier ascii_offset
    __ascii_offset = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ascii_offset'), 'ascii_offset', '__AbsentNamespace0_CTD_ANON_5_ascii_offset', STD_ANON_4)
    
    ascii_offset = property(__ascii_offset.value, __ascii_offset.set, None, u'\n                                                    Character used in representing the minimum quality value.  Helps specify how to decode text rendering of quality data.\n                                                ')

    
    # Attribute filename uses Python identifier filename
    __filename = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'filename'), 'filename', '__AbsentNamespace0_CTD_ANON_5_filename', pyxb.binding.datatypes.string, required=True)
    
    filename = property(__filename.value, __filename.set, None, u'The name or relative pathname of a run data file.')

    
    # Attribute checksum_method uses Python identifier checksum_method
    __checksum_method = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'checksum_method'), 'checksum_method', '__AbsentNamespace0_CTD_ANON_5_checksum_method', STD_ANON)
    
    checksum_method = property(__checksum_method.value, __checksum_method.set, None, u'\n                                                    Checksum method used.\n                                                ')


    _ElementMap = {
        __READ_LABEL.name() : __READ_LABEL
    }
    _AttributeMap = {
        __quality_scoring_system.name() : __quality_scoring_system,
        __quality_encoding.name() : __quality_encoding,
        __checksum.name() : __checksum,
        __unencrypted_checksum.name() : __unencrypted_checksum,
        __filetype.name() : __filetype,
        __ascii_offset.name() : __ascii_offset,
        __filename.name() : __filename,
        __checksum_method.name() : __checksum_method
    }



# Complex type CTD_ANON_6 with content type ELEMENT_ONLY
class CTD_ANON_6 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element RUN_ATTRIBUTE uses Python identifier RUN_ATTRIBUTE
    __RUN_ATTRIBUTE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'RUN_ATTRIBUTE'), 'RUN_ATTRIBUTE', '__AbsentNamespace0_CTD_ANON_6_RUN_ATTRIBUTE', True)

    
    RUN_ATTRIBUTE = property(__RUN_ATTRIBUTE.value, __RUN_ATTRIBUTE.set, None, None)


    _ElementMap = {
        __RUN_ATTRIBUTE.name() : __RUN_ATTRIBUTE
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
    
    # Element REFERENCE_ALIGNMENT uses Python identifier REFERENCE_ALIGNMENT
    __REFERENCE_ALIGNMENT = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'REFERENCE_ALIGNMENT'), 'REFERENCE_ALIGNMENT', '__AbsentNamespace0_CTD_ANON_7_REFERENCE_ALIGNMENT', False)

    
    REFERENCE_ALIGNMENT = property(__REFERENCE_ALIGNMENT.value, __REFERENCE_ALIGNMENT.set, None, u'')


    _ElementMap = {
        __REFERENCE_ALIGNMENT.name() : __REFERENCE_ALIGNMENT
    }
    _AttributeMap = {
        
    }



RUN_SET = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'RUN_SET'), RunSetType, documentation=u'\n                RUN_SET serves as a container for a set of runs and a name space\n                for establishing referential integrity between them. \n            ')
Namespace.addCategoryObject('elementBinding', RUN_SET.name().localName(), RUN_SET)

RUN = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'RUN'), RunType)
Namespace.addCategoryObject('elementBinding', RUN.name().localName(), RUN)



CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'FILE'), CTD_ANON_5, scope=CTD_ANON_))
CTD_ANON_._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, u'FILE')), min_occurs=1, max_occurs=None)
    )
CTD_ANON_._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_._GroupModel, min_occurs=1L, max_occurs=1L)



CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'FILES'), CTD_ANON_, scope=CTD_ANON_2, documentation=u' Actual run data are contained in one of the files listed in the submission manifest. \n                                           Each data block is represented by one SRF file, one SFF file, one compressed fastq file, \n                                           or one compressed tar archive file.\n                                       '))
CTD_ANON_2._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, u'FILES')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_2._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_2._GroupModel, min_occurs=1, max_occurs=1)



RunSetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'RUN'), RunType, scope=RunSetType))
RunSetType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(RunSetType._UseForTag(pyxb.namespace.ExpandedName(None, u'RUN')), min_occurs=1, max_occurs=None)
    )
RunSetType._ContentModel = pyxb.binding.content.ParticleModel(RunSetType._GroupModel, min_occurs=1L, max_occurs=1L)



RunType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PLATFORM'), common.PlatformType, scope=RunType, documentation=u'\n                            The platform block can be used to set the instrument configuration (eg read length), \n                            or to override a generic  instrument configuration defined at the level of SRA Experiment.                         \n                        '))

RunType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SPOT_DESCRIPTOR'), common.SpotDescriptorType, scope=RunType, documentation=u'\n                            The spot descriptor can be used to define a spot layout specific to the run, \n                            or to override a generic spot descriptor defined at the level of SRA Experiment\n                        '))

RunType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'EXPERIMENT_REF'), CTD_ANON, scope=RunType, documentation=u' The EXPERIMENT_REF descriptor identifies the parent experiment\n                            to which this run pertains.\n                            The Experiment object contains all the mapping information needed to decode each spot and map application reads\n                            to RUN objects.\n                        '))

RunType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'RUN_ATTRIBUTES'), CTD_ANON_6, scope=RunType, documentation=u'\n                            Properties and attributes of a RUN.  These can be entered as free-form \n                            tag-value pairs. For certain studies, submitters may be asked to follow a\n                            community established ontology when describing the work.\n                        '))

RunType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PROCESSING'), CTD_ANON_3, scope=RunType, documentation=u'\n                        Identify the processing steps used to produce the sequencing data, and specify\n                        directives used to load and interpret the data supplied by the submitter.\n                    '))

RunType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'RUN_LINKS'), CTD_ANON_4, scope=RunType, documentation=u'\n                            Links to resources related to this RUN or RUN set (publication, datasets, online databases).\n                        '))

RunType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'GAP_DESCRIPTOR'), common.GapDescriptorType, scope=RunType, documentation=u'\n                        The gap descriptor can be used to define a spot tag gaps and orientation specific to the run, \n                        or to override a generic gap descriptor defined at the level of SRA Experiment\n                    '))

RunType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DATA_BLOCK'), CTD_ANON_2, scope=RunType, documentation=u'\n                                 Convenience partition for processing large datasets.         \n                             '))

RunType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'RUN_TYPE'), CTD_ANON_7, scope=RunType, documentation=u'The type of the run. '))
RunType._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(RunType._UseForTag(pyxb.namespace.ExpandedName(None, u'DATA_BLOCK')), min_occurs=0L, max_occurs=1L)
    )
RunType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(RunType._UseForTag(pyxb.namespace.ExpandedName(None, u'EXPERIMENT_REF')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(RunType._UseForTag(pyxb.namespace.ExpandedName(None, u'SPOT_DESCRIPTOR')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(RunType._UseForTag(pyxb.namespace.ExpandedName(None, u'GAP_DESCRIPTOR')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(RunType._UseForTag(pyxb.namespace.ExpandedName(None, u'PLATFORM')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(RunType._UseForTag(pyxb.namespace.ExpandedName(None, u'PROCESSING')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(RunType._UseForTag(pyxb.namespace.ExpandedName(None, u'RUN_TYPE')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(RunType._GroupModel_, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(RunType._UseForTag(pyxb.namespace.ExpandedName(None, u'RUN_LINKS')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(RunType._UseForTag(pyxb.namespace.ExpandedName(None, u'RUN_ATTRIBUTES')), min_occurs=0L, max_occurs=1L)
    )
RunType._ContentModel = pyxb.binding.content.ParticleModel(RunType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PIPELINE'), common.PipelineType, scope=CTD_ANON_3))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DIRECTIVES'), common.SequencingDirectivesType, scope=CTD_ANON_3))
CTD_ANON_3._GroupModel = pyxb.binding.content.GroupAll(
    pyxb.binding.content.ParticleModel(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, u'PIPELINE')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, u'DIRECTIVES')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_3._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_3._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'RUN_LINK'), common.LinkType, scope=CTD_ANON_4))
CTD_ANON_4._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, u'RUN_LINK')), min_occurs=1, max_occurs=None)
    )
CTD_ANON_4._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_4._GroupModel, min_occurs=1L, max_occurs=1L)



CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'READ_LABEL'), pyxb.binding.datatypes.string, scope=CTD_ANON_5, documentation=u'\n                                                        The READ_LABEL can associate a certain file to a certain read_label defined in the SPOT_DESCRIPTOR.\n                                                        For example, the file "slide1_F3.csfasta" can be associated with read labeled F3 (the first forward read in a mate pair).\n                                                        The FILE may contain data from multiple READ_LABELs.\n                                                    '))
CTD_ANON_5._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, u'READ_LABEL')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_5._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_5._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'RUN_ATTRIBUTE'), common.AttributeType, scope=CTD_ANON_6))
CTD_ANON_6._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, u'RUN_ATTRIBUTE')), min_occurs=1, max_occurs=None)
    )
CTD_ANON_6._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_6._GroupModel, min_occurs=1L, max_occurs=1L)



CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'REFERENCE_ALIGNMENT'), common.ReferenceSequenceType, scope=CTD_ANON_7, documentation=u''))
CTD_ANON_7._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, u'REFERENCE_ALIGNMENT')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_7._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_7._GroupModel, min_occurs=1, max_occurs=1)
