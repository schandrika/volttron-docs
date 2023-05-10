.. _Agent-Development:

=================
Agent Development - TODO
=================

needs update. Has lots of good content about general agent dev but should reword could we update vpkg for modular
----------------------------------------------------------------------------------

To develop a new agent that works with the modular VOLTTRON code, a developer need not clone VOLTTRON core.
The developer only needs a VOLTTRON setup as described in :ref:`platform installation <Platform-Installation>`. Users
can then use a template agent to create a starting point that can be modified for their specific use case

Create Agent Code using copier
==============================

Copier is a program that allows simple question answer format to fill in templates that are
created from a github repository. You can use the copier program with the
`volttron agent template <https://github.com/VOLTTRON/copier-poetry-volttron-agent.git>`_

Pre-requisites for Copier
--------------------------

* Install Python 3.7 or newer (3.8 or newer if you're on Windows).
* Install Git 2.27 or newer.
* Install python3-pip (sudo apt install python3-pip)

Install Copier
--------------
Create a virtual environment and install copier in the activated environment

.. code-block:: bash

    python3 -m venv <path to virtual env dir>
    source <path to virtual env dir>/bin/activate
    pip install copier

Run copier to create agent
---------------------------
Executing the following will start prompting the user for information and then generating a custom agent based upon
the answers

.. code-block:: bash

    copier "https://github.com/VOLTTRON/copier-poetry-volttron-agent.git" /path/to/your/new/project --vcs-ref=HEAD


The Wizard will prompt for the following information:

.. code-block:: bash

    (env) kefei@ubuntu-22:~/project/test-project$ copier "https://github.com/VOLTTRON/copier-poetry-volttron-agent.git" ExampleAgent --vcs-ref=HEAD

    🎤 Your project name

       ExampleAgent

    🎤 Your project description

       Example Agent

    🎤 Your full name

       Kefei Mo

    🎤 Your email

       kefei.mo@pnnl.gov

    🎤 Your username (e.g. on GitHub)

       kefeimo

    🎤 Your repository provider

       github.com

    🎤 Your repository namespace

       kefeimo

    🎤 Your repository name

       exampleagent

    🎤 The name of the person/entity holding the copyright

       Kefei Mo

    🎤 The email of the person/entity holding the copyright

       kefei.mo@pnnl.gov

    🎤 The copyright date

       2023

    🎤 Your project's license

       Apache License 2.0

    🎤 Your Python package distribution name (for `pip install NAME`)

       exampleagent

    🎤 Your Python package import name (for `import NAME` in Python code)

       exampleagent

    🎤 Main class name for your agent

       Exampleagent

    🎤 Your CLI name if any (for use in the shell)

       exampleagent

    🎤 Do you want to use pre-commit?

       No

    Copying from template version 0.3.0b0.post25.dev0+e61c744

        create  .
        create  mypy.ini
        create  config
        create  pyproject.toml
        create  scripts
        create  scripts/post_generation.py
        create  .copier-answers.yml
        create  .pre-commit-config.yaml
        create  src
        create  src/exampleagent
        create  src/exampleagent/__init__.py
        create  src/exampleagent/agent.py
        create  .gitlab-ci.yml
        create  CHANGELOG.md
        create  tests
        create  tests/conftest.py
        create  tests/test_cli.py
        create  docs
        create  docs/source
        create  docs/source/index.rst
        create  docs/source/conf.py
        create  docs/Makefile
        create  LICENSE
        create  CONTRIBUTING.md
        create  .gitignore
        create  .github
        create  .github/workflows
        create  .github/workflows/create_release.yml
        create  .github/workflows/publish_to_pypi.yml
        create  .github/workflows/ci.yml
        create  .github/workflows/code_analysis.yml
        create  .github/ISSUE_TEMPLATE
        create  .github/ISSUE_TEMPLATE/feature_request.md
        create  .github/ISSUE_TEMPLATE/bug_report.md
        create  README.md

     > Running task 1 of 1: python scripts/post_generation.py

    Project successfully generated!

Deactivate virtual environment created for copier
-------------------------------------------------

.. code-block:: bash
    deactivate

Agent Directory
---------------

The above command would have created a ExampleAgent directory with the following structure

::

    (env) kefei@ubuntu-22:~/project/copier-for-chandrika$ tree ExampleAgent/

    ExampleAgent/
    ├── CHANGELOG.md
    ├── config
    ├── CONTRIBUTING.md
    ├── docs
    │   ├── Makefile
    │   └── source
    │   ├── conf.py
    │   └── index.rst
    ├── LICENSE
    ├── mypy.ini
    ├── pyproject.toml
    ├── README.md
    ├── scripts
    ├── src
    │   └── exampleagent
    │     ├── agent.py
    │     └── __init__.py
    └── tests
        ├── conftest.py
        └── test_cli.py
    6 directories, 14 files

Setting up agent environment
----------------------------

The generated agent comes with a pyproject.toml file that can be used to install the agent locally for development.
Update the pyproject.toml with the correct version of volttron you want to use and the python version in your
environment. VOLTTRON support python version >= 3.10 <4.0. Also add any additional dependencies your agent may require.
Once you update the pyproject.toml file, run the following command from within the ExampleAgent directory

.. code-block:: bash
    poetry install

The ```poetry install``` command will create a virtual environment and pull down all the dependencies for the
ExampleAgent. Now the agent is ready for development. You can open the ExampleAgent directory in an IDE of your choice
(ex. Pycharm, VS code etc), point to the python in the virtual environment created by poetry and start updating the
agent code.

Agent Skeleton
--------------

The `agent.py` file in the `ExampleAgent/src/exampleagent` directory of the newly created agent module will contain
skeleton code (below). Descriptions of the features of this code as well as additional development help are found in
the rest of this document.

.. code-block:: python

    """
    Agent documentation goes here.
    For a quick tutorial on Agent Development, see https://volttron.readthedocs.io/en/develop/developing-volttron/developing-agents/agent-development.html#agent-development
    """

    import logging
    import sys
    from pprint import pformat
    import datetime

    from volttron import utils
    from volttron.utils.commands import vip_main
    from volttron.client.messaging.health import STATUS_GOOD
    from volttron.client.vip.agent import Agent, Core, PubSub, RPC
    from volttron.client.vip.agent.subsystems.query import Query

    # from . import __version__
    __version__ = "0.1.0"

    # Setup logging so that it runs within the platform
    utils.setup_logging()

    # The logger for this agent is _log and can be used throughout this file.
    _log = logging.getLogger(__name__)


    def exampleagent(config_path, **kwargs):
        """
        Parses the Agent configuration and returns an instance of
        the agent created using that configuration.

        :param config_path: Path to a configuration file.
        :type config_path: str
        :returns: Exampleagent
        :rtype: Exampleagent
        """
        try:
            config = utils.load_config(config_path)
        except Exception:
            config = {}

        if not config:
            _log.info("Using Agent defaults for starting configuration.")

        setting1 = int(config.get('setting1', 1))
        setting2 = config.get('setting2', "some/random/topic")

        return Exampleagent(setting1, setting2, **kwargs)


    class Exampleagent(Agent):
        """
        Exampleagent is an example file that listens to the message bus and prints it to the log.
        """

        def __init__(self, setting1=1, setting2="some/random/topic", **kwargs):
            super(Exampleagent, self).__init__(**kwargs)
            _log.debug("vip_identity: " + self.core.identity)

            self.setting1 = setting1
            self.setting2 = setting2
            # Runtime limit allows the agent to stop automatically after a specified number of seconds.
            self.runtime_limit = 0

            self.default_config = {"setting1": setting1,
                                   "setting2": setting2}
            # Set a default configuration to ensure that self.configure is called immediately to setup
            # the agent.
            self.vip.config.set_default("config", self.default_config)
            # Hook self.configure up to changes to the configuration file "config".
            self.vip.config.subscribe(self.configure, actions=["NEW", "UPDATE"], pattern="config")

        def configure(self, config_name, action, contents):
            """
            Called after the Agent has connected to the message bus. If a configuration exists at startup
            this will be called before onstart.

            Is called every time the configuration in the store changes.
            """
            config = self.default_config.copy()
            config.update(contents)

            _log.debug("Configuring Agent")

            try:
                setting1 = int(config["setting1"])
                setting2 = str(config["setting2"])
            except ValueError as e:
                _log.error("ERROR PROCESSING CONFIGURATION: {}".format(e))
                return

            self.setting1 = setting1
            self.setting2 = setting2
            self.runtime_limit = int(config.get('runtime_limit', 0))

            self._set_runtime_limit()
            self._create_subscriptions(self.setting2)

        def _set_runtime_limit(self):
            if not self.runtime_limit and self.runtime_limit > 0:
                stop_time = datetime.datetime.now() + datetime.timedelta(seconds=self.runtime_limit)
                _log.info('Exampleagent agent will stop at {}'.format(stop_time))
                self.core.schedule(stop_time, self.core.stop)
            else:
                _log.info('No valid runtime_limit configured; Exampleagent agent will run until manually stopped')

        def _create_subscriptions(self, topic):
            """
            Unsubscribe from all pub/sub topics and create a subscription to a topic in the configuration which triggers
            the _handle_publish callback
            """
            self.vip.pubsub.unsubscribe("pubsub", None, None)

            self.vip.pubsub.subscribe(peer='pubsub',
                                      prefix=topic,
                                      callback=self._handle_publish)

        def _handle_publish(self, peer, sender, bus, topic, headers, message):
            """
            Callback triggered by the subscription setup using the topic from the agent's config file
            """
            pass

        @Core.receiver("onstart")
        def onstart(self, sender, **kwargs):
            """
            This is method is called once the Agent has successfully connected to the platform.
            This is a good place to setup subscriptions if they are not dynamic or
            do any other startup activities that require a connection to the message bus.
            Called after any configurations methods that are called at startup.

            Usually not needed if using the configuration store.
            """
            # Example publish to pubsub
            # self.vip.pubsub.publish('pubsub', "some/random/topic", message="HI!")

            # Example RPC call
            # self.vip.rpc.call("some_agent", "some_method", arg1, arg2)
            pass

        @Core.receiver("onstop")
        def onstop(self, sender, **kwargs):
            """
            This method is called when the Agent is about to shutdown, but before it disconnects from
            the message bus.
            """
            pass

        @RPC.export
        def rpc_method(self, arg1, arg2, kwarg1=None, kwarg2=None):
            """
            RPC method

            May be called from another agent via self.vip.rpc.call
            """
            return self.setting1 + arg1 - arg2

        @PubSub.subscribe('pubsub', '', all_platforms=True)
        def on_match(self, peer, sender, bus, topic, headers, message):
            """Use match_all to receive all messages and print them out."""
            self._logfn(
                "Peer: {0}, Sender: {1}:, Bus: {2}, Topic: {3}, Headers: {4}, "
                "Message: \n{5}".format(peer, sender, bus, topic, headers, pformat(message)))


    def main():
        """
        Main method called during startup of agent.
        :return:
        """
        try:
            vip_main(exampleagent, version=__version__)
        except Exception as e:
            _log.exception('unhandled exception')


    if __name__ == '__main__':
        # Entry point for script
        try:
            sys.exit(main())
        except KeyboardInterrupt:
            pass


The resulting code is well documented with comments and documentation strings. It gives examples of how to do common
tasks in VOLTTRON Agents.  The main agent code is found in `ExampleAgent/src/exampleagent/agent.py`.


Building an Agent
=================

The following section includes guidance on several important components for building agents in VOLTTRON.


Parse Packaged Configuration and Create Agent Instance
------------------------------------------------------

The code to parse a configuration file packaged and installed with the agent is found in the `tester` function:

.. code-block:: python

    def exampleagent(config_path, **kwargs):
        """
        Parses the Agent configuration and returns an instance of
        the agent created using that configuration.

        :param config_path: Path to a configuration file.
        :type config_path: str
        :returns: Tester
        :rtype: Tester
        """
        try:
            config = utils.load_config(config_path)
        except Exception:
            config = {}

        if not config:
            _log.info("Using Agent defaults for starting configuration.")

        setting1 = int(config.get('setting1', 1))
        setting2 = config.get('setting2', "some/random/topic")

        return Exampleagent(setting1, setting2, **kwargs)

The configuration is parsed with the `utils.load_config` function and the results are stored in the `config` variable.
An instance of the Agent is created from the parsed values and is returned.


Initialization and Configuration Store Support
----------------------------------------------

The :ref:`configuration store <Agent-Configuration-Store-Interface>` is a powerful feature.  The agent template provides
a simple example of setting up default configuration store values and setting up a configuration handler.

.. code-block:: python

    class Exampleagent(Agent):
        """
        Exampleagent is an example file that listens to the message bus and prints it to the log.
        """


        def __init__(self, setting1=1, setting2="some/random/topic", **kwargs):
            super(Exampleagent, self).__init__(**kwargs)
             _log.debug("vip_identity: " + self.core.identity)

            self.setting1 = setting1
            self.setting2 = setting2
            # Runtime limit allows the agent to stop automatically after a specified number of seconds.
            self.runtime_limit = 0

            self.default_config = {"setting1": setting1,
                                   "setting2": setting2}
            # Set a default configuration to ensure that self.configure is called immediately to setup
            # the agent.
            self.vip.config.set_default("config", self.default_config)
            # Hook self.configure up to changes to the configuration file "config".
            self.vip.config.subscribe(self.configure, actions=["NEW", "UPDATE"], pattern="config")

        def configure(self, config_name, action, contents):
            """
            Called after the Agent has connected to the message bus. If a configuration exists at startup
            this will be called before onstart.

            Is called every time the configuration in the store changes.
            """
            config = self.default_config.copy()
            config.update(contents)

            _log.debug("Configuring Agent")

            try:
                setting1 = int(config["setting1"])
                setting2 = str(config["setting2"])
            except ValueError as e:
                _log.error("ERROR PROCESSING CONFIGURATION: {}".format(e))
                return

            self.setting1 = setting1
            self.setting2 = setting2
            self.runtime_limit = int(config.get('runtime_limit', 0))

            self._set_runtime_limit()
            self._create_subscriptions(self.setting2)

        def _set_runtime_limit(self):
            if not self.runtime_limit and self.runtime_limit > 0:
                stop_time = datetime.datetime.now() + datetime.timedelta(seconds=self.runtime_limit)
                _log.info('Exampleagent agent will stop at {}'.format(stop_time))
                self.core.schedule(stop_time, self.core.stop)
            else:
                _log.info('No valid runtime_limit configured; Exampleagent agent will run until manually stopped')

.. note::

    Support for the configuration store is instantiated by subscribing to configuration changes with
    `self.vip.config.subscribe`.

    .. code-block:: python

        self.vip.config.subscribe(self.configure_main, actions=["NEW", "UPDATE"], pattern="config")

Values in the default config can be built into the agent or come from the packaged configuration file. The subscribe
method tells our agent which function to call whenever there is a new or updated config file. For more information
on using the configuration store see :ref:`Agent Configuration Store <Agent-Configuration-Store-Interface>`.

`_create_subscriptions` (covered in a later section) will use the value in `self.setting2` to create a new subscription.


Agent Lifecycle Events
----------------------

The agent lifecycle is controlled in the agents VIP `core`.  The agent lifecycle manages :ref:`scheduling and periodic
function calls <Agent-Periodics-Scheduling>`, the main agent loop, and trigger a number of signals for callbacks in the
concrete agent code.  These callbacks are listed and described in the skeleton code below:

.. note::

   The lifecycle signals can trigger any method.  To cause a method to be triggered by a lifecycle signal, use a
   decorator:

    .. code-block:: python

        @Core.receiver("<lifecycle_method>")
        def my_callback(self, sender, **kwargs):
            # do my lifecycle method callback
            pass

.. code-block:: python

    @Core.receiver("onsetup")
    def onsetup(self, sender, **kwargs)
        """
        This method is called after the agent has successfully connected to the platform, but before the scheduled
        methods loop has started.  This method not often used, but is most commonly used to define periodic
        functions or do some pre-configuration.
        """
        self.vip.core.periodic(60, send_request)

    @Core.receiver("onstart")
    def onstart(self, sender, **kwargs):
        """
        This method is called once the Agent has successfully connected to the platform.
        This is a good place to setup subscriptions if they are not dynamic or to
        do any other startup activities that require a connection to the message bus.
        Called after any configurations methods that are called at startup.

        Usually not needed if using the configuration store.
        """
        #Example publish to pubsub
        self.vip.pubsub.publish('pubsub', "some/random/topic", message="HI!")

        #Example RPC call
        self.vip.rpc.call("some_agent", "some_method", arg1, arg2)

    @Core.receiver("onstop")
    def onstop(self, sender, **kwargs):
        """
        This method is called when the Agent is about to shutdown, but before it disconnects from
        the message bus.  Common use-cases for this method are to stop periodic processing, closing connections and
        setting agent state prior to cleanup.
        """
        self.publishing = False
        self.cache.close()

    @Core.receiver("onfinish")
    def onfinish(self, sender, **kwargs)
        """
        This method is called after all scheduled threads have concluded.  This method is rarely used, but could be
        used to send shut down signals to other agents, etc.
        """
        self.vip.pubsub.publish('pubsub', 'some/topic', message=f'agent {self.core.identity} shutdown')


.. _Agent-Periodics-Scheduling:

Periodics and Scheduling
------------------------

Periodic and Scheduled callback functions are callbacks made to functions in agent code from the thread scheduling in
the agent core.


Scheduled Callbacks
^^^^^^^^^^^^^^^^^^^

Scheduled callback functions are often used similarly to cron jobs to perform tasks at specific times, or to schedule
tasks ad-hoc as agent state is updated.  There are 2 ways to schedule callbacks: using a decorator, or calling the
core's scheduling function.  Example usage follows.

.. code-block:: python

    # using the agent's core to schedule a task
    self.core.schedule(periodic(5), self.sayhi)

    def sayhi(self):
        print("Hello-World!")

.. code-block:: python

    # using the decorator to schedule a task
    @Core.schedule(cron('0 1 * * *'))
    def cron_function(self):
       print("this is a cron-scheduled function")

.. note::

    Scheduled Callbacks can use CRON scheduling, a datetime object, a number of seconds (from current time), or a
    `periodic` which will make the schedule function as a periodic.

    .. code-block:: python

        # inside some agent method
        self.core.schedule(t, function)
        self.core.schedule(periodic(t), periodic_function)
        self.core.schedule(cron('0 1 * * *'), cron_function)


Periodic Callbacks
^^^^^^^^^^^^^^^^^^

Periodic call back functions are functions which are repeatedly called at a regular interval until the periodic is
cancelled in the agent code or the agent stops running.  Like scheduled callbacks, periodics can be specified using
either decorators or using core function calls.

.. code-block:: python

    self.core.periodic(10, self.saybye)

    def saybye(self):
        print('Good-bye Cruel World!')

.. code-block:: python

    @Core.periodic(60)
    def poll_api(self):
        return requests.get("https://lmgtfy.com").json()

.. note::

    Periodic intervals are specified in seconds.


Publishing Data to the Message Bus
----------------------------------

The agent's VIP connection can be used to publish data to the message bus.  The message published and topic to publish
to are determined by the agent implementation.

.. code-block:: python

    def publish_oscillating_update(self):
        """
        Publish an "oscillating_value" which cycles between values 1 and 0 to the message bus using the topic
        "some/topic/oscillating_value"
        """
        self.publish_value = 1 if self.publish_value = 0 else 0
        self. vip.pubsub.publish('pubsub', 'some/topic/', message=f'{"oscillating_value": "{self.publish_value}"')


Setting up a Subscription
-------------------------

The Agent creates a subscription to a topic on the message bus using the value of `self.setting2` in the method
`_create_subscription`. The messages for this subscription are handled with the `_handle_publish` method:

.. code-block:: python

    def _create_subscriptions(self, topic):
        """
        Unsubscribe from all pub/sub topics and create a subscription to a topic in the configuration which triggers
        the _handle_publish callback
        """
        # Unsubscribe from everything.
        self.vip.pubsub.unsubscribe("pubsub", None, None)

        self.vip.pubsub.subscribe(peer='pubsub',
                                  prefix=topic,
                                  callback=self._handle_publish)

    def _handle_publish(self, peer, sender, bus, topic, headers, message):
        """
        Callback triggered by the subscription setup using the topic from the agent's config file
        """
        # By default no action is taken.
        pass

Alternatively, a decorator can be used to specify the function as a callback:

.. code-block:: python

    @PubSub.subscribe('pubsub', "topic_prefix")
    def _handle_publish(self, peer, sender, bus, topic, headers, message):
        """
        Callback triggered by the subscription setup using the topic from the agent's config file
        """
        # By default no action is taken.
        pass

`self.vip.pubsub.unsubscribe` can be used to unsubscribe from a topic:

.. code-block:: python

    self.vip.pubsub.unsubscribe(peer='pubsub',
                                prefix=topic,
                                callback=self._handle_publish)

Giving ``None`` as values for the prefix and callback argument will unsubscribe from everything on that bus.  This is
handy for subscriptions that must be updated base on a configuration setting.


Heartbeat
^^^^^^^^^

The heartbeat subsystem provides access to a periodic publish so that others can observe the agent's status.  Other
agents can subscribe to the `heartbeat` topic to see who is actively publishing to it.  It it turned off by default.

Enabling the `heartbeat` publish:

.. code-block:: python

    self.vip.heartbeat.start_with_period(self._heartbeat_period)

Subscribing to the heartbeat topic:

.. code-block:: python

    self.vip.pubsub.subscribe(peer='pubsub',
                              prefix='heartbeat',
                              callback=handle_heartbeat)


Health
^^^^^^

The health subsystem adds extra status information to the an agent's heartbeat.  Setting the status will start the
heartbeat if it wasn't already.  Health is used to represent the internal state of the agent at runtime.  `GOOD` health
indicates that all is fine with the agent and it is operating normally.  `BAD` health indicates some kind of problem,
such as if an agent is unable to reach a remote web API.

Example of setting health:

.. code-block:: python

    from volttron.client.messaging.health import STATUS_BAD, STATUS_GOOD,

    self.vip.health.set_status(STATUS_GOOD, "Configuration of agent successful")


Remote Procedure Calls
----------------------

An agent may receive commands from other agents via a Remote Procedure Call (RPC).
This is done with the `@RPC.export` decorator:

.. code-block:: python

    @RPC.export
    def rpc_method(self, arg1, arg2, kwarg1=None, kwarg2=None):
        """
        RPC method. May be called from another agent via self.vip.rpc.call
        """
        return self.setting1 + arg1 - arg2

To send an RPC call to another agent running on the platform, the agent must invoke the `rpc.call` method of its VIP
connection.

.. code-block:: python

    # in agent code
    def send_remote_procedure_call(self):
        peer = "<agent identity>"
        peer_method = "<method in peer agent API>"
        args = ["list", "of", "peer", "method", "arguments", "..."]
        self.vip.rpc.call(peer, peer_method, *args)


Agent Resiliency
----------------

The VOLTTRON team has come up with a number of methods to help users develop more robust agents.

#. Use `gevent.sleep(<seconds>)` in callbacks which perform long running functions.  Long running functions can cause
   other agent functions including those in the base agent to be delayed. Calling `gevent.sleep` transfers control from
   the current executing greenlet to the next scheduled greenlet for the duration of the sleep, allowing other
   components of the agent code to run.
#. Call `.get(<timeout>) on VIP subsystem calls (i.e. ``self.vip.rpc.call(...).get()``) to ensure that the call
   returns a value or throws an Exception in a timely manner.  A number of seconds can be provided to specify a timeout
   duration.
#. Many of the :ref:`Operations Agents <Operations-Agents>` can be used to monitor agent health, status, publishing
   frequency and more.  Read up on the "ops agents" for more information.(TODO. These agents are not ported to modular
   code yet.)

    .. note::

       If an agent crashes, becomes unreachable, etc., it is up to the user to restart or reconnect the agent.

#. The main agent thread should monitor any spawned threads or processes to ensure they're cleaned up and/or exit
   safely.


Building a resilient API
^^^^^^^^^^^^^^^^^^^^^^^^

Many agents export RPC calls or expose an API (application programming interface) which can be used by other agents
on the platform.  The agent should include validation against input data for its API to ensure the agent is able to
continue to operate even if asked to handle faulty or malicious requests.


Type-hints
""""""""""

`Type-hints <https://docs.python.org/3/library/typing.html>`_ can be used in function definitions to help the user
determine what the agent expects as input.

.. warning::

 Type-hints do not validate the type of data input to a function call, they are merely suggestions about what the
 function is expecting.

* To specify the type expected as input:

.. code-block:: python

   # When calling this RPC method, the user should supply a string as input
   @RPC.export
   def type_hint_rpc(input_string: str):

* To specify the type of function output:

.. code-block:: python

   # This demonstrates a function that expects a string as input and that will return an integer value
   @RPC.export
   def type_hint_rpc(input_string: str) -> int:

* Specifying multiple types:

.. code-block:: python

    # Here our function expects either a string or dictionary
    @RPC.export
    def type_hint_rpc(input_json: Union[str, dict]) -> str:

* To specify an optional argument with None as the default value:

.. code-block:: python

    # 'Optional' is used to specify either a string should be passed or the default value 'None' will be used
    @RPC.export
    def type_hint_rpc(optional_input: Optional[str] = None) -> str:

* These techniques can be combined:

.. code-block:: python

    # 'Optional' can be used in combination with 'Union' for optional arguments which expect one of multiple types and
    # default to None
    @RPC.export
    def type_hint_rpc(optional_input: Optional[Union[str, dict]] = None) -> str:


API Validation
""""""""""""""

Each function within an agent should validate its input parameters, especially with structured data.

* Make use of isinstance to do type checking:

    .. code-block:: python

       @RPC.export
       def type_checking_rpc(input_str: str) -> dict:
           if not isinstance(input_str, str):
               # Include a descriptive error message to help the user determine why input validation failed
               # You can make use of 'f-strings' to help the user with debugging
               raise ValueError(
                   f'The expected input type for function "type_checking_rpc" is str, received {type(input_str)}')

* Add logic to validate the range of values supplied as input with a valid type:

    .. code-block:: python

       @RPC.export
       def value_checking_rpc(input_json: Union[str, dict]) -> dict:
           if not isinstance(input_json, str) or not isinstance(input_json, dict):
               # You can make use of 'f-strings' to help the user determine why input validation failed
               raise ValueError(
                   f'The expected input type for function "type_checking_rpc" is str or dict, received {type(input_str)}')
           else:
               # since we expected the input to be valid JSON, be sure that it can be correctly parsed
               if isinstance(input_json, str):
                   input_json = json.loads(input_json)
               # for this example, we expect our JSON to include two fields: test1 and test2
               # Use 'dict.get(<key>)' rather than 'dict[<key>]' to return None and avoid causing a KeyError if the key
               #  is not present.  Optionally, a second argument can be added to specify a default value to use in
               # place of None: 'dict.get(<key>, <default value>)'
               test_1 = input_json.get("test1")
               test_2 = input_json.get("test2")
               # test 1 must be any string value
               if not isinstance(test_1, str):
                    raise ValueError('Input JSON should contain key "test1" with value of type str')
               # test 2 must be an integer value with value between 0 and 100 inclusive
               if not isinstance(test_2, int) and 0 <= test_2 <= 100:
                    _log.warning(f'Field "test2" in input JSON was out of range (0 - 100): {test_2}, defaulting to 50')
                    test_2 = 50

.. note::

   It is possible to restrict access to RPC functions using an :ref:`agent's authentication <Agent-Authentication>`
   capabilities.


Packaging Configuration
=======================

The wizard will automatically create a `setup.py` file. This file sets up the name, version, required packages, method
to execute, etc. for the agent based on your answers to the wizard. The packaging process will also use this
information to name the resulting file.

.. code-block:: python

    from setuptools import setup, find_packages

    MAIN_MODULE = 'agent'

    # Find the agent package that contains the main module
    packages = find_packages('.')
    agent_package = 'tester'

    # Find the version number from the main module
    agent_module = agent_package + '.' + MAIN_MODULE
    _temp = __import__(agent_module, globals(), locals(), ['__version__'], -1)
    __version__ = _temp.__version__

    # Setup
    setup(
        name=agent_package + 'agent',
        version=__version__,
        author_email="volttron@pnnl.gov",
        url="https://volttron.org/",
        description="Agent development tutorial.",
        author="VOLTTRON Team",
        install_requires=['volttron'],
        packages=packages,
        entry_points={
            'setuptools.installation': [
                'eggsecutable = ' + agent_module + ':main',
            ]
        }
    )


Launch Configuration
====================

In TestAgent, the wizard will automatically create a JSON file called "config". It contains configuration information
for the agent.  This file contains examples of every data type supported by the configuration system:

::

    {
      # VOLTTRON config files are JSON with support for python style comments.
      "setting1": 2, # Integers
      "setting2": "some/random/topic2", #Strings
      "setting3": true, # Booleans: remember that in JSON true and false are not capitalized.
      "setting4": false,
      "setting5": 5.1, # Floating point numbers.
      "setting6": [1,2,3,4], #Lists
      "setting7": {"setting7a": "a", "setting7b": "b"} #Objects
    }


.. _Agent-Packaging-and-Install:

Agent Installation
==================

To install the agent the platform must be running. Start the platform with the command:

.. code-block:: bash

    volttron

.. note::

    If you are not in an activated environment, this script will start the platform running in the background in the
    correct environment. However the environment will not be activated for you; you must activate it yourself.

Now we must install it into the platform. Use the following command to install it and add a tag for easily referring to
the agent. From the project directory, run the following command:

.. code-block:: bash



To verify it has been installed, use the following command:

.. code-block:: bash

    vctl status

This will result in output similar to the following:

.. code-block:: bash

      AGENT                    IDENTITY           TAG        Status     Health      PRI
  df  testeragent-0.5          testeragent-0.5_1  testagent

* The first string is a unique portion of the full UUID for the agent
* AGENT is the "name" of the agent based on the contents of its class name and the version in its setup.py.
* IDENTITY is the agent's identity in the platform. This is automatically assigned based on class name and instance
  number. This agent's ID is _1 because it is the first instance.
* TAG is the name we assigned in the command above
* Status indicates the running status of an agent - running agents are *running*, agents which are not running will have
  no listed status
* Health is an indication of the internal state of the agent.  'Healthy' agents will have GOOD health.  If an agent
  enters an error state, it will continue to run, but its health will be BAD.
* PRI is the priority for agents which have been "enabled" using the ``vctl enable`` command.

When using lifecycle commands on agents, they can be referred to by the UUID (default) or AGENT (name) or TAG.


Running and Testing the Agent
=============================

Now that the first pass of the agent code is complete, we can see if the agent works.  It is highly-suggested to build
a set of automated tests for the agent code prior to writing the agent, and running those tests after the agent is
code-complete.  Another quick way to determine if the agent is going the right direction is to run the agent on the
platform using the VOLTTRON command line interface.


From the Command Line
---------------------

To test the agent, we will start the platform (if not already running), launch the agent, and check the log file.
With the VOLTTRON environment activated, start the platform by running (if needed):

.. code-block:: bash

    ./start-volttron

You can launch the agent in three ways, all of which you can find by using the `vctl list` command:

* By using the <uuid>:

.. code-block:: bash

    vctl start <uuid>

* By name:

.. code-block:: bash

    vctl start --name testeragent-0.1

* By tag:

.. code-block:: bash

    vctl start --tag testagent

Check that it is :ref:`running <Agent-Status>`:

.. code-block:: bash

    vctl status

* Start the ListenerAgent as in the :ref:`platform installation guide <Platform-Installation>`.
* Check the log file for messages indicating the TestAgent is receiving the ListenerAgents messages:

.. code-block:: console

    2021-01-12 16:46:58,291 (listeneragent-3.3 12136) __main__ INFO: Peer: pubsub, Sender: testeragent-0.1_1:, Bus: , Topic: some/random/topic, Headers: {'min_compatible_version': '5.0', 'max_compatible_version': ''}, Message: 'HI!'


Automated Test Cases and Documentation
--------------------------------------

Before contributing a new agent to the VOLTTRON source code repository, please consider adding two other essential
elements.

1. Integration and unit test cases
2. README file that includes details of pre-requisite software, agent setup details (such as setting up databases,
   permissions, etc.) and sample configuration

VOLTTRON uses *pytest* as a framework for executing tests.  All unit tests should be based on the *pytest* framework.
For instructions on writing unit and integration tests with *pytest*, refer to the
:ref:`Writing Agent Tests <Writing-Agent-Tests>` documentation.

*pytest* is not installed with the distribution by default. To install py.test and it's dependencies execute the
following:

.. code-block:: bash

    python bootstrap.py --testing

.. note::

  There are other options for different agent requirements.  To see all of the options use:

  .. code-block:: bash

      python bootstrap.py --help

  in the Extra Package Options section.

To run a single test module, use the command

.. code-block:: bash

    pytest <testmodule.py>

To run all of the tests in the volttron repository execute the following in the root directory using an activated
command prompt:

.. code-block:: bash

    ./ci-integration/run-tests.sh


.. _Utility-Scripts:

Scripts
=======

In order to make repetitive tasks less repetitive the VOLTTRON team has create several scripts in order to help.  These
tasks are available in the `scripts` directory.

.. note::

    In addition to the `scripts` directory, the VOLTTRON team has added the config directory to the .gitignore file.  By
    convention this is where we store customized scripts and configuration that will not be made public.  Please feel
    free to use this convention in your own processes.

The `scripts/core` directory is laid out in such a way that we can build scripts on top of a base core.  For example the
scripts in sub-folders such as the `historian-scripts` and `demo-comms` use the scripts that are present in the core
directory.

The most widely used script is `scripts/install-agent.py`.  The `install_agent.py` script will remove an agent if the
tag is already present, create a new agent package, and install the agent to :term:`VOLTTRON_HOME`.  This script has
three required arguments and has the following signature:

.. note::

    Agent to Package must have a setup.py in the root of the directory.  Additionally, the user must be in an activated
    Python Virtual Environment for VOLTTRON

    .. code-block:: bash

      cd $VOLTTRON_ROOT
      source env/bin/activate

.. code-block:: console

   python scripts/install_agent.py -s <agent path> -c <agent config file> -i <agent VIP identity> --tag <Tag>

.. note::

   The ``--help`` optional argument can be used with `scripts/install-agent.py` to view all available options for the
   script

The `install_agent.py` script will respect the `VOLTTRON_HOME` specified on the command line or set in the global
environment.  An example of setting `VOLTTRON_HOME` to `/tmp/v1home` is as follows.

.. code-block:: bash

    VOLTTRON_HOME=/tmp/v1home python scripts/install-agent.py -s <Agent to Package> -c <Config file> --tag <Tag>


.. toctree::
   :hidden:
   :maxdepth: 1

   agent-configuration-store
   writing-agent-tests
   documenting-agents
   using-asyncio-in-agents

..

   developing-historian-agents  - should point to externally pulled in data
   example-agents/index - should point to data pulled from different repo at a later point

