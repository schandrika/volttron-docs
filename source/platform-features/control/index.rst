.. _Control:

================
VOLTTRON Control
================

The base platform functionality focuses on the agent lifecycle, management of the platform itself, and security.  This
section describes how to use the commands included with VOLTTRON to configure and control the platform, agents and
drivers.

.. _Platform-Commands:


Platform Commands
=================

Eclipse VOLTTRON\ :sup:`tm`\  (VOLTTRON/volttron) files for a platform instance are stored under a single directory known as the VOLTTRON home.  This home
directory is set via the :term:`VOLTTRON_HOME` environment variable and defaults to ``$HOME/.volttron``.  Multiple instances
of the platform may exist under the same account on a system by setting the `VOLTTRON_HOME` environment variable
appropriately before executing VOLTTRON commands.  The ``volttron`` and ``volttron-ctrl`` commands can be passed arguments or be specified in a configuration file.  By
default a configuration file will be created the first time an instance is executed at `VOLTTRON_HOME/config`.  

VOLTTRON's configuration file uses a modified INI format where section names are command names for which the settings in
the section apply.  Settings before the first section are considered global and will be used by all commands for which
the settings are valid.  Settings keys are long options (with or without the opening "--") and are followed by a colon
(``:``) or equal (``=``) and then the value.  Boolean options need not include the separator or value, but may specify a
value of ``1``, ``yes``, or ``true`` for `true` or ``0``, ``no``, or ``false`` for `false`.

.. code-block:: config

    [volttron]
    instance-name = volttron1
    vip-address = tcp://127.0.0.1:22916
 
where:

* **instance-name** - Name of the VOLTTRON instance. This has to be unique if multiple instances need to be connected
  together
* **vip-address** - :term:`VIP address` of the VOLTTRON instance. It contains the IP address and port number (default
  port number is 22916)

.. code-block:: bash
   :caption: Start volttron with default config file

   volttron -l volttron.log &

.. code-block:: bash      
   :caption: Start with alternate configuration file

   volttron -c <config> -l volttron.log &

Below is a compendium of commands which can be used to operate the VOLTTRON Platform from the command line interface.


VOLTTRON Platform Command
=========================

The main VOLTTRON platform command is ``volttron``, however this command is seldom run as-is.  In most cases the user
will want to run the platform in the background.  In a limited number of cases, the user will wish to enable verbose
logging.  A typical command to start the platform is:

.. note::

    * All commands and sub-commands have help available with ``-h`` or ``--help``
    * Additional configuration files may be specified with ``-c`` or ``-config``
    * To specify a log file, use ``-l`` or ``--log``
    * The ampersand (``&``) can be added to then end of the command to run the platform in the background, freeing the
      open shell to be used for additional commands.

.. code-block:: bash

    volttron -vv -l volttron.log &


volttron Optional Arguments
---------------------------

- **-c FILE, --config FILE** - Start the platform using the configuration from the provided FILE
- **-l FILE, --log FILE** - send log output to FILE instead of standard output/error
- **-L FILE, --log-config FILE** - Use the configuration from FILE for VOLTTRON platform logging
- **--log-level LOGGER:LEVEL** - override default logger logging level (`INFO`, `DEBUG`, `WARNING`, `ERROR`, `CRITICAL`,
  `NOTSET`)
- **-q, --quiet** - decrease logger verboseness; may be used multiple times to further reduce logging (i.e. ``-qq``)
- **-v, --verbose** - increase logger verboseness; may be used multiple times (i.e. ``-vv``)
- **--verboseness LEVEL** - set logger verboseness level
- **-h, --help** - show this help message and exit
- **--version** - show program's version number and exit

.. note::

    Visit the Python 3 logging documentation for more information about
    `logging and verboseness levels <https://docs.python.org/3/library/logging.html#logging-levels>`_.


Agent Options
-------------

- **--autostart** - automatically start enabled agents and services after platform startup
- **--vip-address ADDR** - Address to bind for VIP connections
- **--instance-name INSTANCE_NAME** - The name of the instance that will be reported to VOLTTRON Central.

.. warning::

   Certain options alter some basic behaviors of the platform, such as `--agent-isolation-mode` which causes the platform
   to run each agent using its own Unix user to spawn the process.  Please view the documentation for each feature to
   understand its implications before choosing to run the platform in that fashion.


volttron-ctl Commands
=====================

`volttron-ctl` (`vctl`) is used to issue commands to the platform from the command line.  Through `volttron-ctl` it is possible
to install and removed agents, start and stop agents, manage the configuration store, get the platform status, and
shutdown the platform.

.. warning::

    `vctl` creates a special temporary agent to communicate with the platform with a specific :term:`VIP Identity`, thus
    multiple instances of `vctl` cannot run at the same time.  Attempting to do so will result in a conflicting
    identity error.

