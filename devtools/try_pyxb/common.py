# ./common.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:1c06abdc99453cc1e399eecb45b4dd01ec9af52b
# Generated 2012-08-06 22:21:52.436544 by PyXB version 1.1.5-DEV
# Namespace SRA.common [xmlns:com]

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:f9e0c94c-dffb-11e1-a305-0026c7825912')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

Namespace = pyxb.namespace.NamespaceForURI(u'SRA.common', create_if_missing=True)
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
STD_ANON.Helicos_HeliScope = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'Helicos HeliScope', tag=u'Helicos_HeliScope')
STD_ANON.unspecified = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'unspecified', tag=u'unspecified')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_ (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_, enum_prefix=None)
STD_ANON_.AB_SOLiD_System = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'AB SOLiD System', tag=u'AB_SOLiD_System')
STD_ANON_.AB_SOLiD_System_2_0 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'AB SOLiD System 2.0', tag=u'AB_SOLiD_System_2_0')
STD_ANON_.AB_SOLiD_System_3_0 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'AB SOLiD System 3.0', tag=u'AB_SOLiD_System_3_0')
STD_ANON_.AB_SOLiD_3_Plus_System = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'AB SOLiD 3 Plus System', tag=u'AB_SOLiD_3_Plus_System')
STD_ANON_.AB_SOLiD_4_System = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'AB SOLiD 4 System', tag=u'AB_SOLiD_4_System')
STD_ANON_.AB_SOLiD_4hq_System = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'AB SOLiD 4hq System', tag=u'AB_SOLiD_4hq_System')
STD_ANON_.AB_SOLiD_PI_System = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'AB SOLiD PI System', tag=u'AB_SOLiD_PI_System')
STD_ANON_.AB_SOLiD_5500 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'AB SOLiD 5500', tag=u'AB_SOLiD_5500')
STD_ANON_.AB_SOLiD_5500xl = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'AB SOLiD 5500xl', tag=u'AB_SOLiD_5500xl')
STD_ANON_.AB_5500_Genetic_Analyzer = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'AB 5500 Genetic Analyzer', tag=u'AB_5500_Genetic_Analyzer')
STD_ANON_.AB_5500xl_Genetic_Analyzer = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'AB 5500xl Genetic Analyzer', tag=u'AB_5500xl_Genetic_Analyzer')
STD_ANON_.unspecified = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'unspecified', tag=u'unspecified')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_2 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_2._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_2, enum_prefix=None)
STD_ANON_2.absolute_frequency = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value=u'absolute_frequency', tag=u'absolute_frequency')
STD_ANON_2.relative_frequency = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value=u'relative_frequency', tag=u'relative_frequency')
STD_ANON_2._InitializeFacetMap(STD_ANON_2._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_3 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_3._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_3, enum_prefix=None)
STD_ANON_3.Application_Read = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value=u'Application Read', tag=u'Application_Read')
STD_ANON_3.Technical_Read = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value=u'Technical Read', tag=u'Technical_Read')
STD_ANON_3._InitializeFacetMap(STD_ANON_3._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_4 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_4._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_4, enum_prefix=None)
STD_ANON_4.Forward = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'Forward', tag=u'Forward')
STD_ANON_4.Reverse = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'Reverse', tag=u'Reverse')
STD_ANON_4.Adapter = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'Adapter', tag=u'Adapter')
STD_ANON_4.Primer = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'Primer', tag=u'Primer')
STD_ANON_4.Linker = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'Linker', tag=u'Linker')
STD_ANON_4.BarCode = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'BarCode', tag=u'BarCode')
STD_ANON_4.Other = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'Other', tag=u'Other')
STD_ANON_4._InitializeFacetMap(STD_ANON_4._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_5 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_5._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_5, enum_prefix=None)
STD_ANON_5.Complete_Genomics = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'Complete Genomics', tag=u'Complete_Genomics')
STD_ANON_5.unspecified = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'unspecified', tag=u'unspecified')
STD_ANON_5._InitializeFacetMap(STD_ANON_5._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_6 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_6._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_6, enum_prefix=None)
STD_ANON_6.PacBio_RS = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value=u'PacBio RS', tag=u'PacBio_RS')
STD_ANON_6.unspecified = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value=u'unspecified', tag=u'unspecified')
STD_ANON_6._InitializeFacetMap(STD_ANON_6._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_7 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_7._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_7, enum_prefix=None)
STD_ANON_7.Ion_Torrent_PGM = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value=u'Ion Torrent PGM', tag=u'Ion_Torrent_PGM')
STD_ANON_7.Ion_Torrent_Proton = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value=u'Ion Torrent Proton', tag=u'Ion_Torrent_Proton')
STD_ANON_7.unspecified = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value=u'unspecified', tag=u'unspecified')
STD_ANON_7._InitializeFacetMap(STD_ANON_7._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_8 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_8._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_8, enum_prefix=None)
STD_ANON_8.AB_3730xL_Genetic_Analyzer = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'AB 3730xL Genetic Analyzer', tag=u'AB_3730xL_Genetic_Analyzer')
STD_ANON_8.AB_3730_Genetic_Analyzer = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'AB 3730 Genetic Analyzer', tag=u'AB_3730_Genetic_Analyzer')
STD_ANON_8.AB_3500xL_Genetic_Analyzer = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'AB 3500xL Genetic Analyzer', tag=u'AB_3500xL_Genetic_Analyzer')
STD_ANON_8.AB_3500_Genetic_Analyzer = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'AB 3500 Genetic Analyzer', tag=u'AB_3500_Genetic_Analyzer')
STD_ANON_8.AB_3130xL_Genetic_Analyzer = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'AB 3130xL Genetic Analyzer', tag=u'AB_3130xL_Genetic_Analyzer')
STD_ANON_8.AB_3130_Genetic_Analyzer = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'AB 3130 Genetic Analyzer', tag=u'AB_3130_Genetic_Analyzer')
STD_ANON_8.AB_310_Genetic_Analyzer = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'AB 310 Genetic Analyzer', tag=u'AB_310_Genetic_Analyzer')
STD_ANON_8.unspecified = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'unspecified', tag=u'unspecified')
STD_ANON_8._InitializeFacetMap(STD_ANON_8._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_9 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_9._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_9, enum_prefix=None)
STD_ANON_9.STUDY = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'STUDY', tag=u'STUDY')
STD_ANON_9.SAMPLE = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'SAMPLE', tag=u'SAMPLE')
STD_ANON_9.ANALYSIS = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'ANALYSIS', tag=u'ANALYSIS')
STD_ANON_9.EXPERIMENT = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'EXPERIMENT', tag=u'EXPERIMENT')
STD_ANON_9.RUN = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'RUN', tag=u'RUN')
STD_ANON_9._InitializeFacetMap(STD_ANON_9._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_10 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_10._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_10, enum_prefix=None)
STD_ANON_10.WGS = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'WGS', tag=u'WGS')
STD_ANON_10.WGA = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'WGA', tag=u'WGA')
STD_ANON_10.WXS = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'WXS', tag=u'WXS')
STD_ANON_10.RNA_Seq = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'RNA-Seq', tag=u'RNA_Seq')
STD_ANON_10.miRNA_Seq = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'miRNA-Seq', tag=u'miRNA_Seq')
STD_ANON_10.WCS = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'WCS', tag=u'WCS')
STD_ANON_10.CLONE = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'CLONE', tag=u'CLONE')
STD_ANON_10.POOLCLONE = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'POOLCLONE', tag=u'POOLCLONE')
STD_ANON_10.AMPLICON = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'AMPLICON', tag=u'AMPLICON')
STD_ANON_10.CLONEEND = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'CLONEEND', tag=u'CLONEEND')
STD_ANON_10.FINISHING = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'FINISHING', tag=u'FINISHING')
STD_ANON_10.ChIP_Seq = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'ChIP-Seq', tag=u'ChIP_Seq')
STD_ANON_10.MNase_Seq = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'MNase-Seq', tag=u'MNase_Seq')
STD_ANON_10.DNase_Hypersensitivity = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'DNase-Hypersensitivity', tag=u'DNase_Hypersensitivity')
STD_ANON_10.Bisulfite_Seq = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'Bisulfite-Seq', tag=u'Bisulfite_Seq')
STD_ANON_10.EST = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'EST', tag=u'EST')
STD_ANON_10.FL_cDNA = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'FL-cDNA', tag=u'FL_cDNA')
STD_ANON_10.CTS = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'CTS', tag=u'CTS')
STD_ANON_10.MRE_Seq = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'MRE-Seq', tag=u'MRE_Seq')
STD_ANON_10.MeDIP_Seq = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'MeDIP-Seq', tag=u'MeDIP_Seq')
STD_ANON_10.MBD_Seq = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'MBD-Seq', tag=u'MBD_Seq')
STD_ANON_10.Tn_Seq = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'Tn-Seq', tag=u'Tn_Seq')
STD_ANON_10.OTHER = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'OTHER', tag=u'OTHER')
STD_ANON_10._InitializeFacetMap(STD_ANON_10._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_11 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_11._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_11, enum_prefix=None)
STD_ANON_11.GENOMIC = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value=u'GENOMIC', tag=u'GENOMIC')
STD_ANON_11.TRANSCRIPTOMIC = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value=u'TRANSCRIPTOMIC', tag=u'TRANSCRIPTOMIC')
STD_ANON_11.METAGENOMIC = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value=u'METAGENOMIC', tag=u'METAGENOMIC')
STD_ANON_11.METATRANSCRIPTOMIC = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value=u'METATRANSCRIPTOMIC', tag=u'METATRANSCRIPTOMIC')
STD_ANON_11.NON_GENOMIC = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value=u'NON GENOMIC', tag=u'NON_GENOMIC')
STD_ANON_11.SYNTHETIC = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value=u'SYNTHETIC', tag=u'SYNTHETIC')
STD_ANON_11.VIRAL_RNA = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value=u'VIRAL RNA', tag=u'VIRAL_RNA')
STD_ANON_11.OTHER = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value=u'OTHER', tag=u'OTHER')
STD_ANON_11._InitializeFacetMap(STD_ANON_11._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_12 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_12._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_12, enum_prefix=None)
STD_ANON_12.leave_as_pool = STD_ANON_12._CF_enumeration.addEnumeration(unicode_value=u'leave_as_pool', tag=u'leave_as_pool')
STD_ANON_12.submitter_demultiplexed = STD_ANON_12._CF_enumeration.addEnumeration(unicode_value=u'submitter_demultiplexed', tag=u'submitter_demultiplexed')
STD_ANON_12._InitializeFacetMap(STD_ANON_12._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_13 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_13._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_13, enum_prefix=None)
STD_ANON_13.n454_GS = STD_ANON_13._CF_enumeration.addEnumeration(unicode_value=u'454 GS', tag=u'n454_GS')
STD_ANON_13.n454_GS_20 = STD_ANON_13._CF_enumeration.addEnumeration(unicode_value=u'454 GS 20', tag=u'n454_GS_20')
STD_ANON_13.n454_GS_FLX = STD_ANON_13._CF_enumeration.addEnumeration(unicode_value=u'454 GS FLX', tag=u'n454_GS_FLX')
STD_ANON_13.n454_GS_FLX_ = STD_ANON_13._CF_enumeration.addEnumeration(unicode_value=u'454 GS FLX+', tag=u'n454_GS_FLX_')
STD_ANON_13.n454_GS_FLX_Titanium = STD_ANON_13._CF_enumeration.addEnumeration(unicode_value=u'454 GS FLX Titanium', tag=u'n454_GS_FLX_Titanium')
STD_ANON_13.n454_GS_Junior = STD_ANON_13._CF_enumeration.addEnumeration(unicode_value=u'454 GS Junior', tag=u'n454_GS_Junior')
STD_ANON_13.unspecified = STD_ANON_13._CF_enumeration.addEnumeration(unicode_value=u'unspecified', tag=u'unspecified')
STD_ANON_13._InitializeFacetMap(STD_ANON_13._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_14 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_14._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_14, enum_prefix=None)
STD_ANON_14.full = STD_ANON_14._CF_enumeration.addEnumeration(unicode_value=u'full', tag=u'full')
STD_ANON_14.start = STD_ANON_14._CF_enumeration.addEnumeration(unicode_value=u'start', tag=u'start')
STD_ANON_14.end = STD_ANON_14._CF_enumeration.addEnumeration(unicode_value=u'end', tag=u'end')
STD_ANON_14._InitializeFacetMap(STD_ANON_14._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_15 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_15._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_15, enum_prefix=None)
STD_ANON_15.Illumina_Genome_Analyzer = STD_ANON_15._CF_enumeration.addEnumeration(unicode_value=u'Illumina Genome Analyzer', tag=u'Illumina_Genome_Analyzer')
STD_ANON_15.Illumina_Genome_Analyzer_II = STD_ANON_15._CF_enumeration.addEnumeration(unicode_value=u'Illumina Genome Analyzer II', tag=u'Illumina_Genome_Analyzer_II')
STD_ANON_15.Illumina_Genome_Analyzer_IIx = STD_ANON_15._CF_enumeration.addEnumeration(unicode_value=u'Illumina Genome Analyzer IIx', tag=u'Illumina_Genome_Analyzer_IIx')
STD_ANON_15.Illumina_HiSeq_2500 = STD_ANON_15._CF_enumeration.addEnumeration(unicode_value=u'Illumina HiSeq 2500', tag=u'Illumina_HiSeq_2500')
STD_ANON_15.Illumina_HiSeq_2000 = STD_ANON_15._CF_enumeration.addEnumeration(unicode_value=u'Illumina HiSeq 2000', tag=u'Illumina_HiSeq_2000')
STD_ANON_15.Illumina_HiSeq_1000 = STD_ANON_15._CF_enumeration.addEnumeration(unicode_value=u'Illumina HiSeq 1000', tag=u'Illumina_HiSeq_1000')
STD_ANON_15.Illumina_MiSeq = STD_ANON_15._CF_enumeration.addEnumeration(unicode_value=u'Illumina MiSeq', tag=u'Illumina_MiSeq')
STD_ANON_15.Illumina_HiScanSQ = STD_ANON_15._CF_enumeration.addEnumeration(unicode_value=u'Illumina HiScanSQ', tag=u'Illumina_HiScanSQ')
STD_ANON_15.unspecified = STD_ANON_15._CF_enumeration.addEnumeration(unicode_value=u'unspecified', tag=u'unspecified')
STD_ANON_15._InitializeFacetMap(STD_ANON_15._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_16 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_16._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_16, enum_prefix=None)
STD_ANON_16.n16S_rRNA = STD_ANON_16._CF_enumeration.addEnumeration(unicode_value=u'16S rRNA', tag=u'n16S_rRNA')
STD_ANON_16.n18S_rRNA = STD_ANON_16._CF_enumeration.addEnumeration(unicode_value=u'18S rRNA', tag=u'n18S_rRNA')
STD_ANON_16.RBCL = STD_ANON_16._CF_enumeration.addEnumeration(unicode_value=u'RBCL', tag=u'RBCL')
STD_ANON_16.matK = STD_ANON_16._CF_enumeration.addEnumeration(unicode_value=u'matK', tag=u'matK')
STD_ANON_16.COX1 = STD_ANON_16._CF_enumeration.addEnumeration(unicode_value=u'COX1', tag=u'COX1')
STD_ANON_16.ITS1_5_8S_ITS2 = STD_ANON_16._CF_enumeration.addEnumeration(unicode_value=u'ITS1-5.8S-ITS2', tag=u'ITS1_5_8S_ITS2')
STD_ANON_16.exome = STD_ANON_16._CF_enumeration.addEnumeration(unicode_value=u'exome', tag=u'exome')
STD_ANON_16.other = STD_ANON_16._CF_enumeration.addEnumeration(unicode_value=u'other', tag=u'other')
STD_ANON_16._InitializeFacetMap(STD_ANON_16._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_17 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_17._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_17, enum_prefix=None)
STD_ANON_17.RANDOM = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'RANDOM', tag=u'RANDOM')
STD_ANON_17.PCR = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'PCR', tag=u'PCR')
STD_ANON_17.RANDOM_PCR = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'RANDOM PCR', tag=u'RANDOM_PCR')
STD_ANON_17.RT_PCR = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'RT-PCR', tag=u'RT_PCR')
STD_ANON_17.HMPR = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'HMPR', tag=u'HMPR')
STD_ANON_17.MF = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'MF', tag=u'MF')
STD_ANON_17.CF_S = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'CF-S', tag=u'CF_S')
STD_ANON_17.CF_M = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'CF-M', tag=u'CF_M')
STD_ANON_17.CF_H = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'CF-H', tag=u'CF_H')
STD_ANON_17.CF_T = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'CF-T', tag=u'CF_T')
STD_ANON_17.MSLL = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'MSLL', tag=u'MSLL')
STD_ANON_17.cDNA = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'cDNA', tag=u'cDNA')
STD_ANON_17.ChIP = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'ChIP', tag=u'ChIP')
STD_ANON_17.MNase = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'MNase', tag=u'MNase')
STD_ANON_17.DNAse = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'DNAse', tag=u'DNAse')
STD_ANON_17.Hybrid_Selection = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'Hybrid Selection', tag=u'Hybrid_Selection')
STD_ANON_17.Reduced_Representation = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'Reduced Representation', tag=u'Reduced_Representation')
STD_ANON_17.Restriction_Digest = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'Restriction Digest', tag=u'Restriction_Digest')
STD_ANON_17.n5_methylcytidine_antibody = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'5-methylcytidine antibody', tag=u'n5_methylcytidine_antibody')
STD_ANON_17.MBD2_protein_methyl_CpG_binding_domain = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'MBD2 protein methyl-CpG binding domain', tag=u'MBD2_protein_methyl_CpG_binding_domain')
STD_ANON_17.CAGE = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'CAGE', tag=u'CAGE')
STD_ANON_17.RACE = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'RACE', tag=u'RACE')
STD_ANON_17.size_fractionation = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'size fractionation', tag=u'size_fractionation')
STD_ANON_17.MDA = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'MDA', tag=u'MDA')
STD_ANON_17.padlock_probes_capture_method = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'padlock probes capture method', tag=u'padlock_probes_capture_method')
STD_ANON_17.other = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'other', tag=u'other')
STD_ANON_17.unspecified = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'unspecified', tag=u'unspecified')
STD_ANON_17._InitializeFacetMap(STD_ANON_17._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_18 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_18._InitializeFacetMap()

# Atomic SimpleTypeDefinition
class STD_ANON_19 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_19._InitializeFacetMap()

# Complex type CTD_ANON with content type EMPTY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType

    _ElementMap = {
        
    }
    _AttributeMap = {
        
    }



# Complex type PipelineType with content type ELEMENT_ONLY
class PipelineType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'PipelineType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element PIPE_SECTION uses Python identifier PIPE_SECTION
    __PIPE_SECTION = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PIPE_SECTION'), 'PIPE_SECTION', '__SRA_common_PipelineType_PIPE_SECTION', True)

    
    PIPE_SECTION = property(__PIPE_SECTION.value, __PIPE_SECTION.set, None, None)


    _ElementMap = {
        __PIPE_SECTION.name() : __PIPE_SECTION
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'PipelineType', PipelineType)


# Complex type CTD_ANON_ with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element LOCUS uses Python identifier LOCUS
    __LOCUS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LOCUS'), 'LOCUS', '__SRA_common_CTD_ANON__LOCUS', True)

    
    LOCUS = property(__LOCUS.value, __LOCUS.set, None, None)


    _ElementMap = {
        __LOCUS.name() : __LOCUS
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
    
    # Element statistic_mean uses Python identifier statistic_mean
    __statistic_mean = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'statistic_mean'), 'statistic_mean', '__SRA_common_CTD_ANON_2_statistic_mean', False)

    
    statistic_mean = property(__statistic_mean.value, __statistic_mean.set, None, None)

    
    # Element statistic_median uses Python identifier statistic_median
    __statistic_median = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'statistic_median'), 'statistic_median', '__SRA_common_CTD_ANON_2_statistic_median', False)

    
    statistic_median = property(__statistic_median.value, __statistic_median.set, None, None)

    
    # Element interval uses Python identifier interval
    __interval = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'interval'), 'interval', '__SRA_common_CTD_ANON_2_interval', False)

    
    interval = property(__interval.value, __interval.set, None, None)

    
    # Element histogram uses Python identifier histogram
    __histogram = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'histogram'), 'histogram', '__SRA_common_CTD_ANON_2_histogram', False)

    
    histogram = property(__histogram.value, __histogram.set, None, None)

    
    # Attribute link5 uses Python identifier link5
    __link5 = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'link5'), 'link5', '__SRA_common_CTD_ANON_2_link5', pyxb.binding.datatypes.anySimpleType, unicode_default=u'NULL')
    
    link5 = property(__link5.value, __link5.set, None, u" Specify the read label at the 5' end of the gap, or NULL if it's the\n                                            first tag. ")

    
    # Attribute link3 uses Python identifier link3
    __link3 = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'link3'), 'link3', '__SRA_common_CTD_ANON_2_link3', pyxb.binding.datatypes.anySimpleType, unicode_default=u'NULL')
    
    link3 = property(__link3.value, __link3.set, None, u" Specify the read label at the 3' end of the gap, or NULL if it's the\n                                            last tag. ")


    _ElementMap = {
        __statistic_mean.name() : __statistic_mean,
        __statistic_median.name() : __statistic_median,
        __interval.name() : __interval,
        __histogram.name() : __histogram
    }
    _AttributeMap = {
        __link5.name() : __link5,
        __link3.name() : __link3
    }



