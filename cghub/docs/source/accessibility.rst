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

    <div id="main-content"></div>

Search page has next skip nav links:

    - Skip to Navigation bar
    - Skip to Filters
    - Skip to Summary of results
    - Skip to Main results

And for cart page skip nav links are next:

    - Skip to Navigation bar
    - Skip to Summary of results
    - Skip to Main results

Data table navigation via keyboard
----------------------------------

    - alt + arrow - move to next cell
    - arrows - move screen
    - space bar - check/uncheck checkbox
    - enter - submit form (add selected files to cart)
    - alt + enter - show details popup
    - ctrl + enter - go to file details page

Screen readers uses their own keyboard shortcuts to navigate in table. For example, arrow keys used to switch between cells.

Raw xml naviagtion via keyboard
-------------------------------

User can navigate thru raw xml on details page using arrows keys. And space bar can be used to open/close nodes.

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

    - skip to main content links: 1-9
    - primary menu: 10-20
    - filters bar: 30-50
    - main content > 50
    - popups > 100

Tricks
------

NVDA does not read links titles in IE.
This is only `one decision <http://blog.silktide.com/2013/01/i-thought-title-text-improved-accessibility-i-was-wrong/>`__ I found to fix this.
