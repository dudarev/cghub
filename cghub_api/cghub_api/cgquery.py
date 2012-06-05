#!/usr/bin/env python

"""
    cgquery

    Simple client to send a query to the cghub server and parse the 
    resulting XML.    Optionally, the raw XML can be stored to an
    output file for processing by the GeneTorrent client.

    Revision History:
        6-Jan-2012 v1.9:      Version 1 software
       26-Feb-2012 v2.1.0:    Added URL encoding of query strings and 
                              parsing for new cghub error XML.  
                              Cleaned up any backwared-incompatible
                              syntax (through 2.1.1), so we can 
                              exit nicely with older interpreters.
                                

    When adding an entry to the revision history, be sure to update 
    the CGQUERY_VER value below.

"""

"""
TODO:
	- Python version check?
    - Interpret XML error contents?
"""

CGQUERY_VER = '2.1.0'

#
# Check the python version for compatability.  Python 3 is not
# backward compatible.   Need to get sys to check the version.
# But, delay the remaining imports because we'd rather spit
# out a version error than an import error if using an old
# interpreter that doesn't have the necessary modules.
#
try:
    import os
    import sys
except:
    # Nothing we can do here
    print "Unable to verify Python version"
    raise

if sys.version_info[0] != 2 or sys.version_info[1] < 6:
    print "%s requires Python version 2.6 or 2.7" % os.path.basename(sys.argv[0])
    sys.exit(1)

#
# Now get the rest of our required modules
#
try:
    import urllib
    import urllib2
    import datetime
    import re
    import optparse 
    import traceback 
    from optparse import OptionParser
    from xml.dom import minidom, Node
    from collections import defaultdict
    from subprocess import call
    from cStringIO import StringIO
except Exception, (err):
    print "Can't find required Python module (%s)" % (err)
    sys.exit(1)

#
# Check that SSL support is available for the https requests.
#
try:
    import _ssl
except ImportError:
    print "Python must be compiled with SSL support to use https"
    sys.exit(1)

DEBUG = 0

#
# Constants for contacting the CGHub server.  
#
CGHUB_SVR  = 'https://cghub.ucsc.edu'
CGHUB_ANAL_OBJECT_URI = '/cghub/metadata/analysisObject'
CGHUB_ANAL_ATTR_URI = '/cghub/metadata/analysisAttributes'

#
# Location of the GeneTorrent binary and conf file for interactive mode
#
GT_BIN        = '/usr/bin/GeneTorrent' 

#
# Column width (up to the :)
#
C_WIDTH =      32   

global Log 

#
# Utility lambda functions
#
lowerStr = lambda s: s and s[:1].lower() + s[1:] or ''
upperStr = lambda s: s and s[:1].upper() + s[1:] or ''


#
# Other utility functions
#
def columnize(str, indent, colwidth):
    """ -----------------------------------------------------------------
        Given a string, attempt to break it into a column with the 
        passed indent and column width.  Note that the first line will 
        not be indented.   This is similar to the textwrap module, but 
        customized to work better with our formatting style.
        -----------------------------------------------------------------
    """

    idx = 0
    wsidx = -1
    width = 0

    while True:
        #
        # Are we at the end of the string?
        #
        if idx >= len(str):
            break

        if str[idx] == '\n':
            # 
            # Respect any newlines we find by just forcing a
            # line break
            #
            wsidx = idx
            width = colwidth 
        elif str[idx] == ' ':
            #
            # Keep track of the last space we saw as we may
            # need to use that location as our line break
            #
            wsidx = idx;

        idx = idx+1
        width = width+1

        if (width >= colwidth):
            #
            # Okay, we've exceeded the column width.  Go back
            # to the last whitespace and insert a newline
            # followed by the proper indentation, and repeat.
            #
            if wsidx > 0:
                str = str[:wsidx] + "\n" + " " * indent + str[wsidx+1:]
                idx = idx + indent
                wsidx = -1
                width = 0
    return str

