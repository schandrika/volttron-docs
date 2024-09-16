.. _deep_dive_into_launch_json:

Deep Dive into launch.json
============================

**launch.json** in Visual Studio Code enables users to configure debugging sessions. This file specifies the settings and parameters for launching your application in various debug configurations. Below, we explore each setting's purpose and provide examples from the configuration.

.. _Launch Settings Overview:

Launch Settings Overview
------------------------

1. **name**
   Specifies a unique name for the debug configuration which appears in the debugging dropdown.

2. **type**
   Indicates the type of debugger to use. Typically set to ``python`` for Python applications.

3. **request**
   Determines the mode of the debugger, usually ``launch`` to start the debugging or ``attach`` to connect to an already running process.

4. **program**
   Path to the main file of the application being debugged. 

5. **args**
   Lists the command-line arguments to pass to the program when launched.

6. **console**
   Configures the type of console to use for the output, often set to ``integratedTerminal``.

7. **cwd (current working directory)**
   Sets the directory from which the program is run. This is crucial when your application expects a specific starting directory.

8. **env**
   Defines environment variables to be set only within the launched application.

9. **justMyCode**
   Controls whether the debugger should skip over code outside of the user's control, typically vendor libraries.

10. **python**
    Specifies the Python interpreter's path when the environment isn't determined by a ``.venv``.

For detailed guidance on each attribute and setting configuration, visit the official Visual Studio Code documentation on :doc:`launch configurations <https://code.visualstudio.com/docs/editor/debugging#_launch-configurations>`.

Functionality Grouping
----------------------

- **Environment Setup**
  Settings related to the environment such as ``env``, ``cwd``, and Python interpreter configurations are critical for ensuring that the application runs in the correct context.

- **Debugging and Execution**
  Settings like ``console``, ``args``, and ``justMyCode`` directly influence the behavior of the debugging session and how the application is executed and controlled.

- **Editor Enhancements**
  While not directly part of ``launch.json``, settings in other areas such as ``[markdown]`` and ``[restructuredtext]`` affect how content is displayed in the editor, improving readability and workflow.

Example Configuration
---------------------

The following example illustrates a typical ``launch.json`` file configuration for a Python project in Visual Studio Code. Also note that the enviornment has the following structure setup.
.. code-block:: bash

    ~/project/volttron-modular$ tree -L 1
    .
    ├── volttron-core
    ├── volttron-lib-auth
    ├── volttron-lib-zmq
    ├── volttron-listener
    └── volttron-zmq