# Complex type CTD_ANON_3 with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element INSTRUMENT_MODEL uses Python identifier INSTRUMENT_MODEL
    __INSTRUMENT_MODEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), 'INSTRUMENT_MODEL', '__SRA_common_CTD_ANON_3_INSTRUMENT_MODEL', False)

    
    INSTRUMENT_MODEL = property(__INSTRUMENT_MODEL.value, __INSTRUMENT_MODEL.set, None, None)


    _ElementMap = {
        __INSTRUMENT_MODEL.name() : __INSTRUMENT_MODEL
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
    
    # Element URL uses Python identifier URL
    __URL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'URL'), 'URL', '__SRA_common_CTD_ANON_4_URL', False)

    
    URL = property(__URL.value, __URL.set, None, u'An URL to the cross-references accession. ')

    
    # Element DB uses Python identifier DB
    __DB = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DB'), 'DB', '__SRA_common_CTD_ANON_4_DB', False)

    
    DB = property(__DB.value, __DB.set, None, u'DDBJ controlled vocabulary of permitted cross references. ')

    
    # Element ID uses Python identifier ID
    __ID = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__SRA_common_CTD_ANON_4_ID', False)

    
    ID = property(__ID.value, __ID.set, None, u'Accession in the referenced database. ')

    
    # Element LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LABEL'), 'LABEL', '__SRA_common_CTD_ANON_4_LABEL', False)

    
    LABEL = property(__LABEL.value, __LABEL.set, None, u'A textual description of the cross-reference. ')


    _ElementMap = {
        __URL.name() : __URL,
        __DB.name() : __DB,
        __ID.name() : __ID,
        __LABEL.name() : __LABEL
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_5 with content type SIMPLE
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute default_length uses Python identifier default_length
    __default_length = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'default_length'), 'default_length', '__SRA_common_CTD_ANON_5_default_length', pyxb.binding.datatypes.nonNegativeInteger)
    
    default_length = property(__default_length.value, __default_length.set, None, u' Specify whether the spot should have a default\n                                                                  length for this tag if the expected base cannot be matched. ')

    
    # Attribute base_coord uses Python identifier base_coord
    __base_coord = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'base_coord'), 'base_coord', '__SRA_common_CTD_ANON_5_base_coord', pyxb.binding.datatypes.nonNegativeInteger)
    
    base_coord = property(__base_coord.value, __base_coord.set, None, u' Specify an optional starting point for tag (base\n                                                                  offset from 1). ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __default_length.name() : __default_length,
        __base_coord.name() : __base_coord
    }



# Complex type CTD_ANON_6 with content type ELEMENT_ONLY
class CTD_ANON_6 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element CYCLE_COUNT uses Python identifier CYCLE_COUNT
    __CYCLE_COUNT = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'CYCLE_COUNT'), 'CYCLE_COUNT', '__SRA_common_CTD_ANON_6_CYCLE_COUNT', False)

    
    CYCLE_COUNT = property(__CYCLE_COUNT.value, __CYCLE_COUNT.set, None, u' DEPRECATED. Use SPOT_LENGTH instead. ')

    
    # Element SEQUENCE_LENGTH uses Python identifier SEQUENCE_LENGTH
    __SEQUENCE_LENGTH = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SEQUENCE_LENGTH'), 'SEQUENCE_LENGTH', '__SRA_common_CTD_ANON_6_SEQUENCE_LENGTH', False)

    
    SEQUENCE_LENGTH = property(__SEQUENCE_LENGTH.value, __SEQUENCE_LENGTH.set, None, u' DEPRECATED. Use SPOT_LENGTH instead. The fixed number of bases expected in each\n                                    raw sequence, including both mate pairs and any technical reads. This is optional in the schema\n                                    now but will be required by business rules and future schema versions. ')

    
    # Element INSTRUMENT_MODEL uses Python identifier INSTRUMENT_MODEL
    __INSTRUMENT_MODEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), 'INSTRUMENT_MODEL', '__SRA_common_CTD_ANON_6_INSTRUMENT_MODEL', False)

    
    INSTRUMENT_MODEL = property(__INSTRUMENT_MODEL.value, __INSTRUMENT_MODEL.set, None, None)

    
    # Element COLOR_MATRIX uses Python identifier COLOR_MATRIX
    __COLOR_MATRIX = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'COLOR_MATRIX'), 'COLOR_MATRIX', '__SRA_common_CTD_ANON_6_COLOR_MATRIX', False)

    
    COLOR_MATRIX = property(__COLOR_MATRIX.value, __COLOR_MATRIX.set, None, u' DEPRECATED. ')

    
    # Element COLOR_MATRIX_CODE uses Python identifier COLOR_MATRIX_CODE
    __COLOR_MATRIX_CODE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'COLOR_MATRIX_CODE'), 'COLOR_MATRIX_CODE', '__SRA_common_CTD_ANON_6_COLOR_MATRIX_CODE', False)

    
    COLOR_MATRIX_CODE = property(__COLOR_MATRIX_CODE.value, __COLOR_MATRIX_CODE.set, None, u' DEPRECATED. ')


    _ElementMap = {
        __CYCLE_COUNT.name() : __CYCLE_COUNT,
        __SEQUENCE_LENGTH.name() : __SEQUENCE_LENGTH,
        __INSTRUMENT_MODEL.name() : __INSTRUMENT_MODEL,
        __COLOR_MATRIX.name() : __COLOR_MATRIX,
        __COLOR_MATRIX_CODE.name() : __COLOR_MATRIX_CODE
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
    
    # Element ADAPTER_SPEC uses Python identifier ADAPTER_SPEC
    __ADAPTER_SPEC = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ADAPTER_SPEC'), 'ADAPTER_SPEC', '__SRA_common_CTD_ANON_7_ADAPTER_SPEC', False)

    
    ADAPTER_SPEC = property(__ADAPTER_SPEC.value, __ADAPTER_SPEC.set, None, u' Some technologies will require knowledge of the sequencing adapter or the last\n                                    base of the adapter in order to decode the spot. ')

    
    # Element NUMBER_OF_READS_PER_SPOT uses Python identifier NUMBER_OF_READS_PER_SPOT
    __NUMBER_OF_READS_PER_SPOT = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'NUMBER_OF_READS_PER_SPOT'), 'NUMBER_OF_READS_PER_SPOT', '__SRA_common_CTD_ANON_7_NUMBER_OF_READS_PER_SPOT', False)

    
    NUMBER_OF_READS_PER_SPOT = property(__NUMBER_OF_READS_PER_SPOT.value, __NUMBER_OF_READS_PER_SPOT.set, None, u' DEPRECATED. Number of tags (reads) per spot. ')

    
    # Element READ_SPEC uses Python identifier READ_SPEC
    __READ_SPEC = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'READ_SPEC'), 'READ_SPEC', '__SRA_common_CTD_ANON_7_READ_SPEC', True)

    
    READ_SPEC = property(__READ_SPEC.value, __READ_SPEC.set, None, None)

    
    # Element SPOT_LENGTH uses Python identifier SPOT_LENGTH
    __SPOT_LENGTH = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SPOT_LENGTH'), 'SPOT_LENGTH', '__SRA_common_CTD_ANON_7_SPOT_LENGTH', False)

    
    SPOT_LENGTH = property(__SPOT_LENGTH.value, __SPOT_LENGTH.set, None, u' Number of base/color calls, cycles, or flows per spot (raw sequence length or\n                                    flow length including all application and technical tags and mate pairs, but not including gap\n                                    lengths). This value will be platform dependent, library dependent, and possibly run dependent.\n                                    Variable length platforms will still have a constant flow/cycle length. ')


    _ElementMap = {
        __ADAPTER_SPEC.name() : __ADAPTER_SPEC,
        __NUMBER_OF_READS_PER_SPOT.name() : __NUMBER_OF_READS_PER_SPOT,
        __READ_SPEC.name() : __READ_SPEC,
        __SPOT_LENGTH.name() : __SPOT_LENGTH
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_8 with content type EMPTY
class CTD_ANON_8 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute max_length uses Python identifier max_length
    __max_length = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'max_length'), 'max_length', '__SRA_common_CTD_ANON_8_max_length', pyxb.binding.datatypes.integer, required=True)
    
    max_length = property(__max_length.value, __max_length.set, None, u' Minimum length in base pairs of the\n                                                        interval.')

    
    # Attribute min_length uses Python identifier min_length
    __min_length = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'min_length'), 'min_length', '__SRA_common_CTD_ANON_8_min_length', pyxb.binding.datatypes.integer, required=True)
    
    min_length = property(__min_length.value, __min_length.set, None, u' Minimum length in base pairs of the\n                                                        interval.')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __max_length.name() : __max_length,
        __min_length.name() : __min_length
    }



# Complex type IdentifierNodeType with content type SIMPLE
class IdentifierNodeType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'IdentifierNodeType')
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute label uses Python identifier label
    __label = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'label'), 'label', '__SRA_common_IdentifierNodeType_label', pyxb.binding.datatypes.string)
    
    label = property(__label.value, __label.set, None, u'A string value that can be used as a display hint, or to qualify a non-SRA\n                            identifier.')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __label.name() : __label
    }
Namespace.addCategoryObject('typeBinding', u'IdentifierNodeType', IdentifierNodeType)


# Complex type NameType with content type SIMPLE
class NameType (IdentifierNodeType):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NameType')
    # Base type is IdentifierNodeType
    
    # Attribute label inherited from {SRA.common}IdentifierNodeType
    
    # Attribute namespace uses Python identifier namespace
    __namespace = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'namespace'), 'namespace', '__SRA_common_NameType_namespace', pyxb.binding.datatypes.string, required=True)
    
    namespace = property(__namespace.value, __namespace.set, None, u'A string value that constrains the domain of named identifiers (namespace). ')


    _ElementMap = IdentifierNodeType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = IdentifierNodeType._AttributeMap.copy()
    _AttributeMap.update({
        __namespace.name() : __namespace
    })
Namespace.addCategoryObject('typeBinding', u'NameType', NameType)


# Complex type AccessionType with content type SIMPLE
class AccessionType (IdentifierNodeType):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AccessionType')
    # Base type is IdentifierNodeType
    
    # Attribute label inherited from {SRA.common}IdentifierNodeType

    _ElementMap = IdentifierNodeType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = IdentifierNodeType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'AccessionType', AccessionType)


# Complex type CTD_ANON_9 with content type EMPTY
class CTD_ANON_9 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute count_type uses Python identifier count_type
    __count_type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'count_type'), 'count_type', '__SRA_common_CTD_ANON_9_count_type', STD_ANON_2, required=True)
    
    count_type = property(__count_type.value, __count_type.set, None, u' Whether absolute or relative frequency. ')

    
    # Attribute gap_size uses Python identifier gap_size
    __gap_size = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'gap_size'), 'gap_size', '__SRA_common_CTD_ANON_9_gap_size', pyxb.binding.datatypes.integer, required=True)
    
    gap_size = property(__gap_size.value, __gap_size.set, None, u' Gap size in base pairs. Gap sizes can be\n                                                                  expressed as actual values, or k-iles where k is the number of\n                                                                  bins. Gap sizes can be negative to reflect overlaps, or 0 to\n                                                                  reflect adjacent extents (eg no gap). ')

    
    # Attribute gap_count uses Python identifier gap_count
    __gap_count = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'gap_count'), 'gap_count', '__SRA_common_CTD_ANON_9_gap_count', pyxb.binding.datatypes.double, required=True)
    
    gap_count = property(__gap_count.value, __gap_count.set, None, u' Frequency count or 0. Abolute counts are\n                                                                  integers greater than 0, relative counts in the range\n                                                                  [0,1].')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __count_type.name() : __count_type,
        __gap_size.name() : __gap_size,
        __gap_count.name() : __gap_count
    }



