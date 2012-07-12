.. 

Other things tried
============================================

-----
PyXB
-----

Usage of PyXB for validation is also described in the :doc:`Validation section <validation>` of this documentation.

PyXB (“pixbee”) is a pure Python package that generates Python source code for classes that correspond to data structures defined by XMLSchema. The generated classes support bi-directional conversion between XML documents and Python objects.

http://pyxb.sourceforge.net/

XSD files are downloaded and saved. Analysis, experiment, and run schemas require ``SRA.common.xsd`` schema. Bindings are generated with

.. code-block:: bash

    # genbindings_common.sh

    pyxbgen \
      -u SRA.common.xsd -m common \
      --archive-to-file common.wxs


.. code-block:: bash

    # genbindings_analysis.sh

    FILE='SRA.analysis.xsd'
    PREFIX='analysis'

    pyxbgen \
       -m "${PREFIX}" \
       -u "${FILE}" \
       --archive-path .:+ \

For more details see http://pyxb.sourceforge.net/userref_pyxbgen.html?highlight=common#sharing-namespace-bindings

Problem
----------

Problem was that generated bindings work well with real data for experiment, but generate exceptions for analysis and run schemas.

--------------------
generateDS
--------------------

http://cutter.rexx.com/~dkuhlman/generateDS.html

generateDS.py generates Python data structures (for example, class definitions) from an XML Schema document. These data structures represent the elements in an XML document described by the XML Schema. It also generates parsers that load an XML document into those data structures. In addition, a separate file containing subclasses (stubs) is optionally generated. The user can add methods to the subclasses in order to process the contents of an XML document.

Problem
--------------------

The error that was generated:

.. code-block:: python

    AttributeError: 'NoneType' object has no attribute 'annotate'

Namespace prefix mismatch is mentioned as one of the possible reasons in the `docs <http://cutter.rexx.com/~dkuhlman/generateDS.html#namespace-prefix-mis-match>`__.

Using flag when calling the command was tried similar to what is mentioned there, but it did not help.

.. code-block:: bash

    generateDS.py -a "xsd:" --super=mylib -o mylib.py -s myapp.py someschema.xsd