class Logger:
    """ =================================================================
        Logger
        
        Logging object used to output various messages, warnings and 
        errors in a consistent format. 
        =================================================================
    """
    def __init__(self):
        """ -----------------------------------------------------------------
            Constructor
            -----------------------------------------------------------------
        """
        self.verbose = False
        self.errorstats = defaultdict(int)

    def setVerbose(self, verbose):
        """ -----------------------------------------------------------------
            Set verbose mode
            -----------------------------------------------------------------
        """
        self.verbose = verbose

    def Verbose(self):
        """ -----------------------------------------------------------------
            Get verbose mode value
            -----------------------------------------------------------------
        """
        return self.verbose 

    def debug(self, msg):
        if DEBUG:  
            sys.stderr.write("{0} Debug: {1}.\n".format(datetime.datetime.now(), msg) )

    def status(self, msg):
        """ -----------------------------------------------------------------
            Print a status message to the terminal.  These are intended
            to be temporary messages that get erased, so should not
            have a trailing newline.
            -----------------------------------------------------------------
        """

        if not sys.stdout.isatty():
            return 0
        msglen = len(msg)
        sys.stdout.write(msg)
        sys.stdout.flush()
        return msglen

    def clearStatus(self, msglen):
        """ -----------------------------------------------------------------
            Clear a status message.   msglen is the value returned by
            self.status() above.
            -----------------------------------------------------------------
        """

        if sys.stdout.isatty():
            sys.stdout.write('\r' + msglen * ' ' + '\r')
            sys.stdout.flush()

    def messageV(self, msg):
        """ -----------------------------------------------------------------
            Print a message in verbose mode
            -----------------------------------------------------------------
        """
        if self.verbose:
            print msg

    def warningV(self, msg):
        """ -----------------------------------------------------------------
            Report a warning in verbose mode
            -----------------------------------------------------------------
        """
        if self.verbose:
            sys.stderr.write("++ Warning: {0}.\n".format(msg) )

    def notice(self, msg):
        """ -----------------------------------------------------------------
            Report a generic notice
            -----------------------------------------------------------------
        """
        sys.stderr.write("## NOTICE: {0}.\n".format(msg) )

    def error(self, type_str, err):
        """ -----------------------------------------------------------------
            Report a generic error 
            -----------------------------------------------------------------
        """
        sys.stderr.write("## {0}: {1}.\n".format(type_str, err) )

    def execError(self, err):
        """ -----------------------------------------------------------------
            Report a non-fatal execution error 
            -----------------------------------------------------------------
        """
        err_msg = "{0}.  Continuing" . format(err)
        sys.stderr.write("\n")
        self.error("Error", err_msg)
        sys.stderr.write("\n")

    def fatalError(self):
        """ -----------------------------------------------------------------
            Silently exit with an error status
            -----------------------------------------------------------------
        """
        sys.exit(1)

    def fatalExecError(self, err, doExit=True):
        """ -----------------------------------------------------------------
            Report a fatal execution error to stderr and exit
            -----------------------------------------------------------------
        """
        sys.stderr.write("\n")
        self.error("Error", err)
        sys.stderr.write("\n")
        if (doExit):
            sys.exit(1)

    def fatalOptError(self, parser, err):
        """ -----------------------------------------------------------------
            Report a fatal option parsing error to stderr and exit
            -----------------------------------------------------------------
        """
        sys.stderr.write("\nError: %s.\n\n" % (err))
        parser.print_help()
        sys.exit(1)

    def parseWarning(self, msg):
        """ -----------------------------------------------------------------
            Dump out an XML parsing error and increment the error
            count for use in the summary stats.
            -----------------------------------------------------------------
        """
        self.errorstats["warnings"] += 1
        self.warningV(msg)

    def parseError(self, msg):
        """ -----------------------------------------------------------------
            Dump out an XML parsing error and increment the error
            count for use in the summary stats.
            -----------------------------------------------------------------
        """
        self.errorstats["errors"] += 1
        self.error("Parse Error", msg)

    def getParseWarningCount(self):
        """ -----------------------------------------------------------------
            Return the warning count
            -----------------------------------------------------------------
        """
        return self.errorstats["warnings"]

    def getParseErrorCount(self):
        """ -----------------------------------------------------------------
            Return the error count
            -----------------------------------------------------------------
        """
        return self.errorstats["errors"]

class QueryString:
    """ =================================================================
        QueryString
        
        Object to manage raw and encoded querystrings.
        =================================================================
    """

    def __init__(self, rawqs):
        """ -----------------------------------------------------------------
            Given a raw (unencoded) string, instantiate a QueryString 
            object that can return either the raw or encoded value.
            Raises an exception if the raw value can not be encoded.
            -----------------------------------------------------------------
        """

        self.encodedqs = ''

        if not rawqs:
            raise ValueError("Non-existent querystring")
        self.rawqs = rawqs

        qsdict = dict()

        #
        # Split the raw querystring into individual parameters
        #
        for item in self.rawqs.split("&"):
            if not item:
                continue
            #
            # Now extract the actual field/value pair and insert
            # them into the dictionary
            #
            field,value = '',''
            fvp = item.split("=")

            if len(fvp) > 0:
                field=fvp[0]
            if len(fvp) > 1:
                value=fvp[1]
            if len(fvp) > 2:
                raise ValueError("Invalid field=value pair at %s" % item)

            qsdict[field] = value

            #
            # Now do the encoding.   Let any encoding errors get
            # thrown.
            #
            self.encodedqs=urllib.urlencode(qsdict)

    def Raw(self):
        """ -----------------------------------------------------------------
            Return a raw (unencoded) version of the QueryString
            -----------------------------------------------------------------
        """
        return self.rawqs

    def Encoded(self):
        """ -----------------------------------------------------------------
            Return an encoded version of the QueryString
            -----------------------------------------------------------------
        """
        return self.encodedqs

class XMLLogFile:
    """ =================================================================
        XMLLogFile
        
        Manage the output file used to log any XML return data
        =================================================================
    """
    def __init__(self, logfile):
        """ -----------------------------------------------------------------
            Requires a filename.  The file will not be opened until the
            first write.
            -----------------------------------------------------------------
        """
        #
        # Make sure we got a file name
        #
        if logfile == None:
            raise ValueError("XML output file name not set")
        self.xmlfh = None
        self.xmlfilename = logfile

    def Write(self, buffer):
        """ -----------------------------------------------------------------
            Write a buffer to the output file.   Open the file if this
            is the first write.
            -----------------------------------------------------------------
        """
        #
        # Is it open yet?  If not, open it
        #
        if self.xmlfh == None:
            try:
                self.xmlfh = open(self.xmlfilename, 'w')
            except IOError, (err):
                Log.fatalExecError("Failed to open output file (%s)" % err)

        #
        # Now write the data
        #
        try: 
            self.xmlfh.write(buffer)
        except IOError, (err):
            Log.fatalExecError("Failed to write to output file (%s)" % err)

    def Close(self):
        """ -----------------------------------------------------------------
            Close the output file if it's been opened.
            -----------------------------------------------------------------
        """
        if self.xmlfh != None:
            self.xmlfh.close()
            self.xmlfl = None

