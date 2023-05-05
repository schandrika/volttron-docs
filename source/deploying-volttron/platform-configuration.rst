.. _Platform-Configuration:

======================
Platform Configuration
======================

Each instance of the VOLTTRON platform includes a `config` file which is used to configure the platform instance on
startup.  This file is kept in :term:`VOLTTRON_HOME`

VOLTTRON_HOME
=============

By default, the VOLTTRON project bases its files out of `VOLTTRON_HOME` which defaults to `~/.volttron`.  This directory
features directories and files used by the platform for important operation and management tasks as well as containing
packaged agents and their individual runtime environments (including data directories, identity files, etc.)

- **$VOLTTRON_HOME/agents** - contains the agents installed on the platform
- **$VOLTTRON_HOME/auth.json** - file containing authentication and authorization rules for agents connecting to the
  VOLTTRON instance.
- **$VOLTTRON_HOME/certificates** - contains the certificates for use with the Licensed VOLTTRON code.
- **$VOLTTRON_HOME/configuration_store** - agent configuration store files are stored in this directory.  Each agent
  may have a file here in which JSON representations of their stored configuration files are stored.
- **$VOLTTRON_HOME/run** - contains files create by the platform during execution.  The main ones are the ZMQ files
  created for publish and subscribe functionality.
- **$VOLTTRON_HOME/ssh** - keys used by agent mobility in the Licensed VOLTTRON code
- **$VOLTTRON_HOME/config** - Default location to place a config file to override any platform settings.
- **$VOLTTRON_HOME/packaged** - agent packages created with `volttron-pkg` are created in this directory
- **$VOLTTRON_HOME/VOLTTRON_PID** - File containing the Unix process ID for the VOLTTRON platform - used for tracking
  platform status.
- **$VOLTTRON_HOME/<volttron log file>** - default path to log file if volttron is started with -l <file name without path>


.. _Platform-Config-File:

VOLTTRON Config File
====================

The `config` file in `VOLTTRON_HOME` is the config file used by the platform.  This configuration file specifies the
behavior of the platform at runtime, including which message bus it uses, the name of the platform instance, and the
address bound to by :term:`VIP`.  The `VOLTTRON Config`_ wizard (explained below) can be used to configure an instance
for the first time.  The user may run the wizard again or edit the config file directly as necessary for operations.
The following is a simple  example `config` for a multi-platform deployment:

::

    [volttron]
    message-bus = zmq
    vip-address = tcp://127.0.0.1:22916
    bind-web-address = <web service bind address>
    web-ssl-cert = <VOLTTRON_HOME>/certificates/certs/platform_web-server.crt
    web-ssl-key = <VOLTTRON_HOME>/certificates/private/platform_web-server.pem
    instance-name = volttron1
    volttron-central-address = <VC address>

The example consists of the following entries:

* **message-bus** - message bus being used for this instance (Though monolithic volttron supports both zmq and rmq, modular volttron currently only supports zmq.)
* **vip-address** - address bound to by VIP for message bus communication
* **bind-web-address** - Optional, needed if platform has to support web feature. Represents address bound to by the
  platform web service for handling HTTP(s) requests.  Typical address would be ``https://<hostname>:8443``
* **web-ssl-cert** - Optional, needed if platform has to support web feature. Represents path to the certificate for the
  instance's web service
* **web-ssl-key** - Optional, needed if platform has to support web feature. Represents secret key or path to secret key
  file used by web service authenticate requests
* **instance-name** - Optional, name of this VOLTTRON platform instance, should be unique for the deployment. Defaults to volttron1
* **volttron-central-address** - Optional, needed if instance is running Volttron Central.  Represents web address of
  VOLTTRON Central agent managing this platform instance.  Typical address would be ``https://<hostname>:8443``