.. code-block:: json

    {
        // Use IntelliSense to learn about possible attributes.
        // Hover to view descriptions of existing attributes.
        // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
        "version": "0.2.0",
        "configurations": [
            {
                "name": "volttron -vv",
                "type": "python",
                "request": "launch",
                "program": ".venv/bin/volttron",
                "console": "integratedTerminal",
                "justMyCode": true,
                "args": [
                    "-vv",
                    "--dev",
                    "-l",
                    "volttron.log",
                    "--log-config",
                    "logging_config.yaml"
                ],
                "env": {
                    "GEVENT_SUPPORT": "True",
                    "VOLTTRON_HOME": "~/.volttron_redo"
                },
                "cwd": "${workspaceFolder}/volttron-zmq"
            },
            {
                "name": "Python Debugger: Current File",
                "type": "debugpy",
                "request": "launch",
                "program": "${file}",
                "console": "integratedTerminal",
                "python": ".venv/bin/python",
                "env": {
                    "GEVENT_SUPPORT": "True",
                    "VOLTTRON_HOME": "~/.volttron_redo",
                }
            },
            {
                "name": "launch volttron-listener",
                "type": "debugpy",
                "request": "launch",
                "program": "/home/os2204/repos/volttron-redo/volttron-listener/src/listener/agent.py",
                "console": "integratedTerminal",
                "python": ".venv/bin/python",
                "justMyCode": true,
                "args": [
                    "-vv",
                    "--json",
                    "start",
                    "volttron-listener-0.2.0rc0"
                ],
                "env": {
                    "GEVENT_SUPPORT": "True",
                    "VOLTTRON_HOME": "~/.volttron_redo",
                    "AGENT_CREDENTIALS": "/home/os2204/.volttron_redo/credentials_store/volttron-listener-0.2.0rc0_2.json",
                    "AGENT_VIP_IDENTITY": "volttron-listener",
                    //"AGENT_VIP_IDENTITY": "volttron-listener-0.2.0rc0_2",
                    "VOLTTRON_PLATFORM_ADDRESS": "ipc://@/home/os2204/.volttron_redo/run/vip.socket"
                    //"VOLTTRON_PLATFORM_ADDRESS": "tcp://127.0.0.1:22916"
                },
                "cwd": "${workspaceFolder}/volttron-zmq"
            },
            {
                "name": "vctl start volttron-listener",
                "type": "debugpy",
                "request": "launch",
                "module": "volttron.client.commands.control",
                "console": "integratedTerminal",
                "python": ".venv/bin/python",
                "justMyCode": true,
                "args": [
                    "--json",
                    "start",
                    //"volttron-listener-0.2.0rc0",
                    //"volttron-listener-0.2.0rc0_2"
                    "9"
                ],
                "env": {
                    "GEVENT_SUPPORT": "True",
                    "VOLTTRON_HOME": "~/.volttron_redo"
                },
                "cwd": "${workspaceFolder}/volttron-zmq"
            },
            {
                "name": "vctl install local volttron-listener from agent dir",
                "type": "debugpy",
                "request": "launch",
                "module": "volttron.client.commands.control",
                "console": "integratedTerminal",
                "python": ".venv/bin/python",
                "justMyCode": true,
                "args": [
                    "--json",
                    "install",
                    "/home/os2204/repos/volttron-redo/volttron-listener",
                    "--tag",
                    "listener"
                ],
                "env": {
                    "GEVENT_SUPPORT": "True",
                    "VOLTTRON_HOME": "~/.volttron_redo"
                },
                "cwd": "${workspaceFolder}/volttron-zmq"
            },
            {
                "name": "vctl install tag local volttron-listener from agent dir",
                "type": "debugpy",
                "request": "launch",
                "module": "volttron.client.commands.control",
                "console": "integratedTerminal",
                "python": ".venv/bin/python",
                "justMyCode": true,
                "args": [
                    "--json",
                    "install",
                    "/home/os2204/repos/volttron-redo/volttron-listener",
                    "--tag",
                    "listener",
                    "--priority",
                    "10",
                    "--start"
                ],
                "env": {
                    "GEVENT_SUPPORT": "True",
                    "VOLTTRON_HOME": "~/.volttron_redo"
                },
                "cwd": "${workspaceFolder}/volttron-zmq"
            },
            {
                "name": "vctl -vv peerlist",
                "type": "debugpy",
                "request": "launch",
                "module": "volttron.client.commands.control",
                "console": "integratedTerminal",
                "python": ".venv/bin/python",
                "justMyCode": true,
                "args": [
                    "--json",
                    "peerlist"
                ],
                "env": {
                    "GEVENT_SUPPORT": "True",
                    "VOLTTRON_HOME": "~/.volttron_redo"
                },
                "cwd": "${workspaceFolder}/volttron-zmq"
            },
            {
                "name": "vctl -vv install volttron-listener",
                "type": "debugpy",
                "request": "launch",
                "module": "volttron.client.commands.control",
                "console": "integratedTerminal",
                "justMyCode": true,
                "python": ".venv/bin/python",
                "args": [
                    "--json",
                    "install",
                    "volttron-listener"
                ],
                "env": {
                    "GEVENT_SUPPORT": "True",
                    "VOLTTRON_HOME": "~/.volttron_redo"
                },
                "cwd": "${workspaceFolder}/volttron-zmq"
            },
            {
                "name": "vctl -vv status",
                "type": "debugpy",
                "request": "launch",
                "module": "volttron.client.commands.control",
                "console": "integratedTerminal",
                "justMyCode": true,
                "python": ".venv/bin/python",
                "args": [
                    //"-vv",
                    "status"
                ],
                "env": {
                    "GEVENT_SUPPORT": "True",
                    "VOLTTRON_HOME": "~/.volttron_redo"
                },
                "cwd": "${workspaceFolder}/volttron-zmq"
            },
            {
                "name": "vctl -vv start 8",
                "type": "debugpy",
                "request": "launch",
                "module": "volttron.client.commands.control",
                "console": "integratedTerminal",
                "justMyCode": true,
                "python": ".venv/bin/python",
                "args": [
                    "-vv",
                    "start",
                    "8"
                ],
                "env": {
                    "GEVENT_SUPPORT": "True",
                    "VOLTTRON_HOME": "~/.volttron_redo"
                },
                "cwd": "${workspaceFolder}/volttron-zmq"
            },
            {
                "name": "volttron -vv",
                "type": "debugpy",
                "request": "launch",
                "module": "volttron.server",
                "console": "integratedTerminal",
                "justMyCode": true,
                "python": ".venv/bin/python",
                "args": [
                    "-vv",
                    "--dev",
                    "--log-config",
                    "logging_config.yaml"
                ],
                "env": {
                    "GEVENT_SUPPORT": "True",
                    "VOLTTRON_HOME": "~/.volttron_redo",
                    "PYTHONPATH": "${userHome}/repos/volttron-redo/volttron-lib-auth/src:${userHome}/repos/volttron-redo/volttron-lib-auth-zap/src"
                },
                "subProcess": true,
                "cwd": "${workspaceFolder}/volttron-zmq"
            },
            {
                "name": "volttron -v",
                "type": "debugpy",
                "request": "launch",
                "module": "volttron.server",
                "console": "integratedTerminal",
                "justMyCode": true,
                "python": ".venv/bin/python",
                "args": [
                    "-v"
                    // ,
                    // "--log-config",
                    // "logging_config.yaml"
                ],
                "env": {
                    "GEVENT_SUPPORT": "True",
                    "VOLTTRON_HOME": "~/.volttron_redo",
                    "PYTHONPATH": "${userHome}/repos/volttron-redo/volttron-lib-auth/src:${userHome}/repos/volttron-redo/volttron-lib-auth-zap/src"
                },
                "subProcess": true,
                "cwd": "${workspaceFolder}/volttron-zmq"
            },
            {
                "name": "volttron",
                "type": "debugpy",
                "request": "launch",
                "module": "volttron.server",
                "console": "integratedTerminal",
                "justMyCode": true,
                "python": ".venv/bin/python",
                "args": [
                    //"-v"
                    // ,
                    // "--log-config",
                    // "logging_config.yaml"
                ],
                "env": {
                    "GEVENT_SUPPORT": "True",
                    "VOLTTRON_HOME": "~/.volttron_redo",
                    "PYTHONPATH": "${userHome}/repos/volttron-redo/volttron-lib-auth/src:${userHome}/repos/volttron-redo/volttron-lib-auth-zap/src"
                },
                "subProcess": true,
                "cwd": "${workspaceFolder}/volttron-zmq"
            },
            {
                "name": "connect_to_volttron",
                "type": "debugpy",
                "request": "launch",
                "program": "connect_to_volttron.py",
                "console": "integratedTerminal",
                "justMyCode": true,
                "python": ".venv/bin/python",
                "args": [
                    "-vv"
                ],
                "env": {
                    "GEVENT_SUPPORT": "True",
                    "VOLTTRON_HOME": "~/.volttron_redo",
                    // "PYTHONPATH": "/home/os2204/repos/volttron-redo/volttron-lib-auth/src"
                },
                "subProcess": true,
                "cwd": "${workspaceFolder}/volttron-zmq"
            },
            {
                "name": "pytest",
                "type": "debugpy",
                "request": "launch",
                "module": "pytest",
                "console": "integratedTerminal",
                "justMyCode": true,
                "args": [
                    "-s",
                    "${file}"
                ],
                "env": {
                    "GEVENT_SUPPORT": "True",
                    "VOLTTRON_HOME": "~/.volttron_redo"
                }
            }
        ]
    }

This configuration launches a Python application with verbose logging, specific environment variables, and using a virtual environment located at ``.venv/bin/volttron``.