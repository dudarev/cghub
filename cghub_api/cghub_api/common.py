# ./common.py
# PyXB bindings for NM:1c06abdc99453cc1e399eecb45b4dd01ec9af52b
# Generated 2012-06-04 19:53:07.344181 by PyXB version 1.1.3
# Namespace SRA.common

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:c230210e-ae65-11e1-bc27-0026c7825912')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

Namespace = pyxb.namespace.NamespaceForURI(u'SRA.common', create_if_missing=True)
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
STD_ANON.Illumina_Genome_Analyzer = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'Illumina Genome Analyzer', tag=u'Illumina_Genome_Analyzer')
STD_ANON.Illumina_Genome_Analyzer_II = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'Illumina Genome Analyzer II', tag=u'Illumina_Genome_Analyzer_II')
STD_ANON.Illumina_Genome_Analyzer_IIx = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'Illumina Genome Analyzer IIx', tag=u'Illumina_Genome_Analyzer_IIx')
STD_ANON.Illumina_HiSeq_2500 = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'Illumina HiSeq 2500', tag=u'Illumina_HiSeq_2500')
STD_ANON.Illumina_HiSeq_2000 = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'Illumina HiSeq 2000', tag=u'Illumina_HiSeq_2000')
STD_ANON.Illumina_HiSeq_1000 = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'Illumina HiSeq 1000', tag=u'Illumina_HiSeq_1000')
STD_ANON.Illumina_HiScanSQ = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'Illumina HiScanSQ', tag=u'Illumina_HiScanSQ')
STD_ANON.Illumina_MiSeq = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'Illumina MiSeq', tag=u'Illumina_MiSeq')
STD_ANON.unspecified = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'unspecified', tag=u'unspecified')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_ (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_, enum_prefix=None)
STD_ANON_.none = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'none', tag=u'none')
STD_ANON_.simple_pool = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'simple pool', tag=u'simple_pool')
STD_ANON_.multiplexed_samples = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'multiplexed samples', tag=u'multiplexed_samples')
STD_ANON_.multiplexed_libraries = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'multiplexed libraries', tag=u'multiplexed_libraries')
STD_ANON_.spiked_library = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'spiked library', tag=u'spiked_library')
STD_ANON_.other = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'other', tag=u'other')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_2 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_2._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_2, enum_prefix=None)
STD_ANON_2.n16S_rRNA = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value=u'16S rRNA', tag=u'n16S_rRNA')
STD_ANON_2.exome = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value=u'exome', tag=u'exome')
STD_ANON_2.other = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value=u'other', tag=u'other')
STD_ANON_2._InitializeFacetMap(STD_ANON_2._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_3 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_3._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_3, enum_prefix=None)
STD_ANON_3.Helicos_HeliScope = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value=u'Helicos HeliScope', tag=u'Helicos_HeliScope')
STD_ANON_3.unspecified = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value=u'unspecified', tag=u'unspecified')
STD_ANON_3._InitializeFacetMap(STD_ANON_3._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_4 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_4._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_4, enum_prefix=None)
STD_ANON_4.full = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'full', tag=u'full')
STD_ANON_4.start = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'start', tag=u'start')
STD_ANON_4.end = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'end', tag=u'end')
STD_ANON_4._InitializeFacetMap(STD_ANON_4._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_5 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_5._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_5, enum_prefix=None)
STD_ANON_5.WGS = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'WGS', tag=u'WGS')
STD_ANON_5.WXS = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'WXS', tag=u'WXS')
STD_ANON_5.RNA_Seq = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'RNA-Seq', tag=u'RNA_Seq')
STD_ANON_5.WCS = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'WCS', tag=u'WCS')
STD_ANON_5.CLONE = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'CLONE', tag=u'CLONE')
STD_ANON_5.POOLCLONE = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'POOLCLONE', tag=u'POOLCLONE')
STD_ANON_5.AMPLICON = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'AMPLICON', tag=u'AMPLICON')
STD_ANON_5.CLONEEND = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'CLONEEND', tag=u'CLONEEND')
STD_ANON_5.FINISHING = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'FINISHING', tag=u'FINISHING')
STD_ANON_5.ChIP_Seq = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'ChIP-Seq', tag=u'ChIP_Seq')
STD_ANON_5.MNase_Seq = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'MNase-Seq', tag=u'MNase_Seq')
STD_ANON_5.DNase_Hypersensitivity = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'DNase-Hypersensitivity', tag=u'DNase_Hypersensitivity')
STD_ANON_5.Bisulfite_Seq = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'Bisulfite-Seq', tag=u'Bisulfite_Seq')
STD_ANON_5.EST = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'EST', tag=u'EST')
STD_ANON_5.FL_cDNA = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'FL-cDNA', tag=u'FL_cDNA')
STD_ANON_5.CTS = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'CTS', tag=u'CTS')
STD_ANON_5.MRE_Seq = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'MRE-Seq', tag=u'MRE_Seq')
STD_ANON_5.MeDIP_Seq = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'MeDIP-Seq', tag=u'MeDIP_Seq')
STD_ANON_5.MBD_Seq = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'MBD-Seq', tag=u'MBD_Seq')
STD_ANON_5.OTHER = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value=u'OTHER', tag=u'OTHER')
STD_ANON_5._InitializeFacetMap(STD_ANON_5._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_6 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_6._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_6, enum_prefix=None)
STD_ANON_6.GENOMIC = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value=u'GENOMIC', tag=u'GENOMIC')
STD_ANON_6.TRANSCRIPTOMIC = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value=u'TRANSCRIPTOMIC', tag=u'TRANSCRIPTOMIC')
STD_ANON_6.METAGENOMIC = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value=u'METAGENOMIC', tag=u'METAGENOMIC')
STD_ANON_6.METATRANSCRIPTOMIC = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value=u'METATRANSCRIPTOMIC', tag=u'METATRANSCRIPTOMIC')
STD_ANON_6.NON_GENOMIC = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value=u'NON GENOMIC', tag=u'NON_GENOMIC')
STD_ANON_6.SYNTHETIC = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value=u'SYNTHETIC', tag=u'SYNTHETIC')
STD_ANON_6.VIRAL_RNA = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value=u'VIRAL RNA', tag=u'VIRAL_RNA')
STD_ANON_6.OTHER = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value=u'OTHER', tag=u'OTHER')
STD_ANON_6._InitializeFacetMap(STD_ANON_6._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_7 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_7._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_7, enum_prefix=None)
STD_ANON_7.AB_SOLiD_System = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value=u'AB SOLiD System', tag=u'AB_SOLiD_System')
STD_ANON_7.AB_SOLiD_System_2_0 = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value=u'AB SOLiD System 2.0', tag=u'AB_SOLiD_System_2_0')
STD_ANON_7.AB_SOLiD_System_3_0 = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value=u'AB SOLiD System 3.0', tag=u'AB_SOLiD_System_3_0')
STD_ANON_7.AB_SOLiD_System_3_Plus = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value=u'AB SOLiD System 3 Plus', tag=u'AB_SOLiD_System_3_Plus')
STD_ANON_7.AB_SOLiD_4_System = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value=u'AB SOLiD 4 System', tag=u'AB_SOLiD_4_System')
STD_ANON_7.AB_SOLiD_4hq_System = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value=u'AB SOLiD 4hq System', tag=u'AB_SOLiD_4hq_System')
STD_ANON_7.AB_SOLiD_PI_System = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value=u'AB SOLiD PI System', tag=u'AB_SOLiD_PI_System')
STD_ANON_7.AB_SOLiD_5500 = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value=u'AB SOLiD 5500', tag=u'AB_SOLiD_5500')
STD_ANON_7.AB_SOLiD_5500xl = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value=u'AB SOLiD 5500xl', tag=u'AB_SOLiD_5500xl')
STD_ANON_7.unspecified = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value=u'unspecified', tag=u'unspecified')
STD_ANON_7._InitializeFacetMap(STD_ANON_7._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_8 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_8._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_8, enum_prefix=None)
STD_ANON_8.RANDOM = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'RANDOM', tag=u'RANDOM')
STD_ANON_8.PCR = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'PCR', tag=u'PCR')
STD_ANON_8.RANDOM_PCR = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'RANDOM PCR', tag=u'RANDOM_PCR')
STD_ANON_8.RT_PCR = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'RT-PCR', tag=u'RT_PCR')
STD_ANON_8.HMPR = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'HMPR', tag=u'HMPR')
STD_ANON_8.MF = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'MF', tag=u'MF')
STD_ANON_8.CF_S = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'CF-S', tag=u'CF_S')
STD_ANON_8.CF_M = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'CF-M', tag=u'CF_M')
STD_ANON_8.CF_H = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'CF-H', tag=u'CF_H')
STD_ANON_8.CF_T = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'CF-T', tag=u'CF_T')
STD_ANON_8.MSLL = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'MSLL', tag=u'MSLL')
STD_ANON_8.cDNA = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'cDNA', tag=u'cDNA')
STD_ANON_8.ChIP = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'ChIP', tag=u'ChIP')
STD_ANON_8.MNase = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'MNase', tag=u'MNase')
STD_ANON_8.DNAse = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'DNAse', tag=u'DNAse')
STD_ANON_8.Hybrid_Selection = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'Hybrid Selection', tag=u'Hybrid_Selection')
STD_ANON_8.Reduced_Representation = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'Reduced Representation', tag=u'Reduced_Representation')
STD_ANON_8.Restriction_Digest = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'Restriction Digest', tag=u'Restriction_Digest')
STD_ANON_8.n5_methylcytidine_antibody = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'5-methylcytidine antibody', tag=u'n5_methylcytidine_antibody')
STD_ANON_8.MBD2_protein_methyl_CpG_binding_domain = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'MBD2 protein methyl-CpG binding domain', tag=u'MBD2_protein_methyl_CpG_binding_domain')
STD_ANON_8.CAGE = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'CAGE', tag=u'CAGE')
STD_ANON_8.RACE = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'RACE', tag=u'RACE')
STD_ANON_8.size_fractionation = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'size fractionation', tag=u'size_fractionation')
STD_ANON_8.other = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'other', tag=u'other')
STD_ANON_8.unspecified = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value=u'unspecified', tag=u'unspecified')
STD_ANON_8._InitializeFacetMap(STD_ANON_8._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_9 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_9._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_9, enum_prefix=None)
STD_ANON_9.Application_Read = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'Application Read', tag=u'Application_Read')
STD_ANON_9.Technical_Read = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value=u'Technical Read', tag=u'Technical_Read')
STD_ANON_9._InitializeFacetMap(STD_ANON_9._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_10 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_10._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_10, enum_prefix=None)
STD_ANON_10.STUDY = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'STUDY', tag=u'STUDY')
STD_ANON_10.SAMPLE = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'SAMPLE', tag=u'SAMPLE')
STD_ANON_10.ANALYSIS = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'ANALYSIS', tag=u'ANALYSIS')
STD_ANON_10.EXPERIMENT = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'EXPERIMENT', tag=u'EXPERIMENT')
STD_ANON_10.RUN = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value=u'RUN', tag=u'RUN')
STD_ANON_10._InitializeFacetMap(STD_ANON_10._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_11 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_11._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_11, enum_prefix=None)
STD_ANON_11.Forward = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value=u'Forward', tag=u'Forward')
STD_ANON_11.Reverse = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value=u'Reverse', tag=u'Reverse')
STD_ANON_11.Adapter = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value=u'Adapter', tag=u'Adapter')
STD_ANON_11.Primer = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value=u'Primer', tag=u'Primer')
STD_ANON_11.Linker = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value=u'Linker', tag=u'Linker')
STD_ANON_11.BarCode = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value=u'BarCode', tag=u'BarCode')
STD_ANON_11.Other = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value=u'Other', tag=u'Other')
STD_ANON_11._InitializeFacetMap(STD_ANON_11._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_12 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_12._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_12, enum_prefix=None)
STD_ANON_12.innie = STD_ANON_12._CF_enumeration.addEnumeration(unicode_value=u'innie', tag=u'innie')
STD_ANON_12.outie = STD_ANON_12._CF_enumeration.addEnumeration(unicode_value=u'outie', tag=u'outie')
STD_ANON_12.normal = STD_ANON_12._CF_enumeration.addEnumeration(unicode_value=u'normal', tag=u'normal')
STD_ANON_12.anti_normal = STD_ANON_12._CF_enumeration.addEnumeration(unicode_value=u'anti-normal', tag=u'anti_normal')
STD_ANON_12._InitializeFacetMap(STD_ANON_12._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_13 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_13._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_13, enum_prefix=None)
STD_ANON_13.Complete_Genomics = STD_ANON_13._CF_enumeration.addEnumeration(unicode_value=u'Complete Genomics', tag=u'Complete_Genomics')
STD_ANON_13.unspecified = STD_ANON_13._CF_enumeration.addEnumeration(unicode_value=u'unspecified', tag=u'unspecified')
STD_ANON_13.none = STD_ANON_13._CF_enumeration.addEnumeration(unicode_value=u'none', tag=u'none')
STD_ANON_13._InitializeFacetMap(STD_ANON_13._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_14 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_14._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_14, enum_prefix=None)
STD_ANON_14.PacBio_RS = STD_ANON_14._CF_enumeration.addEnumeration(unicode_value=u'PacBio RS', tag=u'PacBio_RS')
STD_ANON_14.unspecified = STD_ANON_14._CF_enumeration.addEnumeration(unicode_value=u'unspecified', tag=u'unspecified')
STD_ANON_14.none = STD_ANON_14._CF_enumeration.addEnumeration(unicode_value=u'none', tag=u'none')
STD_ANON_14._InitializeFacetMap(STD_ANON_14._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_15 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_15._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_15, enum_prefix=None)
STD_ANON_15.Ion_Torrent_PGM = STD_ANON_15._CF_enumeration.addEnumeration(unicode_value=u'Ion Torrent PGM', tag=u'Ion_Torrent_PGM')
STD_ANON_15.Ion_Torrent_Proton = STD_ANON_15._CF_enumeration.addEnumeration(unicode_value=u'Ion Torrent Proton', tag=u'Ion_Torrent_Proton')
STD_ANON_15.unspecified = STD_ANON_15._CF_enumeration.addEnumeration(unicode_value=u'unspecified', tag=u'unspecified')
STD_ANON_15._InitializeFacetMap(STD_ANON_15._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_16 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_16._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_16, enum_prefix=None)
STD_ANON_16.leave_as_pool = STD_ANON_16._CF_enumeration.addEnumeration(unicode_value=u'leave_as_pool', tag=u'leave_as_pool')
STD_ANON_16.submitter_demultiplexed = STD_ANON_16._CF_enumeration.addEnumeration(unicode_value=u'submitter_demultiplexed', tag=u'submitter_demultiplexed')
STD_ANON_16._InitializeFacetMap(STD_ANON_16._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_17 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_17._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_17, enum_prefix=None)
STD_ANON_17.n454_GS = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'454 GS', tag=u'n454_GS')
STD_ANON_17.n454_GS_20 = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'454 GS 20', tag=u'n454_GS_20')
STD_ANON_17.n454_GS_FLX = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'454 GS FLX', tag=u'n454_GS_FLX')
STD_ANON_17.n454_GS_FLX_Titanium = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'454 GS FLX Titanium', tag=u'n454_GS_FLX_Titanium')
STD_ANON_17.n454_GS_FLX_Plus = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'454 GS FLX Plus', tag=u'n454_GS_FLX_Plus')
STD_ANON_17.n454_GS_Junior = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'454 GS Junior', tag=u'n454_GS_Junior')
STD_ANON_17.unspecified = STD_ANON_17._CF_enumeration.addEnumeration(unicode_value=u'unspecified', tag=u'unspecified')
STD_ANON_17._InitializeFacetMap(STD_ANON_17._CF_enumeration)

