.. _Contributing-Documentation:

==========================
Contributing Documentation
==========================

The Community is encouraged to contribute documentation back to the project as they work through use cases the
developers may not have considered or documented.  By contributing documentation back, the community can
learn from each other and build up a more extensive knowledge base.

|VOLTTRON| documentation utilizes ReadTheDocs: http://volttron.readthedocs.io/en/develop/ and is built
using the `Sphinx <http://www.sphinx-doc.org/en/stable/>`_ Python library with static content in
`Restructured Text <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_ at
`volttron-docs <https://github.com/eclipse-volttron/volttron-docs>`_


Building the Documentation
==========================

Static documentation can be found in the `volttron-docs <https://github.com/eclipse-volttron/volttron-docs>`_ in the
source directory.  Edit or create new .rst files to add new content
using the `Restructured Text <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_ format.  To see the results
of your changes the documentation can be built locally through the command line using the following instructions:

This project depends on the following

    * python = "^3.10"
    * Sphinx = "^6.0.0"
    * pyyaml = "^6.0"
    * sphinx-rtd-theme = "^1.2.0"
    * m2r2 = "0.3.2"

If you have poetry installed you can run the below command :code:`poetry install` from the cloned volttron-docs
directory to install all the requirements. Alternatively, you can install python and pip and use pip to install
the rest of the requirements.

.. code-block::

    sudo apt install python3-venv python3-pip
    python3 -m venv /path/to/new/virtual/environment
    source  /path/to/new/virtual/environment/activate
    pip install sphinx>=6.0 sphinx-rtd-theme>=1.2  pyyaml>=6.0 m2r2==0.3.2

Once you have all the pre-requisites install, run the below command to generate html files locally

.. code-block::

    make html

Then, open your browser to the created local files:

.. code-block:: bash

   file:///home/<USER>/git/volttron/docs/build/html/index.html


When complete, changes can be contributed back using the same process as code :ref:`contributions <Contributing-Code>`
by creating a pull request.  When the changes are accepted and merged, they will be reflected in the ReadTheDocs site.

.. |VOLTTRON| unicode:: VOLTTRON U+2122


.. _Documentation-Styleguide:

Documentation Styleguide
========================


Naming Conventions
------------------

* File names and directories should be all lower-case and use only dashes/minus signs (-) as word separators

::

    index.rst
    ├── first-document.rst
    ├── more-documents
    │   ├──second-document.rst

* Reference Labels should be Capitalized and dash/minus separated:

::

    .. _Reference-Label:

* Headings and Sub-headings should be written like book titles:

::

    ==============
    The Page Title
    ==============


Headings
--------

Each page should have a main title:

::

    ==================================
    This is the Main Title of the Page
    ==================================

It can be useful to include reference labels throughout the document to use to refer back to that section of
documentation.  Include reference labels above titles and important headings:

::

    .. _Main-Title:

    ==================================
    This is the main title of the page
    ==================================


Heading Levels
^^^^^^^^^^^^^^

* Page titles and documentation parts should use over-line and underline hashes:

::

    =====
    Title
    =====

* Chapter headings should be over-lined and underlined with asterisks

::

    *******
    Chapter
    *******

* For sections, subsections, sub-subsections, etc. underline the heading with the following:

    * =, for sections
    * -, for subsections
    * ^, for sub-subsections
    * “, for paragraphs


In addition to following guidelines for styling, please separate headers from previous content by two newlines.

::

    =====
    Title
    =====

        Content


    Subheading
    ==========


Example Code Blocks
--------------------

Use bash for commands or user actions:

.. code-block:: bash

   ls -al


Use this for the results of a command:

.. code-block:: console

   total 5277200
   drwxr-xr-x 22 volttron volttron       4096 Oct 20 09:44 .
   drwxr-xr-x 23 volttron volttron       4096 Oct 19 18:39 ..
   -rwxr-xr-x  1 volttron volttron        164 Sep 29 17:08 agent-setup.sh
   drwxr-xr-x  3 volttron volttron       4096 Sep 29 17:13 applications


Use this when Python source code is displayed

.. code-block:: python

    @RPC.export
    def status_agents(self):
        return self._aip.status_agents()


Directives
----------

.. DANGER::

   Something very bad!

.. tip::

   This is something good to know


Some other directives
^^^^^^^^^^^^^^^^^^^^^

"attention", "caution", "danger", "error", "hint", "important", "note", "tip", "warning", "admonition"


Links
-----

Linking to external sites is simple:

::

    Link to `Google <www.google.com>`_


References
----------

You can reference other sections of documentation using the `ref` directive:

::

    This will reference the :ref:`platform installation <Platform-Installation>`


Other resources
---------------

- http://pygments.org/docs/lexers/
- http://documentation-style-guide-sphinx.readthedocs.io/en/latest/style-guide.html
- http://www.sphinx-doc.org/en/stable/markup/code.html
