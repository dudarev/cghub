/* Copyright (c) 2007 Lev Muchnik <LevMuchnik@gmail.com>. All rights reserved.
 * You may copy and modify this script as long as the above copyright notice,
 * this condition and the following disclaimer is left intact.
 * This software is provided by the author "AS IS" and no warranties are
 * implied, including fitness for a particular purpose. In no event shall
 * the author be liable for any damages arising in any way out of the use
 * of this software, even if advised of the possibility of such damage.
 * $Date: 2007-10-03 19:08:15 -0700 (Wed, 03 Oct 2007) $
 * 
 * 2013.09.19 Modified by 42cc.
 */

function LoadXML(ParentElementID,URL) {
    var xmlHolderElement = GetParentElement(ParentElementID);
    if (xmlHolderElement==null) { return false; }
    ToggleElementVisibility(xmlHolderElement);
    return RequestURL(URL, URLReceiveCallback, ParentElementID);
}

function LoadXMLDom(ParentElementID,xmlDoc) {
    if (xmlDoc) {
        var xmlHolderElement = GetParentElement(ParentElementID);
        if (xmlHolderElement==null) { return false; }
        while (xmlHolderElement.childNodes.length) { xmlHolderElement.removeChild(xmlHolderElement.childNodes.item(xmlHolderElement.childNodes.length-1));	}
        var Result = ShowXML(xmlHolderElement,xmlDoc.documentElement,0);
        return Result;
    }
    else { return false; }
}

function LoadXMLString(ParentElementID,XMLString) {
    xmlDoc = CreateXMLDOM(XMLString);
    LoadXMLDom(ParentElementID,xmlDoc) ;
    /* open first root by default */
}
////////////////////////////////////////////////////////////
// HELPER FUNCTIONS - SHOULD NOT BE DIRECTLY CALLED BY USERS
////////////////////////////////////////////////////////////
function GetParentElement(ParentElementID) {
    if (typeof(ParentElementID)=='string') {	return document.getElementById(ParentElementID);	}
    else if (typeof(ParentElementID)=='object') { return ParentElementID;} 
    else { return null; }
}

/**
 * @return {boolean}
 */
function URLReceiveCallback(httpRequest, xmlHolderElement) {
    try {
        if (httpRequest.readyState == 4) {
            if (httpRequest.status == 200) {
                var xmlDoc = httpRequest.responseXML;
                if (xmlHolderElement && xmlHolderElement!=null) {
                    xmlHolderElement.innerHTML = '';
                    return LoadXMLDom(xmlHolderElement,xmlDoc);
                }
            } else {
                return false;
            }
        }
    }
    catch( e ) { return false; }	
}

/**
 * @return {boolean}
 */
function RequestURL(url,callback,ExtraData) { // based on: http://developer.mozilla.org/en/docs/AJAX:Getting_Started
    var httpRequest;
    if (window.XMLHttpRequest) { // Mozilla, Safari, ...
        httpRequest = new XMLHttpRequest();
        if (httpRequest.overrideMimeType) { httpRequest.overrideMimeType('text/xml'); }
    }
    else if (window.ActiveXObject) { // IE
        try {
            httpRequest = new ActiveXObject("Msxml2.XMLHTTP");
        }
        catch (e) {
            try { httpRequest = new ActiveXObject("Microsoft.XMLHTTP"); }
            catch (e) {}
        }
    }
    if (!httpRequest) {
        return false;
    }
    httpRequest.onreadystatechange = function() { callback(httpRequest,ExtraData); };
    httpRequest.open('GET', url, true);
    httpRequest.send('');
    return true;
}

function CreateXMLDOM(XMLStr) {
    if (window.ActiveXObject) {
        xmlDoc=new ActiveXObject("Microsoft.XMLDOM"); 
        xmlDoc.loadXML(XMLStr);	
        return xmlDoc;
    }
    else if (document.implementation && document.implementation.createDocument)	  {
        var parser=new DOMParser();
        return parser.parseFromString(XMLStr,"text/xml");
    }
    else { return null; }
}

var IDCounter = 1;
var NestingIndent = 15;

/**
 * @return {boolean}
 */