class ResultStream:
    """ =================================================================
        ResultStream
        
        Streams the XML output in response to a query.  The actual XML 
        is read from the server in large chunks that get parsed and
        handed back to the caller one Result at a time.
        =================================================================
    """

    def __init__(self, xmlstream, size, logfile):
        """ -----------------------------------------------------------------
            Initialize the instance variables.  
                buffer : a raw chunk of XML that's been read from the 
                    server.   As requests are made to get additional 
                    Results the beginning of the chunk "slides"
                    forward, and the end grows as needed.   
                chunksize : the size of the individual reads.   
                stream : the file handle for the response 
                xmlfh : the file handle for the raw xml logfile (opt)
            -----------------------------------------------------------------
        """
        self.buffer = None
        if size <= 100000:
            self.chunksize = size
        else:
            self.chunksize = 100000
        self.stream = xmlstream
        self.logfile = logfile

    def Grow(self):
        """ -----------------------------------------------------------------
            Expand the buffer by another chunk.  This might be needed to
            get the next Result, or to find the end of the curren one.
            -----------------------------------------------------------------
        """
        
        #
        # Read another chunk
        #
        b2 = self.stream.read(self.chunksize)
        if not b2: 
            return False

        #
        # Log it (if needed)
        #
        if self.logfile != None:
            self.logfile.Write(b2)

        #
        # And append it to the existing buffer so the caller can just
        # keep scanning through the buffer
        #
        if self.buffer != None:
            self.buffer = self.buffer+b2
        else:
            self.buffer = b2
        return True

    def Close(self):
        """ -----------------------------------------------------------------
            Perform any house keeping
            -----------------------------------------------------------------
        """
        pass
        
    def FindNode(self, node):
        """ -----------------------------------------------------------------
            Locate an XML key (in the form "Key" or "/Key") and return its
            offset (from the beginning of the buffer) and length (up to 
            the closing bracket).
            -----------------------------------------------------------------
        """
        node = "<" + node
        ofs = len(node)

        #
        # Start searching at our current location
        #
        start = 0

        while True:
            loc = self.buffer[start:].find(node)

            if loc == -1:
                #
                # Not found in the buffer.   Get some more data
                # and try again.
                #
                if not self.Grow():
                    return (-1,-1)
                continue
            
            end = start + loc + ofs

            if end > len(self.buffer):
                #
                # The key name spans across a chunk boundary.
                # Get more data and try again
                #
                if not self.Grow():
                    return (-1,-1)
                continue

            if self.buffer[end:][:1] != " " and self.buffer[end:][:1] != '>':
                #
                # Probably found a key that's a superset of the key
                # we want.   Keep looking
                #
                start = end
                continue

            #
            # Found our node.   Find the closing bracket
            #
            loc2 = self.buffer[start+loc:].find(">")
            if loc2 == -1:
                #
                # The key spans across a chunk boundary.  Get more
                # data and try again.
                #
                if not self.Grow():
                    return (-1,-1)
                continue

            return (loc,loc2+1)

    def getResultSetXML(self):
        """ -----------------------------------------------------------------
            Returns the XML ResultSet, which is assumed to be the first 
            thing returned by the query. 
            -----------------------------------------------------------------
        """
        #
        # The ResultSet must get loaded before any of the
        # Results
        #
        if self.buffer != None:
            Log.fatalExecError("ResultSet loaded twice")

        #
        # Even if there are no results, we should get
        # something in response to the query.  So, get our
        # first chunk.
        #
        if not self.Grow():
            Log.fatalExecError("Failed to parse ResultSet.  Unexpected response format")

        #
        # Find the beginning of the ResultSet
        #
        rsstart,rslen = self.FindNode('ResultSet')
        if rsstart == -1:
            Log.fatalExecError("ResultSet not found")

        #
        # Find the start of the Hits node
        #
        hitstart,hitlen = self.FindNode('/Hits')
        if hitstart == -1:
            Log.fatalExecError("Hit count not found in ResultSet")

        if hitstart <= rsstart:
            Log.fatalExecError("Hit count found outside of ResultSet")

        #
        # Save the ResultSet and terminate it so that we can 
        # load it into a dom
        #
        rsbuffer = self.buffer[rsstart:hitstart+hitlen]
        rsbuffer += "</ResultSet>"

        #
        # Advance the window
        #
        self.buffer = self.buffer[hitstart+hitlen:]
        
        return rsbuffer

    def getResultXML(self):
        """ -----------------------------------------------------------------
            Return the next Result block found in the stream.
            -----------------------------------------------------------------
        """
        #
        # Find the beginning
        #
        start,len = self.FindNode("Result")
        if start == -1:
            # No more found
            return None

        #
        # Advance the window to the beginning of the block
        #
        self.buffer = self.buffer[start:]

        #
        # From that point, find the end
        #
        start,len = self.FindNode("/Result")
        if start == -1:
            print self.buffer
            Log.fatalExecError("Unterminated Result")

        #
        # Save the block of XML, and advance the window
        # past the block, ready for the next search
        #
        result = self.buffer[:start+len]
        self.buffer = self.buffer[start+len:]

        return result

class CGObject:
    """ =================================================================
        CGObject
        
        Base class for loading raw cghub XML into a dom
        =================================================================
    """

    def __init__(self, rawxml):
        #
        # Load the XML into a dom
        #
        self.dom = None
        self.dom = minidom.parseString(rawxml)

    def __del__(self):
        if self.dom != None:
            self.dom.unlink()