# Complex type CTD_ANON with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element LOCUS uses Python identifier LOCUS
    __LOCUS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LOCUS'), 'LOCUS', '__SRA_common_CTD_ANON_LOCUS', True)

    
    LOCUS = property(__LOCUS.value, __LOCUS.set, None, None)


    _ElementMap = {
        __LOCUS.name() : __LOCUS
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
    
    # Element SEQUENCE_LENGTH uses Python identifier SEQUENCE_LENGTH
    __SEQUENCE_LENGTH = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SEQUENCE_LENGTH'), 'SEQUENCE_LENGTH', '__SRA_common_CTD_ANON__SEQUENCE_LENGTH', False)

    
    SEQUENCE_LENGTH = property(__SEQUENCE_LENGTH.value, __SEQUENCE_LENGTH.set, None, u'\n                                        The fixed number of bases expected in each raw sequence, including both mate pairs and any technical reads.\n                                    ')

    
    # Element CYCLE_COUNT uses Python identifier CYCLE_COUNT
    __CYCLE_COUNT = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'CYCLE_COUNT'), 'CYCLE_COUNT', '__SRA_common_CTD_ANON__CYCLE_COUNT', False)

    
    CYCLE_COUNT = property(__CYCLE_COUNT.value, __CYCLE_COUNT.set, None, u'\n                                        DEPRECATED, use SEQUENCE_LENGTH instead.  The fixed number of bases  in each raw sequence, including both mate pairs and any technical reads.\n                                    ')

    
    # Element INSTRUMENT_MODEL uses Python identifier INSTRUMENT_MODEL
    __INSTRUMENT_MODEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), 'INSTRUMENT_MODEL', '__SRA_common_CTD_ANON__INSTRUMENT_MODEL', False)

    
    INSTRUMENT_MODEL = property(__INSTRUMENT_MODEL.value, __INSTRUMENT_MODEL.set, None, None)

    
    # Element CYCLE_SEQUENCE uses Python identifier CYCLE_SEQUENCE
    __CYCLE_SEQUENCE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'CYCLE_SEQUENCE'), 'CYCLE_SEQUENCE', '__SRA_common_CTD_ANON__CYCLE_SEQUENCE', False)

    
    CYCLE_SEQUENCE = property(__CYCLE_SEQUENCE.value, __CYCLE_SEQUENCE.set, None, u'\n                                        DEPRECATED.\n                                    ')


    _ElementMap = {
        __SEQUENCE_LENGTH.name() : __SEQUENCE_LENGTH,
        __CYCLE_COUNT.name() : __CYCLE_COUNT,
        __INSTRUMENT_MODEL.name() : __INSTRUMENT_MODEL,
        __CYCLE_SEQUENCE.name() : __CYCLE_SEQUENCE
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

    
    POOL = property(__POOL.value, __POOL.set, None, u'\n                        Identifies a list of group/pool/multiplex sample members.  This implies that\n                        this sample record is a group, pool, or multiplex, but is continues to receive\n                        its own accession and can be referenced by an experiment.  By default if\n                        no match to any of the listed members can be determined, then the default\n                        sampel reference is used.\n                    ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'accession'), 'accession', '__SRA_common_SampleDescriptorType_accession', pyxb.binding.datatypes.string)
    
    accession = property(__accession.value, __accession.set, None, u'\n                    Identifies a record by its accession.  The scope of resolution is the entire Archive.\n                ')

    
    # Attribute refcenter uses Python identifier refcenter
    __refcenter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refcenter'), 'refcenter', '__SRA_common_SampleDescriptorType_refcenter', pyxb.binding.datatypes.string)
    
    refcenter = property(__refcenter.value, __refcenter.set, None, u'\n                    The center namespace of the attribute "refname". When absent, the namespace is assumed to be the current submission.\n                ')

    
    # Attribute refname uses Python identifier refname
    __refname = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refname'), 'refname', '__SRA_common_SampleDescriptorType_refname', pyxb.binding.datatypes.string)
    
    refname = property(__refname.value, __refname.set, None, u'\n                    Identifies a record by name that is known within the namespace defined by attribute "refcenter"\n                    Use this field when referencing an object for which an accession has not yet been issued.\n                ')


    _ElementMap = {
        __POOL.name() : __POOL
    }
    _AttributeMap = {
        __accession.name() : __accession,
        __refcenter.name() : __refcenter,
        __refname.name() : __refname
    }
Namespace.addCategoryObject('typeBinding', u'SampleDescriptorType', SampleDescriptorType)


# Complex type CTD_ANON_2 with content type ELEMENT_ONLY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element DESCRIPTION uses Python identifier DESCRIPTION
    __DESCRIPTION = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DESCRIPTION'), 'DESCRIPTION', '__SRA_common_CTD_ANON_2_DESCRIPTION', False)

    
    DESCRIPTION = property(__DESCRIPTION.value, __DESCRIPTION.set, None, u'Description of the genome\n                                                 assembly.')

    
    # Element URL_LINK uses Python identifier URL_LINK
    __URL_LINK = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'URL_LINK'), 'URL_LINK', '__SRA_common_CTD_ANON_2_URL_LINK', True)

    
    URL_LINK = property(__URL_LINK.value, __URL_LINK.set, None, u'A link to the genome\n                                                 assembly.')


    _ElementMap = {
        __DESCRIPTION.name() : __DESCRIPTION,
        __URL_LINK.name() : __URL_LINK
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
    
    # Element MEMBER uses Python identifier MEMBER
    __MEMBER = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'MEMBER'), 'MEMBER', '__SRA_common_CTD_ANON_3_MEMBER', True)

    
    MEMBER = property(__MEMBER.value, __MEMBER.set, None, None)


    _ElementMap = {
        __MEMBER.name() : __MEMBER
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_4 with content type SIMPLE
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute base_coord uses Python identifier base_coord
    __base_coord = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'base_coord'), 'base_coord', '__SRA_common_CTD_ANON_4_base_coord', pyxb.binding.datatypes.nonNegativeInteger)
    
    base_coord = property(__base_coord.value, __base_coord.set, None, u'\n                                                                        Specify an optional starting point for tag (base offset from 1).  \n                                                                    ')

    
    # Attribute default_length uses Python identifier default_length
    __default_length = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'default_length'), 'default_length', '__SRA_common_CTD_ANON_4_default_length', pyxb.binding.datatypes.nonNegativeInteger)
    
    default_length = property(__default_length.value, __default_length.set, None, u'\n                                                                        Specify whether the spot should have a default length for this tag if the expected base cannot be matched.\n                                                                    ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __base_coord.name() : __base_coord,
        __default_length.name() : __default_length
    }



# Complex type CTD_ANON_5 with content type ELEMENT_ONLY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LABEL'), 'LABEL', '__SRA_common_CTD_ANON_5_LABEL', False)

    
    LABEL = property(__LABEL.value, __LABEL.set, None, u' Text label to display for the\n                                                 link. ')

    
    # Element URL uses Python identifier URL
    __URL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'URL'), 'URL', '__SRA_common_CTD_ANON_5_URL', False)

    
    URL = property(__URL.value, __URL.set, None, u' The internet service link\n                                                 (file:, http:, ftp:, etc). ')


    _ElementMap = {
        __LABEL.name() : __LABEL,
        __URL.name() : __URL
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_6 with content type ELEMENT_ONLY
class CTD_ANON_6 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element READ_LABEL uses Python identifier READ_LABEL
    __READ_LABEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'READ_LABEL'), 'READ_LABEL', '__SRA_common_CTD_ANON_6_READ_LABEL', True)

    
    READ_LABEL = property(__READ_LABEL.value, __READ_LABEL.set, None, None)

    
    # Attribute proportion uses Python identifier proportion
    __proportion = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'proportion'), 'proportion', '__SRA_common_CTD_ANON_6_proportion', pyxb.binding.datatypes.float)
    
    proportion = property(__proportion.value, __proportion.set, None, u'\n                                            Proportion of this sample (in percent) that was included in sample pool.\n                                        ')

    
    # Attribute refcenter uses Python identifier refcenter
    __refcenter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refcenter'), 'refcenter', '__SRA_common_CTD_ANON_6_refcenter', pyxb.binding.datatypes.string)
    
    refcenter = property(__refcenter.value, __refcenter.set, None, u'\n                    The center namespace of the attribute "refname". When absent, the namespace is assumed to be the current submission.\n                ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'accession'), 'accession', '__SRA_common_CTD_ANON_6_accession', pyxb.binding.datatypes.string)
    
    accession = property(__accession.value, __accession.set, None, u'\n                    Identifies a record by its accession.  The scope of resolution is the entire Archive.\n                ')

    
    # Attribute member_name uses Python identifier member_name
    __member_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'member_name'), 'member_name', '__SRA_common_CTD_ANON_6_member_name', pyxb.binding.datatypes.string)
    
    member_name = property(__member_name.value, __member_name.set, None, u'\n                                            Label a sample within a scope of the pool \n                                        ')

    
    # Attribute refname uses Python identifier refname
    __refname = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refname'), 'refname', '__SRA_common_CTD_ANON_6_refname', pyxb.binding.datatypes.string)
    
    refname = property(__refname.value, __refname.set, None, u'\n                    Identifies a record by name that is known within the namespace defined by attribute "refcenter"\n                    Use this field when referencing an object for which an accession has not yet been issued.\n                ')


    _ElementMap = {
        __READ_LABEL.name() : __READ_LABEL
    }
    _AttributeMap = {
        __proportion.name() : __proportion,
        __refcenter.name() : __refcenter,
        __accession.name() : __accession,
        __member_name.name() : __member_name,
        __refname.name() : __refname
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


# Complex type CTD_ANON_7 with content type ELEMENT_ONLY
class CTD_ANON_7 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element BASECALL uses Python identifier BASECALL
    __BASECALL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'BASECALL'), 'BASECALL', '__SRA_common_CTD_ANON_7_BASECALL', True)

    
    BASECALL = property(__BASECALL.value, __BASECALL.set, None, u"\n                                                                    Element's body contains a basecall, attribute provide description of this read meaning as well as matching rules.\n                                                                ")

    
    # Attribute default_length uses Python identifier default_length
    __default_length = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'default_length'), 'default_length', '__SRA_common_CTD_ANON_7_default_length', pyxb.binding.datatypes.nonNegativeInteger)
    
    default_length = property(__default_length.value, __default_length.set, None, u'\n                                                                Specify whether the spot should have a default length for this tag if the expected base cannot be matched.\n                                                            ')

    
    # Attribute base_coord uses Python identifier base_coord
    __base_coord = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'base_coord'), 'base_coord', '__SRA_common_CTD_ANON_7_base_coord', pyxb.binding.datatypes.nonNegativeInteger)
    
    base_coord = property(__base_coord.value, __base_coord.set, None, u'\n                                                                Specify an optional starting point for tag (base offset from 1).  \n                                                            ')


    _ElementMap = {
        __BASECALL.name() : __BASECALL
    }
    _AttributeMap = {
        __default_length.name() : __default_length,
        __base_coord.name() : __base_coord
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

    
    SPOT_DECODE_METHOD = property(__SPOT_DECODE_METHOD.value, __SPOT_DECODE_METHOD.set, None, u'\n                            DEPRECATED.                                    \n                        ')


    _ElementMap = {
        __SPOT_DECODE_SPEC.name() : __SPOT_DECODE_SPEC,
        __SPOT_DECODE_METHOD.name() : __SPOT_DECODE_METHOD
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'SpotDescriptorType', SpotDescriptorType)


# Complex type CTD_ANON_8 with content type ELEMENT_ONLY
class CTD_ANON_8 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element PROBE_SET uses Python identifier PROBE_SET
    __PROBE_SET = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PROBE_SET'), 'PROBE_SET', '__SRA_common_CTD_ANON_8_PROBE_SET', False)

    
    PROBE_SET = property(__PROBE_SET.value, __PROBE_SET.set, None, u'\n                                              Reference to an archived primer or probe set.  Example:  dbProbe\n                                          ')

    
    # Attribute locus_name uses Python identifier locus_name
    __locus_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'locus_name'), 'locus_name', '__SRA_common_CTD_ANON_8_locus_name', STD_ANON_2)
    
    locus_name = property(__locus_name.value, __locus_name.set, None, None)

    
    # Attribute description uses Python identifier description
    __description = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'description'), 'description', '__SRA_common_CTD_ANON_8_description', pyxb.binding.datatypes.string)
    
    description = property(__description.value, __description.set, None, None)


    _ElementMap = {
        __PROBE_SET.name() : __PROBE_SET
    }
    _AttributeMap = {
        __locus_name.name() : __locus_name,
        __description.name() : __description
    }