function ShowXML(xmlHolderElement, RootNode, indent) {
    if (RootNode==null || xmlHolderElement==null) { return false; }
    var Result  = true;
    var TagEmptyElement = document.createElement('div');
    TagEmptyElement.className = 'Element';
    TagEmptyElement.style.position = 'relative';
    TagEmptyElement.style.left = NestingIndent+'px';

    var TagElement = document.createElement('div');
    TagElement.className = 'Element';
    TagElement.style.position = 'relative';
    TagElement.style.left = NestingIndent+'px';

    // empty tag: <some_empty_tag />
    if (RootNode.childNodes.length==0) {
        AddNodeNameWithAttributes(TagEmptyElement, RootNode);
        CloseElement(TagEmptyElement,' />');
        xmlHolderElement.appendChild(TagEmptyElement);
    }
    // only text inside: <tag_with_text>Here is text</tag_with_text>
    else if (RootNode.childNodes.length==1 && RootNode.childNodes.item(0).nodeName == '#text'){
        AddNodeNameWithAttributes(TagElement, RootNode);
        CloseElement(TagElement, '>') ;
        var NodeText = RootNode.childNodes.item(i).nodeValue;
        if (NodeText) {
            AddTextNode(TagElement, NodeText, 'NodeValue') ;
        }
        AddClosingElement(TagElement, RootNode.nodeName);
        xmlHolderElement.appendChild(TagElement);
    }
    // nodes with children
    else {
        AddClickablePlus (TagEmptyElement, IDCounter);
        AddNodeNameWithAttributes(TagEmptyElement, RootNode);
        CloseElement(TagEmptyElement,'>');
        AddClosingElement(TagEmptyElement, RootNode.nodeName);
        xmlHolderElement.appendChild(TagEmptyElement);
        SetVisibility(TagEmptyElement,false);
        //----------------------------------------------

        AddClickableMinus(TagElement, IDCounter);
        ++IDCounter;

        AddNodeNameWithAttributes(TagElement, RootNode);
        CloseElement(TagElement, '>') ;

        TagElement.appendChild(document.createElement('br'));
        NodeText = null;
        for (var i = 0; RootNode.childNodes && i < RootNode.childNodes.length; ++i) {
            if (RootNode.childNodes.item(i).nodeName != '#text') {
            Result &= ShowXML(TagElement, RootNode.childNodes.item(i), indent+1);
            } else {
                NodeText = RootNode.childNodes.item(i).nodeValue;
            }
        }
        if (RootNode.nodeValue) {
            NodeText = RootNode.nodeValue;
        }
        if (NodeText) {
            AddTextInDiv(TagElement, NodeText);
        }
        AddClosingElement(TagElement, RootNode.nodeName) ;
        xmlHolderElement.appendChild(TagElement);
    }
    // if (indent==0) { ToggleElementVisibility(TagElement.childNodes(0)); } - uncomment to collapse the external element
    return Result;
}

function CloseElement (element, closing) {
    AddTextNode(element, closing);
}

function AddClosingElement (element, nodeName) {
    AddTextNode(element, ' </', 'Utility') ;
    AddTextNode(element, nodeName, 'NodeName') ;
    AddTextNode(element, '>', 'Utility') ;
}

function AddNodeNameWithAttributes(TagEmptyElement, RootNode) {
    AddTextNode(TagEmptyElement,'<','Utility') ;
    AddTextNode(TagEmptyElement,RootNode.nodeName ,'NodeName')
    for (var i = 0; RootNode.attributes && i < RootNode.attributes.length; ++i) {
        var CurrentAttribute  = RootNode.attributes.item(i);
        AddTextNode(TagEmptyElement,' ' + CurrentAttribute.nodeName ,'AttributeName') ;
        AddTextNode(TagEmptyElement,'=','Utility') ;
        AddTextNode(TagEmptyElement,'"' + CurrentAttribute.nodeValue + '"','AttributeValue') ;
    }
}

function AddClickablePlus (element, counter) {
    var ClickableElement = AddTextNode(element,'','Clickable element-expand') ;
    ClickableElement.onclick  = function() {ToggleElementVisibility(this); }
    ClickableElement.id = 'div_empty_' + counter;
    var ClickableElementAll = AddTextNode(element,'','Clickable element-expand-all') ;
    ClickableElementAll.onclick  = function() {
        ClickableElement.click();
        ToggleSubElements(ClickableElement, true);
    }
}