# Complex type CTD_ANON_10 with content type ELEMENT_ONLY
class CTD_ANON_10 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element COLOR uses Python identifier COLOR
    __COLOR = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'COLOR'), 'COLOR', '__SRA_common_CTD_ANON_10_COLOR', True)

    
    COLOR = property(__COLOR.value, __COLOR.set, None, None)


    _ElementMap = {
        __COLOR.name() : __COLOR
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_11 with content type EMPTY
class CTD_ANON_11 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute mean uses Python identifier mean
    __mean = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'mean'), 'mean', '__SRA_common_CTD_ANON_11_mean', pyxb.binding.datatypes.float, required=True)
    
    mean = property(__mean.value, __mean.set, None, u' Mean length in base pairs of the\n                                                        interval.')

    
    # Attribute stdev uses Python identifier stdev
    __stdev = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'stdev'), 'stdev', '__SRA_common_CTD_ANON_11_stdev', pyxb.binding.datatypes.float, required=True)
    
    stdev = property(__stdev.value, __stdev.set, None, u' Standard deviation of length in base pairs of the\n                                                        interval.')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __mean.name() : __mean,
        __stdev.name() : __stdev
    }



# Complex type XRefType with content type ELEMENT_ONLY
class XRefType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'XRefType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element DB uses Python identifier DB
    __DB = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DB'), 'DB', '__SRA_common_XRefType_DB', False)

    
    DB = property(__DB.value, __DB.set, None, u' INSDC controlled vocabulary of permitted cross references. Please see\n                        http://www.insdc.org/db_xref.html . For example, FLYBASE. ')

    
    # Element ID uses Python identifier ID
    __ID = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__SRA_common_XRefType_ID', False)

    
    ID = property(__ID.value, __ID.set, None, u' Accession in the referenced database. For example, FBtr0080008 (in FLYBASE). ')

    
    # Element LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LABEL'), 'LABEL', '__SRA_common_XRefType_LABEL', False)

    
    LABEL = property(__LABEL.value, __LABEL.set, None, u' Text label to display for the link. ')


    _ElementMap = {
        __DB.name() : __DB,
        __ID.name() : __ID,
        __LABEL.name() : __LABEL
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'XRefType', XRefType)


# Complex type CTD_ANON_12 with content type SIMPLE
class CTD_ANON_12 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute dibase uses Python identifier dibase
    __dibase = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'dibase'), 'dibase', '__SRA_common_CTD_ANON_12_dibase', pyxb.binding.datatypes.string)
    
    dibase = property(__dibase.value, __dibase.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __dibase.name() : __dibase
    }



# Complex type CTD_ANON_13 with content type ELEMENT_ONLY
class CTD_ANON_13 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element READ_CLASS uses Python identifier READ_CLASS
    __READ_CLASS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'READ_CLASS'), 'READ_CLASS', '__SRA_common_CTD_ANON_13_READ_CLASS', False)

    
    READ_CLASS = property(__READ_CLASS.value, __READ_CLASS.set, None, None)

    
    # Element READ_LABEL uses Python identifier READ_LABEL
    __READ_LABEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'READ_LABEL'), 'READ_LABEL', '__SRA_common_CTD_ANON_13_READ_LABEL', False)

    
    READ_LABEL = property(__READ_LABEL.value, __READ_LABEL.set, None, u'READ_LABEL is a name for this tag, and can be used to on output to\n                                                determine read name, for example F or R.')

    
    # Element RELATIVE_ORDER uses Python identifier RELATIVE_ORDER
    __RELATIVE_ORDER = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'RELATIVE_ORDER'), 'RELATIVE_ORDER', '__SRA_common_CTD_ANON_13_RELATIVE_ORDER', False)

    
    RELATIVE_ORDER = property(__RELATIVE_ORDER.value, __RELATIVE_ORDER.set, None, u' The read is located beginning at the offset or cycle relative to\n                                                    another read. This choice is appropriate for example when specifying a read that\n                                                    follows a variable length expected sequence(s). ')

    
    # Element READ_INDEX uses Python identifier READ_INDEX
    __READ_INDEX = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'READ_INDEX'), 'READ_INDEX', '__SRA_common_CTD_ANON_13_READ_INDEX', False)

    
    READ_INDEX = property(__READ_INDEX.value, __READ_INDEX.set, None, u'READ_INDEX starts at 0 and is incrementally increased for each\n                                                sequential READ_SPEC within a SPOT_DECODE_SPEC')

    
    # Element EXPECTED_BASECALL uses Python identifier EXPECTED_BASECALL
    __EXPECTED_BASECALL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'EXPECTED_BASECALL'), 'EXPECTED_BASECALL', '__SRA_common_CTD_ANON_13_EXPECTED_BASECALL', False)

    
    EXPECTED_BASECALL = property(__EXPECTED_BASECALL.value, __EXPECTED_BASECALL.set, None, u' An expected basecall for a current read. Read will be\n                                                    zero-length if basecall is not present. Users of this facility should start\n                                                    migrating to EXPECTED_BASECALL_TABLE, as this field will be phased out. ')

    
    # Element BASE_COORD uses Python identifier BASE_COORD
    __BASE_COORD = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'BASE_COORD'), 'BASE_COORD', '__SRA_common_CTD_ANON_13_BASE_COORD', False)

    
    BASE_COORD = property(__BASE_COORD.value, __BASE_COORD.set, None, u' The location of the read start in terms of base count (1 is\n                                                    beginning of spot). ')

    
    # Element CYCLE_COORD uses Python identifier CYCLE_COORD
    __CYCLE_COORD = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'CYCLE_COORD'), 'CYCLE_COORD', '__SRA_common_CTD_ANON_13_CYCLE_COORD', False)

    
    CYCLE_COORD = property(__CYCLE_COORD.value, __CYCLE_COORD.set, None, u' The location of the read start in terms of cycle count (1 is\n                                                    beginning of spot). ')

    
    # Element READ_TYPE uses Python identifier READ_TYPE
    __READ_TYPE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'READ_TYPE'), 'READ_TYPE', '__SRA_common_CTD_ANON_13_READ_TYPE', False)

    
    READ_TYPE = property(__READ_TYPE.value, __READ_TYPE.set, None, None)

    
    # Element EXPECTED_BASECALL_TABLE uses Python identifier EXPECTED_BASECALL_TABLE
    __EXPECTED_BASECALL_TABLE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'EXPECTED_BASECALL_TABLE'), 'EXPECTED_BASECALL_TABLE', '__SRA_common_CTD_ANON_13_EXPECTED_BASECALL_TABLE', False)

    
    EXPECTED_BASECALL_TABLE = property(__EXPECTED_BASECALL_TABLE.value, __EXPECTED_BASECALL_TABLE.set, None, u' A set of choices of expected basecalls for a current read. Read\n                                                    will be zero-length if none is found. ')


    _ElementMap = {
        __READ_CLASS.name() : __READ_CLASS,
        __READ_LABEL.name() : __READ_LABEL,
        __RELATIVE_ORDER.name() : __RELATIVE_ORDER,
        __READ_INDEX.name() : __READ_INDEX,
        __EXPECTED_BASECALL.name() : __EXPECTED_BASECALL,
        __BASE_COORD.name() : __BASE_COORD,
        __CYCLE_COORD.name() : __CYCLE_COORD,
        __READ_TYPE.name() : __READ_TYPE,
        __EXPECTED_BASECALL_TABLE.name() : __EXPECTED_BASECALL_TABLE
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_14 with content type EMPTY
class CTD_ANON_14 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute median uses Python identifier median
    __median = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'median'), 'median', '__SRA_common_CTD_ANON_14_median', pyxb.binding.datatypes.integer, required=True)
    
    median = property(__median.value, __median.set, None, u' Median length in base pairs of the interval. Equivalent to\n                                                        the BAM file @RG/PI tag.')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __median.name() : __median
    }



# Complex type CTD_ANON_15 with content type ELEMENT_ONLY
class CTD_ANON_15 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element URL uses Python identifier URL
    __URL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'URL'), 'URL', '__SRA_common_CTD_ANON_15_URL', False)

    
    URL = property(__URL.value, __URL.set, None, u'An URL to the cross-references accession. ')

    
    # Element DB uses Python identifier DB
    __DB = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DB'), 'DB', '__SRA_common_CTD_ANON_15_DB', False)

    
    DB = property(__DB.value, __DB.set, None, u' EBI ENA controlled vocabulary of permitted cross references. ')

    
    # Element LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LABEL'), 'LABEL', '__SRA_common_CTD_ANON_15_LABEL', False)

    
    LABEL = property(__LABEL.value, __LABEL.set, None, u'A textual description of the cross-reference. ')

    
    # Element ID uses Python identifier ID
    __ID = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__SRA_common_CTD_ANON_15_ID', False)

    
    ID = property(__ID.value, __ID.set, None, u' Accession in the referenced database.')


    _ElementMap = {
        __URL.name() : __URL,
        __DB.name() : __DB,
        __LABEL.name() : __LABEL,
        __ID.name() : __ID
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_16 with content type ELEMENT_ONLY
class CTD_ANON_16 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element bin uses Python identifier bin
    __bin = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'bin'), 'bin', '__SRA_common_CTD_ANON_16_bin', True)

    
    bin = property(__bin.value, __bin.set, None, None)


    _ElementMap = {
        __bin.name() : __bin
    }
    _AttributeMap = {
        
    }



# Complex type LinkType with content type ELEMENT_ONLY
class LinkType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'LinkType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element XREF_LINK uses Python identifier XREF_LINK
    __XREF_LINK = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'XREF_LINK'), 'XREF_LINK', '__SRA_common_LinkType_XREF_LINK', False)

    
    XREF_LINK = property(__XREF_LINK.value, __XREF_LINK.set, None, None)

    
    # Element SRA_LINK uses Python identifier SRA_LINK
    __SRA_LINK = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SRA_LINK'), 'SRA_LINK', '__SRA_common_LinkType_SRA_LINK', False)

    
    SRA_LINK = property(__SRA_LINK.value, __SRA_LINK.set, None, None)

    
    # Element ENTREZ_LINK uses Python identifier ENTREZ_LINK
    __ENTREZ_LINK = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ENTREZ_LINK'), 'ENTREZ_LINK', '__SRA_common_LinkType_ENTREZ_LINK', False)

    
    ENTREZ_LINK = property(__ENTREZ_LINK.value, __ENTREZ_LINK.set, None, None)

    
    # Element DDBJ_LINK uses Python identifier DDBJ_LINK
    __DDBJ_LINK = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DDBJ_LINK'), 'DDBJ_LINK', '__SRA_common_LinkType_DDBJ_LINK', False)

    
    DDBJ_LINK = property(__DDBJ_LINK.value, __DDBJ_LINK.set, None, None)

    
    # Element URL_LINK uses Python identifier URL_LINK
    __URL_LINK = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'URL_LINK'), 'URL_LINK', '__SRA_common_LinkType_URL_LINK', False)

    
    URL_LINK = property(__URL_LINK.value, __URL_LINK.set, None, None)

    
    # Element ENA_LINK uses Python identifier ENA_LINK
    __ENA_LINK = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ENA_LINK'), 'ENA_LINK', '__SRA_common_LinkType_ENA_LINK', False)

    
    ENA_LINK = property(__ENA_LINK.value, __ENA_LINK.set, None, None)


    _ElementMap = {
        __XREF_LINK.name() : __XREF_LINK,
        __SRA_LINK.name() : __SRA_LINK,
        __ENTREZ_LINK.name() : __ENTREZ_LINK,
        __DDBJ_LINK.name() : __DDBJ_LINK,
        __URL_LINK.name() : __URL_LINK,
        __ENA_LINK.name() : __ENA_LINK
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'LinkType', LinkType)


# Complex type CTD_ANON_17 with content type EMPTY
class CTD_ANON_17 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute follows_read_index uses Python identifier follows_read_index
    __follows_read_index = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'follows_read_index'), 'follows_read_index', '__SRA_common_CTD_ANON_17_follows_read_index', pyxb.binding.datatypes.nonNegativeInteger)
    
    follows_read_index = property(__follows_read_index.value, __follows_read_index.set, None, u' Specify the read index that precedes this read. ')

    
    # Attribute precedes_read_index uses Python identifier precedes_read_index
    __precedes_read_index = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'precedes_read_index'), 'precedes_read_index', '__SRA_common_CTD_ANON_17_precedes_read_index', pyxb.binding.datatypes.nonNegativeInteger)
    
    precedes_read_index = property(__precedes_read_index.value, __precedes_read_index.set, None, u' Specify the read index that follows this read. ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __follows_read_index.name() : __follows_read_index,
        __precedes_read_index.name() : __precedes_read_index
    }



# Complex type AttributeType with content type ELEMENT_ONLY
class AttributeType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AttributeType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element UNITS uses Python identifier UNITS
    __UNITS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'UNITS'), 'UNITS', '__SRA_common_AttributeType_UNITS', False)

    
    UNITS = property(__UNITS.value, __UNITS.set, None, u' Optional scientific units. ')

    
    # Element VALUE uses Python identifier VALUE
    __VALUE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'VALUE'), 'VALUE', '__SRA_common_AttributeType_VALUE', False)

    
    VALUE = property(__VALUE.value, __VALUE.set, None, u' Value of the attribute. ')

    
    # Element TAG uses Python identifier TAG
    __TAG = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TAG'), 'TAG', '__SRA_common_AttributeType_TAG', False)

    
    TAG = property(__TAG.value, __TAG.set, None, u' Name of the attribute. ')


    _ElementMap = {
        __UNITS.name() : __UNITS,
        __VALUE.name() : __VALUE,
        __TAG.name() : __TAG
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'AttributeType', AttributeType)


# Complex type CTD_ANON_18 with content type ELEMENT_ONLY
class CTD_ANON_18 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element INSTRUMENT_MODEL uses Python identifier INSTRUMENT_MODEL
    __INSTRUMENT_MODEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), 'INSTRUMENT_MODEL', '__SRA_common_CTD_ANON_18_INSTRUMENT_MODEL', False)

    
    INSTRUMENT_MODEL = property(__INSTRUMENT_MODEL.value, __INSTRUMENT_MODEL.set, None, None)


    _ElementMap = {
        __INSTRUMENT_MODEL.name() : __INSTRUMENT_MODEL
    }
    _AttributeMap = {
        
    }



