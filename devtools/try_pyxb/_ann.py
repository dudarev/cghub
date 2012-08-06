# ./_ann.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:f8f801bd79b284bc0391ad8b0b1d66831991e951
# Generated 2012-08-06 22:21:52.436963 by PyXB version 1.1.5-DEV
# Namespace SRA.annotation [xmlns:ann]

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
import common

Namespace = pyxb.namespace.NamespaceForURI(u'SRA.annotation', create_if_missing=True)
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
class useType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'useType')
    _Documentation = None
useType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=useType, enum_prefix=None)
useType.Optional = useType._CF_enumeration.addEnumeration(unicode_value=u'Optional', tag=u'Optional')
useType.Required = useType._CF_enumeration.addEnumeration(unicode_value=u'Required', tag=u'Required')
useType.Prohibited = useType._CF_enumeration.addEnumeration(unicode_value=u'Prohibited', tag=u'Prohibited')
useType._InitializeFacetMap(useType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'useType', useType)

# Atomic SimpleTypeDefinition
class scopeType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'scopeType')
    _Documentation = None
scopeType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=scopeType, enum_prefix=None)
scopeType.INSDC = scopeType._CF_enumeration.addEnumeration(unicode_value=u'INSDC', tag=u'INSDC')
scopeType.INSDCNCBI = scopeType._CF_enumeration.addEnumeration(unicode_value=u'INSDC/NCBI', tag=u'INSDCNCBI')
scopeType.INSDCEBI = scopeType._CF_enumeration.addEnumeration(unicode_value=u'INSDC/EBI', tag=u'INSDCEBI')
scopeType.INSDCDDBJ = scopeType._CF_enumeration.addEnumeration(unicode_value=u'INSDC/DDBJ', tag=u'INSDCDDBJ')
scopeType.non_INSDC = scopeType._CF_enumeration.addEnumeration(unicode_value=u'non-INSDC', tag=u'non_INSDC')
scopeType._InitializeFacetMap(scopeType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'scopeType', scopeType)

# Atomic SimpleTypeDefinition
class statusType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'statusType')
    _Documentation = None
statusType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=statusType, enum_prefix=None)
statusType.Active = statusType._CF_enumeration.addEnumeration(unicode_value=u'Active', tag=u'Active')
statusType.Active_ = statusType._CF_enumeration.addEnumeration(unicode_value=u'Active', tag=u'Active_')
statusType.Deprecated = statusType._CF_enumeration.addEnumeration(unicode_value=u'Deprecated', tag=u'Deprecated')
statusType.Not_Implemented = statusType._CF_enumeration.addEnumeration(unicode_value=u'Not Implemented', tag=u'Not_Implemented')
statusType._InitializeFacetMap(statusType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'statusType', statusType)

# Complex type CTD_ANON with content type EMPTY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute current uses Python identifier current
    __current = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'current'), 'current', '__SRA_annotation_CTD_ANON_current', useType)
    
    current = property(__current.value, __current.set, None, None)

    
    # Attribute future uses Python identifier future
    __future = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'future'), 'future', '__SRA_annotation_CTD_ANON_future', useType)
    
    future = property(__future.value, __future.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __current.name() : __current,
        __future.name() : __future
    }



# Complex type CTD_ANON_ with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Term uses Python identifier Term
    __Term = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Term'), 'Term', '__SRA_annotation_CTD_ANON__Term', True)

    
    Term = property(__Term.value, __Term.set, None, None)


    _ElementMap = {
        __Term.name() : __Term
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
    
    # Element Rule uses Python identifier Rule
    __Rule = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Rule'), 'Rule', '__SRA_annotation_CTD_ANON_2_Rule', True)

    
    Rule = property(__Rule.value, __Rule.set, None, None)


    _ElementMap = {
        __Rule.name() : __Rule
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
    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'version'), 'version', '__SRA_annotation_CTD_ANON_3_version', pyxb.binding.datatypes.string)
    
    version = property(__version.value, __version.set, None, None)

    
    # Attribute date uses Python identifier date
    __date = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'date'), 'date', '__SRA_annotation_CTD_ANON_3_date', pyxb.binding.datatypes.date)
    
    date = property(__date.value, __date.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __version.name() : __version,
        __date.name() : __date
    }



# Complex type CTD_ANON_4 with content type EMPTY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute xpath uses Python identifier xpath
    __xpath = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'xpath'), 'xpath', '__SRA_annotation_CTD_ANON_4_xpath', pyxb.binding.datatypes.string)
    
    xpath = property(__xpath.value, __xpath.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __xpath.name() : __xpath
    }



Use = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Use'), CTD_ANON)
Namespace.addCategoryObject('elementBinding', Use.name().localName(), Use)

Glossary = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Glossary'), CTD_ANON_)
Namespace.addCategoryObject('elementBinding', Glossary.name().localName(), Glossary)

BusinessRules = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'BusinessRules'), CTD_ANON_2)
Namespace.addCategoryObject('elementBinding', BusinessRules.name().localName(), BusinessRules)

ActiveSince = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ActiveSince'), CTD_ANON_3)
Namespace.addCategoryObject('elementBinding', ActiveSince.name().localName(), ActiveSince)

Alternative = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Alternative'), CTD_ANON_4)
Namespace.addCategoryObject('elementBinding', Alternative.name().localName(), Alternative)

DocumentationLinks = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'DocumentationLinks'), common.LinkType)
Namespace.addCategoryObject('elementBinding', DocumentationLinks.name().localName(), DocumentationLinks)

Scope = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Scope'), scopeType)
Namespace.addCategoryObject('elementBinding', Scope.name().localName(), Scope)

Status = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Status'), statusType)
Namespace.addCategoryObject('elementBinding', Status.name().localName(), Status)



CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Term'), pyxb.binding.datatypes.string, scope=CTD_ANON_))
CTD_ANON_._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, u'Term')), min_occurs=1, max_occurs=None)
    )
CTD_ANON_._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_._GroupModel, min_occurs=1, max_occurs=1L)



CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Rule'), pyxb.binding.datatypes.string, scope=CTD_ANON_2))
CTD_ANON_2._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, u'Rule')), min_occurs=1, max_occurs=None)
    )
CTD_ANON_2._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_2._GroupModel, min_occurs=1L, max_occurs=1L)
