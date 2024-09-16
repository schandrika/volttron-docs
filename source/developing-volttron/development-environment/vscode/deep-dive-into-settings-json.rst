.. _deep_dive_into_settings_json:

Deep Dive into settings.json
============================

This document explores the various settings within the `settings.json` file of Visual Studio Code, detailing their purpose and organization based on functionality.

General Appearance and Behavior
-------------------------------
Settings related to the look and feel of the editor, as well as behavior of various components:

- **Window Title**: Configures the title format of VS Code windows.
  Example: ``"window.title": "${rootPath}${separator}${activeEditorShort}${separator}"``

- **Workbench Tree Indent**: Adjusts the indentation level of items in the sidebar tree views.
  Example: ``"workbench.tree.indent": 15``

- **Icon Theme**: Sets the icon theme used in the workbench.
  Example: ``"workbench.iconTheme": "material-icon-theme"``

- **Minimap**: Controls the display of the minimap on the side of the editor.
  Example: ``"editor.minimap.enabled": false``

- **Git Integration**: Configures aspects of git functionality.
  Example: ``"git.mergeEditor": true`` and related settings under ``"gitlens.advanced.messages"``.

Environment Configuration
-------------------------
Settings that define the environment within the editor:

- **Default Python Interpreter**: Specifies the path to the Python interpreter.
  `Documentation <https://code.visualstudio.com/docs/python/environments#_manually-specify-an-interpreter>`_
  Example: ``"python.defaultInterpreterPath": "/apps/base/python3.6/bin/python"``

- **Terminal Settings**: Configures the integrated terminal.
  `Documentation <https://code.visualstudio.com/docs/editor/integrated-terminal>`_
  Example: ``"terminal.integrated.defaultProfile.linux": "bash"`` and environmental variables set under ``"terminal.integrated.env.linux"``.

Development Tools
-----------------
Settings related to formatting, linting, and code analysis:

- **Format on Save**: Automatically formats code upon saving.
  Example: ``"editor.formatOnSave": true``

- **Python Analysis**: Configures the level of type checking for Python code.
  Example: ``"python.analysis.typeCheckingMode": "basic"``

Utilities
---------
Tools that assist with coding and project management:

- **Local History**: Maintains a local history of changes.
  Example: ``"workbench.localHistory.enabled": true``

- **Error Lens**: Configuration for the Error Lens extension.
  Example: ``"errorLens.delay": 2000`` and related settings.

Markdown and reStructuredText
-----------------------------
Settings specific to Markdown and reStructuredText files:

- **Markdown Settings**:
  Configures how Markdown files are handled.
  Example: ``"[markdown]": {"editor.wordWrap": "bounded", "editor.wordWrapColumn": 80}``

- **reStructuredText Settings**:
  Configures how reStructuredText files are handled.
  Example: ``"[restructuredtext]": {"editor.wordWrap": "wordWrapColumn", "editor.wordWrapColumn": 80}``

Language Specific Settings
--------------------------
Settings that apply to specific programming languages:

- **Python Settings**:
  Configuration specific to Python language support.
  Example: ``"[python]": {"editor.codeActionsOnSave": {"source.organizeImports.ruff": "always"}}``

Example Settings
----------------
Below is an example of how these settings might appear in a `settings.json` file:

.. code-block:: json

    {
        // 
        // Look and feel of VS Code (personal preference)
        // 
        "window.title": "${rootPath}${separator}${activeEditorShort}${separator}",
        "workbench.tree.indent": 15,
        "workbench.iconTheme": "material-icon-theme",
        "editor.minimap.enabled": false,
        "git.mergeEditor": true,
        "git.ignoreLegacyWarning": true,
        "gitlens.advanced.messages": {
            "suppressGitVersionWarning": true
        },
        "files.exclude": {
            "**/.git": true,
            "**/.svn": true,
            "**/.hg": true,
            "**/CVS": true,
            "**/.DS_Store": true,
            "**/Thumbs.db": true,
            "**/__pycache__": true,
            "**/*.pyc": true,
            "**/.mypy_cache": true,
        },
        // 
        // Environment settings
        // 
        "python.defaultInterpreterPath": "/apps/base/python3.6/bin/python",
        "terminal.integrated.defaultProfile.linux": "bash",
        // "terminal.integrated.inheritEnv": false,  // For conda environments: https://stackoverflow.com/a/69413270/15641512
        "terminal.integrated.env.linux": {
            "PYTHONPATH": "${workspaceFolder}/src/some-path:${env:PYTHONPATH}",
            "VOLTTRON_HOME": "/home/${env:USER}/.volttron_modular"
        },
        //
        // Formatting, linting, and code analysis
        //
        "editor.formatOnSave": true,
        "python.analysis.typeCheckingMode": "basic", // Set to "basic" or "strict" to encourage using typing
        //
        // Settings for helpful utilities
        //
        "workbench.localHistory.enabled": true,
        "errorLens.delay": 2000,
        "errorLens.statusBarIconsEnabled": true,
        "todo-tree.highlights.highlightDelay": 1000,
        "todo-tree.general.tags": [
            "BUG",
            "HACK",
            "FIXME",
            "TODO",
            "TEST",
            "IDEA",
            "XXX",
            "[ ]",
            "[x]"
        ],
        "[markdown]": {
            "editor.wordWrap": "bounded",
            "editor.wordWrapColumn": 80
        },
        "[restructuredtext]": {
            "editor.wordWrap": "wordWrapColumn",
            "editor.wordWrapColumn": 80 // or any other preferred line length
        },
        "editor.rulers": [
            88,
            120
        ],
        "python.analysis.extraPaths": [
            "./src/",

        ],
        "[python]": {
            "editor.codeActionsOnSave": {
                "source.organizeImports.ruff": "always"
            },
            "editor.defaultFormatter": "charliermarsh.ruff",
            // "editor.defaultFormatter": "ms-python.python",
            "editor.formatOnSave": true
        },
        "ruff.codeAction.fixViolation": {
            "enable": true
        },
        "ruff.fixAll": true,
        "ruff.organizeImports": true,
        "ruff.lint.run": "onSave",
        "ruff.showNotifications": "onError",
    }
