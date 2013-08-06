import re

# FIXME: master is current in CGHub subversion tree with tests, we need
# to integrate this for real once we look at WSAPI structure again.
# this shouldn't even be named browser_text_search, but generalized to
# to support a simplified text search in the wsapi.

# FIXME: tmp flag to indicate if we are using all_metadata index.  This will
# go away when rolled out to production
useAllMetadataIndex = True


# Generally we should split on words and quotation marks, where a word is a sequence
# of anything but white-space or quotation marks.
#
token_re = '("|[^\s"]+)'

# The special characters from
#
# http://lucene.apache.org/core/3_6_2/queryparsersyntax.html#Escaping Special Characters
#
# except quotes, asterisk and question. The former has already been parsed  while the
# latter are reserved for future use (see below). Above page refers to '&&' and '||'
# as special characters, even though they are actuall strings. To be safe, we escape
# every '&' and '|'
#
special_chars_re = re.compile( r'[-+&|!(){}\[\]\^~:\\]' )

# At some point we might want to add wildcard searches, so we should reserve the
# corresponding special characters for that purpose.
#
reserved_chars_re = re.compile( '[*?]' )

# TODO: Verify how the query transliteration works in WSI

def ws_query( user_query ):
    """
    Translates a browser query (which is typically entered by users into the
    CGHub browser's search box) into a query that can be submitted to the CGHub
    WS API using the all_metadata query parameter. The syntax of the supported
    input field is be specified by the following fragment of the CGHub Browser
    user documentation.

    <quote>A full-text search query consists of a space-separated sequence of
    items. Each item is either a single word or a phrase. A phrase is a
    space-separated sequence of words enclosed in quotation marks. A word is
    any sequence of one or more characters other than space or quotation marks.
    Given a particular search query, a document will be included in the
    corresponding search result if all of the query's items are present in the
    document. A phrase is considered to be present in the document if all of
    its words are present in the document, in the same order as in the phrase
    and without additional words between them. Asterisk and question mark are
    not allowed anywhere in the query.</quote>

    Currently not implemented because the CGHub SOLR schema does not support
    wildcard searches for the all_metadata field: <quote>A question mark
    anywhere in a word will match any single character. For example, bi?
    matches bit, bid and so on. Correspondingly, an asterisk matches any
    sequence of characters anywhere in a word. For example, b*rd matches brd,
    bird or beard, foo* matches foo or foobar and *ing matches exciting or
    boring. It is currently not possible to search for a literal question mark
    or asterisk or double quotation mark.</quote>

    Note that 'space' above includes any white-space character.

    The overall goal is for the user query to be as Googley as possible. The
    problem with this goal is that CGHub's SOLR schema currently uses the
    text_general type for the xml_text and all_metadata fields. This type
    breaks the document and incoming queries into words using white-space and
    special characters. For example, a document containing 'a-b-c-d' would be
    considered a match for the query 'a-d', surprisingly so. The document
    'a-b-c-d' is equivalent to 'a b c d' and the query 'a-d' is considered
    equivalent to 'a d'. Since both 'a' and 'd' occur in the document, it is a
    match. The solution is to wrap each word in the user query in quotation
    marks, turning it into a SOLR phrase, except for words that already occur
    in a quotes entered by the user. This also takes care of preventing AND and
    OR from having special meaning in the query.

    SOLR/Lucene defines certain special characters which we should escape,
    whether they occur in a phrase or not. In order to support wildcard
    searches in the future we should also dissallow * and ? characters for now.
    """

    tokens = re.split( token_re, user_query )

    phrases = [ ]
    phrase = None
    for token in tokens:
        if token.isspace( ) or len( token ) < 1:
            pass
        elif token == '"':
            if phrase is None:
                phrase = [ ]
            else:
                phrases.append( phrase )
                phrase = None
        else:
            if reserved_chars_re.search( token ):
                raise RuntimeError( 'Query contains characters reserved for future use' )
            word = special_chars_re.sub( lambda special: '\\' + special.group( ), token )
            if phrase is None:
                phrases.append( [ word ] )
            else:
                phrase.append( word )

    if phrase is not None:
        raise RuntimeError( 'Unbalanced quotation marks in user query' )

    phrases = map( lambda phrase: "'" + ' '.join( phrase ) + "'", phrases )

    return '(' + ' '.join( phrases ) + ')'