function AddClickableMinus (element, counter) {
    var ClickableElement = AddTextNode(element,'','Clickable element-collapse') ;
    ClickableElement.onclick  = function() {ToggleElementVisibility(this); }
    ClickableElement.id = 'div_content_' + counter;
    var ClickableElementAll = AddTextNode(element,'','Clickable element-collapse-all') ;
    ClickableElementAll.onclick  = function() {
        ClickableElement.click();
        ToggleSubElements(ClickableElement, false);
    }
}

function ToggleSubElements(el, show) {
    if (!el|| !el.id) { return; }
    try {
        ElementID = parseInt(el.id.slice(el.id.lastIndexOf('_')+1));
    }
    catch(e) { return ; }
    var ElementToShow = '';
    ElementToShow = 'div_content_' + ElementID;
    ElementToShow = CompatibleGetElementByID(ElementToShow);
    var arr = ElementToShow.parentNode.getElementsByClassName('Clickable');
    var length = arr.length,
        element = null;
    for (var i = 0; i < length; i++) {
        element = arr[i];
        if(show) {
            if(element.className.indexOf('element-expand') != -1 && element.className.indexOf('element-expand-all') == -1 && element.style['display'] != 'none'){
                element.click();
            }
        } else {
            if(element.className.indexOf('element-collapse') != -1 && element.className.indexOf('element-collapse-all') == -1 && element.style['display'] != 'none'){
                element.click();
            }
        }
    }
}

function AddTextInDiv(element, text) {
    var ContentElement = document.createElement('div');
    ContentElement.style.position = 'relative';
    ContentElement.style.left = NestingIndent+'px';
    AddTextNode(ContentElement, text, 'NodeValue') ;
    element.appendChild(ContentElement);
}

function AddTextNode(ParentNode,Text,Class) {
    NewNode = document.createElement('span');
    if (Class) {  NewNode.className  = Class;}
    if (Text) { NewNode.appendChild(document.createTextNode(Text)); }
    if (ParentNode) { ParentNode.appendChild(NewNode); }
    return NewNode;		
}

function CompatibleGetElementByID(id) {
    if (!id) { return null; }
    if (document.getElementById) { // DOM3 = IE5, NS6
        return document.getElementById(id);
    } else {
        if (document.layers) { // Netscape 4
            return document.id;
        } else { // IE 4
            return document.all.id;
        }
    }
}

function SetVisibility(HTMLElement,Visible) {
    if (!HTMLElement) { return; }
    var VisibilityStr  = (Visible) ? 'block' : 'none';
    if (document.getElementById) { // DOM3 = IE5, NS6
        HTMLElement.style.display = VisibilityStr;
    } else {
        if (document.layers) { // Netscape 4
            HTMLElement.display = VisibilityStr; 
        } else { // IE 4
            HTMLElement.id.style.display = VisibilityStr; 
        }
    }
}

function ToggleElementVisibility(Element) {
    if (!Element|| !Element.id) { return; }
    try {
        ElementType = Element.id.slice(0,Element.id.lastIndexOf('_')+1);
        ElementID = parseInt(Element.id.slice(Element.id.lastIndexOf('_')+1));
    }
    catch(e) { return ; }
    var ElementToHide = null;
    var ElementToShow= null;
    if (ElementType=='div_content_') {
        ElementToHide = 'div_content_' + ElementID;
        ElementToShow = 'div_empty_' + ElementID;
    }
    else if (ElementType=='div_empty_') {
        ElementToShow = 'div_content_' + ElementID;
        ElementToHide  = 'div_empty_' + ElementID;
    }
    ElementToHide = CompatibleGetElementByID(ElementToHide);
    ElementToShow = CompatibleGetElementByID(ElementToShow);
    if (ElementToHide) { ElementToHide = ElementToHide.parentNode;}
    if (ElementToShow) { ElementToShow = ElementToShow.parentNode;}
    SetVisibility(ElementToHide,false);
    SetVisibility(ElementToShow,true);
}
