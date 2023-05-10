.. _Writing-Agent-Tests:

===================
Writing Agent Tests
===================

The VOLTTRON team strongly encourages developing agents with a set of unit and integration tests.  Test-driven
development can save developers significant time and effort by clearly defining behavioral expectations for agent code.
We recommend developing agent tests using Pytest.  Agent code contributed to VOLTTRON is expected to include a set of
tests using Pytest in the agent module directory.  Following are instructions for setting up Pytest, structuring your
tests, how to write unit and integration tests (including some helpful tools using Pytest and Mock) and how to run your
tests.


Installation
============

To get started with Pytest, install it in an activated environment:

.. code-block:: bash

    pip install pytest

`Pytest on PyPI <https://pypi.org/project/pytest/>`_


Module Structure
================

We suggest the following structure for your agent module:

::

    ├── UserAgent
    │   ├── src
    │   │   ├── agent_name_package
    │   │   │  └── data
    │   │   │     └── user_agent_data.csv
    │   │   ├── __init__.py
    │   │   └── agent.py
    │   ├── tests
    │   │   └── test_user_agent.py
    │   │   └── contest.py
    │   ├── README.md
    │   ├── config
    │   ├── LICENSE
    │   └── pyproject.toml

The test suite should be in a `tests` directory in the root agent directory, and should contain one or more
test code files (with the `test_<name of test>` convention). `conftest.py` can be used to give all agent tests
access to some portion of the VOLTTRON code. In many cases, agents use `conftest.py` to import VOLTTRON testing
fixtures for integration tests.


Naming Conventions
------------------

Pytest tests are discovered and run using some conventions:

    * Tests will be found recursively in either the directory specified when running Pytest, or the current
      working directory if no argument was supplied
    * Pytest will search in those directories for files called test_<name of test>.py or <name of test>_test.py
    * In those files, Pytest will test:
        * functions and methods prefixed by "test" outside of any class
        * functions and methods prefixed by "test" inside of any class prefixed by "test"

::

    ├── TestDir
    │   ├── MoreTests
    │   │   ├── test2.py
    │   ├── test1.py
    │   └── file.py

.. code-block:: python

    # test1.py

    def helper_method():
        return 1

    def test_success():
        assert helper_method()

    # test2.py

    def test_success():
        assert True

    def test_fail():
        assert False

    # file.py

    def test_success():
        assert True

    def test_fail():
        assert False

In the above example, Pytest will run the tests `test_success` from the file test1.py and `test_success` and test_fail
from test2.py.  No tests will be run from file.txt, even though it contains test code, nor will it try to run
`helper_method` from test1.py as a test.


Writing Unit Tests
==================

These tests should test the various methods of the code base, checking for success and fail conditions. These tests
should capture how the components of the system should function; and describe all the possible output
conditions given the possible range of inputs including how they should fail if given improper input.

`Pytest guide to Unit Testing <https://docs.python-guide.org/writing/tests/#unittest>`_

Pytest Tools
------------

Pytest includes many helpful tools for developing your tests. We'll highlight a few that have been useful for
VOLTTRON core tests, but checkout `the Pytest documentation <https://docs.pytest.org/>`_ for additional information on
each tool as well as tools not covered in this guide.


Pytest Fixtures
^^^^^^^^^^^^^^^

Pytest fixtures can be used to create reusable code for tests that can be accessed by every test in a module based on
scope.  There are several kinds of scopes, but commonly used are "module" (the fixture is run once per module for all
the tests of that module) or "function" (the fixture is run once per test).  For fixtures to be used by tests, they
should be passed as parameters.

`Pytest Fixture documentation <https://docs.pytest.org/en/latest/fixture.html>`_

Here is an example of a fixture, along with using it in a test:

.. code-block:: python

    # Fixtures with scope function will be run once per test if the test accepts the fixture as a parameter
    @pytest.fixture(scope="function")
    def cleanup_database():
        # This fixture cleans up a sqlite database in between each test run
        sqlite_conn = sqlite.connect("test.sqlite")
        cursor = sqlite_conn.cursor()
        cursor.execute("DROP TABLE 'TEST'")
        cursor.commit()

        cursor.execute("CREATE TABLE TEST (ID INTEGER, FirstName TEXT, LastName TEXT, Occupation Text)")
        cursor.commit()
        sqlite.conn.close()

    # when we pass the cleanup function, we expect that the table will be dropped and rebuilt before the test runs
    def test_store_data(cleanup_database):
        sqlite_conn = sqlite.connect("test.sqlite")
        cursor = sqlite_conn.cursor()
        # after this insert, we'd expect to only have 1 value in the table
        cursor.execute("INSERT INTO TEST VALUES(1, 'Test', 'User', 'Developer')")
        cursor.commit()

        # validate the row count
        cursor.execute("SELECT COUNT(*) FROM TEST")
        count = cursor.fetchone()
        assert count == 1


