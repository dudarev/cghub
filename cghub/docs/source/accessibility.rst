.. Accessibility

Accessibility
=============

Skip navigation links
---------------------

When user come to page and press tab-button, skip navigation links will be shown at the top of page.
There are few skip navigation links by default:

    - Skip to Navigation bar
    - Skip to Main content

By default, main content consist in div.base-container.
But we can specify other point where main content starts by

.. code-block:: html

    <div id="main-nav"></div>

Search page has next skip nav links:

    - Skip to Navigation bar
    - Skip to Filters
    - Skip to Summary of results
    - Skip to Main results

And for cart page skip nav links are next:

    - Skip to Navigation bar
    - Skip to Summary of results
    - Skip to Main results

Testing with screen readers
---------------------------

`Using NVDA to Evaluate Web Accessibility <http://webaim.org/articles/nvda/>`__

Keys used to navigate through content
-------------------------------------

    - tab - jump from link to link
    - shift + tab - back to previous element
    - ctrl + home - go to top of the page
    - alt + arrow down - open filter options list
    - use spacebar to select/deselect checkboxes
    - `NVDA shortcuts <http://webaim.org/resources/shortcuts/nvda>`__
    - `JAWS shortcuts <http://webaim.org/resources/shortcuts/jaws>`__

Tab indexes
-----------

Values spaces:

    - skip to main content link: 1
    - primary menu: 10-20
    - filters bar: 30-50
    - main content > 50 