# Complex type LibraryType with content type ELEMENT_ONLY
class LibraryType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'LibraryType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element DESIGN_DESCRIPTION uses Python identifier DESIGN_DESCRIPTION
    __DESIGN_DESCRIPTION = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DESIGN_DESCRIPTION'), 'DESIGN_DESCRIPTION', '__SRA_common_LibraryType_DESIGN_DESCRIPTION', False)

    
    DESIGN_DESCRIPTION = property(__DESIGN_DESCRIPTION.value, __DESIGN_DESCRIPTION.set, None, u'Goal and setup of the individual library.')

    
    # Element SAMPLE_DESCRIPTOR uses Python identifier SAMPLE_DESCRIPTOR
    __SAMPLE_DESCRIPTOR = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SAMPLE_DESCRIPTOR'), 'SAMPLE_DESCRIPTOR', '__SRA_common_LibraryType_SAMPLE_DESCRIPTOR', False)

    
    SAMPLE_DESCRIPTOR = property(__SAMPLE_DESCRIPTOR.value, __SAMPLE_DESCRIPTOR.set, None, u' Pick a sample to associate this experiment with. The sample may be an individual or a pool,\n                        depending on how it is specified. ')

    
    # Element GAP_DESCRIPTOR uses Python identifier GAP_DESCRIPTOR
    __GAP_DESCRIPTOR = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'GAP_DESCRIPTOR'), 'GAP_DESCRIPTOR', '__SRA_common_LibraryType_GAP_DESCRIPTOR', False)

    
    GAP_DESCRIPTOR = property(__GAP_DESCRIPTOR.value, __GAP_DESCRIPTOR.set, None, u' The GAP_DESCRIPTOR specifies how to place the individual tags in the spot against a notinoal\n                        reference sequence. This information is important to interpreting the placement of spot tags in an assembly\n                        or alignment for the purpose of detecting structural variations and other genomic features. ')

    
    # Element LIBRARY_DESCRIPTOR uses Python identifier LIBRARY_DESCRIPTOR
    __LIBRARY_DESCRIPTOR = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LIBRARY_DESCRIPTOR'), 'LIBRARY_DESCRIPTOR', '__SRA_common_LibraryType_LIBRARY_DESCRIPTOR', False)

    
    LIBRARY_DESCRIPTOR = property(__LIBRARY_DESCRIPTOR.value, __LIBRARY_DESCRIPTOR.set, None, u' The LIBRARY_DESCRIPTOR specifies the origin of the material being sequenced and any\n                        treatments that the material might have undergone that affect the sequencing result. This specification is\n                        needed even if the platform does not require a library construction step per se. ')

    
    # Element SPOT_DESCRIPTOR uses Python identifier SPOT_DESCRIPTOR
    __SPOT_DESCRIPTOR = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SPOT_DESCRIPTOR'), 'SPOT_DESCRIPTOR', '__SRA_common_LibraryType_SPOT_DESCRIPTOR', False)

    
    SPOT_DESCRIPTOR = property(__SPOT_DESCRIPTOR.value, __SPOT_DESCRIPTOR.set, None, u' The SPOT_DESCRIPTOR specifies how to decode the individual reads of interest from the\n                        monolithic spot sequence. The spot descriptor contains aspects of the experimental design, platform, and\n                        processing information. There will be two methods of specification: one will be an index into a table of\n                        typical decodings, the other being an exact specification. This construct is needed for loading data and for\n                        interpreting the loaded runs. It can be omitted if the loader can infer read layout (from multiple input\n                        files or from one input files). ')


    _ElementMap = {
        __DESIGN_DESCRIPTION.name() : __DESIGN_DESCRIPTION,
        __SAMPLE_DESCRIPTOR.name() : __SAMPLE_DESCRIPTOR,
        __GAP_DESCRIPTOR.name() : __GAP_DESCRIPTOR,
        __LIBRARY_DESCRIPTOR.name() : __LIBRARY_DESCRIPTOR,
        __SPOT_DESCRIPTOR.name() : __SPOT_DESCRIPTOR
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'LibraryType', LibraryType)


# Complex type UUIDType with content type SIMPLE
class UUIDType (IdentifierNodeType):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'UUIDType')
    # Base type is IdentifierNodeType
    
    # Attribute label inherited from {SRA.common}IdentifierNodeType

    _ElementMap = IdentifierNodeType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = IdentifierNodeType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'UUIDType', UUIDType)


# Complex type CTD_ANON_19 with content type ELEMENT_ONLY
class CTD_ANON_19 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element INSTRUMENT_MODEL uses Python identifier INSTRUMENT_MODEL
    __INSTRUMENT_MODEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), 'INSTRUMENT_MODEL', '__SRA_common_CTD_ANON_19_INSTRUMENT_MODEL', False)

    
    INSTRUMENT_MODEL = property(__INSTRUMENT_MODEL.value, __INSTRUMENT_MODEL.set, None, None)


    _ElementMap = {
        __INSTRUMENT_MODEL.name() : __INSTRUMENT_MODEL
    }
    _AttributeMap = {
        
    }



# Complex type SampleDescriptorType with content type ELEMENT_ONLY
class SampleDescriptorType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SampleDescriptorType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element POOL uses Python identifier POOL
    __POOL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'POOL'), 'POOL', '__SRA_common_SampleDescriptorType_POOL', False)

    
    POOL = property(__POOL.value, __POOL.set, None, u' Identifies a list of group/pool/multiplex sample members. This implies that this sample\n                        record is a group, pool, or multiplex, but is continues to receive its own accession and can be referenced\n                        by an experiment. By default if no match to any of the listed members can be determined, then the default\n                        sampel reference is used. ')

    
    # Element IDENTIFIERS uses Python identifier IDENTIFIERS
    __IDENTIFIERS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'IDENTIFIERS'), 'IDENTIFIERS', '__SRA_common_SampleDescriptorType_IDENTIFIERS', False)

    
    IDENTIFIERS = property(__IDENTIFIERS.value, __IDENTIFIERS.set, None, u' Set of reference IDs to parent experiment record. This block is intended to replace the use\n                        of the less structured RefNameGroup identifiers. ')

    
    # Attribute refname uses Python identifier refname
    __refname = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refname'), 'refname', '__SRA_common_SampleDescriptorType_refname', pyxb.binding.datatypes.string)
    
    refname = property(__refname.value, __refname.set, None, u' Identifies a record by name that is known within the namespace defined by attribute "refcenter"\n                    Use this field when referencing an object for which an accession has not yet been issued. ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'accession'), 'accession', '__SRA_common_SampleDescriptorType_accession', pyxb.binding.datatypes.string)
    
    accession = property(__accession.value, __accession.set, None, u' Identifies a record by its accession. The scope of resolution is the entire Archive. ')

    
    # Attribute refcenter uses Python identifier refcenter
    __refcenter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refcenter'), 'refcenter', '__SRA_common_SampleDescriptorType_refcenter', pyxb.binding.datatypes.string)
    
    refcenter = property(__refcenter.value, __refcenter.set, None, u' The center namespace of the attribute "refname". When absent, the namespace is assumed to be the\n                    current submission. ')


    _ElementMap = {
        __POOL.name() : __POOL,
        __IDENTIFIERS.name() : __IDENTIFIERS
    }
    _AttributeMap = {
        __refname.name() : __refname,
        __accession.name() : __accession,
        __refcenter.name() : __refcenter
    }
Namespace.addCategoryObject('typeBinding', u'SampleDescriptorType', SampleDescriptorType)


# Complex type LibraryDescriptorType with content type ELEMENT_ONLY
class LibraryDescriptorType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'LibraryDescriptorType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element LIBRARY_SOURCE uses Python identifier LIBRARY_SOURCE
    __LIBRARY_SOURCE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LIBRARY_SOURCE'), 'LIBRARY_SOURCE', '__SRA_common_LibraryDescriptorType_LIBRARY_SOURCE', False)

    
    LIBRARY_SOURCE = property(__LIBRARY_SOURCE.value, __LIBRARY_SOURCE.set, None, u' The LIBRARY_SOURCE specifies the type of source material that is being sequenced. ')

    
    # Element LIBRARY_SELECTION uses Python identifier LIBRARY_SELECTION
    __LIBRARY_SELECTION = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LIBRARY_SELECTION'), 'LIBRARY_SELECTION', '__SRA_common_LibraryDescriptorType_LIBRARY_SELECTION', False)

    
    LIBRARY_SELECTION = property(__LIBRARY_SELECTION.value, __LIBRARY_SELECTION.set, None, u' Whether any method was used to select for or against, enrich, or screen the material being\n                        sequenced. ')

    
    # Element LIBRARY_STRATEGY uses Python identifier LIBRARY_STRATEGY
    __LIBRARY_STRATEGY = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LIBRARY_STRATEGY'), 'LIBRARY_STRATEGY', '__SRA_common_LibraryDescriptorType_LIBRARY_STRATEGY', False)

    
    LIBRARY_STRATEGY = property(__LIBRARY_STRATEGY.value, __LIBRARY_STRATEGY.set, None, u' Sequencing technique intended for this library. ')

    
    # Element TARGETED_LOCI uses Python identifier TARGETED_LOCI
    __TARGETED_LOCI = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TARGETED_LOCI'), 'TARGETED_LOCI', '__SRA_common_LibraryDescriptorType_TARGETED_LOCI', False)

    
    TARGETED_LOCI = property(__TARGETED_LOCI.value, __TARGETED_LOCI.set, None, None)

    
    # Element LIBRARY_CONSTRUCTION_PROTOCOL uses Python identifier LIBRARY_CONSTRUCTION_PROTOCOL
    __LIBRARY_CONSTRUCTION_PROTOCOL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LIBRARY_CONSTRUCTION_PROTOCOL'), 'LIBRARY_CONSTRUCTION_PROTOCOL', '__SRA_common_LibraryDescriptorType_LIBRARY_CONSTRUCTION_PROTOCOL', False)

    
    LIBRARY_CONSTRUCTION_PROTOCOL = property(__LIBRARY_CONSTRUCTION_PROTOCOL.value, __LIBRARY_CONSTRUCTION_PROTOCOL.set, None, u' Free form text describing the protocol by which the sequencing library was constructed. ')

    
    # Element LIBRARY_LAYOUT uses Python identifier LIBRARY_LAYOUT
    __LIBRARY_LAYOUT = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LIBRARY_LAYOUT'), 'LIBRARY_LAYOUT', '__SRA_common_LibraryDescriptorType_LIBRARY_LAYOUT', False)

    
    LIBRARY_LAYOUT = property(__LIBRARY_LAYOUT.value, __LIBRARY_LAYOUT.set, None, u' LIBRARY_LAYOUT specifies whether to expect single, paired, or other configuration of reads.\n                        In the case of paired reads, information about the relative distance and orientation is specified. ')

    
    # Element LIBRARY_NAME uses Python identifier LIBRARY_NAME
    __LIBRARY_NAME = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LIBRARY_NAME'), 'LIBRARY_NAME', '__SRA_common_LibraryDescriptorType_LIBRARY_NAME', False)

    
    LIBRARY_NAME = property(__LIBRARY_NAME.value, __LIBRARY_NAME.set, None, u" The submitter's name for this library. ")

    
    # Element POOLING_STRATEGY uses Python identifier POOLING_STRATEGY
    __POOLING_STRATEGY = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'POOLING_STRATEGY'), 'POOLING_STRATEGY', '__SRA_common_LibraryDescriptorType_POOLING_STRATEGY', False)

    
    POOLING_STRATEGY = property(__POOLING_STRATEGY.value, __POOLING_STRATEGY.set, None, u' The optional pooling strategy indicates how the library or libraries are organized if\n                        multiple samples are involved. ')


    _ElementMap = {
        __LIBRARY_SOURCE.name() : __LIBRARY_SOURCE,
        __LIBRARY_SELECTION.name() : __LIBRARY_SELECTION,
        __LIBRARY_STRATEGY.name() : __LIBRARY_STRATEGY,
        __TARGETED_LOCI.name() : __TARGETED_LOCI,
        __LIBRARY_CONSTRUCTION_PROTOCOL.name() : __LIBRARY_CONSTRUCTION_PROTOCOL,
        __LIBRARY_LAYOUT.name() : __LIBRARY_LAYOUT,
        __LIBRARY_NAME.name() : __LIBRARY_NAME,
        __POOLING_STRATEGY.name() : __POOLING_STRATEGY
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'LibraryDescriptorType', LibraryDescriptorType)


# Complex type CTD_ANON_20 with content type ELEMENT_ONLY
class CTD_ANON_20 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element INSTRUMENT_MODEL uses Python identifier INSTRUMENT_MODEL
    __INSTRUMENT_MODEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), 'INSTRUMENT_MODEL', '__SRA_common_CTD_ANON_20_INSTRUMENT_MODEL', False)

    
    INSTRUMENT_MODEL = property(__INSTRUMENT_MODEL.value, __INSTRUMENT_MODEL.set, None, None)


    _ElementMap = {
        __INSTRUMENT_MODEL.name() : __INSTRUMENT_MODEL
    }
    _AttributeMap = {
        
    }



# Complex type SpotDescriptorType with content type ELEMENT_ONLY
class SpotDescriptorType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SpotDescriptorType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element SPOT_DECODE_SPEC uses Python identifier SPOT_DECODE_SPEC
    __SPOT_DECODE_SPEC = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SPOT_DECODE_SPEC'), 'SPOT_DECODE_SPEC', '__SRA_common_SpotDescriptorType_SPOT_DECODE_SPEC', False)

    
    SPOT_DECODE_SPEC = property(__SPOT_DECODE_SPEC.value, __SPOT_DECODE_SPEC.set, None, None)

    
    # Element SPOT_DECODE_METHOD uses Python identifier SPOT_DECODE_METHOD
    __SPOT_DECODE_METHOD = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SPOT_DECODE_METHOD'), 'SPOT_DECODE_METHOD', '__SRA_common_SpotDescriptorType_SPOT_DECODE_METHOD', False)

    
    SPOT_DECODE_METHOD = property(__SPOT_DECODE_METHOD.value, __SPOT_DECODE_METHOD.set, None, u' DEPRECATED. ')


    _ElementMap = {
        __SPOT_DECODE_SPEC.name() : __SPOT_DECODE_SPEC,
        __SPOT_DECODE_METHOD.name() : __SPOT_DECODE_METHOD
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'SpotDescriptorType', SpotDescriptorType)


# Complex type SraLinkType with content type EMPTY
class SraLinkType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SraLinkType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'accession'), 'accession', '__SRA_common_SraLinkType_accession', pyxb.binding.datatypes.string)
    
    accession = property(__accession.value, __accession.set, None, u' Identifies a record by its accession. The scope of resolution is the entire Archive. ')

    
    # Attribute refcenter uses Python identifier refcenter
    __refcenter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refcenter'), 'refcenter', '__SRA_common_SraLinkType_refcenter', pyxb.binding.datatypes.string)
    
    refcenter = property(__refcenter.value, __refcenter.set, None, u' The center namespace of the attribute "refname". When absent, the namespace is assumed to be the\n                    current submission. ')

    
    # Attribute refname uses Python identifier refname
    __refname = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refname'), 'refname', '__SRA_common_SraLinkType_refname', pyxb.binding.datatypes.string)
    
    refname = property(__refname.value, __refname.set, None, u' Identifies a record by name that is known within the namespace defined by attribute "refcenter"\n                    Use this field when referencing an object for which an accession has not yet been issued. ')

    
    # Attribute sra_object_type uses Python identifier sra_object_type
    __sra_object_type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'sra_object_type'), 'sra_object_type', '__SRA_common_SraLinkType_sra_object_type', STD_ANON_9)
    
    sra_object_type = property(__sra_object_type.value, __sra_object_type.set, None, u' SRA link type. ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __accession.name() : __accession,
        __refcenter.name() : __refcenter,
        __refname.name() : __refname,
        __sra_object_type.name() : __sra_object_type
    }
Namespace.addCategoryObject('typeBinding', u'SraLinkType', SraLinkType)


# Complex type PlatformType with content type ELEMENT_ONLY
class PlatformType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'PlatformType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element COMPLETE_GENOMICS uses Python identifier COMPLETE_GENOMICS
    __COMPLETE_GENOMICS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'COMPLETE_GENOMICS'), 'COMPLETE_GENOMICS', '__SRA_common_PlatformType_COMPLETE_GENOMICS', False)

    
    COMPLETE_GENOMICS = property(__COMPLETE_GENOMICS.value, __COMPLETE_GENOMICS.set, None, u' CompleteGenomics platform type. At present there is no instrument model. ')

    
    # Element LS454 uses Python identifier LS454
    __LS454 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LS454'), 'LS454', '__SRA_common_PlatformType_LS454', False)

    
    LS454 = property(__LS454.value, __LS454.set, None, u' 454 technology use 1-color sequential flows ')

    
    # Element HELICOS uses Python identifier HELICOS
    __HELICOS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'HELICOS'), 'HELICOS', '__SRA_common_PlatformType_HELICOS', False)

    
    HELICOS = property(__HELICOS.value, __HELICOS.set, None, u' Helicos is similar to 454 technology - uses 1-color sequential flows ')

    
    # Element ABI_SOLID uses Python identifier ABI_SOLID
    __ABI_SOLID = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ABI_SOLID'), 'ABI_SOLID', '__SRA_common_PlatformType_ABI_SOLID', False)

    
    ABI_SOLID = property(__ABI_SOLID.value, __ABI_SOLID.set, None, u' ABI is 4-channel flowgram with 1-to-1 mapping between basecalls and flows ')

    
    # Element PACBIO_SMRT uses Python identifier PACBIO_SMRT
    __PACBIO_SMRT = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PACBIO_SMRT'), 'PACBIO_SMRT', '__SRA_common_PlatformType_PACBIO_SMRT', False)

    
    PACBIO_SMRT = property(__PACBIO_SMRT.value, __PACBIO_SMRT.set, None, u' PacificBiosciences platform type for the single molecule real time (SMRT) technology. ')

    
    # Element ION_TORRENT uses Python identifier ION_TORRENT
    __ION_TORRENT = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ION_TORRENT'), 'ION_TORRENT', '__SRA_common_PlatformType_ION_TORRENT', False)

    
    ION_TORRENT = property(__ION_TORRENT.value, __ION_TORRENT.set, None, u' Ion Torrent Personal Genome Machine (PGM) from Life Technologies. ')

    
    # Element CAPILLARY uses Python identifier CAPILLARY
    __CAPILLARY = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'CAPILLARY'), 'CAPILLARY', '__SRA_common_PlatformType_CAPILLARY', False)

    
    CAPILLARY = property(__CAPILLARY.value, __CAPILLARY.set, None, u' Sequencers based on capillary electrophoresis technology manufactured by LifeTech (formerly\n                        Applied BioSciences). ')

    
    # Element ILLUMINA uses Python identifier ILLUMINA
    __ILLUMINA = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ILLUMINA'), 'ILLUMINA', '__SRA_common_PlatformType_ILLUMINA', False)

    
    ILLUMINA = property(__ILLUMINA.value, __ILLUMINA.set, None, u' Illumina is 4-channel flowgram with 1-to-1 mapping between basecalls and flows ')


    _ElementMap = {
        __COMPLETE_GENOMICS.name() : __COMPLETE_GENOMICS,
        __LS454.name() : __LS454,
        __HELICOS.name() : __HELICOS,
        __ABI_SOLID.name() : __ABI_SOLID,
        __PACBIO_SMRT.name() : __PACBIO_SMRT,
        __ION_TORRENT.name() : __ION_TORRENT,
        __CAPILLARY.name() : __CAPILLARY,
        __ILLUMINA.name() : __ILLUMINA
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'PlatformType', PlatformType)