class CGError(CGObject):
    """ =================================================================
        CGError
        
        Manage the CGHUB_error object downloaded from cghub HTTP
        error messages
        =================================================================
    """

    def doTraverse(self, parent, ofs, atRoot=False):
        """ -----------------------------------------------------------------
            Traverse this CGError object, printing the contents to stdout.
            In this case, the 'contents' are any tag names and associated
            text/CDATA nodes that we can find in the XML.   Currently,
            there's no further interpretation of the data.   May want to
            add that later.
            -----------------------------------------------------------------
        """

        rc = False
        if parent == None:
            return rc

        for child in parent.childNodes:
            if child.nodeType == Node.ELEMENT_NODE:
                #
                # We got a child element, print it's tag and traverse it.
                # Note that we don't print a newline after the tag, in 
                # case we find a child text element that we want to
                # print on the same line.
                #

                #
                # If the indentation exceeds the column width, just do
                # our best
                #
                width = C_WIDTH-ofs
                if width < 0:
                    width = 1
                print  "\n" + ofs * " " + "{0:{1}}" . format (child.tagName, width),
                rc = self.doTraverse(child, ofs+20)
            else:
                #
                # We reached a leaf (TEXT or CDATA, in our case), print
                # the contents.
                #
                value = ""
                if child.nodeType == Node.TEXT_NODE:
                    value = child.data.strip()
                elif child.nodeType == Node.CDATA_SECTION_NODE:
                    value = child.wholeText
                if value != "":
                    value = columnize(value, C_WIDTH+3, 76-(C_WIDTH+3))
                    print ": {0}" . format (value),
                    rc = True
        #
        # Print the final trailing newline on our way out
        #
        if atRoot:
            print ""

        return rc

    def PrintDetails(self):
        """ -----------------------------------------------------------------
            Parse the XML error information.  We only know how to parse
            the CGHUB_error element.  Anything else will generate an
            exception.
            -----------------------------------------------------------------
        """

        rootNode = self.dom.getElementsByTagName('CGHUB_error')
        if rootNode.length == 0:
            raise ValueError("Error XML contains unknown format")

        if rootNode.length > 1:
            raise ValueError("Malformed CGHUB_error information")

        anyNodes = self.doTraverse(rootNode[0], 6, True)
        if anyNodes == False:
            raise ValueError("No valid error details found in CGHUB_error")



class ResultSet(CGObject):
    """ =================================================================
        ResultSet
        
        ResultSet object downloaded from cghub.  
        =================================================================
    """

    def __init__(self, rawxml):
        
        try:
            CGObject.__init__(self, rawxml)
        except Exception, err:
            Log.fatalExecError("Error parsing XML (%s)" % err)

    def doTraverse(self):
        """ -----------------------------------------------------------------
            Traverse this ResultSet, printing the contents to stdout.
            In the case of a ResultSet, all we care about is the
            hit count.
            -----------------------------------------------------------------
        """
        #
        # Locate the Hits tag.  Should be one and only one.
        #
        hitSet = self.dom.getElementsByTagName('Hits')
        if hitSet.length != 1:
            Log.parseError("Invalid number of Hits tags ({0})".format(hitSet.length))
            return -1

        if hitSet[0].childNodes.length == 0:
            Log.parseError("Hit count not found in Hits node")
            return -1

        hitCount = hitSet[0].childNodes[0].nodeValue

        ofs=4
        width=C_WIDTH-ofs
        print  ofs * " " + "{0:{1}} : {2}" . format ("Results Returned", width, hitCount)
        print 76 * "="


