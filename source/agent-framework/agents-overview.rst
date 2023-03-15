.. _Agent-Framework:

===============
Agents Overview
===============

Agents in VOLTTRON can be loosely defined as software modules communicating on the platform which perform some function
on behalf of the user.  Agents may perform a huge variety of tasks, but common use cases involve data collection,
control of ICS and IOT devices, and various platform management tasks.  Agents implemented using the VOLTTRON agent
framework inherit a number of capabilities, including message bus connectivity and agent lifecycle.

Agents deployed on VOLTTRON can perform one or more roles which can be broadly classified into the following groups:

-  **Platform Agents**: Core agents that provide commonly used service to other agents. Examples are the
   Actuator and Platform Driver agents which serve as interfaces between control agents and drivers.
-  **Control Agents**: These agents implement algorithms to control the devices of interest and interact with other
   resources to achieve some goal.
-  **Service Agents**: These agents perform various data collection or platform management services.  Agents in this
   category include weather service agents which collect weather data from remote sources or operations agents which
   help users maintain situational awareness of their deployment.
-  **Cloud Agents**: These agents represent a remote application which needs access to the messages and data on the
   platform. This agent would subscribe to topics of interest to the remote application and would also allow it publish
   data to the platform.

The platform includes some valuable services which can be leveraged by agents:

-  **Message Bus**: All agents and services publish and subscribe to topics on the message bus. This provides a single
   interface that abstracts the details of devices and agents from each other. Components in the platform basically
   produce and consume events.
-  **Configuration Store**: Using the configuration store, agent operations can be altered ad-hoc without significant
   disruption or downtime.
-  **Control Service**: Allows to control various platform and agent operations such as start, stop, check for status etc.
-  **Health Service**: Provides interface to query/report about installed agents health

In addition to services that are bundled as part of VOLTTRON core, the VOLTTRON development team also maintains several
useful agent frameworks, services, and libraries that can be installed based on specific user requirements.

-  **Historian Framework**: Historian agents automatically collect data from a subset of topics on the message bus and
   store them in a data store of choice. The
   `base historian library <https://pypi.org/project/volttron-lib-base-historian/>`_
   has been developed to be fast and reliable, and to handle many common pitfalls of data collection over a network.
   A `SQLHistorian library <https://pypi.org/project/volttron-lib-sql-historian/>`_ provides a historian
   agent class that extends the base historian provides common functionalities for historians that store data in a
   SQL based datastore. Concrete historian can simply provide database specific query/statements for necessary
   operations such as insert, delete etc. For example,
   `SQLiteHistorian <https://pypi.org/project/volttron-sqlite-historian/>`_ extends
   `SQLHistorian library <https://pypi.org/project/volttron-lib-sql-historian>`_ and store data in a sqlite
   database
-  **Driver Framework**: VOLTTRON drivers act as an interface between agents on the platform and a device. Drivers
   publish device data onto the message bus and send control signals issued from control agents to the corresponding
   device.  Drivers are capable of handling the locking of devices to prevent multiple conflicting directives. VOLTTRON
   team maintains driver interfaces for different device types such as
   `Modbus-TK driver <https://pypi.org/project/volttron-lib-modbustk-driver/>`_ and
   `BACnet driver <https://pypi.org/project/volttron-lib-bacnet-driver/>`_ that work with a
   `Volttron Platform Driver agent <https://pypi.org/project/volttron-platform-driver/>`_ to control and collect data
   from devices
-  **Application Scheduling**: This `service <https://pypi.org/project/volttron-actuator/>`_ allows the scheduling of
   agents’ access to devices in order to prevent conflicts.
-  **Web Service**: This `service <https://pypi.org/project/volttron-lib-web/>`_ provides a RESTful HTTP API for
   communicating with components of the VOLTTRON system


.. toctree::

   ../deploying-volttron/proxy_web_server