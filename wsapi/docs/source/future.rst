.. about things planned

Future functionality planned
============================================

---------------------------------------------
Depending on WSI-API
---------------------------------------------

Only last modification time for a query
----------------------------------------

This would be helpful to validate cache for queries.

Similar to ``analysisId`` and ``analysisAttributes``, 
WSI-API may have a method that would return only one date -- 
the most latest of all modification dates for all results.

Similar to existing query ``analysisId``:

`https://cghub.ucsc.edu/cghub/metadata/analysisId?xml_text=6d7* <https://cghub.ucsc.edu/cghub/metadata/analysisId?xml_text=6d7*>`__

(returns 127 results as of 2013-01-22)

It may use ``lastModified``, for example:

`https://cghub.ucsc.edu/cghub/metadata/lastModified?xml_text=6d7* <https://cghub.ucsc.edu/cghub/metadata/lastModified?xml_text=6d7*>`__

(returns an error)

Only number of results for a query
----------------------------------------

This would help to warn a user if a query may take too long.

Possible interface with ``numberOfResults``:

`https://cghub.ucsc.edu/cghub/metadata/numberOfResults?xml_text=6d7* <https://cghub.ucsc.edu/cghub/metadata/numberOfResults?xml_text=6d7*>`__

Return all elements except ``*_xml``
--------------------------------------------------

This would reduce size of files transfered.

At the moment a query to ``analysisId`` has the most minimum of information 
and ``analysisAttributes`` also return ``*_xml`` elements such as ``analysis_xml``. 
This increases size significantly. 
(``analysisObject`` query is similar to ``analysisId`` but is depricated.)

May be, there could be another query that returns all elements except ``*_xml`` ones.

At the moment the Django app that uses this API is using the following elements: 
``legacy_sample_id``, 
``analysis_id``, 
``sample_accession``, 
``r.files.file.0.filesize``,
``last_modified``, 
``disease_abbr``, 
``sample_type``, 
``analyte_code``, 
``library_strategy``, 
``center_name``.

More elements may be used in the future if requested by users.

Parse ``*_xml`` elements with classes created with PyXB (or similar library)
-----------------------------------------------------------------------------

At the moment ``*_xml`` elements cannot be validated against XSD schemas
(for validation scripts see :doc:`validation` in this documentation).

PyXB library also had an issue that did not allow it to parse documents correctly.
As of version 1.1.4 they were fixed.  See discussion at 
`PyXB forum <http://sourceforge.net/projects/pyxb/forums/forum/956708/topic/5331945>`__.
There are both elements missing and extra elements that do not correspond to the schemas,
also order is not correct for some elements.

When the data is fixed on WSI side implement parsing ``*_xml`` elements with
classes generated directly from XSD schemas with PyXB library or some similar library.