# Complex type CTD_ANON_9 with content type EMPTY
class CTD_ANON_9 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType

    _ElementMap = {
        
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
    
    # Element INSTRUMENT_MODEL uses Python identifier INSTRUMENT_MODEL
    __INSTRUMENT_MODEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), 'INSTRUMENT_MODEL', '__SRA_common_CTD_ANON_10_INSTRUMENT_MODEL', False)

    
    INSTRUMENT_MODEL = property(__INSTRUMENT_MODEL.value, __INSTRUMENT_MODEL.set, None, None)

    
    # Element KEY_SEQUENCE uses Python identifier KEY_SEQUENCE
    __KEY_SEQUENCE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'KEY_SEQUENCE'), 'KEY_SEQUENCE', '__SRA_common_CTD_ANON_10_KEY_SEQUENCE', False)

    
    KEY_SEQUENCE = property(__KEY_SEQUENCE.value, __KEY_SEQUENCE.set, None, u'\n                                        The first bases that are expected to be produced by the challenge bases.  \n                                        This is optional in the schema now but will be required by business rules and future schema versions.\n                                    ')

    
    # Element FLOW_COUNT uses Python identifier FLOW_COUNT
    __FLOW_COUNT = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'FLOW_COUNT'), 'FLOW_COUNT', '__SRA_common_CTD_ANON_10_FLOW_COUNT', False)

    
    FLOW_COUNT = property(__FLOW_COUNT.value, __FLOW_COUNT.set, None, u'\n                                        The number of flows of challenge bases.  This is a constraint on maximum read length, but not equivalent.\n                                        This is optional in the schema now but will be required by business rules and future schema versions.\n                                    ')

    
    # Element FLOW_SEQUENCE uses Python identifier FLOW_SEQUENCE
    __FLOW_SEQUENCE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'FLOW_SEQUENCE'), 'FLOW_SEQUENCE', '__SRA_common_CTD_ANON_10_FLOW_SEQUENCE', False)

    
    FLOW_SEQUENCE = property(__FLOW_SEQUENCE.value, __FLOW_SEQUENCE.set, None, u'\n                                        The fixed sequence of challenge bases that flow across the picotiter plate.  \n                                        This is optional in the schema now but will be required by business rules and future schema versions.\n                                    ')


    _ElementMap = {
        __INSTRUMENT_MODEL.name() : __INSTRUMENT_MODEL,
        __KEY_SEQUENCE.name() : __KEY_SEQUENCE,
        __FLOW_COUNT.name() : __FLOW_COUNT,
        __FLOW_SEQUENCE.name() : __FLOW_SEQUENCE
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_11 with content type SIMPLE
class CTD_ANON_11 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute read_group_tag uses Python identifier read_group_tag
    __read_group_tag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'read_group_tag'), 'read_group_tag', '__SRA_common_CTD_ANON_11_read_group_tag', pyxb.binding.datatypes.string)
    
    read_group_tag = property(__read_group_tag.value, __read_group_tag.set, None, u'\n                                                                Assignment of read_group_tag to decoded read\n                                                            ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __read_group_tag.name() : __read_group_tag
    }



# Complex type ReferenceAssemblyType with content type ELEMENT_ONLY
class ReferenceAssemblyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ReferenceAssemblyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element STANDARD uses Python identifier STANDARD
    __STANDARD = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'STANDARD'), 'STANDARD', '__SRA_common_ReferenceAssemblyType_STANDARD', False)

    
    STANDARD = property(__STANDARD.value, __STANDARD.set, None, u'A standard genome assembly.\n                                                 ')

    
    # Element CUSTOM uses Python identifier CUSTOM
    __CUSTOM = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'CUSTOM'), 'CUSTOM', '__SRA_common_ReferenceAssemblyType_CUSTOM', False)

    
    CUSTOM = property(__CUSTOM.value, __CUSTOM.set, None, u'Other genome\n                                                 assembly.')


    _ElementMap = {
        __STANDARD.name() : __STANDARD,
        __CUSTOM.name() : __CUSTOM
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ReferenceAssemblyType', ReferenceAssemblyType)


# Complex type CTD_ANON_12 with content type ELEMENT_ONLY
class CTD_ANON_12 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element SPOT_LENGTH uses Python identifier SPOT_LENGTH
    __SPOT_LENGTH = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SPOT_LENGTH'), 'SPOT_LENGTH', '__SRA_common_CTD_ANON_12_SPOT_LENGTH', False)

    
    SPOT_LENGTH = property(__SPOT_LENGTH.value, __SPOT_LENGTH.set, None, u'\n                                        Expected number of base calls or cycles per spot (raw sequence length including all application and technical tags and mate pairs)\n                                    ')

    
    # Element READ_SPEC uses Python identifier READ_SPEC
    __READ_SPEC = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'READ_SPEC'), 'READ_SPEC', '__SRA_common_CTD_ANON_12_READ_SPEC', True)

    
    READ_SPEC = property(__READ_SPEC.value, __READ_SPEC.set, None, None)

    
    # Element ADAPTER_SPEC uses Python identifier ADAPTER_SPEC
    __ADAPTER_SPEC = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ADAPTER_SPEC'), 'ADAPTER_SPEC', '__SRA_common_CTD_ANON_12_ADAPTER_SPEC', False)

    
    ADAPTER_SPEC = property(__ADAPTER_SPEC.value, __ADAPTER_SPEC.set, None, u'\n                                        Some technologies will require knowledge of the sequencing adapter or the last base of the adapter in order to decode the spot.\n                                    ')

    
    # Element NUMBER_OF_READS_PER_SPOT uses Python identifier NUMBER_OF_READS_PER_SPOT
    __NUMBER_OF_READS_PER_SPOT = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'NUMBER_OF_READS_PER_SPOT'), 'NUMBER_OF_READS_PER_SPOT', '__SRA_common_CTD_ANON_12_NUMBER_OF_READS_PER_SPOT', False)

    
    NUMBER_OF_READS_PER_SPOT = property(__NUMBER_OF_READS_PER_SPOT.value, __NUMBER_OF_READS_PER_SPOT.set, None, u'\n                                        DEPRECATED.  Number of tags (reads) per spot.\n                                    ')


    _ElementMap = {
        __SPOT_LENGTH.name() : __SPOT_LENGTH,
        __READ_SPEC.name() : __READ_SPEC,
        __ADAPTER_SPEC.name() : __ADAPTER_SPEC,
        __NUMBER_OF_READS_PER_SPOT.name() : __NUMBER_OF_READS_PER_SPOT
    }
    _AttributeMap = {
        
    }



# Complex type LibraryDescriptorType with content type ELEMENT_ONLY
class LibraryDescriptorType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'LibraryDescriptorType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element LIBRARY_NAME uses Python identifier LIBRARY_NAME
    __LIBRARY_NAME = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LIBRARY_NAME'), 'LIBRARY_NAME', '__SRA_common_LibraryDescriptorType_LIBRARY_NAME', False)

    
    LIBRARY_NAME = property(__LIBRARY_NAME.value, __LIBRARY_NAME.set, None, u"\n                      The submitter's name for this library.\n                  ")

    
    # Element TARGETED_LOCI uses Python identifier TARGETED_LOCI
    __TARGETED_LOCI = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TARGETED_LOCI'), 'TARGETED_LOCI', '__SRA_common_LibraryDescriptorType_TARGETED_LOCI', False)

    
    TARGETED_LOCI = property(__TARGETED_LOCI.value, __TARGETED_LOCI.set, None, None)

    
    # Element LIBRARY_SELECTION uses Python identifier LIBRARY_SELECTION
    __LIBRARY_SELECTION = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LIBRARY_SELECTION'), 'LIBRARY_SELECTION', '__SRA_common_LibraryDescriptorType_LIBRARY_SELECTION', False)

    
    LIBRARY_SELECTION = property(__LIBRARY_SELECTION.value, __LIBRARY_SELECTION.set, None, u'\n                      Whether any method was used to select for or against, enrich, or screen \n                      the material being sequenced.     \n                  ')

    
    # Element LIBRARY_CONSTRUCTION_PROTOCOL uses Python identifier LIBRARY_CONSTRUCTION_PROTOCOL
    __LIBRARY_CONSTRUCTION_PROTOCOL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LIBRARY_CONSTRUCTION_PROTOCOL'), 'LIBRARY_CONSTRUCTION_PROTOCOL', '__SRA_common_LibraryDescriptorType_LIBRARY_CONSTRUCTION_PROTOCOL', False)

    
    LIBRARY_CONSTRUCTION_PROTOCOL = property(__LIBRARY_CONSTRUCTION_PROTOCOL.value, __LIBRARY_CONSTRUCTION_PROTOCOL.set, None, u'\n                      Free form text describing the protocol by which the sequencing library was constructed.                             \n                  ')

    
    # Element LIBRARY_STRATEGY uses Python identifier LIBRARY_STRATEGY
    __LIBRARY_STRATEGY = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LIBRARY_STRATEGY'), 'LIBRARY_STRATEGY', '__SRA_common_LibraryDescriptorType_LIBRARY_STRATEGY', False)

    
    LIBRARY_STRATEGY = property(__LIBRARY_STRATEGY.value, __LIBRARY_STRATEGY.set, None, u'\n                      Sequencing technique intended for this library.\n                  ')

    
    # Element LIBRARY_LAYOUT uses Python identifier LIBRARY_LAYOUT
    __LIBRARY_LAYOUT = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LIBRARY_LAYOUT'), 'LIBRARY_LAYOUT', '__SRA_common_LibraryDescriptorType_LIBRARY_LAYOUT', False)

    
    LIBRARY_LAYOUT = property(__LIBRARY_LAYOUT.value, __LIBRARY_LAYOUT.set, None, u'\n                      LIBRARY_LAYOUT specifies whether to expect single, paired, or other configuration of reads.  \n                      In the case of paired reads, information about the relative distance and orientation is specified.\n                  ')

    
    # Element LIBRARY_SOURCE uses Python identifier LIBRARY_SOURCE
    __LIBRARY_SOURCE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LIBRARY_SOURCE'), 'LIBRARY_SOURCE', '__SRA_common_LibraryDescriptorType_LIBRARY_SOURCE', False)

    
    LIBRARY_SOURCE = property(__LIBRARY_SOURCE.value, __LIBRARY_SOURCE.set, None, u'\n                      The LIBRARY_SOURCE specifies the type of source material that is being sequenced.\n                  ')

    
    # Element POOLING_STRATEGY uses Python identifier POOLING_STRATEGY
    __POOLING_STRATEGY = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'POOLING_STRATEGY'), 'POOLING_STRATEGY', '__SRA_common_LibraryDescriptorType_POOLING_STRATEGY', False)

    
    POOLING_STRATEGY = property(__POOLING_STRATEGY.value, __POOLING_STRATEGY.set, None, u'\n                      The optional pooling strategy indicates how the library or libraries are organized if multiple samples are involved.\n                  ')


    _ElementMap = {
        __LIBRARY_NAME.name() : __LIBRARY_NAME,
        __TARGETED_LOCI.name() : __TARGETED_LOCI,
        __LIBRARY_SELECTION.name() : __LIBRARY_SELECTION,
        __LIBRARY_CONSTRUCTION_PROTOCOL.name() : __LIBRARY_CONSTRUCTION_PROTOCOL,
        __LIBRARY_STRATEGY.name() : __LIBRARY_STRATEGY,
        __LIBRARY_LAYOUT.name() : __LIBRARY_LAYOUT,
        __LIBRARY_SOURCE.name() : __LIBRARY_SOURCE,
        __POOLING_STRATEGY.name() : __POOLING_STRATEGY
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'LibraryDescriptorType', LibraryDescriptorType)


# Complex type CTD_ANON_13 with content type SIMPLE
class CTD_ANON_13 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute max_mismatch uses Python identifier max_mismatch
    __max_mismatch = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'max_mismatch'), 'max_mismatch', '__SRA_common_CTD_ANON_13_max_mismatch', pyxb.binding.datatypes.nonNegativeInteger)
    
    max_mismatch = property(__max_mismatch.value, __max_mismatch.set, None, u'\n                                                                                    Maximum number of mismatches \n                                                                                ')

    
    # Attribute read_group_tag uses Python identifier read_group_tag
    __read_group_tag = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'read_group_tag'), 'read_group_tag', '__SRA_common_CTD_ANON_13_read_group_tag', pyxb.binding.datatypes.string)
    
    read_group_tag = property(__read_group_tag.value, __read_group_tag.set, None, u'\n                                                                                    When match occurs, the read will be tagged with this group membership\n                                                                                ')

    
    # Attribute match_edge uses Python identifier match_edge
    __match_edge = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'match_edge'), 'match_edge', '__SRA_common_CTD_ANON_13_match_edge', STD_ANON_4)
    
    match_edge = property(__match_edge.value, __match_edge.set, None, u'\n                                                                                    Where the match should occur. Changes the rules on how min_match and max_mismatch are counted.                                                                                                          \n                                                                                ')

    
    # Attribute min_match uses Python identifier min_match
    __min_match = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'min_match'), 'min_match', '__SRA_common_CTD_ANON_13_min_match', pyxb.binding.datatypes.nonNegativeInteger)
    
    min_match = property(__min_match.value, __min_match.set, None, u'\n                                                                                    Minimum number of matches to trigger identification.\n                                                                                ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __max_mismatch.name() : __max_mismatch,
        __read_group_tag.name() : __read_group_tag,
        __match_edge.name() : __match_edge,
        __min_match.name() : __min_match
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

    
    UNITS = property(__UNITS.value, __UNITS.set, None, u'\n                        Optional scientific units.\n                    ')

    
    # Element TAG uses Python identifier TAG
    __TAG = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TAG'), 'TAG', '__SRA_common_AttributeType_TAG', False)

    
    TAG = property(__TAG.value, __TAG.set, None, u'\n                        Name of the attribute.\n                    ')

    
    # Element VALUE uses Python identifier VALUE
    __VALUE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'VALUE'), 'VALUE', '__SRA_common_AttributeType_VALUE', False)

    
    VALUE = property(__VALUE.value, __VALUE.set, None, u'\n                        Value of the attribute.\n                    ')


    _ElementMap = {
        __UNITS.name() : __UNITS,
        __TAG.name() : __TAG,
        __VALUE.name() : __VALUE
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'AttributeType', AttributeType)