# Complex type CTD_ANON_21 with content type ELEMENT_ONLY
class CTD_ANON_21 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element BASECALL uses Python identifier BASECALL
    __BASECALL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'BASECALL'), 'BASECALL', '__SRA_common_CTD_ANON_21_BASECALL', True)

    
    BASECALL = property(__BASECALL.value, __BASECALL.set, None, u" Element's body contains a basecall, attribute\n                                                                provide description of this read meaning as well as matching rules. ")

    
    # Attribute default_length uses Python identifier default_length
    __default_length = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'default_length'), 'default_length', '__SRA_common_CTD_ANON_21_default_length', pyxb.binding.datatypes.nonNegativeInteger)
    
    default_length = property(__default_length.value, __default_length.set, None, u' Specify whether the spot should have a default length\n                                                            for this tag if the expected base cannot be matched. ')

    
    # Attribute base_coord uses Python identifier base_coord
    __base_coord = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'base_coord'), 'base_coord', '__SRA_common_CTD_ANON_21_base_coord', pyxb.binding.datatypes.nonNegativeInteger)
    
    base_coord = property(__base_coord.value, __base_coord.set, None, u' Specify an optional starting point for tag (base offset\n                                                            from 1). ')


    _ElementMap = {
        __BASECALL.name() : __BASECALL
    }
    _AttributeMap = {
        __default_length.name() : __default_length,
        __base_coord.name() : __base_coord
    }



# Complex type GapDescriptorType with content type ELEMENT_ONLY
class GapDescriptorType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'GapDescriptorType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element GAP uses Python identifier GAP
    __GAP = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'GAP'), 'GAP', '__SRA_common_GapDescriptorType_GAP', True)

    
    GAP = property(__GAP.value, __GAP.set, None, None)


    _ElementMap = {
        __GAP.name() : __GAP
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'GapDescriptorType', GapDescriptorType)


# Complex type CTD_ANON_22 with content type ELEMENT_ONLY
class CTD_ANON_22 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LABEL'), 'LABEL', '__SRA_common_CTD_ANON_22_LABEL', False)

    
    LABEL = property(__LABEL.value, __LABEL.set, None, u' Text label to display for the link. ')

    
    # Element URL uses Python identifier URL
    __URL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'URL'), 'URL', '__SRA_common_CTD_ANON_22_URL', False)

    
    URL = property(__URL.value, __URL.set, None, u' The internet service link (file:, http:, ftp:, etc). ')


    _ElementMap = {
        __LABEL.name() : __LABEL,
        __URL.name() : __URL
    }
    _AttributeMap = {
        
    }



# Complex type SequencingDirectivesType with content type ELEMENT_ONLY
class SequencingDirectivesType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SequencingDirectivesType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element SAMPLE_DEMUX_DIRECTIVE uses Python identifier SAMPLE_DEMUX_DIRECTIVE
    __SAMPLE_DEMUX_DIRECTIVE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SAMPLE_DEMUX_DIRECTIVE'), 'SAMPLE_DEMUX_DIRECTIVE', '__SRA_common_SequencingDirectivesType_SAMPLE_DEMUX_DIRECTIVE', False)

    
    SAMPLE_DEMUX_DIRECTIVE = property(__SAMPLE_DEMUX_DIRECTIVE.value, __SAMPLE_DEMUX_DIRECTIVE.set, None, u' Tells the Archive who will execute the sample demultiplexing operation.. ')


    _ElementMap = {
        __SAMPLE_DEMUX_DIRECTIVE.name() : __SAMPLE_DEMUX_DIRECTIVE
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'SequencingDirectivesType', SequencingDirectivesType)


# Complex type CTD_ANON_23 with content type ELEMENT_ONLY
class CTD_ANON_23 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element PAIRED uses Python identifier PAIRED
    __PAIRED = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PAIRED'), 'PAIRED', '__SRA_common_CTD_ANON_23_PAIRED', False)

    
    PAIRED = property(__PAIRED.value, __PAIRED.set, None, None)

    
    # Element SINGLE uses Python identifier SINGLE
    __SINGLE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SINGLE'), 'SINGLE', '__SRA_common_CTD_ANON_23_SINGLE', False)

    
    SINGLE = property(__SINGLE.value, __SINGLE.set, None, None)


    _ElementMap = {
        __PAIRED.name() : __PAIRED,
        __SINGLE.name() : __SINGLE
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_24 with content type SIMPLE
class CTD_ANON_24 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute max_mismatch uses Python identifier max_mismatch
    __max_mismatch = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'max_mismatch'), 'max_mismatch', '__SRA_common_CTD_ANON_24_max_mismatch', pyxb.binding.datatypes.nonNegativeInteger)
    
    max_mismatch = property(__max_mismatch.value, __max_mismatch.set, None, u' Maximum number of mismatches ')

    
    # Attribute match_edge uses Python identifier match_edge
    __match_edge = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'match_edge'), 'match_edge', '__SRA_common_CTD_ANON_24_match_edge', STD_ANON_14)
    
    match_edge = property(__match_edge.value, __match_edge.set, None, u' Where the match should occur. Changes the\n                                                                  rules on how min_match and max_mismatch are counted. ')

    
    # Attribute min_match uses Python identifier min_match
    __min_match = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'min_match'), 'min_match', '__SRA_common_CTD_ANON_24_min_match', pyxb.binding.datatypes.nonNegativeInteger)
    
    min_match = property(__min_match.value, __min_match.set, None, u' Minimum number of matches to trigger\n                                                                  identification. ')

    
    # Attribute read_group_tag uses Python identifier read_group_tag
    __read_group_tag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'read_group_tag'), 'read_group_tag', '__SRA_common_CTD_ANON_24_read_group_tag', pyxb.binding.datatypes.string)
    
    read_group_tag = property(__read_group_tag.value, __read_group_tag.set, None, u' When match occurs, the read will be tagged\n                                                                  with this group membership ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __max_mismatch.name() : __max_mismatch,
        __match_edge.name() : __match_edge,
        __min_match.name() : __min_match,
        __read_group_tag.name() : __read_group_tag
    }



# Complex type CTD_ANON_25 with content type ELEMENT_ONLY
class CTD_ANON_25 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element PROGRAM uses Python identifier PROGRAM
    __PROGRAM = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PROGRAM'), 'PROGRAM', '__SRA_common_CTD_ANON_25_PROGRAM', False)

    
    PROGRAM = property(__PROGRAM.value, __PROGRAM.set, None, u' Name of the program or process for primary analysis. This may include a test or\n                                    condition that leads to branching in the workflow. ')

    
    # Element PREV_STEP_INDEX uses Python identifier PREV_STEP_INDEX
    __PREV_STEP_INDEX = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PREV_STEP_INDEX'), 'PREV_STEP_INDEX', '__SRA_common_CTD_ANON_25_PREV_STEP_INDEX', True)

    
    PREV_STEP_INDEX = property(__PREV_STEP_INDEX.value, __PREV_STEP_INDEX.set, None, u' STEP_INDEX of the previous step in the workflow. Set toNIL if the first pipe\n                                    section. ')

    
    # Element NOTES uses Python identifier NOTES
    __NOTES = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'NOTES'), 'NOTES', '__SRA_common_CTD_ANON_25_NOTES', False)

    
    NOTES = property(__NOTES.value, __NOTES.set, None, u' Notes about the program or process for primary analysis. ')

    
    # Element STEP_INDEX uses Python identifier STEP_INDEX
    __STEP_INDEX = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'STEP_INDEX'), 'STEP_INDEX', '__SRA_common_CTD_ANON_25_STEP_INDEX', False)

    
    STEP_INDEX = property(__STEP_INDEX.value, __STEP_INDEX.set, None, u' Lexically ordered value that allows for the pipe section to be hierarchically\n                                    ordered. The float primitive data type is used to allow for pipe sections to be inserted later\n                                    on. ')

    
    # Element VERSION uses Python identifier VERSION
    __VERSION = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'VERSION'), 'VERSION', '__SRA_common_CTD_ANON_25_VERSION', False)

    
    VERSION = property(__VERSION.value, __VERSION.set, None, u' Version of the program or process for primary analysis. ')

    
    # Attribute section_name uses Python identifier section_name
    __section_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'section_name'), 'section_name', '__SRA_common_CTD_ANON_25_section_name', pyxb.binding.datatypes.string)
    
    section_name = property(__section_name.value, __section_name.set, None, u' Name of the processing pipeline section. ')


    _ElementMap = {
        __PROGRAM.name() : __PROGRAM,
        __PREV_STEP_INDEX.name() : __PREV_STEP_INDEX,
        __NOTES.name() : __NOTES,
        __STEP_INDEX.name() : __STEP_INDEX,
        __VERSION.name() : __VERSION
    }
    _AttributeMap = {
        __section_name.name() : __section_name
    }



# Complex type CTD_ANON_26 with content type EMPTY
class CTD_ANON_26 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType

    _ElementMap = {
        
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_27 with content type ELEMENT_ONLY
class CTD_ANON_27 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element DB uses Python identifier DB
    __DB = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DB'), 'DB', '__SRA_common_CTD_ANON_27_DB', False)

    
    DB = property(__DB.value, __DB.set, None, u' NCBI controlled vocabulary of permitted cross references. Please see\n                                    http://www.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi? . ')

    
    # Element ID uses Python identifier ID
    __ID = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__SRA_common_CTD_ANON_27_ID', False)

    
    ID = property(__ID.value, __ID.set, None, u' Numeric record id meaningful to the NCBI Entrez system. ')

    
    # Element QUERY uses Python identifier QUERY
    __QUERY = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'QUERY'), 'QUERY', '__SRA_common_CTD_ANON_27_QUERY', False)

    
    QUERY = property(__QUERY.value, __QUERY.set, None, u' Accession string meaningful to the NCBI Entrez system. ')

    
    # Element LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LABEL'), 'LABEL', '__SRA_common_CTD_ANON_27_LABEL', False)

    
    LABEL = property(__LABEL.value, __LABEL.set, None, u' How to label the link. ')


    _ElementMap = {
        __DB.name() : __DB,
        __ID.name() : __ID,
        __QUERY.name() : __QUERY,
        __LABEL.name() : __LABEL
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_28 with content type EMPTY
class CTD_ANON_28 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute ORIENTATION uses Python identifier ORIENTATION
    __ORIENTATION = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ORIENTATION'), 'ORIENTATION', '__SRA_common_CTD_ANON_28_ORIENTATION', pyxb.binding.datatypes.string)
    
    ORIENTATION = property(__ORIENTATION.value, __ORIENTATION.set, None, u' ')

    
    # Attribute NOMINAL_LENGTH uses Python identifier NOMINAL_LENGTH
    __NOMINAL_LENGTH = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'NOMINAL_LENGTH'), 'NOMINAL_LENGTH', '__SRA_common_CTD_ANON_28_NOMINAL_LENGTH', pyxb.binding.datatypes.nonNegativeInteger)
    
    NOMINAL_LENGTH = property(__NOMINAL_LENGTH.value, __NOMINAL_LENGTH.set, None, u' ')

    
    # Attribute NOMINAL_SDEV uses Python identifier NOMINAL_SDEV
    __NOMINAL_SDEV = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'NOMINAL_SDEV'), 'NOMINAL_SDEV', '__SRA_common_CTD_ANON_28_NOMINAL_SDEV', pyxb.binding.datatypes.double)
    
    NOMINAL_SDEV = property(__NOMINAL_SDEV.value, __NOMINAL_SDEV.set, None, u' ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __ORIENTATION.name() : __ORIENTATION,
        __NOMINAL_LENGTH.name() : __NOMINAL_LENGTH,
        __NOMINAL_SDEV.name() : __NOMINAL_SDEV
    }



# Complex type IdentifierType with content type ELEMENT_ONLY
class IdentifierType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'IdentifierType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element EXTERNAL_ID uses Python identifier EXTERNAL_ID
    __EXTERNAL_ID = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'EXTERNAL_ID'), 'EXTERNAL_ID', '__SRA_common_IdentifierType_EXTERNAL_ID', True)

    
    EXTERNAL_ID = property(__EXTERNAL_ID.value, __EXTERNAL_ID.set, None, u'An identifier from another non-INSDC database qualified by a namespace.')

    
    # Element PRIMARY_ID uses Python identifier PRIMARY_ID
    __PRIMARY_ID = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PRIMARY_ID'), 'PRIMARY_ID', '__SRA_common_IdentifierType_PRIMARY_ID', False)

    
    PRIMARY_ID = property(__PRIMARY_ID.value, __PRIMARY_ID.set, None, u'A primary key in an INSDC primary data database.')

    
    # Element SECONDARY_ID uses Python identifier SECONDARY_ID
    __SECONDARY_ID = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SECONDARY_ID'), 'SECONDARY_ID', '__SRA_common_IdentifierType_SECONDARY_ID', True)

    
    SECONDARY_ID = property(__SECONDARY_ID.value, __SECONDARY_ID.set, None, u'A secondary or defunct primary key in an INSDC primary data database.')

    
    # Element UUID uses Python identifier UUID
    __UUID = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'UUID'), 'UUID', '__SRA_common_IdentifierType_UUID', False)

    
    UUID = property(__UUID.value, __UUID.set, None, u'A universally unique identifier that requires no namespace.')

    
    # Element SUBMITTER_ID uses Python identifier SUBMITTER_ID
    __SUBMITTER_ID = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SUBMITTER_ID'), 'SUBMITTER_ID', '__SRA_common_IdentifierType_SUBMITTER_ID', True)

    
    SUBMITTER_ID = property(__SUBMITTER_ID.value, __SUBMITTER_ID.set, None, u'A local identifier provided by a submitter and qualified by a namespace.')


    _ElementMap = {
        __EXTERNAL_ID.name() : __EXTERNAL_ID,
        __PRIMARY_ID.name() : __PRIMARY_ID,
        __SECONDARY_ID.name() : __SECONDARY_ID,
        __UUID.name() : __UUID,
        __SUBMITTER_ID.name() : __SUBMITTER_ID
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'IdentifierType', IdentifierType)