Use `vctl` with one or more of the following arguments, or below sub-commands:


vctl Optional Arguments
-----------------------

- **-c FILE, --config FILE** - Start the platform using the configuration from the provided FILE
- **--debug** - show tracebacks for errors rather than a brief message
- **-t SECS, --timeout SECS** - timeout in seconds for remote calls (default: 60)
- **--vip-address ADDR** - URL to bind for VIP connections
- **-l FILE, --log FILE** - send log output to FILE instead of standard output/error
- **-L FILE, --log-config FILE** - Use the configuration from FILE for VOLTTRON platform logging
- **-q, --quiet** - decrease logger verboseness; may be used multiple times to further reduce logging (i.e. ``-qq``)
- **-v, --verbose** - increase logger verboseness; may be used multiple times (i.e. ``-vv``)
- **--verboseness LEVEL** - set logger verboseness level (this level is a numeric level co
- **--json** - format output to json
- **-h, --help** - show this help message and exit


Commands
--------

- **install** - install an agent from wheel or from an agent package directory

    .. note::

        If --agent-config is not specified then a default config, config.json or config.yml file in the agent
        directory will be used as configuration.  If none present then no configuration file will be loaded.

- **tag AGENT TAG** - set, show, or remove agent tag for a particular agent
- **remove AGENT** - disconnect specified agent from the platform and remove its installed agent package from `VOLTTRON_HOME`
- **peerlist** - list the peers connected to the platform
- **status** - show status of installed agents
- **health AGENT** - show agent health as JSON
- **clear** - clear status of defunct agents
- **enable AGENT** - enable agent to start automatically
- **disable AGENT** - prevent agent from start automatically
- **start AGENT** - start installed agent
- **stop AGENT** - stop agent
- **restart AGENT** - restart agent
- **run PATH** - start any agent by path

    .. note::

       Does *NOT* upgrade agents from the agent's code directory, requires agent wheel file.

- **rpc** - rpc controls
- **certs OPTIONS** - manage certificate creation
- **auth OPTIONS** - manage authorization entries and encryption keys
- **config OPTIONS** - manage the platform configuration store
- **shutdown** - stop all agents (providing the `--platform` optional argument causes the platform to be shutdown)
- **send WHEEL** - send agent and start on a remote platform
- **stats** - manage router message statistics tracking
- **rabbitmq OPTIONS** - manage rabbitmq

.. note::

   For each command with `OPTIONS` in the description, additional options are required to make use of the command.  For
   each, please visit the corresponding section of documentation.

    * :ref:`Auth <VCTL-Auth-Commands>`
    * :ref:`Certs <VCTL-Certs-Commands>`
    * :ref:`Config <VCTL-Config-Commands>`
    * :ref:`RPC <VCTL-RPC-Commands>`

.. note::

    Visit the Python 3 logging documentation for more information about
    `logging and verboseness levels <https://docs.python.org/3/library/logging.html#logging-levels>`_.


.. _VCTL-Auth-Commands:

vctl auth Subcommands
^^^^^^^^^^^^^^^^^^^^^

- **add** - add new authentication record
- **add-known-host** - add server public key to known-hosts file
- **keypair** - generate CurveMQ keys for encrypting VIP connections
- **list** - list authentication records
- **list-known-hosts** - list entries from known-hosts file
- **publickey** - show public key for each agent
- **remove** - removes one or more authentication records by indices
- **remove-known-host** - remove entry from known-hosts file
- **serverkey** - show the serverkey for the instance
- **update** - updates one authentication record by index

.. _VCTL-Certs-Commands:

vctl certs Subcommands
^^^^^^^^^^^^^^^^^^^^^^

- **create-ssl-keypair** - create a SSL keypair
- **export-pkcs12** - create a PKCS12 encoded file containing private and public key from an agent.  This function is
  may also be used to create a Java key store using a p12 file.


.. _VCTL-Config-Commands:

vctl config Subcommands
^^^^^^^^^^^^^^^^^^^^^^^

- **store AGENT CONFIG_NAME CONFIG PATH** - store a configuration file in agent's config store (parses JSON by default,
  use `--csv` for CSV files)
- **edit AGENT CONFIG_NAME** - edit a configuration. (opens nano by default, respects EDITOR env variable)
- **delete AGENT CONFIG_NAME** - delete a configuration from agent's config store (`--all` removes all configs for the
  agent)
- **list AGENT** - list stores or configurations in a store
- **get AGENT CONFIG_NAME** - get the contents of a configuration


.. _VCTL-RPC-Commands:

vctl rpc Subcommands
^^^^^^^^^^^^^^^^^^^^

- **code** - shows how to use RPC call in other agents
- **list** - lists all agents and their RPC methods