class Result(CGObject):
    """ =================================================================
        Result
        
        Base Result object downloaded from cghub.   This does the 
        actual work of parsing and printing the result information.
        =================================================================
    """
    
    #
    # Tuple positions for the parser definition fields 
    #
    PR_TAG =        0   # Tag name
    PR_PRINT =      1   # Print tag name when found?
    PR_INDENT =     2   # Indentation level
    PR_HASCHILD =   3   # Has child elements to parse?
    PR_CHILD =      4   # Optional child element parse definition

    def __init__(self, rawxml):
        """ -----------------------------------------------------------------
            Initialize the instance variables
            -----------------------------------------------------------------
        """
        self.uriList = []

        try:
            CGObject.__init__(self, rawxml)
        except Exception, err:
            Log.fatalExecError("Error parsing XML (%s)" % err)

        

    def GetAttrs_default(self, tag, node):
        """ -----------------------------------------------------------------
            Default function to format the attributes for the
            passed XML node.  By default, we don't assume any
            attributes.
            -----------------------------------------------------------------
        """
        return ""

    def GetAttrs_Result(self, tag, node):
        """ -----------------------------------------------------------------
            Parse and format the attributes for the Result 
            element.
            -----------------------------------------------------------------
        """
        return node.getAttribute('id')

    def ElementAttrs(self, tag, node):
        """ -----------------------------------------------------------------
            Parse attributes for the current node.  This is done
            by looking for a function named GetAttrs_<Tag>.  If
            not found, then GetAttrs_default() is called.  See
            GetAttrs_result() for an example of an element-specific 
            function.
            -----------------------------------------------------------------
        """
        return getattr(self, 'GetAttrs_'+tag,self.GetAttrs_default)(tag, node)

    def Action_default(self, tag, node):
        """ -----------------------------------------------------------------
            Default function to perform any element-specific actions
            for the passed XML node.  By default, we assume no action.
            attributes.
            -----------------------------------------------------------------
        """
        pass

    def Action_analysis_data_uri(self, tag, node):
        """ -----------------------------------------------------------------
            Perform analysis_data_uri specific actions.  Specifically, save
            off the analysis URI value for future processing by the
            GeneTorrent client.
            -----------------------------------------------------------------
        """
        self.uriList.append(node.childNodes[0].nodeValue)

    def ElementAction(self, tag, node):
        """ -----------------------------------------------------------------
            Do any element-specific processing for the current tag by 
            looking for a function named Action_<Tag>.  If not found, 
            then Action_default() is called.  See Action_analysis_data_uri() 
            for an example of an element-specific function.
            -----------------------------------------------------------------
        """
        return getattr(self, 'Action_'+tag,self.Action_default)(tag, node)

    def Print_default(self, head_str, subnode):
        """ -----------------------------------------------------------------
            Default function to perform any element-specific actions
            for the passed XML node.  
            -----------------------------------------------------------------
        """
        if subnode.childNodes.length == 0:
            # Empty tag
            dataVal = ""
        else:
            dataVal = subnode.childNodes[0].nodeValue
        
        print head_str + ": " + dataVal

    def Print_xml(self, head_str, subnode):
        """ -----------------------------------------------------------------
            For elements containing XML documents, just print the length of 
            the XML, not all the data.
            -----------------------------------------------------------------
        """
        if subnode.childNodes.length == 0:
            # No XML was present
            dataVal = "" 
        else:
            dataVal = "{0} bytes of XML".format(len(subnode.toxml()))

        print head_str + ": " + dataVal

    def Print_analysis_xml(self, head_str, subnode):
        self.Print_xml(head_str, subnode)

    def Print_run_xml(self, head_str, subnode):
        self.Print_xml(head_str, subnode)

    def Print_experiment_xml(self, head_str, subnode):
        self.Print_xml(head_str, subnode)

    def ElementPrint(self, tag, head_str, subnode):
        """ -----------------------------------------------------------------
            Do any element-specific printing for the current tag by 
            looking for a function named Print <Tag>.  If not found, 
            then Print_default() is called.  See Action_analysis_data_uri() 
            for an example of an element-specific function.
            -----------------------------------------------------------------
        """
        return getattr(self, 'Print_'+tag,self.Print_default)(head_str, subnode)

    def TraverseElement(self, node, elTupleList):
        """ -----------------------------------------------------------------
            Parse a single CGHub XML element 
            Given a single XML element, and a list of parse definition 
            tuples, loops through each of the parse tuples and dumps
            out any matching child elements.
            -----------------------------------------------------------------
        """
        for elTuple in elTupleList:
            #
            # For each tuple, find the set of matching tags in this 
            # element.  Note that we try with the first character in 
            # both lower and upper case, as the server currently returns 
            # capitalized tags, but the query wants uncapitalized tags.
            #
            dataSet = node.getElementsByTagName(lowerStr(elTuple[Result.PR_TAG]))
            if dataSet.length == 0:
                dataSet = node.getElementsByTagName(upperStr(elTuple[Result.PR_TAG]))
            indent = 4 * ( elTuple[Result.PR_INDENT] + 1 )
            width  = C_WIDTH - indent

            #
            # Loop through each element.  If it's a leaf node (from
            # a parsing perspective), then print out the node value,
            # otherwise, parse the children
            #
            for subnode in dataSet:
                #
                # Do any element-specific actions
                #
                self.ElementAction(elTuple[Result.PR_TAG], subnode)

                attr_str = self.ElementAttrs(elTuple[Result.PR_TAG], subnode)

                tag_str  = elTuple[Result.PR_TAG] + " " + attr_str
                head_str = " " * indent + "{tag:{width}} " . format(tag=tag_str, width=width)

                if not elTuple[Result.PR_HASCHILD]:
                    # Leaf node
                    if subnode.childNodes.length == 0:
                        # Empty tag
                        dataVal = ""
                    else:
                        dataVal = subnode.childNodes[0].nodeValue
                    if elTuple[Result.PR_PRINT]:
                        self.ElementPrint(elTuple[Result.PR_TAG],head_str, subnode)
                else:
                    if elTuple[Result.PR_PRINT]:
                        if elTuple[Result.PR_INDENT] == 0:
                            print ""    # Add space between top level headers
                        print head_str
                    self.TraverseElement(subnode, elTuple[Result.PR_CHILD])

    def doTraverse(self):
        """ -----------------------------------------------------------------
            Traverse all of the subnodes in this Result, printing the
            contents to stdout.
            -----------------------------------------------------------------
        """

        self.TraverseElement(self.dom, self.analysisPR)

    def getUriList(self):
        """ -----------------------------------------------------------------
            Return the list of URIs collected as we traversed this Result.
            -----------------------------------------------------------------
        """

        return self.uriList


class ObjectResult(Result):
    """ =================================================================
        ObjectResult
        
        Object-based Result object downloaded from cghub.   The derived
        class is used to define type-specific parsing attributes.
        =================================================================
    """
    
    #
    # Parser definition structure for the object-based Results.  Determines 
    # which XML tags we're interested in parsing/printing.   To parse a new 
    # tag, add it at the appropriate nesting level below.
    #
    # N.B. If you change the name of an existing tag, you must also check 
    #      to see if it has a custom GetAttrs_<tag> or Action_<tag> function, 
    #      and update the name accordingly.
    #
    #        TagName                           Print  Indent        Has    Child
    #                                        Heading   Level   Children
    analysisPR = [
                ("Result",                      True,     0,      True,       [
                    ("analysis_id",             True,     1,      False),
                    ("analysis_data_uri",       True,     1,      False),
                    ("analysis_attribute_uri",  True,     1,      False),
                    ("last_modified",           True,     1,      False),
                    ("center_name",             True,     1,      False),
                    ("state",                   True,     1,      False),
                    ("study",                   False,    1,      False),
                    ("aliquot_id",              True,     1,      False),
                    ("Files",                   True,     1,      True,       [
                        ("File",                False,    2,      True,       [
                            ("filename",        True,     2,      False),      
                            ("filesize",        True,     2,      False),      
                            ("checksum",        True,     2,      False)      
                        ]) 
                    ]) 
                ])  
        ]