# Complex type CTD_ANON_29 with content type ELEMENT_ONLY
class CTD_ANON_29 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element CYCLE_SEQUENCE uses Python identifier CYCLE_SEQUENCE
    __CYCLE_SEQUENCE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'CYCLE_SEQUENCE'), 'CYCLE_SEQUENCE', '__SRA_common_CTD_ANON_29_CYCLE_SEQUENCE', False)

    
    CYCLE_SEQUENCE = property(__CYCLE_SEQUENCE.value, __CYCLE_SEQUENCE.set, None, u' DEPRECATED. ')

    
    # Element CYCLE_COUNT uses Python identifier CYCLE_COUNT
    __CYCLE_COUNT = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'CYCLE_COUNT'), 'CYCLE_COUNT', '__SRA_common_CTD_ANON_29_CYCLE_COUNT', False)

    
    CYCLE_COUNT = property(__CYCLE_COUNT.value, __CYCLE_COUNT.set, None, u' DEPRECATED, use SPOT_LENGTH instead. The fixed number of bases in each raw\n                                    sequence, including both mate pairs and any technical reads. ')

    
    # Element SEQUENCE_LENGTH uses Python identifier SEQUENCE_LENGTH
    __SEQUENCE_LENGTH = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SEQUENCE_LENGTH'), 'SEQUENCE_LENGTH', '__SRA_common_CTD_ANON_29_SEQUENCE_LENGTH', False)

    
    SEQUENCE_LENGTH = property(__SEQUENCE_LENGTH.value, __SEQUENCE_LENGTH.set, None, u' DEPRECATED, use SPOT_LENGTH instead. The fixed number of bases expected in each\n                                    raw sequence, including both mate pairs and any technical reads. ')

    
    # Element INSTRUMENT_MODEL uses Python identifier INSTRUMENT_MODEL
    __INSTRUMENT_MODEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), 'INSTRUMENT_MODEL', '__SRA_common_CTD_ANON_29_INSTRUMENT_MODEL', False)

    
    INSTRUMENT_MODEL = property(__INSTRUMENT_MODEL.value, __INSTRUMENT_MODEL.set, None, None)


    _ElementMap = {
        __CYCLE_SEQUENCE.name() : __CYCLE_SEQUENCE,
        __CYCLE_COUNT.name() : __CYCLE_COUNT,
        __SEQUENCE_LENGTH.name() : __SEQUENCE_LENGTH,
        __INSTRUMENT_MODEL.name() : __INSTRUMENT_MODEL
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_30 with content type ELEMENT_ONLY
class CTD_ANON_30 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element FLOW_COUNT uses Python identifier FLOW_COUNT
    __FLOW_COUNT = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'FLOW_COUNT'), 'FLOW_COUNT', '__SRA_common_CTD_ANON_30_FLOW_COUNT', False)

    
    FLOW_COUNT = property(__FLOW_COUNT.value, __FLOW_COUNT.set, None, u' DEPRECATED. Use SPOT_LENGTH instead. The number of flows of challenge bases.\n                                    This is a constraint on maximum read length, but not equivalent. This is optional in the schema\n                                    now but will be required by business rules and future schema versions. ')

    
    # Element INSTRUMENT_MODEL uses Python identifier INSTRUMENT_MODEL
    __INSTRUMENT_MODEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), 'INSTRUMENT_MODEL', '__SRA_common_CTD_ANON_30_INSTRUMENT_MODEL', False)

    
    INSTRUMENT_MODEL = property(__INSTRUMENT_MODEL.value, __INSTRUMENT_MODEL.set, None, None)

    
    # Element FLOW_SEQUENCE uses Python identifier FLOW_SEQUENCE
    __FLOW_SEQUENCE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'FLOW_SEQUENCE'), 'FLOW_SEQUENCE', '__SRA_common_CTD_ANON_30_FLOW_SEQUENCE', False)

    
    FLOW_SEQUENCE = property(__FLOW_SEQUENCE.value, __FLOW_SEQUENCE.set, None, u' DEPRECATED. The fixed sequence of challenge bases that flow across the picotiter\n                                    plate. This is optional in the schema now but will be required by business rules and future\n                                    schema versions. ')

    
    # Element KEY_SEQUENCE uses Python identifier KEY_SEQUENCE
    __KEY_SEQUENCE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'KEY_SEQUENCE'), 'KEY_SEQUENCE', '__SRA_common_CTD_ANON_30_KEY_SEQUENCE', False)

    
    KEY_SEQUENCE = property(__KEY_SEQUENCE.value, __KEY_SEQUENCE.set, None, u' DEPRECATED. The first bases that are expected to be produced by the challenge\n                                    bases. This is optional in the schema now but will be required by business rules and future\n                                    schema versions. ')


    _ElementMap = {
        __FLOW_COUNT.name() : __FLOW_COUNT,
        __INSTRUMENT_MODEL.name() : __INSTRUMENT_MODEL,
        __FLOW_SEQUENCE.name() : __FLOW_SEQUENCE,
        __KEY_SEQUENCE.name() : __KEY_SEQUENCE
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_31 with content type ELEMENT_ONLY
class CTD_ANON_31 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element GAP_SPEC uses Python identifier GAP_SPEC
    __GAP_SPEC = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'GAP_SPEC'), 'GAP_SPEC', '__SRA_common_CTD_ANON_31_GAP_SPEC', False)

    
    GAP_SPEC = property(__GAP_SPEC.value, __GAP_SPEC.set, None, None)

    
    # Element GAP_TYPE uses Python identifier GAP_TYPE
    __GAP_TYPE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'GAP_TYPE'), 'GAP_TYPE', '__SRA_common_CTD_ANON_31_GAP_TYPE', False)

    
    GAP_TYPE = property(__GAP_TYPE.value, __GAP_TYPE.set, None, u' Specifies the gap type and parameters. ')


    _ElementMap = {
        __GAP_SPEC.name() : __GAP_SPEC,
        __GAP_TYPE.name() : __GAP_TYPE
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_32 with content type SIMPLE
class CTD_ANON_32 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute read_group_tag uses Python identifier read_group_tag
    __read_group_tag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'read_group_tag'), 'read_group_tag', '__SRA_common_CTD_ANON_32_read_group_tag', pyxb.binding.datatypes.string)
    
    read_group_tag = property(__read_group_tag.value, __read_group_tag.set, None, u' Assignment of read_group_tag to decoded read ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __read_group_tag.name() : __read_group_tag
    }



# Complex type CTD_ANON_33 with content type ELEMENT_ONLY
class CTD_ANON_33 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element PROBE_SET uses Python identifier PROBE_SET
    __PROBE_SET = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PROBE_SET'), 'PROBE_SET', '__SRA_common_CTD_ANON_33_PROBE_SET', False)

    
    PROBE_SET = property(__PROBE_SET.value, __PROBE_SET.set, None, u' Reference to an archived primer or probe set. Example: dbProbe ')

    
    # Attribute description uses Python identifier description
    __description = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'description'), 'description', '__SRA_common_CTD_ANON_33_description', pyxb.binding.datatypes.string)
    
    description = property(__description.value, __description.set, None, u' Submitter supplied description of alternate locus and auxiliary\n                                            information. ')

    
    # Attribute locus_name uses Python identifier locus_name
    __locus_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'locus_name'), 'locus_name', '__SRA_common_CTD_ANON_33_locus_name', STD_ANON_16)
    
    locus_name = property(__locus_name.value, __locus_name.set, None, None)


    _ElementMap = {
        __PROBE_SET.name() : __PROBE_SET
    }
    _AttributeMap = {
        __description.name() : __description,
        __locus_name.name() : __locus_name
    }



# Complex type CTD_ANON_34 with content type ELEMENT_ONLY
class CTD_ANON_34 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element PairedEnd uses Python identifier PairedEnd
    __PairedEnd = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PairedEnd'), 'PairedEnd', '__SRA_common_CTD_ANON_34_PairedEnd', False)

    
    PairedEnd = property(__PairedEnd.value, __PairedEnd.set, None, u' Mated tags sequenced from two ends of a physical extent of genomic\n                                                material. ')

    
    # Element MatePair uses Python identifier MatePair
    __MatePair = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'MatePair'), 'MatePair', '__SRA_common_CTD_ANON_34_MatePair', False)

    
    MatePair = property(__MatePair.value, __MatePair.set, None, u' Mated tags with predicted separation and orientation. ')

    
    # Element Tandem uses Python identifier Tandem
    __Tandem = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Tandem'), 'Tandem', '__SRA_common_CTD_ANON_34_Tandem', False)

    
    Tandem = property(__Tandem.value, __Tandem.set, None, u' Tandem gaps between ligands. ')


    _ElementMap = {
        __PairedEnd.name() : __PairedEnd,
        __MatePair.name() : __MatePair,
        __Tandem.name() : __Tandem
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_35 with content type ELEMENT_ONLY
class CTD_ANON_35 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element DEFAULT_MEMBER uses Python identifier DEFAULT_MEMBER
    __DEFAULT_MEMBER = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DEFAULT_MEMBER'), 'DEFAULT_MEMBER', '__SRA_common_CTD_ANON_35_DEFAULT_MEMBER', False)

    
    DEFAULT_MEMBER = property(__DEFAULT_MEMBER.value, __DEFAULT_MEMBER.set, None, u' Reference to the sample that is used when read membership cannot be determined.\n                                    A default member should be provided if there exists a possibility that some reads will be left\n                                    over from barcode/MID resolution. A default member is not needed when defining a true pool\n                                    (where individual samples are not distinguished in the reads), or the reads have been\n                                    partitioned among the pool members (no leftovers). ')

    
    # Element MEMBER uses Python identifier MEMBER
    __MEMBER = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'MEMBER'), 'MEMBER', '__SRA_common_CTD_ANON_35_MEMBER', True)

    
    MEMBER = property(__MEMBER.value, __MEMBER.set, None, u' Reference to the sample as determined from barcode/MID resolution or read\n                                    partition. ')


    _ElementMap = {
        __DEFAULT_MEMBER.name() : __DEFAULT_MEMBER,
        __MEMBER.name() : __MEMBER
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_36 with content type EMPTY
class CTD_ANON_36 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType

    _ElementMap = {
        
    }
    _AttributeMap = {
        
    }



# Complex type PoolMemberType with content type ELEMENT_ONLY
class PoolMemberType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'PoolMemberType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element IDENTIFIERS uses Python identifier IDENTIFIERS
    __IDENTIFIERS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'IDENTIFIERS'), 'IDENTIFIERS', '__SRA_common_PoolMemberType_IDENTIFIERS', False)

    
    IDENTIFIERS = property(__IDENTIFIERS.value, __IDENTIFIERS.set, None, u' Set of reference IDs to parent experiment record. This block is intended to replace the use\n                        of the less structured RefNameGroup identifiers. ')

    
    # Element READ_LABEL uses Python identifier READ_LABEL
    __READ_LABEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'READ_LABEL'), 'READ_LABEL', '__SRA_common_PoolMemberType_READ_LABEL', True)

    
    READ_LABEL = property(__READ_LABEL.value, __READ_LABEL.set, None, None)

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'accession'), 'accession', '__SRA_common_PoolMemberType_accession', pyxb.binding.datatypes.string)
    
    accession = property(__accession.value, __accession.set, None, u' Identifies a record by its accession. The scope of resolution is the entire Archive. ')

    
    # Attribute member_name uses Python identifier member_name
    __member_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'member_name'), 'member_name', '__SRA_common_PoolMemberType_member_name', pyxb.binding.datatypes.string)
    
    member_name = property(__member_name.value, __member_name.set, None, u' Label a sample within a scope of the pool ')

    
    # Attribute proportion uses Python identifier proportion
    __proportion = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'proportion'), 'proportion', '__SRA_common_PoolMemberType_proportion', pyxb.binding.datatypes.float)
    
    proportion = property(__proportion.value, __proportion.set, None, u' Proportion of this sample (in percent) that was included in sample pool. ')

    
    # Attribute refcenter uses Python identifier refcenter
    __refcenter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refcenter'), 'refcenter', '__SRA_common_PoolMemberType_refcenter', pyxb.binding.datatypes.string)
    
    refcenter = property(__refcenter.value, __refcenter.set, None, u' The center namespace of the attribute "refname". When absent, the namespace is assumed to be the\n                    current submission. ')

    
    # Attribute refname uses Python identifier refname
    __refname = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refname'), 'refname', '__SRA_common_PoolMemberType_refname', pyxb.binding.datatypes.string)
    
    refname = property(__refname.value, __refname.set, None, u' Identifies a record by name that is known within the namespace defined by attribute "refcenter"\n                    Use this field when referencing an object for which an accession has not yet been issued. ')


    _ElementMap = {
        __IDENTIFIERS.name() : __IDENTIFIERS,
        __READ_LABEL.name() : __READ_LABEL
    }
    _AttributeMap = {
        __accession.name() : __accession,
        __member_name.name() : __member_name,
        __proportion.name() : __proportion,
        __refcenter.name() : __refcenter,
        __refname.name() : __refname
    }
Namespace.addCategoryObject('typeBinding', u'PoolMemberType', PoolMemberType)


# Complex type CTD_ANON_37 with content type ELEMENT_ONLY
class CTD_ANON_37 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element FLOW_COUNT uses Python identifier FLOW_COUNT
    __FLOW_COUNT = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'FLOW_COUNT'), 'FLOW_COUNT', '__SRA_common_CTD_ANON_37_FLOW_COUNT', False)

    
    FLOW_COUNT = property(__FLOW_COUNT.value, __FLOW_COUNT.set, None, u' DEPRECATED. Use SPOT_LENGTH instead. The number of flows of challenge bases.\n                                    This is a constraint on maximum read length, but not equivalent. This is optional in the schema\n                                    now but will be required by business rules and future schema versions. ')

    
    # Element INSTRUMENT_MODEL uses Python identifier INSTRUMENT_MODEL
    __INSTRUMENT_MODEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), 'INSTRUMENT_MODEL', '__SRA_common_CTD_ANON_37_INSTRUMENT_MODEL', False)

    
    INSTRUMENT_MODEL = property(__INSTRUMENT_MODEL.value, __INSTRUMENT_MODEL.set, None, None)

    
    # Element FLOW_SEQUENCE uses Python identifier FLOW_SEQUENCE
    __FLOW_SEQUENCE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'FLOW_SEQUENCE'), 'FLOW_SEQUENCE', '__SRA_common_CTD_ANON_37_FLOW_SEQUENCE', False)

    
    FLOW_SEQUENCE = property(__FLOW_SEQUENCE.value, __FLOW_SEQUENCE.set, None, u' DEPRECATED. The fixed sequence of challenge bases that flow across the flowcell.\n                                    This is optional in the schema now but will be required by business rules and future schema\n                                    versions. ')


    _ElementMap = {
        __FLOW_COUNT.name() : __FLOW_COUNT,
        __INSTRUMENT_MODEL.name() : __INSTRUMENT_MODEL,
        __FLOW_SEQUENCE.name() : __FLOW_SEQUENCE
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_38 with content type EMPTY
class CTD_ANON_38 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute orientation uses Python identifier orientation
    __orientation = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'orientation'), 'orientation', '__SRA_common_CTD_ANON_38_orientation', STD_ANON_18)
    
    orientation = property(__orientation.value, __orientation.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __orientation.name() : __orientation
    }





PipelineType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PIPE_SECTION'), CTD_ANON_25, scope=PipelineType))
PipelineType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(PipelineType._UseForTag(pyxb.namespace.ExpandedName(None, u'PIPE_SECTION')), min_occurs=1L, max_occurs=None)
    )
PipelineType._ContentModel = pyxb.binding.content.ParticleModel(PipelineType._GroupModel, min_occurs=1L, max_occurs=1L)



CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LOCUS'), CTD_ANON_33, scope=CTD_ANON_))
CTD_ANON_._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, u'LOCUS')), min_occurs=1L, max_occurs=None)
    )
CTD_ANON_._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'statistic_mean'), CTD_ANON_11, scope=CTD_ANON_2))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'statistic_median'), CTD_ANON_14, scope=CTD_ANON_2))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'interval'), CTD_ANON_8, scope=CTD_ANON_2))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'histogram'), CTD_ANON_16, scope=CTD_ANON_2))
CTD_ANON_2._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, u'interval')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, u'statistic_mean')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, u'statistic_median')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, u'histogram')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_2._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_2._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), STD_ANON_5, scope=CTD_ANON_3))
CTD_ANON_3._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL')), min_occurs=1L, max_occurs=1L)
    )
CTD_ANON_3._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_3._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'URL'), pyxb.binding.datatypes.anyURI, scope=CTD_ANON_4, documentation=u'An URL to the cross-references accession. '))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DB'), pyxb.binding.datatypes.string, scope=CTD_ANON_4, documentation=u'DDBJ controlled vocabulary of permitted cross references. '))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ID'), pyxb.binding.datatypes.string, scope=CTD_ANON_4, documentation=u'Accession in the referenced database. '))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LABEL'), pyxb.binding.datatypes.string, scope=CTD_ANON_4, documentation=u'A textual description of the cross-reference. '))
CTD_ANON_4._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, u'DB')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, u'ID')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, u'URL')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, u'LABEL')), min_occurs=0L, max_occurs=1L)
    )