# Complex type CTD_ANON_14 with content type ELEMENT_ONLY
class CTD_ANON_14 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element CYCLE_COORD uses Python identifier CYCLE_COORD
    __CYCLE_COORD = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'CYCLE_COORD'), 'CYCLE_COORD', '__SRA_common_CTD_ANON_14_CYCLE_COORD', False)

    
    CYCLE_COORD = property(__CYCLE_COORD.value, __CYCLE_COORD.set, None, u'\n                                                        The location of the read start in terms of cycle count (1 is beginning of spot).\n                                                    ')

    
    # Element READ_TYPE uses Python identifier READ_TYPE
    __READ_TYPE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'READ_TYPE'), 'READ_TYPE', '__SRA_common_CTD_ANON_14_READ_TYPE', False)

    
    READ_TYPE = property(__READ_TYPE.value, __READ_TYPE.set, None, None)

    
    # Element READ_CLASS uses Python identifier READ_CLASS
    __READ_CLASS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'READ_CLASS'), 'READ_CLASS', '__SRA_common_CTD_ANON_14_READ_CLASS', False)

    
    READ_CLASS = property(__READ_CLASS.value, __READ_CLASS.set, None, None)

    
    # Element EXPECTED_BASECALL uses Python identifier EXPECTED_BASECALL
    __EXPECTED_BASECALL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'EXPECTED_BASECALL'), 'EXPECTED_BASECALL', '__SRA_common_CTD_ANON_14_EXPECTED_BASECALL', False)

    
    EXPECTED_BASECALL = property(__EXPECTED_BASECALL.value, __EXPECTED_BASECALL.set, None, u'\n                                                        An expected basecall for a current read. Read will be zero-length if basecall is not present.\n                                                        Users of this facility should start migrating to EXPECTED_BASECALL_TABLE, as this field\n                                                        will be phased out.\n                                                    ')

    
    # Element EXPECTED_BASECALL_TABLE uses Python identifier EXPECTED_BASECALL_TABLE
    __EXPECTED_BASECALL_TABLE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'EXPECTED_BASECALL_TABLE'), 'EXPECTED_BASECALL_TABLE', '__SRA_common_CTD_ANON_14_EXPECTED_BASECALL_TABLE', False)

    
    EXPECTED_BASECALL_TABLE = property(__EXPECTED_BASECALL_TABLE.value, __EXPECTED_BASECALL_TABLE.set, None, u'\n                                                        A set of choices of expected basecalls for a current read. Read will be zero-length if none is found.\n                                                    ')

    
    # Element READ_LABEL uses Python identifier READ_LABEL
    __READ_LABEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'READ_LABEL'), 'READ_LABEL', '__SRA_common_CTD_ANON_14_READ_LABEL', False)

    
    READ_LABEL = property(__READ_LABEL.value, __READ_LABEL.set, None, u'READ_LABEL is a name for this tag, and can be used to on output to determine read name, for example F or R.')

    
    # Element RELATIVE_ORDER uses Python identifier RELATIVE_ORDER
    __RELATIVE_ORDER = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'RELATIVE_ORDER'), 'RELATIVE_ORDER', '__SRA_common_CTD_ANON_14_RELATIVE_ORDER', False)

    
    RELATIVE_ORDER = property(__RELATIVE_ORDER.value, __RELATIVE_ORDER.set, None, u'\n                                                        The read is located beginning at the offset or cycle relative to another read.  \n                                                        This choice is appropriate for example when specifying a read\n                                                        that follows a variable length expected sequence(s).\n                                                    ')

    
    # Element BASE_COORD uses Python identifier BASE_COORD
    __BASE_COORD = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'BASE_COORD'), 'BASE_COORD', '__SRA_common_CTD_ANON_14_BASE_COORD', False)

    
    BASE_COORD = property(__BASE_COORD.value, __BASE_COORD.set, None, u'\n                                                        The location of the read start in terms of base count (1 is beginning of spot).\n                                                    ')

    
    # Element READ_INDEX uses Python identifier READ_INDEX
    __READ_INDEX = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'READ_INDEX'), 'READ_INDEX', '__SRA_common_CTD_ANON_14_READ_INDEX', False)

    
    READ_INDEX = property(__READ_INDEX.value, __READ_INDEX.set, None, u'READ_INDEX starts at 0 and is incrementally increased for each sequential READ_SPEC within a SPOT_DECODE_SPEC')


    _ElementMap = {
        __CYCLE_COORD.name() : __CYCLE_COORD,
        __READ_TYPE.name() : __READ_TYPE,
        __READ_CLASS.name() : __READ_CLASS,
        __EXPECTED_BASECALL.name() : __EXPECTED_BASECALL,
        __EXPECTED_BASECALL_TABLE.name() : __EXPECTED_BASECALL_TABLE,
        __READ_LABEL.name() : __READ_LABEL,
        __RELATIVE_ORDER.name() : __RELATIVE_ORDER,
        __BASE_COORD.name() : __BASE_COORD,
        __READ_INDEX.name() : __READ_INDEX
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_15 with content type ELEMENT_ONLY
class CTD_ANON_15 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element PAIRED uses Python identifier PAIRED
    __PAIRED = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PAIRED'), 'PAIRED', '__SRA_common_CTD_ANON_15_PAIRED', False)

    
    PAIRED = property(__PAIRED.value, __PAIRED.set, None, None)

    
    # Element SINGLE uses Python identifier SINGLE
    __SINGLE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SINGLE'), 'SINGLE', '__SRA_common_CTD_ANON_15_SINGLE', False)

    
    SINGLE = property(__SINGLE.value, __SINGLE.set, None, None)


    _ElementMap = {
        __PAIRED.name() : __PAIRED,
        __SINGLE.name() : __SINGLE
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
    
    # Element COLOR uses Python identifier COLOR
    __COLOR = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'COLOR'), 'COLOR', '__SRA_common_CTD_ANON_16_COLOR', True)

    
    COLOR = property(__COLOR.value, __COLOR.set, None, None)


    _ElementMap = {
        __COLOR.name() : __COLOR
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_17 with content type ELEMENT_ONLY
class CTD_ANON_17 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element GAP_SPEC uses Python identifier GAP_SPEC
    __GAP_SPEC = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'GAP_SPEC'), 'GAP_SPEC', '__SRA_common_CTD_ANON_17_GAP_SPEC', False)

    
    GAP_SPEC = property(__GAP_SPEC.value, __GAP_SPEC.set, None, None)

    
    # Element GAP_TYPE uses Python identifier GAP_TYPE
    __GAP_TYPE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'GAP_TYPE'), 'GAP_TYPE', '__SRA_common_CTD_ANON_17_GAP_TYPE', False)

    
    GAP_TYPE = property(__GAP_TYPE.value, __GAP_TYPE.set, None, u' Specifies the gap type and parameters. ')


    _ElementMap = {
        __GAP_SPEC.name() : __GAP_SPEC,
        __GAP_TYPE.name() : __GAP_TYPE
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_18 with content type EMPTY
class CTD_ANON_18 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType

    _ElementMap = {
        
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_19 with content type SIMPLE
class CTD_ANON_19 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute dibase uses Python identifier dibase
    __dibase = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'dibase'), 'dibase', '__SRA_common_CTD_ANON_19_dibase', pyxb.binding.datatypes.string)
    
    dibase = property(__dibase.value, __dibase.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __dibase.name() : __dibase
    }



# Complex type CTD_ANON_20 with content type ELEMENT_ONLY
class CTD_ANON_20 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element PairedEnd uses Python identifier PairedEnd
    __PairedEnd = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PairedEnd'), 'PairedEnd', '__SRA_common_CTD_ANON_20_PairedEnd', False)

    
    PairedEnd = property(__PairedEnd.value, __PairedEnd.set, None, u' Mated tags sequenced from two ends\n                                                of a physical extent of genomic material. \n                                            ')

    
    # Element Tandem uses Python identifier Tandem
    __Tandem = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Tandem'), 'Tandem', '__SRA_common_CTD_ANON_20_Tandem', False)

    
    Tandem = property(__Tandem.value, __Tandem.set, None, u' Tandem gaps between ligands. ')

    
    # Element MatePair uses Python identifier MatePair
    __MatePair = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'MatePair'), 'MatePair', '__SRA_common_CTD_ANON_20_MatePair', False)

    
    MatePair = property(__MatePair.value, __MatePair.set, None, u' Mated tags with predicted separation and orientation. ')


    _ElementMap = {
        __PairedEnd.name() : __PairedEnd,
        __Tandem.name() : __Tandem,
        __MatePair.name() : __MatePair
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_21 with content type EMPTY
class CTD_ANON_21 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute label uses Python identifier label
    __label = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'label'), 'label', '__SRA_common_CTD_ANON_21_label', pyxb.binding.datatypes.string)
    
    label = property(__label.value, __label.set, None, u' This is how Reference Sequence is labeled in submission file(s). \n                                  It is equivalent to  SQ label in BAM. \n                                  Optional when submitted file uses INSDC accession.version')

    
    # Attribute refname uses Python identifier refname
    __refname = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refname'), 'refname', '__SRA_common_CTD_ANON_21_refname', pyxb.binding.datatypes.string)
    
    refname = property(__refname.value, __refname.set, None, u'A recognized name for the\n                                                 reference sequence.')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'accession'), 'accession', '__SRA_common_CTD_ANON_21_accession', pyxb.binding.datatypes.token)
    
    accession = property(__accession.value, __accession.set, None, u'  Accession.version with version being mandatory\n                                  ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __label.name() : __label,
        __refname.name() : __refname,
        __accession.name() : __accession
    }



# Complex type CTD_ANON_22 with content type EMPTY
class CTD_ANON_22 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute NOMINAL_LENGTH uses Python identifier NOMINAL_LENGTH
    __NOMINAL_LENGTH = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'NOMINAL_LENGTH'), 'NOMINAL_LENGTH', '__SRA_common_CTD_ANON_22_NOMINAL_LENGTH', pyxb.binding.datatypes.nonNegativeInteger)
    
    NOMINAL_LENGTH = property(__NOMINAL_LENGTH.value, __NOMINAL_LENGTH.set, None, u'\n                                ')

    
    # Attribute NOMINAL_SDEV uses Python identifier NOMINAL_SDEV
    __NOMINAL_SDEV = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'NOMINAL_SDEV'), 'NOMINAL_SDEV', '__SRA_common_CTD_ANON_22_NOMINAL_SDEV', pyxb.binding.datatypes.double)
    
    NOMINAL_SDEV = property(__NOMINAL_SDEV.value, __NOMINAL_SDEV.set, None, u'\n                                ')

    
    # Attribute ORIENTATION uses Python identifier ORIENTATION
    __ORIENTATION = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ORIENTATION'), 'ORIENTATION', '__SRA_common_CTD_ANON_22_ORIENTATION', pyxb.binding.datatypes.string)
    
    ORIENTATION = property(__ORIENTATION.value, __ORIENTATION.set, None, u'\n                                ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __NOMINAL_LENGTH.name() : __NOMINAL_LENGTH,
        __NOMINAL_SDEV.name() : __NOMINAL_SDEV,
        __ORIENTATION.name() : __ORIENTATION
    }



# Complex type LinkType with content type ELEMENT_ONLY
class LinkType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'LinkType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element SRA_LINK uses Python identifier SRA_LINK
    __SRA_LINK = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SRA_LINK'), 'SRA_LINK', '__SRA_common_LinkType_SRA_LINK', False)

    
    SRA_LINK = property(__SRA_LINK.value, __SRA_LINK.set, None, None)

    
    # Element XREF_LINK uses Python identifier XREF_LINK
    __XREF_LINK = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'XREF_LINK'), 'XREF_LINK', '__SRA_common_LinkType_XREF_LINK', False)

    
    XREF_LINK = property(__XREF_LINK.value, __XREF_LINK.set, None, None)

    
    # Element ENTREZ_LINK uses Python identifier ENTREZ_LINK
    __ENTREZ_LINK = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ENTREZ_LINK'), 'ENTREZ_LINK', '__SRA_common_LinkType_ENTREZ_LINK', False)

    
    ENTREZ_LINK = property(__ENTREZ_LINK.value, __ENTREZ_LINK.set, None, None)

    
    # Element URL_LINK uses Python identifier URL_LINK
    __URL_LINK = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'URL_LINK'), 'URL_LINK', '__SRA_common_LinkType_URL_LINK', False)

    
    URL_LINK = property(__URL_LINK.value, __URL_LINK.set, None, None)

    
    # Element ENA_LINK uses Python identifier ENA_LINK
    __ENA_LINK = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ENA_LINK'), 'ENA_LINK', '__SRA_common_LinkType_ENA_LINK', False)

    
    ENA_LINK = property(__ENA_LINK.value, __ENA_LINK.set, None, None)

    
    # Element DDBJ_LINK uses Python identifier DDBJ_LINK
    __DDBJ_LINK = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DDBJ_LINK'), 'DDBJ_LINK', '__SRA_common_LinkType_DDBJ_LINK', False)

    
    DDBJ_LINK = property(__DDBJ_LINK.value, __DDBJ_LINK.set, None, None)


    _ElementMap = {
        __SRA_LINK.name() : __SRA_LINK,
        __XREF_LINK.name() : __XREF_LINK,
        __ENTREZ_LINK.name() : __ENTREZ_LINK,
        __URL_LINK.name() : __URL_LINK,
        __ENA_LINK.name() : __ENA_LINK,
        __DDBJ_LINK.name() : __DDBJ_LINK
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'LinkType', LinkType)


# Complex type CTD_ANON_23 with content type ELEMENT_ONLY
class CTD_ANON_23 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element INSTRUMENT_MODEL uses Python identifier INSTRUMENT_MODEL
    __INSTRUMENT_MODEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), 'INSTRUMENT_MODEL', '__SRA_common_CTD_ANON_23_INSTRUMENT_MODEL', False)

    
    INSTRUMENT_MODEL = property(__INSTRUMENT_MODEL.value, __INSTRUMENT_MODEL.set, None, None)


    _ElementMap = {
        __INSTRUMENT_MODEL.name() : __INSTRUMENT_MODEL
    }
    _AttributeMap = {
        
    }



# Complex type SraLinkType with content type EMPTY
class SraLinkType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SraLinkType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute refname uses Python identifier refname
    __refname = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refname'), 'refname', '__SRA_common_SraLinkType_refname', pyxb.binding.datatypes.string)
    
    refname = property(__refname.value, __refname.set, None, u'\n                    Identifies a record by name that is known within the namespace defined by attribute "refcenter"\n                    Use this field when referencing an object for which an accession has not yet been issued.\n                ')

    
    # Attribute sra_object_type uses Python identifier sra_object_type
    __sra_object_type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'sra_object_type'), 'sra_object_type', '__SRA_common_SraLinkType_sra_object_type', STD_ANON_10)
    
    sra_object_type = property(__sra_object_type.value, __sra_object_type.set, None, u'\n                    SRA link type.\n                ')

    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'accession'), 'accession', '__SRA_common_SraLinkType_accession', pyxb.binding.datatypes.string)
    
    accession = property(__accession.value, __accession.set, None, u'\n                    Identifies a record by its accession.  The scope of resolution is the entire Archive.\n                ')

    
    # Attribute refcenter uses Python identifier refcenter
    __refcenter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refcenter'), 'refcenter', '__SRA_common_SraLinkType_refcenter', pyxb.binding.datatypes.string)
    
    refcenter = property(__refcenter.value, __refcenter.set, None, u'\n                    The center namespace of the attribute "refname". When absent, the namespace is assumed to be the current submission.\n                ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __refname.name() : __refname,
        __sra_object_type.name() : __sra_object_type,
        __accession.name() : __accession,
        __refcenter.name() : __refcenter
    }
Namespace.addCategoryObject('typeBinding', u'SraLinkType', SraLinkType)