class AttrResult(Result):
    """ =================================================================
        AttrResult
        
        Attribute-based Result object downloaded from cghub.  The 
        derived class is used to define type-specific parsing 
        attributes.
        =================================================================
    """
    #
    # Parser definition structure for the attribute-based Results.  Determines 
    # which XML tags we're interested in parsing/printing.   To parse a new 
    # tag, add it at the appropriate nesting level below.
    #
    # N.B. If you change the name of an existing tag, you must also check 
    #      to see if it has a custom GetAttrs_<tag> or Action_<tag> function, 
    #      and update the name accordingly.
    #
    #        TagName                           Print  Indent        Has    Child
    #                                        Heading   Level   Children
    analysisPR = [
                ("Result",                     True,     0,      True,       [
                    ("analysis_id",            True,     1,      False),
                    ("analysis_data_uri",      True,     1,      False),
                    ("last_modified",          True,     1,      False),
                    ("center_name",            True,     1,      False),
                    ("state",                  True,     1,      False),
                    ("study",                  True,     1,      False),
                    ("library_strategy",       True,     1,      False),
                    ("platform",               True,     1,      False),
                    ("sample_accession",       True,     1,      False),
                    ("legacy_sample_id",       True,     1,      False),
                    ("disease_abbr",           True,     1,      False),
                    ("analyte_code",           True,     1,      False),
                    ("sample_type",            True,     1,      False),
                    ("tss_id",                 True,     1,      False),
                    ("participant_id",         True,     1,      False),
                    ("sample_id",              True,     1,      False),
                    ("aliquot_id",             True,     1,      False),
                    ("analysis_xml",           True,     1,      False),
                    ("run_xml",                True,     1,      False),
                    ("experiment_xml",         True,     1,      False),
                    ("Files",                  True,     1,      True,       [
                        ("File",               False,    2,      True,       [
                            ("filename",       True,     2,      False),      
                            ("filesize",       True,     2,      False),      
                            ("checksum",       True,     2,      False)      
                        ]) 
                    ]) 
                ])  
        ]


class CGHubQuery:
    """ =================================================================
        CGHubQuery
        
        Class to perform a single CGHub query and parse the XML that's 
        returned.

        Basic Usage:
            CGHubQuery()      - Instantiate the query object
            DumpHeader()      - Dump out the execution parameters
            GET()             - Perform the GET operation
            ParseResultSet()  - Parse the ResultSet container
            ParseNextResult() - The next Result container in the stream
            DumpFooter()      - Dump out a summary of the results
        =================================================================
    """
    def __init__(self, cgsvr, useattr, inxml, outxml):
        """ -----------------------------------------------------------------
            Initialize the instance variables
            -----------------------------------------------------------------
        """
        self.infh = None
        self.stream = None
        self.uriList = []
        self.server = cgsvr
        self.inxml = inxml
        self.outxml = outxml
        self.logfile = None

        if useattr:        
            self.uri = CGHUB_ANAL_ATTR_URI
        else:
            self.uri = CGHUB_ANAL_OBJECT_URI

        if self.outxml != None:
            self.logfile = XMLLogFile(self.outxml)


    def DumpHeader(self, qs):
        """ -----------------------------------------------------------------
            Dump out a header that describes this query execution
            -----------------------------------------------------------------
        """

        attrs = [ ("Script Version",  CGQUERY_VER),
                  ("CGHub Server",    self.server),
                  ("REST Resource",   self.uri),
                  ("QueryString",     qs.Raw()),
                  ("Output File",     self.outxml) ]

        print ""
        print 76 * "="
        ofs=4
        width=C_WIDTH-ofs
        for attr in attrs:
            print  ofs * " " + "{0:{1}} : {2}" . format (attr[0], width, attr[1])
        print 76 * "-"

    def DumpFooter(self):
        """ -----------------------------------------------------------------
            Dump out a footer that summarizes the query execution
            -----------------------------------------------------------------
        """

        attrs = [ ("Parse Errors",        Log.getParseErrorCount()),
                  ("Parse Warnings",      Log.getParseWarningCount()) ]

        #
        # Currently, the values in the footer are only displayed
        # in verbose mode
        #
        print ""

        if Log.Verbose():
            print 76 * "-"
            print "    Parse Summary"
            ofs=8
            width=C_WIDTH-ofs
            for attr in attrs:
                print ofs * " " + "{0:{1}} : {2:2}" . format (attr[0], width, attr[1])

            print 76 * "-"
            print ""

    def OpenInFile(self, inxml):
        """ -----------------------------------------------------------------
            Open an input file instead of executing a query.  For testing
            purposes only.
            -----------------------------------------------------------------
        """
        Log.notice("Using file '{0}' as input XML".format(self.inxml))
        try:
            infh = open(inxml, "r")
        except IOError, (err):
            Log.fatalExecError("Can't open input file {0} ({1})".format(inxml, err)) 

        return infh

    def ParseXMLError(self, httperrfmt, httperr):
        """ -----------------------------------------------------------------
            Parse the XML that's returned as part of an HTTP Error 
            -----------------------------------------------------------------
        """
        
        #
        # Dump the HTTP error but don't exit just yet
        #
        Log.fatalExecError(httperrfmt % (httperr), False)

        rawxml = httperr.read()

        #
        # Log it (if needed)
        #
        if self.logfile != None:
            self.logfile.Write(rawxml)

        try:
            print " " * 4 + "Error Details:"

            #
            # Parse the XML
            #
            errorobj = CGError(rawxml)

            #
            # Dump the contents
            #
            errorobj.PrintDetails()

        except Exception, err:
            print " " * 8 + "Unable to parse error details from XML response"

        Log.fatalError()


    def GET(self, qs):
        """ -----------------------------------------------------------------
            Perform the HTTP GET, passing the encoded query string.
            Enough of the resulting XML is read and parsed to get the number
            of results, which is returned for further processing.
            -----------------------------------------------------------------
        """

        errfmt="Query failed (%s)"

        if self.inxml != None:
            # We're using a local file instead of a query
            self.infh = self.OpenInFile(self.inxml)
        else:
            Log.debug("Sending querystring '%s'..." % qs.Encoded())
            url = self.server + self.uri + "?" + qs.Encoded()

            mlen = Log.status("Query in progress...")

            try:
                self.infh = urllib2.urlopen(url)

            except (urllib2.HTTPError), err:        

                Log.clearStatus(mlen)

                if err.info()['Content-Type'] == "text/xml":
                    self.ParseXMLError(errfmt, err)
                else:
                    Log.fatalExecError(errfmt % (err))

            except (ValueError, urllib2.URLError), err:        

                Log.clearStatus(mlen)
                Log.fatalExecError(errfmt % err)

            Log.clearStatus(mlen)
            Log.debug("Query complete.")

        self.stream = ResultStream(self.infh, 128 * 1024, self.logfile)


    def ParseResultSet(self):
        """ -----------------------------------------------------------------
            Parse the initial "ResultSet" XML to get the number of expected
            result objects.
            -----------------------------------------------------------------
        """
        if self.stream == None:
            Log.fatalExecError("Attempt to parse results before query")

        resultset = ResultSet(self.stream.getResultSetXML())

        resultset.doTraverse()

        
    def ParseNextResult(self):
        """ -----------------------------------------------------------------
            Parse the next "Result" XML read from the stream into a dom,
            and then print the contents.
            -----------------------------------------------------------------
        """

        if self.stream == None:
            Log.fatalExecError("Attempt to parse results before query")
        
        #
        # Get the next result text from the stream
        #
        rawxml = self.stream.getResultXML()
        if rawxml == None:
            # No more
            return False

        # 
        # Instantiate the appropriate type of Result object dom
        #
        if (self.uri == CGHUB_ANAL_ATTR_URI):
            result = AttrResult(rawxml)
        else:
            result = ObjectResult(rawxml)

        #
        # Traverse the object, printing the contents
        #
        result.doTraverse()

        #
        # Save any URIs found in this result in case we're interactive
        #
        self.uriList.extend(result.getUriList())

        return True

    def getURIList(self):
        """ -----------------------------------------------------------------
            Return the total list of all URIs found, across all Results
            -----------------------------------------------------------------
        """
        return self.uriList

    def Close(self):
        """ -----------------------------------------------------------------
            Clean up this query operation.  Note that this may be called
            following an exception, so don't make any assumptions about
            the state of the object.
            -----------------------------------------------------------------
        """
        try: 
            if self.infh:
                self.infh.close()
                self.infh = None

            if self.stream:
                self.stream.Close()
                self.stream = None

            if self.logfile:
                self.logfile.Close()
                self.logfile = None

        except IOError, (err):
            Log.fatalExecError("Failed to close file")