CTD_ANON_4._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_4._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'CYCLE_COUNT'), pyxb.binding.datatypes.positiveInteger, scope=CTD_ANON_6, documentation=u' DEPRECATED. Use SPOT_LENGTH instead. '))

CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SEQUENCE_LENGTH'), pyxb.binding.datatypes.positiveInteger, scope=CTD_ANON_6, documentation=u' DEPRECATED. Use SPOT_LENGTH instead. The fixed number of bases expected in each\n                                    raw sequence, including both mate pairs and any technical reads. This is optional in the schema\n                                    now but will be required by business rules and future schema versions. '))

CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), STD_ANON_, scope=CTD_ANON_6))

CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'COLOR_MATRIX'), CTD_ANON_10, scope=CTD_ANON_6, documentation=u' DEPRECATED. '))

CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'COLOR_MATRIX_CODE'), pyxb.binding.datatypes.string, scope=CTD_ANON_6, documentation=u' DEPRECATED. '))
CTD_ANON_6._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, u'COLOR_MATRIX')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, u'COLOR_MATRIX_CODE')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, u'CYCLE_COUNT')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, u'SEQUENCE_LENGTH')), min_occurs=0L, max_occurs=1L)
    )
CTD_ANON_6._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_6._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ADAPTER_SPEC'), pyxb.binding.datatypes.string, scope=CTD_ANON_7, documentation=u' Some technologies will require knowledge of the sequencing adapter or the last\n                                    base of the adapter in order to decode the spot. '))

CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'NUMBER_OF_READS_PER_SPOT'), pyxb.binding.datatypes.unsignedInt, scope=CTD_ANON_7, documentation=u' DEPRECATED. Number of tags (reads) per spot. '))

CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'READ_SPEC'), CTD_ANON_13, scope=CTD_ANON_7))

CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SPOT_LENGTH'), pyxb.binding.datatypes.nonNegativeInteger, scope=CTD_ANON_7, documentation=u' Number of base/color calls, cycles, or flows per spot (raw sequence length or\n                                    flow length including all application and technical tags and mate pairs, but not including gap\n                                    lengths). This value will be platform dependent, library dependent, and possibly run dependent.\n                                    Variable length platforms will still have a constant flow/cycle length. '))
CTD_ANON_7._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, u'NUMBER_OF_READS_PER_SPOT')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, u'SPOT_LENGTH')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, u'ADAPTER_SPEC')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, u'READ_SPEC')), min_occurs=1L, max_occurs=None)
    )
CTD_ANON_7._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_7._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_10._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'COLOR'), CTD_ANON_12, scope=CTD_ANON_10))
CTD_ANON_10._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(None, u'COLOR')), min_occurs=1L, max_occurs=None)
    )
CTD_ANON_10._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_10._GroupModel, min_occurs=1, max_occurs=1)



XRefType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DB'), pyxb.binding.datatypes.string, scope=XRefType, documentation=u' INSDC controlled vocabulary of permitted cross references. Please see\n                        http://www.insdc.org/db_xref.html . For example, FLYBASE. '))

XRefType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ID'), pyxb.binding.datatypes.string, scope=XRefType, documentation=u' Accession in the referenced database. For example, FBtr0080008 (in FLYBASE). '))

XRefType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LABEL'), pyxb.binding.datatypes.string, scope=XRefType, documentation=u' Text label to display for the link. '))
XRefType._GroupModel = pyxb.binding.content.GroupAll(
    pyxb.binding.content.ParticleModel(XRefType._UseForTag(pyxb.namespace.ExpandedName(None, u'DB')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(XRefType._UseForTag(pyxb.namespace.ExpandedName(None, u'ID')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(XRefType._UseForTag(pyxb.namespace.ExpandedName(None, u'LABEL')), min_occurs=0L, max_occurs=1L)
    )
XRefType._ContentModel = pyxb.binding.content.ParticleModel(XRefType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'READ_CLASS'), STD_ANON_3, scope=CTD_ANON_13))

CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'READ_LABEL'), pyxb.binding.datatypes.string, scope=CTD_ANON_13, documentation=u'READ_LABEL is a name for this tag, and can be used to on output to\n                                                determine read name, for example F or R.'))

CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'RELATIVE_ORDER'), CTD_ANON_17, scope=CTD_ANON_13, documentation=u' The read is located beginning at the offset or cycle relative to\n                                                    another read. This choice is appropriate for example when specifying a read that\n                                                    follows a variable length expected sequence(s). '))

CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'READ_INDEX'), pyxb.binding.datatypes.nonNegativeInteger, scope=CTD_ANON_13, documentation=u'READ_INDEX starts at 0 and is incrementally increased for each\n                                                sequential READ_SPEC within a SPOT_DECODE_SPEC'))

CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'EXPECTED_BASECALL'), CTD_ANON_5, scope=CTD_ANON_13, documentation=u' An expected basecall for a current read. Read will be\n                                                    zero-length if basecall is not present. Users of this facility should start\n                                                    migrating to EXPECTED_BASECALL_TABLE, as this field will be phased out. '))

CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'BASE_COORD'), pyxb.binding.datatypes.integer, scope=CTD_ANON_13, documentation=u' The location of the read start in terms of base count (1 is\n                                                    beginning of spot). '))

CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'CYCLE_COORD'), pyxb.binding.datatypes.integer, scope=CTD_ANON_13, documentation=u' The location of the read start in terms of cycle count (1 is\n                                                    beginning of spot). '))

CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'READ_TYPE'), STD_ANON_4, scope=CTD_ANON_13))

CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'EXPECTED_BASECALL_TABLE'), CTD_ANON_21, scope=CTD_ANON_13, documentation=u' A set of choices of expected basecalls for a current read. Read\n                                                    will be zero-length if none is found. '))
CTD_ANON_13._GroupModel_ = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(None, u'RELATIVE_ORDER')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(None, u'BASE_COORD')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(None, u'CYCLE_COORD')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(None, u'EXPECTED_BASECALL')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(None, u'EXPECTED_BASECALL_TABLE')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_13._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(None, u'READ_INDEX')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(None, u'READ_LABEL')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(None, u'READ_CLASS')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(None, u'READ_TYPE')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_13._GroupModel_, min_occurs=1, max_occurs=1)
    )
CTD_ANON_13._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_13._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_15._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'URL'), pyxb.binding.datatypes.anyURI, scope=CTD_ANON_15, documentation=u'An URL to the cross-references accession. '))

CTD_ANON_15._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DB'), pyxb.binding.datatypes.string, scope=CTD_ANON_15, documentation=u' EBI ENA controlled vocabulary of permitted cross references. '))

CTD_ANON_15._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LABEL'), pyxb.binding.datatypes.string, scope=CTD_ANON_15, documentation=u'A textual description of the cross-reference. '))

CTD_ANON_15._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ID'), pyxb.binding.datatypes.string, scope=CTD_ANON_15, documentation=u' Accession in the referenced database.'))
CTD_ANON_15._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(None, u'DB')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(None, u'ID')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(None, u'URL')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(None, u'LABEL')), min_occurs=0L, max_occurs=1L)
    )
CTD_ANON_15._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_15._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_16._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'bin'), CTD_ANON_9, scope=CTD_ANON_16))
CTD_ANON_16._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(None, u'bin')), min_occurs=1L, max_occurs=None)
    )
CTD_ANON_16._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_16._GroupModel, min_occurs=1, max_occurs=1)



LinkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'XREF_LINK'), XRefType, scope=LinkType))

LinkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SRA_LINK'), SraLinkType, scope=LinkType))

LinkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ENTREZ_LINK'), CTD_ANON_27, scope=LinkType))

LinkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DDBJ_LINK'), CTD_ANON_4, scope=LinkType))

LinkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'URL_LINK'), CTD_ANON_22, scope=LinkType))

LinkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ENA_LINK'), CTD_ANON_15, scope=LinkType))
LinkType._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(LinkType._UseForTag(pyxb.namespace.ExpandedName(None, u'SRA_LINK')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(LinkType._UseForTag(pyxb.namespace.ExpandedName(None, u'URL_LINK')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(LinkType._UseForTag(pyxb.namespace.ExpandedName(None, u'XREF_LINK')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(LinkType._UseForTag(pyxb.namespace.ExpandedName(None, u'ENTREZ_LINK')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(LinkType._UseForTag(pyxb.namespace.ExpandedName(None, u'DDBJ_LINK')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(LinkType._UseForTag(pyxb.namespace.ExpandedName(None, u'ENA_LINK')), min_occurs=1, max_occurs=1)
    )
LinkType._ContentModel = pyxb.binding.content.ParticleModel(LinkType._GroupModel, min_occurs=1, max_occurs=1)



AttributeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'UNITS'), pyxb.binding.datatypes.string, scope=AttributeType, documentation=u' Optional scientific units. '))

AttributeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'VALUE'), pyxb.binding.datatypes.string, scope=AttributeType, documentation=u' Value of the attribute. '))

AttributeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TAG'), pyxb.binding.datatypes.string, scope=AttributeType, documentation=u' Name of the attribute. '))
AttributeType._GroupModel = pyxb.binding.content.GroupAll(
    pyxb.binding.content.ParticleModel(AttributeType._UseForTag(pyxb.namespace.ExpandedName(None, u'TAG')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(AttributeType._UseForTag(pyxb.namespace.ExpandedName(None, u'VALUE')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(AttributeType._UseForTag(pyxb.namespace.ExpandedName(None, u'UNITS')), min_occurs=0L, max_occurs=1L)
    )
AttributeType._ContentModel = pyxb.binding.content.ParticleModel(AttributeType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_18._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), STD_ANON_6, scope=CTD_ANON_18))
CTD_ANON_18._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_18._UseForTag(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL')), min_occurs=1L, max_occurs=1L)
    )
CTD_ANON_18._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_18._GroupModel, min_occurs=1, max_occurs=1)



LibraryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DESIGN_DESCRIPTION'), pyxb.binding.datatypes.string, scope=LibraryType, documentation=u'Goal and setup of the individual library.'))

LibraryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SAMPLE_DESCRIPTOR'), SampleDescriptorType, scope=LibraryType, documentation=u' Pick a sample to associate this experiment with. The sample may be an individual or a pool,\n                        depending on how it is specified. '))

LibraryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'GAP_DESCRIPTOR'), GapDescriptorType, scope=LibraryType, documentation=u' The GAP_DESCRIPTOR specifies how to place the individual tags in the spot against a notinoal\n                        reference sequence. This information is important to interpreting the placement of spot tags in an assembly\n                        or alignment for the purpose of detecting structural variations and other genomic features. '))

LibraryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LIBRARY_DESCRIPTOR'), LibraryDescriptorType, scope=LibraryType, documentation=u' The LIBRARY_DESCRIPTOR specifies the origin of the material being sequenced and any\n                        treatments that the material might have undergone that affect the sequencing result. This specification is\n                        needed even if the platform does not require a library construction step per se. '))

LibraryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SPOT_DESCRIPTOR'), SpotDescriptorType, scope=LibraryType, documentation=u' The SPOT_DESCRIPTOR specifies how to decode the individual reads of interest from the\n                        monolithic spot sequence. The spot descriptor contains aspects of the experimental design, platform, and\n                        processing information. There will be two methods of specification: one will be an index into a table of\n                        typical decodings, the other being an exact specification. This construct is needed for loading data and for\n                        interpreting the loaded runs. It can be omitted if the loader can infer read layout (from multiple input\n                        files or from one input files). '))
LibraryType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(LibraryType._UseForTag(pyxb.namespace.ExpandedName(None, u'DESIGN_DESCRIPTION')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(LibraryType._UseForTag(pyxb.namespace.ExpandedName(None, u'SAMPLE_DESCRIPTOR')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(LibraryType._UseForTag(pyxb.namespace.ExpandedName(None, u'LIBRARY_DESCRIPTOR')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(LibraryType._UseForTag(pyxb.namespace.ExpandedName(None, u'SPOT_DESCRIPTOR')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LibraryType._UseForTag(pyxb.namespace.ExpandedName(None, u'GAP_DESCRIPTOR')), min_occurs=0L, max_occurs=1L)
    )
LibraryType._ContentModel = pyxb.binding.content.ParticleModel(LibraryType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_19._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), STD_ANON_7, scope=CTD_ANON_19))
CTD_ANON_19._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL')), min_occurs=1L, max_occurs=1L)
    )
CTD_ANON_19._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_19._GroupModel, min_occurs=1, max_occurs=1)



SampleDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'POOL'), CTD_ANON_35, scope=SampleDescriptorType, documentation=u' Identifies a list of group/pool/multiplex sample members. This implies that this sample\n                        record is a group, pool, or multiplex, but is continues to receive its own accession and can be referenced\n                        by an experiment. By default if no match to any of the listed members can be determined, then the default\n                        sampel reference is used. '))

SampleDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'IDENTIFIERS'), IdentifierType, scope=SampleDescriptorType, documentation=u' Set of reference IDs to parent experiment record. This block is intended to replace the use\n                        of the less structured RefNameGroup identifiers. '))
SampleDescriptorType._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(SampleDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'IDENTIFIERS')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SampleDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'POOL')), min_occurs=1, max_occurs=1)
    )
SampleDescriptorType._ContentModel = pyxb.binding.content.ParticleModel(SampleDescriptorType._GroupModel, min_occurs=0L, max_occurs=1L)



LibraryDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LIBRARY_SOURCE'), STD_ANON_11, scope=LibraryDescriptorType, documentation=u' The LIBRARY_SOURCE specifies the type of source material that is being sequenced. '))

LibraryDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LIBRARY_SELECTION'), STD_ANON_17, scope=LibraryDescriptorType, documentation=u' Whether any method was used to select for or against, enrich, or screen the material being\n                        sequenced. '))

LibraryDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LIBRARY_STRATEGY'), STD_ANON_10, scope=LibraryDescriptorType, documentation=u' Sequencing technique intended for this library. '))

LibraryDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TARGETED_LOCI'), CTD_ANON_, scope=LibraryDescriptorType))

LibraryDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LIBRARY_CONSTRUCTION_PROTOCOL'), pyxb.binding.datatypes.string, scope=LibraryDescriptorType, documentation=u' Free form text describing the protocol by which the sequencing library was constructed. '))

LibraryDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LIBRARY_LAYOUT'), CTD_ANON_23, scope=LibraryDescriptorType, documentation=u' LIBRARY_LAYOUT specifies whether to expect single, paired, or other configuration of reads.\n                        In the case of paired reads, information about the relative distance and orientation is specified. '))

LibraryDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LIBRARY_NAME'), pyxb.binding.datatypes.string, scope=LibraryDescriptorType, documentation=u" The submitter's name for this library. "))

LibraryDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'POOLING_STRATEGY'), STD_ANON_19, scope=LibraryDescriptorType, documentation=u' The optional pooling strategy indicates how the library or libraries are organized if\n                        multiple samples are involved. '))
LibraryDescriptorType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(LibraryDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'LIBRARY_NAME')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LibraryDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'LIBRARY_STRATEGY')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LibraryDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'LIBRARY_SOURCE')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(LibraryDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'LIBRARY_SELECTION')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(LibraryDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'LIBRARY_LAYOUT')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(LibraryDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'TARGETED_LOCI')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LibraryDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'POOLING_STRATEGY')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LibraryDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'LIBRARY_CONSTRUCTION_PROTOCOL')), min_occurs=0L, max_occurs=1L)
    )
LibraryDescriptorType._ContentModel = pyxb.binding.content.ParticleModel(LibraryDescriptorType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_20._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), STD_ANON_8, scope=CTD_ANON_20))
CTD_ANON_20._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_20._UseForTag(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL')), min_occurs=1L, max_occurs=1L)
    )
CTD_ANON_20._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_20._GroupModel, min_occurs=1, max_occurs=1)



SpotDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SPOT_DECODE_SPEC'), CTD_ANON_7, scope=SpotDescriptorType))

SpotDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SPOT_DECODE_METHOD'), pyxb.binding.datatypes.unsignedInt, scope=SpotDescriptorType, documentation=u' DEPRECATED. '))
SpotDescriptorType._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(SpotDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'SPOT_DECODE_METHOD')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SpotDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'SPOT_DECODE_SPEC')), min_occurs=1, max_occurs=1)
    )
