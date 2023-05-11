===================================
Setup VOLTTRON core for development
===================================

Prerequisites
=============

* A Linux environment(machine/VM/docker container/WSL2 environment) VOLTTRON is tested on Ubuntu 22.04 but other Linux environments should work.
* Fork of volttron-core repository. See :ref:`forking volttron-core for development <Fork-Repository>`

Install VOLTTRON requirements
==============================
- git >= 2.25
- poetry >= 1.2.2
- python >= 3.10

Optional but handy is installing the tree command.

The below commands assume you have the required version of python already installed.

.. code-block:: bash

    $> sudo apt install git

    # As of this writting the 1.2 version of poetry is in beta and is in the  master branch of poetry.
    $> curl -sSL https://install.python-poetry.org | python3 - --preview

    # Add poetry path to PATH variable. Also add this to your ~/.bashrc file
    export PATH="/home/volttron/.local/bin:$PATH"

    # Configure poetry to use project root virtual environments
    $> poetry config virtualenvs.in-project true

    # Check the configuration
    $> poetry config --list

Environment Setup
=================
For the rest of the document we assume /repos/volttron-core is the root of the git cloned repository and is designated
as the VOLTTRON_ROOT.

Clone the forked volttron-core
-------------------------------

.. code-block::

    cd /repos
    git clone https://github.com/<your namespace>/volttron-core --branch develop
    cd volttron-core

Install VOLTTRON
----------------

.. code-block::

    cd /repos/volttron-core
    poetry install

Activated shell
---------------

.. code-block::

    # creates a new shell and activate the environment
    poetry shell

After executing the above commands your environment is setup for starting volttron.  The next
step is to begin developing an agent(see :ref:`agent development <Agent-Development>`, or continue on with setting up
pycharm for use with this environment(see :ref:`Pycharm development environment <Pycharm-Dev-Environment>`)

Note: To exit the poetry shell use the exit command. this deactivates the environment and exits the spawned shell.