# Complex type CTD_ANON_24 with content type ELEMENT_ONLY
class CTD_ANON_24 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element URL uses Python identifier URL
    __URL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'URL'), 'URL', '__SRA_common_CTD_ANON_24_URL', False)

    
    URL = property(__URL.value, __URL.set, None, u'\n                                    The internet service link (file:, http:, ftp:, etc).\n                                ')

    
    # Element LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LABEL'), 'LABEL', '__SRA_common_CTD_ANON_24_LABEL', False)

    
    LABEL = property(__LABEL.value, __LABEL.set, None, u'\n                                    Text label to display for the link.\n                                ')


    _ElementMap = {
        __URL.name() : __URL,
        __LABEL.name() : __LABEL
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_25 with content type EMPTY
class CTD_ANON_25 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute follows_read_index uses Python identifier follows_read_index
    __follows_read_index = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'follows_read_index'), 'follows_read_index', '__SRA_common_CTD_ANON_25_follows_read_index', pyxb.binding.datatypes.nonNegativeInteger)
    
    follows_read_index = property(__follows_read_index.value, __follows_read_index.set, None, u'\n                                                                Specify the read index that precedes this read.\n                                                            ')

    
    # Attribute precedes_read_index uses Python identifier precedes_read_index
    __precedes_read_index = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'precedes_read_index'), 'precedes_read_index', '__SRA_common_CTD_ANON_25_precedes_read_index', pyxb.binding.datatypes.nonNegativeInteger)
    
    precedes_read_index = property(__precedes_read_index.value, __precedes_read_index.set, None, u'\n                                                                Specify the read index that follows this read.\n                                                            ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __follows_read_index.name() : __follows_read_index,
        __precedes_read_index.name() : __precedes_read_index
    }



# Complex type CTD_ANON_26 with content type EMPTY
class CTD_ANON_26 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute orientation uses Python identifier orientation
    __orientation = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'orientation'), 'orientation', '__SRA_common_CTD_ANON_26_orientation', STD_ANON_12)
    
    orientation = property(__orientation.value, __orientation.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __orientation.name() : __orientation
    }



# Complex type CTD_ANON_27 with content type ELEMENT_ONLY
class CTD_ANON_27 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element INSTRUMENT_MODEL uses Python identifier INSTRUMENT_MODEL
    __INSTRUMENT_MODEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), 'INSTRUMENT_MODEL', '__SRA_common_CTD_ANON_27_INSTRUMENT_MODEL', False)

    
    INSTRUMENT_MODEL = property(__INSTRUMENT_MODEL.value, __INSTRUMENT_MODEL.set, None, None)


    _ElementMap = {
        __INSTRUMENT_MODEL.name() : __INSTRUMENT_MODEL
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

    _ElementMap = {
        
    }
    _AttributeMap = {
        
    }



# Complex type XRefType with content type ELEMENT_ONLY
class XRefType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'XRefType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LABEL'), 'LABEL', '__SRA_common_XRefType_LABEL', False)

    
    LABEL = property(__LABEL.value, __LABEL.set, None, u'\n                            Text label to display for the link.\n                        ')

    
    # Element ID uses Python identifier ID
    __ID = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__SRA_common_XRefType_ID', False)

    
    ID = property(__ID.value, __ID.set, None, u'\n                            Accession in the referenced database.    For example,  FBtr0080008 (in FLYBASE).\n                        ')

    
    # Element DB uses Python identifier DB
    __DB = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DB'), 'DB', '__SRA_common_XRefType_DB', False)

    
    DB = property(__DB.value, __DB.set, None, u'\n                            INSDC controlled vocabulary of permitted cross references.  Please see http://www.insdc.org/page.php?page=db_xref .\n                            For example, FLYBASE.\n                        ')


    _ElementMap = {
        __LABEL.name() : __LABEL,
        __ID.name() : __ID,
        __DB.name() : __DB
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'XRefType', XRefType)


# Complex type CTD_ANON_29 with content type ELEMENT_ONLY
class CTD_ANON_29 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element interval uses Python identifier interval
    __interval = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'interval'), 'interval', '__SRA_common_CTD_ANON_29_interval', False)

    
    interval = property(__interval.value, __interval.set, None, None)

    
    # Element statistic uses Python identifier statistic
    __statistic = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'statistic'), 'statistic', '__SRA_common_CTD_ANON_29_statistic', False)

    
    statistic = property(__statistic.value, __statistic.set, None, None)

    
    # Element histogram uses Python identifier histogram
    __histogram = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'histogram'), 'histogram', '__SRA_common_CTD_ANON_29_histogram', False)

    
    histogram = property(__histogram.value, __histogram.set, None, None)

    
    # Attribute link3 uses Python identifier link3
    __link3 = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'link3'), 'link3', '__SRA_common_CTD_ANON_29_link3', pyxb.binding.datatypes.anySimpleType, unicode_default=u'NULL')
    
    link3 = property(__link3.value, __link3.set, None, u" Specify the read label at the 3' end of\n                                            the gap, or NULL if it's the last tag. ")

    
    # Attribute link5 uses Python identifier link5
    __link5 = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'link5'), 'link5', '__SRA_common_CTD_ANON_29_link5', pyxb.binding.datatypes.anySimpleType, unicode_default=u'NULL')
    
    link5 = property(__link5.value, __link5.set, None, u" Specify the read label at the 5' end of\n                                            the gap, or NULL if it's the first tag. ")


    _ElementMap = {
        __interval.name() : __interval,
        __statistic.name() : __statistic,
        __histogram.name() : __histogram
    }
    _AttributeMap = {
        __link3.name() : __link3,
        __link5.name() : __link5
    }



# Complex type CTD_ANON_30 with content type ELEMENT_ONLY
class CTD_ANON_30 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element QUERY uses Python identifier QUERY
    __QUERY = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'QUERY'), 'QUERY', '__SRA_common_CTD_ANON_30_QUERY', False)

    
    QUERY = property(__QUERY.value, __QUERY.set, None, u'\n                                        Accession string meaningful to the NCBI Entrez system.\n                                    ')

    
    # Element LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LABEL'), 'LABEL', '__SRA_common_CTD_ANON_30_LABEL', False)

    
    LABEL = property(__LABEL.value, __LABEL.set, None, u'\n                                    How to label the link.\n                                ')

    
    # Element ID uses Python identifier ID
    __ID = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__SRA_common_CTD_ANON_30_ID', False)

    
    ID = property(__ID.value, __ID.set, None, u'\n                                        Numeric record id meaningful to the NCBI Entrez system.\n                                    ')

    
    # Element DB uses Python identifier DB
    __DB = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DB'), 'DB', '__SRA_common_CTD_ANON_30_DB', False)

    
    DB = property(__DB.value, __DB.set, None, u'\n                                    NCBI controlled vocabulary of permitted cross references.  Please see http://www.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi? .\n                                ')


    _ElementMap = {
        __QUERY.name() : __QUERY,
        __LABEL.name() : __LABEL,
        __ID.name() : __ID,
        __DB.name() : __DB
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_31 with content type EMPTY
class CTD_ANON_31 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute min_length uses Python identifier min_length
    __min_length = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'min_length'), 'min_length', '__SRA_common_CTD_ANON_31_min_length', pyxb.binding.datatypes.integer, required=True)
    
    min_length = property(__min_length.value, __min_length.set, None, u' Minimum length in base pairs\n                                                  of the interval.')

    
    # Attribute max_length uses Python identifier max_length
    __max_length = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'max_length'), 'max_length', '__SRA_common_CTD_ANON_31_max_length', pyxb.binding.datatypes.integer, required=True)
    
    max_length = property(__max_length.value, __max_length.set, None, u' Minimum length in base pairs\n                                                  of the interval.')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __min_length.name() : __min_length,
        __max_length.name() : __max_length
    }



# Complex type CTD_ANON_32 with content type ELEMENT_ONLY
class CTD_ANON_32 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element INSTRUMENT_MODEL uses Python identifier INSTRUMENT_MODEL
    __INSTRUMENT_MODEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), 'INSTRUMENT_MODEL', '__SRA_common_CTD_ANON_32_INSTRUMENT_MODEL', False)

    
    INSTRUMENT_MODEL = property(__INSTRUMENT_MODEL.value, __INSTRUMENT_MODEL.set, None, None)


    _ElementMap = {
        __INSTRUMENT_MODEL.name() : __INSTRUMENT_MODEL
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_33 with content type ELEMENT_ONLY
class CTD_ANON_33 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element CYCLE_COUNT uses Python identifier CYCLE_COUNT
    __CYCLE_COUNT = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'CYCLE_COUNT'), 'CYCLE_COUNT', '__SRA_common_CTD_ANON_33_CYCLE_COUNT', False)

    
    CYCLE_COUNT = property(__CYCLE_COUNT.value, __CYCLE_COUNT.set, None, u'\n                                        DEPRECATED.  Use SEQUENCE_LENGTH instead.\n                                    ')

    
    # Element INSTRUMENT_MODEL uses Python identifier INSTRUMENT_MODEL
    __INSTRUMENT_MODEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), 'INSTRUMENT_MODEL', '__SRA_common_CTD_ANON_33_INSTRUMENT_MODEL', False)

    
    INSTRUMENT_MODEL = property(__INSTRUMENT_MODEL.value, __INSTRUMENT_MODEL.set, None, None)

    
    # Element COLOR_MATRIX uses Python identifier COLOR_MATRIX
    __COLOR_MATRIX = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'COLOR_MATRIX'), 'COLOR_MATRIX', '__SRA_common_CTD_ANON_33_COLOR_MATRIX', False)

    
    COLOR_MATRIX = property(__COLOR_MATRIX.value, __COLOR_MATRIX.set, None, u' DEPRECATED. ')

    
    # Element COLOR_MATRIX_CODE uses Python identifier COLOR_MATRIX_CODE
    __COLOR_MATRIX_CODE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'COLOR_MATRIX_CODE'), 'COLOR_MATRIX_CODE', '__SRA_common_CTD_ANON_33_COLOR_MATRIX_CODE', False)

    
    COLOR_MATRIX_CODE = property(__COLOR_MATRIX_CODE.value, __COLOR_MATRIX_CODE.set, None, u' DEPRECATED. ')

    
    # Element SEQUENCE_LENGTH uses Python identifier SEQUENCE_LENGTH
    __SEQUENCE_LENGTH = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SEQUENCE_LENGTH'), 'SEQUENCE_LENGTH', '__SRA_common_CTD_ANON_33_SEQUENCE_LENGTH', False)

    
    SEQUENCE_LENGTH = property(__SEQUENCE_LENGTH.value, __SEQUENCE_LENGTH.set, None, u'\n                                        The fixed number of bases expected in each raw sequence, including both mate pairs and any technical reads.\n                                        This is optional in the schema now but will be required by business rules and future schema versions.\n                                    ')


    _ElementMap = {
        __CYCLE_COUNT.name() : __CYCLE_COUNT,
        __INSTRUMENT_MODEL.name() : __INSTRUMENT_MODEL,
        __COLOR_MATRIX.name() : __COLOR_MATRIX,
        __COLOR_MATRIX_CODE.name() : __COLOR_MATRIX_CODE,
        __SEQUENCE_LENGTH.name() : __SEQUENCE_LENGTH
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_34 with content type EMPTY
class CTD_ANON_34 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute stdev uses Python identifier stdev
    __stdev = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'stdev'), 'stdev', '__SRA_common_CTD_ANON_34_stdev', pyxb.binding.datatypes.float, required=True)
    
    stdev = property(__stdev.value, __stdev.set, None, u' Standard deviation of length\n                                                  in base pairs of the interval.')

    
    # Attribute mean uses Python identifier mean
    __mean = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'mean'), 'mean', '__SRA_common_CTD_ANON_34_mean', pyxb.binding.datatypes.float, required=True)
    
    mean = property(__mean.value, __mean.set, None, u' Mean length in base pairs of\n                                                  the interval.')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __stdev.name() : __stdev,
        __mean.name() : __mean
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

    
    SAMPLE_DEMUX_DIRECTIVE = property(__SAMPLE_DEMUX_DIRECTIVE.value, __SAMPLE_DEMUX_DIRECTIVE.set, None, u'\n                        Tells the Archive who will execute the sample demultiplexing operation..\n                    ')


    _ElementMap = {
        __SAMPLE_DEMUX_DIRECTIVE.name() : __SAMPLE_DEMUX_DIRECTIVE
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'SequencingDirectivesType', SequencingDirectivesType)


# Complex type CTD_ANON_35 with content type ELEMENT_ONLY
class CTD_ANON_35 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element bin uses Python identifier bin
    __bin = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'bin'), 'bin', '__SRA_common_CTD_ANON_35_bin', True)

    
    bin = property(__bin.value, __bin.set, None, None)


    _ElementMap = {
        __bin.name() : __bin
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


# Complex type CTD_ANON_36 with content type ELEMENT_ONLY
class CTD_ANON_36 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element URL uses Python identifier URL
    __URL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'URL'), 'URL', '__SRA_common_CTD_ANON_36_URL', False)

    
    URL = property(__URL.value, __URL.set, None, u'An URL to the cross-references accession.\n                            ')

    
    # Element LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LABEL'), 'LABEL', '__SRA_common_CTD_ANON_36_LABEL', False)

    
    LABEL = property(__LABEL.value, __LABEL.set, None, u'A textual description of the cross-reference.\n                            ')

    
    # Element DB uses Python identifier DB
    __DB = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DB'), 'DB', '__SRA_common_CTD_ANON_36_DB', False)

    
    DB = property(__DB.value, __DB.set, None, u'DDBJ controlled vocabulary of permitted cross references.\n                            ')

    
    # Element ID uses Python identifier ID
    __ID = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__SRA_common_CTD_ANON_36_ID', False)

    
    ID = property(__ID.value, __ID.set, None, u'Accession in the referenced database.\n                            ')


    _ElementMap = {
        __URL.name() : __URL,
        __LABEL.name() : __LABEL,
        __DB.name() : __DB,
        __ID.name() : __ID
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_37 with content type ELEMENT_ONLY
class CTD_ANON_37 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element NOTES uses Python identifier NOTES
    __NOTES = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'NOTES'), 'NOTES', '__SRA_common_CTD_ANON_37_NOTES', False)

    
    NOTES = property(__NOTES.value, __NOTES.set, None, u'\n                                    Notes about the program or process for primary analysis. \n                                ')

    
    # Element STEP_INDEX uses Python identifier STEP_INDEX
    __STEP_INDEX = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'STEP_INDEX'), 'STEP_INDEX', '__SRA_common_CTD_ANON_37_STEP_INDEX', False)

    
    STEP_INDEX = property(__STEP_INDEX.value, __STEP_INDEX.set, None, u'\n                                    Lexically ordered  value that allows for the pipe section to be hierarchically ordered.  The float primitive data type is\n                                    used to allow for pipe sections to be inserted later on.\n                                ')

    
    # Element VERSION uses Python identifier VERSION
    __VERSION = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'VERSION'), 'VERSION', '__SRA_common_CTD_ANON_37_VERSION', False)

    
    VERSION = property(__VERSION.value, __VERSION.set, None, u'\n                                    Version of the program or process for primary analysis. \n                                ')

    
    # Element PREV_STEP_INDEX uses Python identifier PREV_STEP_INDEX
    __PREV_STEP_INDEX = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PREV_STEP_INDEX'), 'PREV_STEP_INDEX', '__SRA_common_CTD_ANON_37_PREV_STEP_INDEX', True)

    
    PREV_STEP_INDEX = property(__PREV_STEP_INDEX.value, __PREV_STEP_INDEX.set, None, u'\n                                    STEP_INDEX of the previous step in the workflow.  Set toNIL if the first pipe section.\n                                ')

    
    # Element PROGRAM uses Python identifier PROGRAM
    __PROGRAM = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PROGRAM'), 'PROGRAM', '__SRA_common_CTD_ANON_37_PROGRAM', False)

    
    PROGRAM = property(__PROGRAM.value, __PROGRAM.set, None, u'\n                                    Name of the program or process for primary analysis.   This may include a test or condition\n                                    that leads to branching in the workflow.\n                                ')

    
    # Attribute section_name uses Python identifier section_name
    __section_name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'section_name'), 'section_name', '__SRA_common_CTD_ANON_37_section_name', pyxb.binding.datatypes.string)
    
    section_name = property(__section_name.value, __section_name.set, None, u'\n                                Name of the processing pipeline section.\n                            ')


    _ElementMap = {
        __NOTES.name() : __NOTES,
        __STEP_INDEX.name() : __STEP_INDEX,
        __VERSION.name() : __VERSION,
        __PREV_STEP_INDEX.name() : __PREV_STEP_INDEX,
        __PROGRAM.name() : __PROGRAM
    }
    _AttributeMap = {
        __section_name.name() : __section_name
    }