SpotDescriptorType._ContentModel = pyxb.binding.content.ParticleModel(SpotDescriptorType._GroupModel, min_occurs=1, max_occurs=1)



PlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'COMPLETE_GENOMICS'), CTD_ANON_3, scope=PlatformType, documentation=u' CompleteGenomics platform type. At present there is no instrument model. '))

PlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LS454'), CTD_ANON_30, scope=PlatformType, documentation=u' 454 technology use 1-color sequential flows '))

PlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'HELICOS'), CTD_ANON_37, scope=PlatformType, documentation=u' Helicos is similar to 454 technology - uses 1-color sequential flows '))

PlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ABI_SOLID'), CTD_ANON_6, scope=PlatformType, documentation=u' ABI is 4-channel flowgram with 1-to-1 mapping between basecalls and flows '))

PlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PACBIO_SMRT'), CTD_ANON_18, scope=PlatformType, documentation=u' PacificBiosciences platform type for the single molecule real time (SMRT) technology. '))

PlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ION_TORRENT'), CTD_ANON_19, scope=PlatformType, documentation=u' Ion Torrent Personal Genome Machine (PGM) from Life Technologies. '))

PlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'CAPILLARY'), CTD_ANON_20, scope=PlatformType, documentation=u' Sequencers based on capillary electrophoresis technology manufactured by LifeTech (formerly\n                        Applied BioSciences). '))

PlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ILLUMINA'), CTD_ANON_29, scope=PlatformType, documentation=u' Illumina is 4-channel flowgram with 1-to-1 mapping between basecalls and flows '))
PlatformType._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, u'LS454')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, u'ILLUMINA')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, u'HELICOS')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, u'ABI_SOLID')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, u'COMPLETE_GENOMICS')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, u'PACBIO_SMRT')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, u'ION_TORRENT')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, u'CAPILLARY')), min_occurs=1, max_occurs=1)
    )
PlatformType._ContentModel = pyxb.binding.content.ParticleModel(PlatformType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_21._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'BASECALL'), CTD_ANON_24, scope=CTD_ANON_21, documentation=u" Element's body contains a basecall, attribute\n                                                                provide description of this read meaning as well as matching rules. "))
CTD_ANON_21._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_21._UseForTag(pyxb.namespace.ExpandedName(None, u'BASECALL')), min_occurs=1, max_occurs=None)
    )
CTD_ANON_21._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_21._GroupModel, min_occurs=1L, max_occurs=1L)



GapDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'GAP'), CTD_ANON_31, scope=GapDescriptorType))
GapDescriptorType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(GapDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'GAP')), min_occurs=1L, max_occurs=None)
    )
GapDescriptorType._ContentModel = pyxb.binding.content.ParticleModel(GapDescriptorType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LABEL'), pyxb.binding.datatypes.string, scope=CTD_ANON_22, documentation=u' Text label to display for the link. '))

CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'URL'), pyxb.binding.datatypes.anyURI, scope=CTD_ANON_22, documentation=u' The internet service link (file:, http:, ftp:, etc). '))
CTD_ANON_22._GroupModel = pyxb.binding.content.GroupAll(
    pyxb.binding.content.ParticleModel(CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(None, u'LABEL')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(None, u'URL')), min_occurs=1L, max_occurs=1L)
    )
CTD_ANON_22._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_22._GroupModel, min_occurs=1, max_occurs=1)



SequencingDirectivesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SAMPLE_DEMUX_DIRECTIVE'), STD_ANON_12, scope=SequencingDirectivesType, documentation=u' Tells the Archive who will execute the sample demultiplexing operation.. '))
SequencingDirectivesType._GroupModel = pyxb.binding.content.GroupAll(
    pyxb.binding.content.ParticleModel(SequencingDirectivesType._UseForTag(pyxb.namespace.ExpandedName(None, u'SAMPLE_DEMUX_DIRECTIVE')), min_occurs=0L, max_occurs=1L)
    )
SequencingDirectivesType._ContentModel = pyxb.binding.content.ParticleModel(SequencingDirectivesType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_23._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PAIRED'), CTD_ANON_28, scope=CTD_ANON_23))

CTD_ANON_23._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SINGLE'), CTD_ANON_26, scope=CTD_ANON_23))
CTD_ANON_23._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_23._UseForTag(pyxb.namespace.ExpandedName(None, u'SINGLE')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_23._UseForTag(pyxb.namespace.ExpandedName(None, u'PAIRED')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_23._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_23._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_25._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PROGRAM'), pyxb.binding.datatypes.string, scope=CTD_ANON_25, documentation=u' Name of the program or process for primary analysis. This may include a test or\n                                    condition that leads to branching in the workflow. '))

CTD_ANON_25._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PREV_STEP_INDEX'), pyxb.binding.datatypes.string, nillable=pyxb.binding.datatypes.boolean(1), scope=CTD_ANON_25, documentation=u' STEP_INDEX of the previous step in the workflow. Set toNIL if the first pipe\n                                    section. '))

CTD_ANON_25._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'NOTES'), pyxb.binding.datatypes.string, scope=CTD_ANON_25, documentation=u' Notes about the program or process for primary analysis. '))

CTD_ANON_25._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'STEP_INDEX'), pyxb.binding.datatypes.string, scope=CTD_ANON_25, documentation=u' Lexically ordered value that allows for the pipe section to be hierarchically\n                                    ordered. The float primitive data type is used to allow for pipe sections to be inserted later\n                                    on. '))

CTD_ANON_25._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'VERSION'), pyxb.binding.datatypes.string, scope=CTD_ANON_25, documentation=u' Version of the program or process for primary analysis. '))
CTD_ANON_25._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_25._UseForTag(pyxb.namespace.ExpandedName(None, u'STEP_INDEX')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_25._UseForTag(pyxb.namespace.ExpandedName(None, u'PREV_STEP_INDEX')), min_occurs=1L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_25._UseForTag(pyxb.namespace.ExpandedName(None, u'PROGRAM')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_25._UseForTag(pyxb.namespace.ExpandedName(None, u'VERSION')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_25._UseForTag(pyxb.namespace.ExpandedName(None, u'NOTES')), min_occurs=0L, max_occurs=1L)
    )
CTD_ANON_25._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_25._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_27._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DB'), pyxb.binding.datatypes.string, scope=CTD_ANON_27, documentation=u' NCBI controlled vocabulary of permitted cross references. Please see\n                                    http://www.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi? . '))

CTD_ANON_27._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ID'), pyxb.binding.datatypes.nonNegativeInteger, scope=CTD_ANON_27, documentation=u' Numeric record id meaningful to the NCBI Entrez system. '))

CTD_ANON_27._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'QUERY'), pyxb.binding.datatypes.string, scope=CTD_ANON_27, documentation=u' Accession string meaningful to the NCBI Entrez system. '))

CTD_ANON_27._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LABEL'), pyxb.binding.datatypes.string, scope=CTD_ANON_27, documentation=u' How to label the link. '))
CTD_ANON_27._GroupModel_ = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_27._UseForTag(pyxb.namespace.ExpandedName(None, u'ID')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_27._UseForTag(pyxb.namespace.ExpandedName(None, u'QUERY')), min_occurs=1L, max_occurs=1L)
    )
CTD_ANON_27._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_27._UseForTag(pyxb.namespace.ExpandedName(None, u'DB')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_27._GroupModel_, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_27._UseForTag(pyxb.namespace.ExpandedName(None, u'LABEL')), min_occurs=0L, max_occurs=1L)
    )
CTD_ANON_27._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_27._GroupModel, min_occurs=1, max_occurs=1)



IdentifierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'EXTERNAL_ID'), NameType, scope=IdentifierType, documentation=u'An identifier from another non-INSDC database qualified by a namespace.'))

IdentifierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PRIMARY_ID'), AccessionType, scope=IdentifierType, documentation=u'A primary key in an INSDC primary data database.'))

IdentifierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SECONDARY_ID'), AccessionType, scope=IdentifierType, documentation=u'A secondary or defunct primary key in an INSDC primary data database.'))

IdentifierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'UUID'), UUIDType, scope=IdentifierType, documentation=u'A universally unique identifier that requires no namespace.'))

IdentifierType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SUBMITTER_ID'), NameType, scope=IdentifierType, documentation=u'A local identifier provided by a submitter and qualified by a namespace.'))
IdentifierType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(IdentifierType._UseForTag(pyxb.namespace.ExpandedName(None, u'PRIMARY_ID')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(IdentifierType._UseForTag(pyxb.namespace.ExpandedName(None, u'SECONDARY_ID')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(IdentifierType._UseForTag(pyxb.namespace.ExpandedName(None, u'EXTERNAL_ID')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(IdentifierType._UseForTag(pyxb.namespace.ExpandedName(None, u'SUBMITTER_ID')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(IdentifierType._UseForTag(pyxb.namespace.ExpandedName(None, u'UUID')), min_occurs=0L, max_occurs=1L)
    )
IdentifierType._ContentModel = pyxb.binding.content.ParticleModel(IdentifierType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_29._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'CYCLE_SEQUENCE'), pyxb.binding.datatypes.string, scope=CTD_ANON_29, documentation=u' DEPRECATED. '))

CTD_ANON_29._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'CYCLE_COUNT'), pyxb.binding.datatypes.positiveInteger, scope=CTD_ANON_29, documentation=u' DEPRECATED, use SPOT_LENGTH instead. The fixed number of bases in each raw\n                                    sequence, including both mate pairs and any technical reads. '))

CTD_ANON_29._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SEQUENCE_LENGTH'), pyxb.binding.datatypes.positiveInteger, scope=CTD_ANON_29, documentation=u' DEPRECATED, use SPOT_LENGTH instead. The fixed number of bases expected in each\n                                    raw sequence, including both mate pairs and any technical reads. '))

CTD_ANON_29._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), STD_ANON_15, scope=CTD_ANON_29))
CTD_ANON_29._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_29._UseForTag(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_29._UseForTag(pyxb.namespace.ExpandedName(None, u'CYCLE_SEQUENCE')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_29._UseForTag(pyxb.namespace.ExpandedName(None, u'CYCLE_COUNT')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_29._UseForTag(pyxb.namespace.ExpandedName(None, u'SEQUENCE_LENGTH')), min_occurs=0L, max_occurs=1L)
    )
CTD_ANON_29._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_29._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_30._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'FLOW_COUNT'), pyxb.binding.datatypes.positiveInteger, scope=CTD_ANON_30, documentation=u' DEPRECATED. Use SPOT_LENGTH instead. The number of flows of challenge bases.\n                                    This is a constraint on maximum read length, but not equivalent. This is optional in the schema\n                                    now but will be required by business rules and future schema versions. '))

CTD_ANON_30._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), STD_ANON_13, scope=CTD_ANON_30))

CTD_ANON_30._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'FLOW_SEQUENCE'), pyxb.binding.datatypes.string, scope=CTD_ANON_30, documentation=u' DEPRECATED. The fixed sequence of challenge bases that flow across the picotiter\n                                    plate. This is optional in the schema now but will be required by business rules and future\n                                    schema versions. '))

CTD_ANON_30._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'KEY_SEQUENCE'), pyxb.binding.datatypes.string, scope=CTD_ANON_30, documentation=u' DEPRECATED. The first bases that are expected to be produced by the challenge\n                                    bases. This is optional in the schema now but will be required by business rules and future\n                                    schema versions. '))
CTD_ANON_30._GroupModel = pyxb.binding.content.GroupAll(
    pyxb.binding.content.ParticleModel(CTD_ANON_30._UseForTag(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_30._UseForTag(pyxb.namespace.ExpandedName(None, u'KEY_SEQUENCE')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_30._UseForTag(pyxb.namespace.ExpandedName(None, u'FLOW_SEQUENCE')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_30._UseForTag(pyxb.namespace.ExpandedName(None, u'FLOW_COUNT')), min_occurs=0L, max_occurs=1L)
    )
CTD_ANON_30._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_30._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_31._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'GAP_SPEC'), CTD_ANON_2, scope=CTD_ANON_31))

CTD_ANON_31._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'GAP_TYPE'), CTD_ANON_34, scope=CTD_ANON_31, documentation=u' Specifies the gap type and parameters. '))
CTD_ANON_31._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_31._UseForTag(pyxb.namespace.ExpandedName(None, u'GAP_TYPE')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_31._UseForTag(pyxb.namespace.ExpandedName(None, u'GAP_SPEC')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_31._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_31._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_33._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PROBE_SET'), XRefType, scope=CTD_ANON_33, documentation=u' Reference to an archived primer or probe set. Example: dbProbe '))
CTD_ANON_33._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_33._UseForTag(pyxb.namespace.ExpandedName(None, u'PROBE_SET')), min_occurs=0L, max_occurs=1L)
    )
CTD_ANON_33._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_33._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_34._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PairedEnd'), CTD_ANON, scope=CTD_ANON_34, documentation=u' Mated tags sequenced from two ends of a physical extent of genomic\n                                                material. '))

CTD_ANON_34._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'MatePair'), CTD_ANON_38, scope=CTD_ANON_34, documentation=u' Mated tags with predicted separation and orientation. '))

CTD_ANON_34._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Tandem'), CTD_ANON_36, scope=CTD_ANON_34, documentation=u' Tandem gaps between ligands. '))
CTD_ANON_34._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_34._UseForTag(pyxb.namespace.ExpandedName(None, u'Tandem')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_34._UseForTag(pyxb.namespace.ExpandedName(None, u'MatePair')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_34._UseForTag(pyxb.namespace.ExpandedName(None, u'PairedEnd')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_34._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_34._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_35._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DEFAULT_MEMBER'), PoolMemberType, scope=CTD_ANON_35, documentation=u' Reference to the sample that is used when read membership cannot be determined.\n                                    A default member should be provided if there exists a possibility that some reads will be left\n                                    over from barcode/MID resolution. A default member is not needed when defining a true pool\n                                    (where individual samples are not distinguished in the reads), or the reads have been\n                                    partitioned among the pool members (no leftovers). '))

CTD_ANON_35._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'MEMBER'), PoolMemberType, scope=CTD_ANON_35, documentation=u' Reference to the sample as determined from barcode/MID resolution or read\n                                    partition. '))
CTD_ANON_35._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_35._UseForTag(pyxb.namespace.ExpandedName(None, u'DEFAULT_MEMBER')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_35._UseForTag(pyxb.namespace.ExpandedName(None, u'MEMBER')), min_occurs=1L, max_occurs=None)
    )
CTD_ANON_35._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_35._GroupModel, min_occurs=1, max_occurs=1)



PoolMemberType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'IDENTIFIERS'), IdentifierType, scope=PoolMemberType, documentation=u' Set of reference IDs to parent experiment record. This block is intended to replace the use\n                        of the less structured RefNameGroup identifiers. '))

PoolMemberType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'READ_LABEL'), CTD_ANON_32, scope=PoolMemberType))
PoolMemberType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(PoolMemberType._UseForTag(pyxb.namespace.ExpandedName(None, u'IDENTIFIERS')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(PoolMemberType._UseForTag(pyxb.namespace.ExpandedName(None, u'READ_LABEL')), min_occurs=0L, max_occurs=None)
    )
PoolMemberType._ContentModel = pyxb.binding.content.ParticleModel(PoolMemberType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_37._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'FLOW_COUNT'), pyxb.binding.datatypes.positiveInteger, scope=CTD_ANON_37, documentation=u' DEPRECATED. Use SPOT_LENGTH instead. The number of flows of challenge bases.\n                                    This is a constraint on maximum read length, but not equivalent. This is optional in the schema\n                                    now but will be required by business rules and future schema versions. '))

CTD_ANON_37._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), STD_ANON, scope=CTD_ANON_37))

CTD_ANON_37._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'FLOW_SEQUENCE'), pyxb.binding.datatypes.string, scope=CTD_ANON_37, documentation=u' DEPRECATED. The fixed sequence of challenge bases that flow across the flowcell.\n                                    This is optional in the schema now but will be required by business rules and future schema\n                                    versions. '))
CTD_ANON_37._GroupModel = pyxb.binding.content.GroupAll(
    pyxb.binding.content.ParticleModel(CTD_ANON_37._UseForTag(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_37._UseForTag(pyxb.namespace.ExpandedName(None, u'FLOW_SEQUENCE')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_37._UseForTag(pyxb.namespace.ExpandedName(None, u'FLOW_COUNT')), min_occurs=0L, max_occurs=1L)
    )
CTD_ANON_37._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_37._GroupModel, min_occurs=1, max_occurs=1)
