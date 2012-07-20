.. About testing

Performance Test Suite
============================================

Setting up required files
-----------------------------

All files to run profiling scripts are located in ``cghub_api/utils/profile``, but some extra dependencies need to be installed.

Gprof2Dot_ utility converts profile files into dot format for visualization in a form of graphs. Get it with ``make get_gprof2dot`` command.

Matplotlib_ is used in another script for plotting. It is not included into the requirements since it is not required for functionality. Install it directly from its site.

Running profiling scripts
----------------------------------------

.. image:: imgs/time_four_pos_queries_with_cache.png
   :height: 300px
   :align: center

.. _Gprof2Dot: http://code.google.com/p/jrfonseca/wiki/Gprof2Dot