# Complex type CTD_ANON_38 with content type EMPTY
class CTD_ANON_38 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute ktile uses Python identifier ktile
    __ktile = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ktile'), 'ktile', '__SRA_common_CTD_ANON_38_ktile', pyxb.binding.datatypes.positiveInteger, required=True)
    
    ktile = property(__ktile.value, __ktile.set, None, u' k-tile where k is the k-th bin ')

    
    # Attribute value uses Python identifier value_
    __value = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'value'), 'value_', '__SRA_common_CTD_ANON_38_value', pyxb.binding.datatypes.nonNegativeInteger, required=True)
    
    value_ = property(__value.value, __value.set, None, u' Frequency count or 0. ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __ktile.name() : __ktile,
        __value.name() : __value
    }



# Complex type PlatformType with content type ELEMENT_ONLY
class PlatformType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'PlatformType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element COMPLETE_GENOMICS uses Python identifier COMPLETE_GENOMICS
    __COMPLETE_GENOMICS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'COMPLETE_GENOMICS'), 'COMPLETE_GENOMICS', '__SRA_common_PlatformType_COMPLETE_GENOMICS', False)

    
    COMPLETE_GENOMICS = property(__COMPLETE_GENOMICS.value, __COMPLETE_GENOMICS.set, None, u'\n                            Placeholder for CompleteGenomics platform type.   At present there is no instrument model.\n                        ')

    
    # Element PACBIO_SMRT uses Python identifier PACBIO_SMRT
    __PACBIO_SMRT = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PACBIO_SMRT'), 'PACBIO_SMRT', '__SRA_common_PlatformType_PACBIO_SMRT', False)

    
    PACBIO_SMRT = property(__PACBIO_SMRT.value, __PACBIO_SMRT.set, None, u'\n                            Placeholder for PacificBiosciences platform type.   At present there is no instrument model.\n                        ')

    
    # Element ILLUMINA uses Python identifier ILLUMINA
    __ILLUMINA = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ILLUMINA'), 'ILLUMINA', '__SRA_common_PlatformType_ILLUMINA', False)

    
    ILLUMINA = property(__ILLUMINA.value, __ILLUMINA.set, None, u'\n                            Illumina is 4-channel flowgram with 1-to-1 mapping between basecalls and flows\n                        ')

    
    # Element ABI_SOLID uses Python identifier ABI_SOLID
    __ABI_SOLID = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ABI_SOLID'), 'ABI_SOLID', '__SRA_common_PlatformType_ABI_SOLID', False)

    
    ABI_SOLID = property(__ABI_SOLID.value, __ABI_SOLID.set, None, u'\n                            ABI is 4-channel flowgram with 1-to-1 mapping between basecalls and flows\n                        ')

    
    # Element HELICOS uses Python identifier HELICOS
    __HELICOS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'HELICOS'), 'HELICOS', '__SRA_common_PlatformType_HELICOS', False)

    
    HELICOS = property(__HELICOS.value, __HELICOS.set, None, u'\n                            Helicos is similar to 454 technology - uses 1-color sequential flows   \n                        ')

    
    # Element ION_TORRENT uses Python identifier ION_TORRENT
    __ION_TORRENT = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ION_TORRENT'), 'ION_TORRENT', '__SRA_common_PlatformType_ION_TORRENT', False)

    
    ION_TORRENT = property(__ION_TORRENT.value, __ION_TORRENT.set, None, u'\n                    ')

    
    # Element LS454 uses Python identifier LS454
    __LS454 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LS454'), 'LS454', '__SRA_common_PlatformType_LS454', False)

    
    LS454 = property(__LS454.value, __LS454.set, None, u'\n                            454 technology use 1-color sequential flows \n                        ')


    _ElementMap = {
        __COMPLETE_GENOMICS.name() : __COMPLETE_GENOMICS,
        __PACBIO_SMRT.name() : __PACBIO_SMRT,
        __ILLUMINA.name() : __ILLUMINA,
        __ABI_SOLID.name() : __ABI_SOLID,
        __HELICOS.name() : __HELICOS,
        __ION_TORRENT.name() : __ION_TORRENT,
        __LS454.name() : __LS454
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'PlatformType', PlatformType)


# Complex type CTD_ANON_39 with content type ELEMENT_ONLY
class CTD_ANON_39 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element DB uses Python identifier DB
    __DB = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DB'), 'DB', '__SRA_common_CTD_ANON_39_DB', False)

    
    DB = property(__DB.value, __DB.set, None, u'\n                                EBI ENA controlled vocabulary of permitted\n                                cross references.\n                            ')

    
    # Element LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LABEL'), 'LABEL', '__SRA_common_CTD_ANON_39_LABEL', False)

    
    LABEL = property(__LABEL.value, __LABEL.set, None, u'A textual description of the cross-reference.\n                            ')

    
    # Element URL uses Python identifier URL
    __URL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'URL'), 'URL', '__SRA_common_CTD_ANON_39_URL', False)

    
    URL = property(__URL.value, __URL.set, None, u'An URL to the cross-references accession.\n                            ')

    
    # Element ID uses Python identifier ID
    __ID = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ID'), 'ID', '__SRA_common_CTD_ANON_39_ID', False)

    
    ID = property(__ID.value, __ID.set, None, u' Accession in the referenced\n                                database.')


    _ElementMap = {
        __DB.name() : __DB,
        __LABEL.name() : __LABEL,
        __URL.name() : __URL,
        __ID.name() : __ID
    }
    _AttributeMap = {
        
    }



# Complex type ReferenceSequenceType with content type ELEMENT_ONLY
class ReferenceSequenceType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ReferenceSequenceType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element SEQUENCE uses Python identifier SEQUENCE
    __SEQUENCE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SEQUENCE'), 'SEQUENCE', '__SRA_common_ReferenceSequenceType_SEQUENCE', True)

    
    SEQUENCE = property(__SEQUENCE.value, __SEQUENCE.set, None, u'Reference sequence details.')

    
    # Element ASSEMBLY uses Python identifier ASSEMBLY
    __ASSEMBLY = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ASSEMBLY'), 'ASSEMBLY', '__SRA_common_ReferenceSequenceType_ASSEMBLY', False)

    
    ASSEMBLY = property(__ASSEMBLY.value, __ASSEMBLY.set, None, u'Reference assembly details.')


    _ElementMap = {
        __SEQUENCE.name() : __SEQUENCE,
        __ASSEMBLY.name() : __ASSEMBLY
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ReferenceSequenceType', ReferenceSequenceType)


# Complex type CTD_ANON_40 with content type EMPTY
class CTD_ANON_40 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute accession uses Python identifier accession
    __accession = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'accession'), 'accession', '__SRA_common_CTD_ANON_40_accession', pyxb.binding.datatypes.token)
    
    accession = property(__accession.value, __accession.set, None, u'Identifies the genome assembly\n                                                 using an accession number and a sequence version.\n                                                 ')

    
    # Attribute refname uses Python identifier refname
    __refname = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'refname'), 'refname', '__SRA_common_CTD_ANON_40_refname', pyxb.binding.datatypes.string)
    
    refname = property(__refname.value, __refname.set, None, u'A recognized name for the\n                                                 genome assembly.')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __accession.name() : __accession,
        __refname.name() : __refname
    }



# Complex type CTD_ANON_41 with content type ELEMENT_ONLY
class CTD_ANON_41 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element FLOW_SEQUENCE uses Python identifier FLOW_SEQUENCE
    __FLOW_SEQUENCE = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'FLOW_SEQUENCE'), 'FLOW_SEQUENCE', '__SRA_common_CTD_ANON_41_FLOW_SEQUENCE', False)

    
    FLOW_SEQUENCE = property(__FLOW_SEQUENCE.value, __FLOW_SEQUENCE.set, None, u'\n                                        The fixed sequence of challenge bases that flow across the flowcell. \n                                        This is optional in the schema now but will be required by business rules and future schema versions.\n                                    ')

    
    # Element FLOW_COUNT uses Python identifier FLOW_COUNT
    __FLOW_COUNT = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'FLOW_COUNT'), 'FLOW_COUNT', '__SRA_common_CTD_ANON_41_FLOW_COUNT', False)

    
    FLOW_COUNT = property(__FLOW_COUNT.value, __FLOW_COUNT.set, None, u'\n                                        The number of flows of challenge bases.  This is a constraint on maximum read length, but not equivalent. \n                                        This is optional in the schema now but will be required by business rules and future schema versions.\n                                    ')

    
    # Element INSTRUMENT_MODEL uses Python identifier INSTRUMENT_MODEL
    __INSTRUMENT_MODEL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), 'INSTRUMENT_MODEL', '__SRA_common_CTD_ANON_41_INSTRUMENT_MODEL', False)

    
    INSTRUMENT_MODEL = property(__INSTRUMENT_MODEL.value, __INSTRUMENT_MODEL.set, None, None)


    _ElementMap = {
        __FLOW_SEQUENCE.name() : __FLOW_SEQUENCE,
        __FLOW_COUNT.name() : __FLOW_COUNT,
        __INSTRUMENT_MODEL.name() : __INSTRUMENT_MODEL
    }
    _AttributeMap = {
        
    }





CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LOCUS'), CTD_ANON_8, scope=CTD_ANON))
CTD_ANON._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, u'LOCUS')), min_occurs=1L, max_occurs=None)
    )
CTD_ANON._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SEQUENCE_LENGTH'), pyxb.binding.datatypes.positiveInteger, scope=CTD_ANON_, documentation=u'\n                                        The fixed number of bases expected in each raw sequence, including both mate pairs and any technical reads.\n                                    '))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'CYCLE_COUNT'), pyxb.binding.datatypes.positiveInteger, scope=CTD_ANON_, documentation=u'\n                                        DEPRECATED, use SEQUENCE_LENGTH instead.  The fixed number of bases  in each raw sequence, including both mate pairs and any technical reads.\n                                    '))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), STD_ANON, scope=CTD_ANON_))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'CYCLE_SEQUENCE'), pyxb.binding.datatypes.string, scope=CTD_ANON_, documentation=u'\n                                        DEPRECATED.\n                                    '))
CTD_ANON_._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, u'CYCLE_SEQUENCE')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, u'CYCLE_COUNT')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, u'SEQUENCE_LENGTH')), min_occurs=0L, max_occurs=1L)
    )
CTD_ANON_._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_._GroupModel, min_occurs=1, max_occurs=1)



SampleDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'POOL'), CTD_ANON_3, scope=SampleDescriptorType, documentation=u'\n                        Identifies a list of group/pool/multiplex sample members.  This implies that\n                        this sample record is a group, pool, or multiplex, but is continues to receive\n                        its own accession and can be referenced by an experiment.  By default if\n                        no match to any of the listed members can be determined, then the default\n                        sampel reference is used.\n                    '))
SampleDescriptorType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SampleDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'POOL')), min_occurs=0L, max_occurs=1L)
    )
SampleDescriptorType._ContentModel = pyxb.binding.content.ParticleModel(SampleDescriptorType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DESCRIPTION'), pyxb.binding.datatypes.string, scope=CTD_ANON_2, documentation=u'Description of the genome\n                                                 assembly.'))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'URL_LINK'), CTD_ANON_5, scope=CTD_ANON_2, documentation=u'A link to the genome\n                                                 assembly.'))
CTD_ANON_2._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, u'DESCRIPTION')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, u'URL_LINK')), min_occurs=1, max_occurs=None)
    )
CTD_ANON_2._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_2._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'MEMBER'), CTD_ANON_6, scope=CTD_ANON_3))
CTD_ANON_3._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, u'MEMBER')), min_occurs=1L, max_occurs=None)
    )
CTD_ANON_3._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_3._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LABEL'), pyxb.binding.datatypes.string, scope=CTD_ANON_5, documentation=u' Text label to display for the\n                                                 link. '))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'URL'), pyxb.binding.datatypes.anyURI, scope=CTD_ANON_5, documentation=u' The internet service link\n                                                 (file:, http:, ftp:, etc). '))
CTD_ANON_5._GroupModel = pyxb.binding.content.GroupAll(
    pyxb.binding.content.ParticleModel(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, u'LABEL')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, u'URL')), min_occurs=1L, max_occurs=1L)
    )
CTD_ANON_5._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_5._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'READ_LABEL'), CTD_ANON_11, scope=CTD_ANON_6))
CTD_ANON_6._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, u'READ_LABEL')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_6._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_6._GroupModel, min_occurs=0L, max_occurs=None)



GapDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'GAP'), CTD_ANON_17, scope=GapDescriptorType))
GapDescriptorType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(GapDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'GAP')), min_occurs=1L, max_occurs=None)
    )
GapDescriptorType._ContentModel = pyxb.binding.content.ParticleModel(GapDescriptorType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'BASECALL'), CTD_ANON_13, scope=CTD_ANON_7, documentation=u"\n                                                                    Element's body contains a basecall, attribute provide description of this read meaning as well as matching rules.\n                                                                "))
CTD_ANON_7._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, u'BASECALL')), min_occurs=1, max_occurs=None)
    )
CTD_ANON_7._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_7._GroupModel, min_occurs=1L, max_occurs=1L)



SpotDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SPOT_DECODE_SPEC'), CTD_ANON_12, scope=SpotDescriptorType))

SpotDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SPOT_DECODE_METHOD'), pyxb.binding.datatypes.unsignedInt, scope=SpotDescriptorType, documentation=u'\n                            DEPRECATED.                                    \n                        '))
SpotDescriptorType._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(SpotDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'SPOT_DECODE_METHOD')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SpotDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'SPOT_DECODE_SPEC')), min_occurs=1, max_occurs=1)
    )
SpotDescriptorType._ContentModel = pyxb.binding.content.ParticleModel(SpotDescriptorType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_8._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PROBE_SET'), XRefType, scope=CTD_ANON_8, documentation=u'\n                                              Reference to an archived primer or probe set.  Example:  dbProbe\n                                          '))
CTD_ANON_8._GroupModel = pyxb.binding.content.GroupAll(
    pyxb.binding.content.ParticleModel(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(None, u'PROBE_SET')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_8._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_8._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_10._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), STD_ANON_17, scope=CTD_ANON_10))

CTD_ANON_10._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'KEY_SEQUENCE'), pyxb.binding.datatypes.string, scope=CTD_ANON_10, documentation=u'\n                                        The first bases that are expected to be produced by the challenge bases.  \n                                        This is optional in the schema now but will be required by business rules and future schema versions.\n                                    '))

CTD_ANON_10._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'FLOW_COUNT'), pyxb.binding.datatypes.positiveInteger, scope=CTD_ANON_10, documentation=u'\n                                        The number of flows of challenge bases.  This is a constraint on maximum read length, but not equivalent.\n                                        This is optional in the schema now but will be required by business rules and future schema versions.\n                                    '))

CTD_ANON_10._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'FLOW_SEQUENCE'), pyxb.binding.datatypes.string, scope=CTD_ANON_10, documentation=u'\n                                        The fixed sequence of challenge bases that flow across the picotiter plate.  \n                                        This is optional in the schema now but will be required by business rules and future schema versions.\n                                    '))
CTD_ANON_10._GroupModel = pyxb.binding.content.GroupAll(
    pyxb.binding.content.ParticleModel(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(None, u'KEY_SEQUENCE')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(None, u'FLOW_SEQUENCE')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(None, u'FLOW_COUNT')), min_occurs=0L, max_occurs=1L)
    )
CTD_ANON_10._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_10._GroupModel, min_occurs=1, max_occurs=1)



ReferenceAssemblyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'STANDARD'), CTD_ANON_40, scope=ReferenceAssemblyType, documentation=u'A standard genome assembly.\n                                                 '))

ReferenceAssemblyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'CUSTOM'), CTD_ANON_2, scope=ReferenceAssemblyType, documentation=u'Other genome\n                                                 assembly.'))
ReferenceAssemblyType._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(ReferenceAssemblyType._UseForTag(pyxb.namespace.ExpandedName(None, u'STANDARD')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ReferenceAssemblyType._UseForTag(pyxb.namespace.ExpandedName(None, u'CUSTOM')), min_occurs=1, max_occurs=1)
    )
ReferenceAssemblyType._ContentModel = pyxb.binding.content.ParticleModel(ReferenceAssemblyType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SPOT_LENGTH'), pyxb.binding.datatypes.nonNegativeInteger, scope=CTD_ANON_12, documentation=u'\n                                        Expected number of base calls or cycles per spot (raw sequence length including all application and technical tags and mate pairs)\n                                    '))

CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'READ_SPEC'), CTD_ANON_14, scope=CTD_ANON_12))

CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ADAPTER_SPEC'), pyxb.binding.datatypes.string, scope=CTD_ANON_12, documentation=u'\n                                        Some technologies will require knowledge of the sequencing adapter or the last base of the adapter in order to decode the spot.\n                                    '))

CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'NUMBER_OF_READS_PER_SPOT'), pyxb.binding.datatypes.unsignedInt, scope=CTD_ANON_12, documentation=u'\n                                        DEPRECATED.  Number of tags (reads) per spot.\n                                    '))
CTD_ANON_12._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(None, u'NUMBER_OF_READS_PER_SPOT')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(None, u'SPOT_LENGTH')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(None, u'ADAPTER_SPEC')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(None, u'READ_SPEC')), min_occurs=1L, max_occurs=None)
    )
CTD_ANON_12._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_12._GroupModel, min_occurs=1, max_occurs=1)



LibraryDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LIBRARY_NAME'), pyxb.binding.datatypes.string, scope=LibraryDescriptorType, documentation=u"\n                      The submitter's name for this library.\n                  "))

LibraryDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TARGETED_LOCI'), CTD_ANON, scope=LibraryDescriptorType))

LibraryDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LIBRARY_SELECTION'), STD_ANON_8, scope=LibraryDescriptorType, documentation=u'\n                      Whether any method was used to select for or against, enrich, or screen \n                      the material being sequenced.     \n                  '))

LibraryDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LIBRARY_CONSTRUCTION_PROTOCOL'), pyxb.binding.datatypes.string, scope=LibraryDescriptorType, documentation=u'\n                      Free form text describing the protocol by which the sequencing library was constructed.                             \n                  '))

LibraryDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LIBRARY_STRATEGY'), STD_ANON_5, scope=LibraryDescriptorType, documentation=u'\n                      Sequencing technique intended for this library.\n                  '))

LibraryDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LIBRARY_LAYOUT'), CTD_ANON_15, scope=LibraryDescriptorType, documentation=u'\n                      LIBRARY_LAYOUT specifies whether to expect single, paired, or other configuration of reads.  \n                      In the case of paired reads, information about the relative distance and orientation is specified.\n                  '))

LibraryDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LIBRARY_SOURCE'), STD_ANON_6, scope=LibraryDescriptorType, documentation=u'\n                      The LIBRARY_SOURCE specifies the type of source material that is being sequenced.\n                  '))

LibraryDescriptorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'POOLING_STRATEGY'), STD_ANON_, scope=LibraryDescriptorType, documentation=u'\n                      The optional pooling strategy indicates how the library or libraries are organized if multiple samples are involved.\n                  '))
LibraryDescriptorType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(LibraryDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'LIBRARY_NAME')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(LibraryDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'LIBRARY_STRATEGY')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LibraryDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'LIBRARY_SOURCE')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(LibraryDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'LIBRARY_SELECTION')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(LibraryDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'LIBRARY_LAYOUT')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(LibraryDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'TARGETED_LOCI')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LibraryDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'POOLING_STRATEGY')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(LibraryDescriptorType._UseForTag(pyxb.namespace.ExpandedName(None, u'LIBRARY_CONSTRUCTION_PROTOCOL')), min_occurs=0L, max_occurs=1L)
    )
LibraryDescriptorType._ContentModel = pyxb.binding.content.ParticleModel(LibraryDescriptorType._GroupModel, min_occurs=1, max_occurs=1)



AttributeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'UNITS'), pyxb.binding.datatypes.string, scope=AttributeType, documentation=u'\n                        Optional scientific units.\n                    '))

AttributeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TAG'), pyxb.binding.datatypes.string, scope=AttributeType, documentation=u'\n                        Name of the attribute.\n                    '))

AttributeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'VALUE'), pyxb.binding.datatypes.string, scope=AttributeType, documentation=u'\n                        Value of the attribute.\n                    '))
AttributeType._GroupModel = pyxb.binding.content.GroupAll(
    pyxb.binding.content.ParticleModel(AttributeType._UseForTag(pyxb.namespace.ExpandedName(None, u'TAG')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(AttributeType._UseForTag(pyxb.namespace.ExpandedName(None, u'VALUE')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(AttributeType._UseForTag(pyxb.namespace.ExpandedName(None, u'UNITS')), min_occurs=0L, max_occurs=1L)
    )
AttributeType._ContentModel = pyxb.binding.content.ParticleModel(AttributeType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_14._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'CYCLE_COORD'), pyxb.binding.datatypes.integer, scope=CTD_ANON_14, documentation=u'\n                                                        The location of the read start in terms of cycle count (1 is beginning of spot).\n                                                    '))

CTD_ANON_14._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'READ_TYPE'), STD_ANON_11, scope=CTD_ANON_14))

CTD_ANON_14._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'READ_CLASS'), STD_ANON_9, scope=CTD_ANON_14))

CTD_ANON_14._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'EXPECTED_BASECALL'), CTD_ANON_4, scope=CTD_ANON_14, documentation=u'\n                                                        An expected basecall for a current read. Read will be zero-length if basecall is not present.\n                                                        Users of this facility should start migrating to EXPECTED_BASECALL_TABLE, as this field\n                                                        will be phased out.\n                                                    '))

CTD_ANON_14._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'EXPECTED_BASECALL_TABLE'), CTD_ANON_7, scope=CTD_ANON_14, documentation=u'\n                                                        A set of choices of expected basecalls for a current read. Read will be zero-length if none is found.\n                                                    '))

CTD_ANON_14._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'READ_LABEL'), pyxb.binding.datatypes.string, scope=CTD_ANON_14, documentation=u'READ_LABEL is a name for this tag, and can be used to on output to determine read name, for example F or R.'))

CTD_ANON_14._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'RELATIVE_ORDER'), CTD_ANON_25, scope=CTD_ANON_14, documentation=u'\n                                                        The read is located beginning at the offset or cycle relative to another read.  \n                                                        This choice is appropriate for example when specifying a read\n                                                        that follows a variable length expected sequence(s).\n                                                    '))

CTD_ANON_14._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'BASE_COORD'), pyxb.binding.datatypes.integer, scope=CTD_ANON_14, documentation=u'\n                                                        The location of the read start in terms of base count (1 is beginning of spot).\n                                                    '))

CTD_ANON_14._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'READ_INDEX'), pyxb.binding.datatypes.nonNegativeInteger, scope=CTD_ANON_14, documentation=u'READ_INDEX starts at 0 and is incrementally increased for each sequential READ_SPEC within a SPOT_DECODE_SPEC'))
CTD_ANON_14._GroupModel_ = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_14._UseForTag(pyxb.namespace.ExpandedName(None, u'RELATIVE_ORDER')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_14._UseForTag(pyxb.namespace.ExpandedName(None, u'BASE_COORD')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_14._UseForTag(pyxb.namespace.ExpandedName(None, u'CYCLE_COORD')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_14._UseForTag(pyxb.namespace.ExpandedName(None, u'EXPECTED_BASECALL')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_14._UseForTag(pyxb.namespace.ExpandedName(None, u'EXPECTED_BASECALL_TABLE')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_14._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_14._UseForTag(pyxb.namespace.ExpandedName(None, u'READ_INDEX')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_14._UseForTag(pyxb.namespace.ExpandedName(None, u'READ_LABEL')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_14._UseForTag(pyxb.namespace.ExpandedName(None, u'READ_CLASS')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_14._UseForTag(pyxb.namespace.ExpandedName(None, u'READ_TYPE')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_14._GroupModel_, min_occurs=1, max_occurs=1)
    )
CTD_ANON_14._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_14._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_15._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PAIRED'), CTD_ANON_22, scope=CTD_ANON_15))

CTD_ANON_15._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SINGLE'), CTD_ANON_18, scope=CTD_ANON_15))
CTD_ANON_15._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(None, u'SINGLE')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(None, u'PAIRED')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_15._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_15._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_16._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'COLOR'), CTD_ANON_19, scope=CTD_ANON_16))
CTD_ANON_16._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(None, u'COLOR')), min_occurs=1L, max_occurs=None)
    )
CTD_ANON_16._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_16._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_17._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'GAP_SPEC'), CTD_ANON_29, scope=CTD_ANON_17))

CTD_ANON_17._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'GAP_TYPE'), CTD_ANON_20, scope=CTD_ANON_17, documentation=u' Specifies the gap type and parameters. '))
CTD_ANON_17._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_17._UseForTag(pyxb.namespace.ExpandedName(None, u'GAP_TYPE')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_17._UseForTag(pyxb.namespace.ExpandedName(None, u'GAP_SPEC')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_17._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_17._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_20._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PairedEnd'), CTD_ANON_28, scope=CTD_ANON_20, documentation=u' Mated tags sequenced from two ends\n                                                of a physical extent of genomic material. \n                                            '))

CTD_ANON_20._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Tandem'), CTD_ANON_9, scope=CTD_ANON_20, documentation=u' Tandem gaps between ligands. '))

CTD_ANON_20._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'MatePair'), CTD_ANON_26, scope=CTD_ANON_20, documentation=u' Mated tags with predicted separation and orientation. '))
CTD_ANON_20._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_20._UseForTag(pyxb.namespace.ExpandedName(None, u'Tandem')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_20._UseForTag(pyxb.namespace.ExpandedName(None, u'MatePair')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_20._UseForTag(pyxb.namespace.ExpandedName(None, u'PairedEnd')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_20._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_20._GroupModel, min_occurs=1, max_occurs=1)



LinkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SRA_LINK'), SraLinkType, scope=LinkType))

LinkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'XREF_LINK'), XRefType, scope=LinkType))

LinkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ENTREZ_LINK'), CTD_ANON_30, scope=LinkType))

LinkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'URL_LINK'), CTD_ANON_24, scope=LinkType))

LinkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ENA_LINK'), CTD_ANON_39, scope=LinkType))

LinkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DDBJ_LINK'), CTD_ANON_36, scope=LinkType))
LinkType._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(LinkType._UseForTag(pyxb.namespace.ExpandedName(None, u'SRA_LINK')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(LinkType._UseForTag(pyxb.namespace.ExpandedName(None, u'URL_LINK')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(LinkType._UseForTag(pyxb.namespace.ExpandedName(None, u'XREF_LINK')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(LinkType._UseForTag(pyxb.namespace.ExpandedName(None, u'ENTREZ_LINK')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(LinkType._UseForTag(pyxb.namespace.ExpandedName(None, u'DDBJ_LINK')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(LinkType._UseForTag(pyxb.namespace.ExpandedName(None, u'ENA_LINK')), min_occurs=1, max_occurs=1)
    )
LinkType._ContentModel = pyxb.binding.content.ParticleModel(LinkType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_23._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), STD_ANON_14, scope=CTD_ANON_23))
CTD_ANON_23._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_23._UseForTag(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL')), min_occurs=1L, max_occurs=1L)
    )
CTD_ANON_23._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_23._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_24._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'URL'), pyxb.binding.datatypes.anyURI, scope=CTD_ANON_24, documentation=u'\n                                    The internet service link (file:, http:, ftp:, etc).\n                                '))

CTD_ANON_24._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LABEL'), pyxb.binding.datatypes.string, scope=CTD_ANON_24, documentation=u'\n                                    Text label to display for the link.\n                                '))
CTD_ANON_24._GroupModel = pyxb.binding.content.GroupAll(
    pyxb.binding.content.ParticleModel(CTD_ANON_24._UseForTag(pyxb.namespace.ExpandedName(None, u'LABEL')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_24._UseForTag(pyxb.namespace.ExpandedName(None, u'URL')), min_occurs=1L, max_occurs=1L)
    )
CTD_ANON_24._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_24._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_27._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), STD_ANON_13, scope=CTD_ANON_27))
CTD_ANON_27._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_27._UseForTag(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL')), min_occurs=1L, max_occurs=1L)
    )
CTD_ANON_27._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_27._GroupModel, min_occurs=1, max_occurs=1)



XRefType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LABEL'), pyxb.binding.datatypes.string, scope=XRefType, documentation=u'\n                            Text label to display for the link.\n                        '))

XRefType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ID'), pyxb.binding.datatypes.string, scope=XRefType, documentation=u'\n                            Accession in the referenced database.    For example,  FBtr0080008 (in FLYBASE).\n                        '))

XRefType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DB'), pyxb.binding.datatypes.string, scope=XRefType, documentation=u'\n                            INSDC controlled vocabulary of permitted cross references.  Please see http://www.insdc.org/page.php?page=db_xref .\n                            For example, FLYBASE.\n                        '))
XRefType._GroupModel = pyxb.binding.content.GroupAll(
    pyxb.binding.content.ParticleModel(XRefType._UseForTag(pyxb.namespace.ExpandedName(None, u'DB')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(XRefType._UseForTag(pyxb.namespace.ExpandedName(None, u'ID')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(XRefType._UseForTag(pyxb.namespace.ExpandedName(None, u'LABEL')), min_occurs=0L, max_occurs=1L)
    )
XRefType._ContentModel = pyxb.binding.content.ParticleModel(XRefType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_29._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'interval'), CTD_ANON_31, scope=CTD_ANON_29))

CTD_ANON_29._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'statistic'), CTD_ANON_34, scope=CTD_ANON_29))

CTD_ANON_29._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'histogram'), CTD_ANON_35, scope=CTD_ANON_29))
CTD_ANON_29._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_29._UseForTag(pyxb.namespace.ExpandedName(None, u'interval')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_29._UseForTag(pyxb.namespace.ExpandedName(None, u'statistic')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_29._UseForTag(pyxb.namespace.ExpandedName(None, u'histogram')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_29._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_29._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_30._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'QUERY'), pyxb.binding.datatypes.string, scope=CTD_ANON_30, documentation=u'\n                                        Accession string meaningful to the NCBI Entrez system.\n                                    '))

CTD_ANON_30._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LABEL'), pyxb.binding.datatypes.string, scope=CTD_ANON_30, documentation=u'\n                                    How to label the link.\n                                '))

CTD_ANON_30._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ID'), pyxb.binding.datatypes.nonNegativeInteger, scope=CTD_ANON_30, documentation=u'\n                                        Numeric record id meaningful to the NCBI Entrez system.\n                                    '))

CTD_ANON_30._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DB'), pyxb.binding.datatypes.string, scope=CTD_ANON_30, documentation=u'\n                                    NCBI controlled vocabulary of permitted cross references.  Please see http://www.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi? .\n                                '))
CTD_ANON_30._GroupModel_ = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_30._UseForTag(pyxb.namespace.ExpandedName(None, u'ID')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_30._UseForTag(pyxb.namespace.ExpandedName(None, u'QUERY')), min_occurs=1L, max_occurs=1L)
    )
CTD_ANON_30._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_30._UseForTag(pyxb.namespace.ExpandedName(None, u'DB')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_30._GroupModel_, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_30._UseForTag(pyxb.namespace.ExpandedName(None, u'LABEL')), min_occurs=0L, max_occurs=1L)
    )
CTD_ANON_30._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_30._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_32._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), STD_ANON_15, scope=CTD_ANON_32))
CTD_ANON_32._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_32._UseForTag(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL')), min_occurs=1L, max_occurs=1L)
    )
CTD_ANON_32._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_32._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_33._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'CYCLE_COUNT'), pyxb.binding.datatypes.positiveInteger, scope=CTD_ANON_33, documentation=u'\n                                        DEPRECATED.  Use SEQUENCE_LENGTH instead.\n                                    '))

CTD_ANON_33._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), STD_ANON_7, scope=CTD_ANON_33))

CTD_ANON_33._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'COLOR_MATRIX'), CTD_ANON_16, scope=CTD_ANON_33, documentation=u' DEPRECATED. '))

CTD_ANON_33._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'COLOR_MATRIX_CODE'), pyxb.binding.datatypes.string, scope=CTD_ANON_33, documentation=u' DEPRECATED. '))

CTD_ANON_33._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SEQUENCE_LENGTH'), pyxb.binding.datatypes.positiveInteger, scope=CTD_ANON_33, documentation=u'\n                                        The fixed number of bases expected in each raw sequence, including both mate pairs and any technical reads.\n                                        This is optional in the schema now but will be required by business rules and future schema versions.\n                                    '))
CTD_ANON_33._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_33._UseForTag(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_33._UseForTag(pyxb.namespace.ExpandedName(None, u'COLOR_MATRIX')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_33._UseForTag(pyxb.namespace.ExpandedName(None, u'COLOR_MATRIX_CODE')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_33._UseForTag(pyxb.namespace.ExpandedName(None, u'CYCLE_COUNT')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_33._UseForTag(pyxb.namespace.ExpandedName(None, u'SEQUENCE_LENGTH')), min_occurs=0L, max_occurs=1L)
    )
CTD_ANON_33._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_33._GroupModel, min_occurs=1, max_occurs=1)



SequencingDirectivesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SAMPLE_DEMUX_DIRECTIVE'), STD_ANON_16, scope=SequencingDirectivesType, documentation=u'\n                        Tells the Archive who will execute the sample demultiplexing operation..\n                    '))
SequencingDirectivesType._GroupModel = pyxb.binding.content.GroupAll(
    pyxb.binding.content.ParticleModel(SequencingDirectivesType._UseForTag(pyxb.namespace.ExpandedName(None, u'SAMPLE_DEMUX_DIRECTIVE')), min_occurs=0L, max_occurs=1L)
    )
SequencingDirectivesType._ContentModel = pyxb.binding.content.ParticleModel(SequencingDirectivesType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_35._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'bin'), CTD_ANON_38, scope=CTD_ANON_35))
CTD_ANON_35._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_35._UseForTag(pyxb.namespace.ExpandedName(None, u'bin')), min_occurs=1L, max_occurs=None)
    )
CTD_ANON_35._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_35._GroupModel, min_occurs=1, max_occurs=1)



PipelineType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PIPE_SECTION'), CTD_ANON_37, scope=PipelineType))
PipelineType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(PipelineType._UseForTag(pyxb.namespace.ExpandedName(None, u'PIPE_SECTION')), min_occurs=1L, max_occurs=None)
    )
PipelineType._ContentModel = pyxb.binding.content.ParticleModel(PipelineType._GroupModel, min_occurs=1L, max_occurs=1L)



CTD_ANON_36._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'URL'), pyxb.binding.datatypes.anyURI, scope=CTD_ANON_36, documentation=u'An URL to the cross-references accession.\n                            '))

CTD_ANON_36._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LABEL'), pyxb.binding.datatypes.string, scope=CTD_ANON_36, documentation=u'A textual description of the cross-reference.\n                            '))

CTD_ANON_36._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DB'), pyxb.binding.datatypes.string, scope=CTD_ANON_36, documentation=u'DDBJ controlled vocabulary of permitted cross references.\n                            '))

CTD_ANON_36._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ID'), pyxb.binding.datatypes.string, scope=CTD_ANON_36, documentation=u'Accession in the referenced database.\n                            '))
CTD_ANON_36._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_36._UseForTag(pyxb.namespace.ExpandedName(None, u'DB')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_36._UseForTag(pyxb.namespace.ExpandedName(None, u'ID')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_36._UseForTag(pyxb.namespace.ExpandedName(None, u'URL')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_36._UseForTag(pyxb.namespace.ExpandedName(None, u'LABEL')), min_occurs=0L, max_occurs=1L)
    )
CTD_ANON_36._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_36._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_37._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'NOTES'), pyxb.binding.datatypes.string, scope=CTD_ANON_37, documentation=u'\n                                    Notes about the program or process for primary analysis. \n                                '))

CTD_ANON_37._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'STEP_INDEX'), pyxb.binding.datatypes.string, scope=CTD_ANON_37, documentation=u'\n                                    Lexically ordered  value that allows for the pipe section to be hierarchically ordered.  The float primitive data type is\n                                    used to allow for pipe sections to be inserted later on.\n                                '))

CTD_ANON_37._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'VERSION'), pyxb.binding.datatypes.string, scope=CTD_ANON_37, documentation=u'\n                                    Version of the program or process for primary analysis. \n                                '))

CTD_ANON_37._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PREV_STEP_INDEX'), pyxb.binding.datatypes.string, nillable=pyxb.binding.datatypes.boolean(1), scope=CTD_ANON_37, documentation=u'\n                                    STEP_INDEX of the previous step in the workflow.  Set toNIL if the first pipe section.\n                                '))

CTD_ANON_37._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PROGRAM'), pyxb.binding.datatypes.string, scope=CTD_ANON_37, documentation=u'\n                                    Name of the program or process for primary analysis.   This may include a test or condition\n                                    that leads to branching in the workflow.\n                                '))
CTD_ANON_37._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_37._UseForTag(pyxb.namespace.ExpandedName(None, u'STEP_INDEX')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_37._UseForTag(pyxb.namespace.ExpandedName(None, u'PREV_STEP_INDEX')), min_occurs=1L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_37._UseForTag(pyxb.namespace.ExpandedName(None, u'PROGRAM')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_37._UseForTag(pyxb.namespace.ExpandedName(None, u'VERSION')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_37._UseForTag(pyxb.namespace.ExpandedName(None, u'NOTES')), min_occurs=0L, max_occurs=1L)
    )
CTD_ANON_37._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_37._GroupModel, min_occurs=1, max_occurs=1)



PlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'COMPLETE_GENOMICS'), CTD_ANON_27, scope=PlatformType, documentation=u'\n                            Placeholder for CompleteGenomics platform type.   At present there is no instrument model.\n                        '))

PlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PACBIO_SMRT'), CTD_ANON_23, scope=PlatformType, documentation=u'\n                            Placeholder for PacificBiosciences platform type.   At present there is no instrument model.\n                        '))

PlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ILLUMINA'), CTD_ANON_, scope=PlatformType, documentation=u'\n                            Illumina is 4-channel flowgram with 1-to-1 mapping between basecalls and flows\n                        '))

PlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ABI_SOLID'), CTD_ANON_33, scope=PlatformType, documentation=u'\n                            ABI is 4-channel flowgram with 1-to-1 mapping between basecalls and flows\n                        '))

PlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'HELICOS'), CTD_ANON_41, scope=PlatformType, documentation=u'\n                            Helicos is similar to 454 technology - uses 1-color sequential flows   \n                        '))

PlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ION_TORRENT'), CTD_ANON_32, scope=PlatformType, documentation=u'\n                    '))

PlatformType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LS454'), CTD_ANON_10, scope=PlatformType, documentation=u'\n                            454 technology use 1-color sequential flows \n                        '))
PlatformType._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, u'LS454')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, u'ILLUMINA')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, u'HELICOS')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, u'ABI_SOLID')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, u'COMPLETE_GENOMICS')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, u'PACBIO_SMRT')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(PlatformType._UseForTag(pyxb.namespace.ExpandedName(None, u'ION_TORRENT')), min_occurs=1, max_occurs=1)
    )
PlatformType._ContentModel = pyxb.binding.content.ParticleModel(PlatformType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_39._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DB'), pyxb.binding.datatypes.string, scope=CTD_ANON_39, documentation=u'\n                                EBI ENA controlled vocabulary of permitted\n                                cross references.\n                            '))

CTD_ANON_39._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LABEL'), pyxb.binding.datatypes.string, scope=CTD_ANON_39, documentation=u'A textual description of the cross-reference.\n                            '))

CTD_ANON_39._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'URL'), pyxb.binding.datatypes.anyURI, scope=CTD_ANON_39, documentation=u'An URL to the cross-references accession.\n                            '))

CTD_ANON_39._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ID'), pyxb.binding.datatypes.string, scope=CTD_ANON_39, documentation=u' Accession in the referenced\n                                database.'))
CTD_ANON_39._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_39._UseForTag(pyxb.namespace.ExpandedName(None, u'DB')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_39._UseForTag(pyxb.namespace.ExpandedName(None, u'ID')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_39._UseForTag(pyxb.namespace.ExpandedName(None, u'URL')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_39._UseForTag(pyxb.namespace.ExpandedName(None, u'LABEL')), min_occurs=0L, max_occurs=1L)
    )
CTD_ANON_39._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_39._GroupModel, min_occurs=1, max_occurs=1)



ReferenceSequenceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SEQUENCE'), CTD_ANON_21, scope=ReferenceSequenceType, documentation=u'Reference sequence details.'))

ReferenceSequenceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ASSEMBLY'), ReferenceAssemblyType, scope=ReferenceSequenceType, documentation=u'Reference assembly details.'))
ReferenceSequenceType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ReferenceSequenceType._UseForTag(pyxb.namespace.ExpandedName(None, u'ASSEMBLY')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ReferenceSequenceType._UseForTag(pyxb.namespace.ExpandedName(None, u'SEQUENCE')), min_occurs=0L, max_occurs=None)
    )
ReferenceSequenceType._ContentModel = pyxb.binding.content.ParticleModel(ReferenceSequenceType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_41._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'FLOW_SEQUENCE'), pyxb.binding.datatypes.string, scope=CTD_ANON_41, documentation=u'\n                                        The fixed sequence of challenge bases that flow across the flowcell. \n                                        This is optional in the schema now but will be required by business rules and future schema versions.\n                                    '))

CTD_ANON_41._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'FLOW_COUNT'), pyxb.binding.datatypes.positiveInteger, scope=CTD_ANON_41, documentation=u'\n                                        The number of flows of challenge bases.  This is a constraint on maximum read length, but not equivalent. \n                                        This is optional in the schema now but will be required by business rules and future schema versions.\n                                    '))

CTD_ANON_41._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL'), STD_ANON_3, scope=CTD_ANON_41))
CTD_ANON_41._GroupModel = pyxb.binding.content.GroupAll(
    pyxb.binding.content.ParticleModel(CTD_ANON_41._UseForTag(pyxb.namespace.ExpandedName(None, u'INSTRUMENT_MODEL')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_41._UseForTag(pyxb.namespace.ExpandedName(None, u'FLOW_SEQUENCE')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(CTD_ANON_41._UseForTag(pyxb.namespace.ExpandedName(None, u'FLOW_COUNT')), min_occurs=0L, max_occurs=1L)
    )
CTD_ANON_41._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_41._GroupModel, min_occurs=1, max_occurs=1)