def GTDownload(uri, prog, credFile, confdir):
    """ -----------------------------------------------------------------
        Perform a single GeneTorrent download.   Returns True on 
        success, False on (non-fatal) failure.
        -----------------------------------------------------------------
    """
    print "\nProcessing URI " + uri

    cmdline = [prog, 
               "-v",
               "-c", credFile,
               "-d", uri]

    if confdir != None:
        cmdline.extend(["--confDir", confdir])

    print "\nExecuting command '{0}'\n".format(" ".join(cmdline))

    try:
        ec = call(cmdline)
    except OSError, (err):
        Log.fatalExecError("Failed to execute {0} ({1})" . format(prog, err))
    except KeyboardInterrupt:
        # ^C.  Simulate a sigint but continue to the next download
        ec = -2
        

    #
    # Check the exit code/signal status
    #
    rc = False
    if ec < 0:
        Log.execError (prog + " was killed by signal {0}" . format(-ec))
    elif ec > 0:
        Log.execError (prog + " failed with return code {0}" . format(ec))
    else:
        rc = True
        print prog + " returned success."

    return rc

def InteractiveGT(uriList, gtbin, credFile, confdir):
    """ -----------------------------------------------------------------
        Interactively download specific URIs found in the XML using 
        GeneTorrent
        -----------------------------------------------------------------
    """

    if uriList == None or len(uriList) == 0:
        print "No analysis URI values found in downloaded XML"
        return

    fmt_str = 4 * " " + "[{0:2}] : {1}" 
    while True:
        print "Enter the index of a URI to download (0 for all), a range\nof indeces separated by dash, or 'q' to quit"
        print fmt_str . format(0,"All URIs")
        for idx, uri in enumerate(uriList):
            print fmt_str . format(idx+1, uri)
        print

        #
        # Read the index (offset by 1) from the cmd line
        #
        response = raw_input("Index (0=all, q=quit)> ")

        #
        # Consider anything starting with 'q' as 'quit'
        #
        if response[:1] == 'q':
            print ""
            break

        try:
            if re.match('(\d+)-(\d+)$',response):
                # Got a range
                idx_range = [int(i) for i in re.findall(r'(\d+)', response)]
                assert len(idx_range) == 2
                start_idx = idx_range[0]
                end_idx = idx_range[1]

                if start_idx > end_idx:
                    print "Invalid range.  Starting index is greater than ending index.\n"
                    continue

                if start_idx == 0:
                    print "Invalid range.  0 is reserved for all.\n"
                    continue

                assert end_idx <= len(uriList)
                start_idx = start_idx - 1
            else:
                if re.match('(\d+)$',response):
                    # Got a single index
                    idx = int(response)
                    assert idx >= 0 and idx <= len(uriList)

                    if idx > 0:
                        end_idx = idx
                    else:
                        end_idx = len(uriList)

                    if idx > 0:
                        start_idx = idx-1
                    else:
                        start_idx = idx
                else:
                    # Got invalid input
                    print "Invalid input format.\n"
                    assert False
        except (ValueError, AssertionError):
            print "Index must be a numeric value between 0 and {0} or a range\nof values separated by dash.\n" . format(len(uriList))
            continue
        
        success = 0

        for idx in range(start_idx, end_idx):
            #
            # Execute the GeneTorrent command
            #
            if GTDownload(uriList[idx], gtbin, credFile, confdir) == True: success += 1

        print
        print 76 * "-"
        print "{0} of {1} downloads completed successfully".format(success, end_idx-start_idx)
        print 76 * "-"
        print