Pytest.mark
^^^^^^^^^^^

Pytest marks are used to set metadata for test functions. Defining your own custom marks can allow you to run
subsections of your tests.  Parametrize can be used to pass a series of parameters to a test, so that it can be run
many times to cover the space of potential inputs.  Marks also exist to specify expected behavior for tests.

`Mark documentation <https://docs.pytest.org/en/latest/mark.html>`_


Custom Marks
""""""""""""

To add a custom mark, add the name of the mark followed by a colon then a description string to the 'markers' section
of Pytest.ini (an example of this exists in the core VOLTTRON repository).  Then add the appropriate decorator:

.. code-block:: python

    @pytest.mark.UserAgent
    def test_success_case():
        # TODO unit test here
        pass

The VOLTTRON team also has a `dev` mark for running individual (or a few) one-off tests.

.. code-block:: python

    @pytest.mark.dev
    @pytest.mark.UserAgent
    def test_success_case():
        # TODO unit test here
        pass


Parametrize
"""""""""""

Parametrize will allow tests to be run with a variety of parameters. Add the parametrize decorator, and for parameters
include a list of parameter names matching the test parameter names as a comma-delimited string followed by a list of
tuples containing parameters for each test.

`Parametrize docs <https://docs.pytest.org/en/latest/parametrize.html>`_

.. code-block:: python

    @pytest.mark.parametrize("test_input1, test_input2, expected", [(1, 2, 3), (-1, 0, "")])
    def test_user_agent(param1, param2, param3):
        # TODO unit test here
        pass


Skip, skipif, and xfail
"""""""""""""""""""""""

The `skip` mark can be used to skip a test for any reason every time the test suite is run:

.. code-block:: python

    # This test will be skipped!
    @pytest.mark.skip
    def test_user_agent():
        # TODO unit test here
        pass

The `skipif` mark can be used to skip a test based on some condition:

.. code-block:: python

    # This test will be skipped if RabbitMQ hasn't been set up yet!
    @pytest.mark.skipif(not isRabbitMQInstalled)
    def test_user_agent():
        # TODO unit test here
        pass

The `xfail` mark can be used to run a test, but to show that the test is currently expected to fail

.. code-block:: python

    # This test will fail, but will not cause the module tests to be considered failing!
    @pytest.mark.xfail
    def test_user_agent():
        # TODO unit test here
        assert False

`Skip, skipif, and xfail docs <https://docs.pytest.org/en/documentation-restructure/how-to/skipping.html>`_


Writing Integration Tests
=========================

Integration tests are useful for testing the faults that occur between integrated units.  In the context of VOLTTRON
agents, integration tests should test the interactions between the agent, the platform, and other agents installed on
the platform that would interface with the agent.  It is typical for integration tests to test configuration, behavior
and content of RPC calls and agent Pub/Sub, the agent subsystems, etc.

`Pytest best practices for Integration Testing <https://docs.pytest.org/en/latest/goodpractices.html>`_

volttron-testing package
-------------------------

The `volttron-testing <https://pypi.org/project/volttron-lib-sql-historian/>`_ package includes several helpful
fixtures and utilities for your tests. Including the following line at the
top of your tests, or in `conftest.py`, will allow you to utilize the platform wrapper fixtures and the PlatformWrapper
class that helps you create a volttron test instance for integration testing.

.. code-block:: python

    from volttrontesting.fixtures.volttron_platform_fixtures import volttron_instance

You can also include the following code in `conftest.py` to include your src directory in the system path

.. code-block:: python

    # the following assumes that the testconf.py is in the tests directory.
    volttron_src_path = Path(__file__).resolve().parent.parent.joinpath("src")

    assert volttron_src_path.exists()

    print(sys.path)
    if str(volttron_src_path) not in sys.path:
        print(f"Adding source path {volttron_src_path}")
        sys.path.insert(0, str(volttron_src_path))


Here is an example success case integration test:

.. code-block:: python

    import gevent
    from pathlib import Path

    from volttron.client.messaging.health import STATUS_GOOD
    from volttron.client.vip.agent import Agent
    from volttrontesting.platformwrapper import PlatformWrapper


    def test_platform_driver_agent_successful_install_on_volttron_platform(
            publish_agent: Agent, volttron_instance: PlatformWrapper):
        # Agent install path based upon root of this repository
        agent_dir = Path(__file__).parent.parent.resolve().as_posix()
        config = {
            "driver_scrape_interval": 0.05,
            "publish_breadth_first_all": "false",
            "publish_depth_first": "false",
            "publish_breadth_first": "false"
        }
        pdriver_id = "pdriver_health_id"

        pdriver_uuid = volttron_instance.install_agent(agent_dir=agent_dir,
                                                       config_file=config,
                                                       start=False,
                                                       vip_identity=pdriver_id)

        assert pdriver_uuid is not None
        gevent.sleep(1)

        started = volttron_instance.start_agent(pdriver_uuid)
        assert started
        assert volttron_instance.is_agent_running(pdriver_uuid)

        assert publish_agent.vip.rpc.call(
            pdriver_id, "health.get_status").get(timeout=10).get('status') == STATUS_GOOD

For more integration test examples, it is recommended to take a look at some of the VOLTTRON core agents, such as
`Platform Driver agent <https://github.com/eclipse-volttron/volttron-platform-driver/blob/main/tests/test_agent_integ.py>`_.

Using Docker for Limited-Integration Testing
--------------------------------------------

If you want to run limited-integration tests which do not require the setup of a volttron system, you can use Docker
containers to mimic dependencies of an agent. The
`docker wrapper module <https://github.com/eclipse-volttron/volttron-testing/blob/develop/src/volttrontesting/fixtures/docker_wrapper.py>`_
provides a convenient function to create docker containers for use in limited-integration tests. For example,
suppose that you had an agent with a dependency on a MySQL database. If you want to test the connection between the
Agent and the MySQL dependency, you can create a Docker container to act as a real MySQL database. Below is an example:

.. code-block:: python

    from volttrontesting.fixtures.docker_wrapper import create_container
    from UserAgent import UserAgentClass

    def test_docker_wrapper_example():
        ports_config = {'3306/tcp': 3306}
        with create_container("mysql:5.7", ports=ports_config) as container:
            init_database(container)
            agent = UserAgent(ports_config)

            results = agent.some_method_that_talks_to_container()


Running your Tests and Debugging
================================

Pytest can be run from the command line to run a test module.

.. code-block:: bash

    pytest <path to module to be tested>

If using marks, you can add ``-m <mark>`` to specify your testing subset, and -s can be used to suppress standard
output.  For more information about optional arguments you can type `pytest --help` into your command line interface to
see the full list of options.

Testing output should look something like this:

.. code-block:: console

    (volttron-py3.10) volttron@evolttron1:~/git/volttron-core$ pytest tests/unit/utils/test_client_context.py
    =================================================== test session starts ===========================================
    platform linux -- Python 3.10.6, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
    rootdir: /home/volttron/git/volttron-core, configfile: pytest.ini
    collected 4 items

    tests/unit/utils/test_client_context.py ....                                                                 [100%]

    ==================================================== 4 passed in 0.07s ============================================


Running Tests Via PyCharm
-------------------------

To run our Pytests using PyCharm, we'll need to create a run configuration.  To do so, select "edit configurations" from
the "Run" menu (or if using the toolbar UI element you can click on the run configurations dropdown to select "edit
configurations").  Use the plus symbol at the top right of the pop-up menu, scroll to "Python Tests" and expand this
menu and select "pytest".  This will create a run configuration, which will then need to be filled out. We recommend the
following in general:

    * Set the "Script Path" radio and fill the form with the path to your module. Pytest will run any tests in that
      module using the discovery process described above (and any marks if specified)
    * In the interpreter dropdown, select the VOLTTRON virtual environment - this will likely be your project default
    * Set the working directory to your project's root directory
    * Add any environment variables - For debugging, add variable "DEBUG_MODE" = True or "DEBUG" 1
    * Add any optional arguments (-s will prevent standard output from being displayed in the console window, -m is used
      to specify a mark)

`PyCharm testing instructions <https://www.jetbrains.com/help/pycharm/run-debug-configuration-py-test.html>`_

----

`More information on testing in Python <https://realpython.com/python-testing/>`_
