.. VOLTTRON documentation root file

==========================
|VOLTTRON|  documentation! sphinx_hooks-v3api build
==========================

|VOLTTRON Tagline|

|VOLTTRON| is an open source, scalable, and distributed platform that seamlessly integrates data, devices, and
systems for sensing and control applications.  It is built on extensible frameworks allowing contributors to easily
expand the capabilities of the platform to meet their use cases.  Features are implemented as loosely coupled software
components, called agents, enabling flexible deployment options and easy customization.


Key Use-Cases
=============

- Developing scalable, reusable applications to deploy in the field without spending development resources on
  operational components not specific to the application
- Low-cost data collection deployable on commodity hardware
- Integration hub for connecting a diverse set of devices together in a common interface
- Testbed for developing applications for a simulated environment


.. image:: files/volttron_diagram.png

Features
========

- A :ref:`message bus <Message-Bus>` allowing connectivity between agents on individual platforms and
  between platform instances in large scale deployments
- Integrated security features enabling the management of secure communication between agents and platform instances
- A flexible :ref:`agent framework <Agent-Framework>` allowing users to adapt the platform to their unique use-cases
- A configurable :ref:`driver framework <Driver-Framework>` for collecting data from and sending control
  signals to buildings and devices
- automatic data capture and retrieval through our :ref:`historian framework <Historian-Framework>`
- An extensible :ref:`web framework <Web-Framework>` allowing users and services to securely connect to the platform
  from anywhere
- Capability to interface with simulation engines and applications to evaluate applications prior to deployment


VOLTTRON™ is publicly available from `GitHub <https://github.com/volttron/volttron.git>`_. The project
is supported by the U.S. Department of Energy and receives ongoing updates from a team of core developers at PNNL.  The
VOLTTRON team encourages and appreciates community involvement including issues and pull requests on Github, meetings
at our bi-weekly office-hours and on Slack. To be invited to office-hours or slack, please `send the team an email
<volttron@pnnl.gov>`_.


.. toctree::
   :caption: Introduction
   :hidden:
   :titlesonly:
   :maxdepth: 1

   introduction/platform-install
   introduction/definitions
   introduction/license

.. toctree::
   :caption: Platform Features
   :hidden:
   :titlesonly:
   :maxdepth: 1

   platform-features/message-bus/index
   platform-features/control/index
   platform-features/config-store/configuration-store
   platform-features/security/volttron-security
   platform-features/web-api/introduction


.. toctree::
   :caption: Agent docs
   :hidden:
   :titlesonly:
   :maxdepth: 1

   SQLiteHistorian <agent-docs/volttron-sqlite-historian/docs/source/index>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`

.. |VOLTTRON| unicode:: VOLTTRON U+2122
.. |VOLTTRON Tagline| image:: files/VOLLTRON_Logo_Black_Horizontal_with_Tagline.png