def main():
    """ -----------------------------------------------------------------
        main
    
        Parses the command line arguments to get the query string.  
        Instantiates a CGHubQuery object, performs a GET with the
        query string, and then parses the resulting XML.
        -----------------------------------------------------------------
    """
    cq = None
     
    #
    # Parse the command line arguments
    #
    epilog = '<querystring> should be the fully quoted query string, without the question mark separator, e.g. "disease_abbr=COAD".'

    parser = OptionParser(usage='%prog [options] <querystring>', version='%prog version '+CGQUERY_VER+' (c) 2012 Annai Systems, Inc. All rights reserved.', epilog=epilog)
    
    parser.add_option("", "--input-xml",
                      action="store", type="string", dest="inputxml",
                      help=optparse.SUPPRESS_HELP)

    parser.add_option("-o", "--output-xml",
                      action="store", type="string", dest="outputxml",
                      help="file in which to store raw xml output")

    parser.add_option("-s", "--server",
                      action="store", type="string", dest="server", default=CGHUB_SVR,
                      help="CGHub server location, including protocol and port, e.g. https://cghub-01.ucsc.edu:20000")

    parser.add_option("-g", "--gt-binary",
                      action="store", type="string", dest="gtbin", default=GT_BIN,
                      help="The GeneTorrent binary used in interactive mode.  Use a fully qualified path if the binary is not in your PATH. e.g. /usr/bin/GeneTorrent")

    parser.add_option("-f", "--conf-dir",
                      action="store", type="string", dest="confdir", default=None,
                      help="Path to the GeneTorrent configuration file")

    parser.add_option("-a", "--attributes",
                      action="store_true", dest="attributes", default=False,
                      help="query the /cghub/metadata/analysisAttributes instead of analysisObjects resource")

    parser.add_option("-i", "--interactive",
                      action="store_true", dest="interactive", default=False,
                      help="enable interactive mode")

    parser.add_option("-c", "--credential",
                      action="store", type="string", dest="credential",
                      help="file containing the GeneTorrent credential.  Only required for interactive mode.")

    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="enable verbose output")

    (options, args) = parser.parse_args()

    if len(args) == 0:
        Log.fatalOptError (parser, "Querystring must be provided")

    if len(args) > 1:
        Log.fatalOptError (parser, "Only one querystring may be provided")

    if options.interactive:
        if options.credential == None:
            Log.fatalOptError (parser, "Credential is required in interactive mode")
    else:
        if options.credential != None:
            Log.fatalOptError (parser, "Credential is only used in interactive mode")

    #
    # Instantiate the querystring object.  This will raise an exception if
    # the string is invalid.
    #
    try:
        qs = QueryString(args[0])
    except (UnicodeEncodeError, ValueError), err:
        Log.fatalOptError (parser, "Invalid querystring: %s" % err)

    Log.setVerbose(options.verbose)

    try:
        #
        # Instantiate the query object, execute the query, and parse the XML
        #
        cq = CGHubQuery(options.server, options.attributes, options.inputxml, options.outputxml)

        #
        # Dump the header before starting the query, in case the query 
        # takes a while, and turns out to be the wrong one.
        #
        cq.DumpHeader(qs)

        cq.GET(qs)

        cq.ParseResultSet()

        #
        # We process one Result at a time to allow us to scale to large numbers
        # of results
        #
        while cq.ParseNextResult():
            pass

        cq.DumpFooter()

        if options.interactive:
            InteractiveGT(cq.getURIList(), options.gtbin, options.credential, options.confdir)

    except:
        #
        # Just clean up and pass the exception along.   We don't use
        # finally for this purpose as it's not syntactally backward
        # compatible.
        #
        if cq:
            cq.Close()
        raise

    cq.Close()

if __name__ == "__main__":
    Log = Logger()
    try:
        main()

    except SystemExit, err:
        #
        # Exit from within the script
        #
        sys.exit(err)

    except (KeyboardInterrupt, EOFError):
        #
        # Generic ^C/^D Handler so we don't spit out a python stack.
        #
        sys.stderr.write("\nKilled.\n")
        sys.exit(1)

    except IOError, err:
        #
        # Some kind of IO Error.  If it's a broken pipe (32), just 
        # exit silently -- user probably quit out of more or some 
        # other output processor.   Otherwise, try to spit out an 
        # error.
        #
        if err.errno == 32:
            sys.exit(0)
        sys.stderr.write("\nIOError (%s)\n" % err)
        sys.exit(1)

    except:
        #
        # All other uncaught errors.   
        #
        sys.stderr.write("\nInternal Error:\n\n")
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

