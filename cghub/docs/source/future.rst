.. about things planned

Future improvements
============================================

---------------------------------------------
Depending on WSI-API
---------------------------------------------

Some queries do not search UUID
----------------------------------------

Some queries do not return results when entering exact UUID even though such UUID exists.

https://cghub.ucsc.edu/cghub/metadata/analysisAttributes?xml_text=0974ab6a-2ffa-4365-bc46-06f3152f4f6b

https://cghub.ucsc.edu/cghub/metadata/analysisAttributes?xml_text=79c99eb1-c79b-4130-a439-35632508c169

The first query above is problematic. In this case an explicit query has to be made.

https://cghub.ucsc.edu/cghub/metadata/analysisAttributes?analysis_id=0974ab6a-2ffa-4365-bc46-06f3152f4f6b

https://cghub.ucsc.edu/cghub/metadata/analysisAttributes?analysis_id=79c99eb1-c79b-4130-a439-35632508c169

The problem is with WSI-API because for these problematic queries it does not return ``UUID`` field. Compare with the second "good" query.

At the moment this problem is solved by making a second query every time we have zero results. 
If this is fixed for WSI-API this extra query should be removed.
