# VOLTTRON documentation

This repository contains code and documentation that generate VOLTTRON core documentation and core agent documentation   
on https://volttron.readthedoc.io

## Building

```bash
# Install documentation dependencies
poetry install

# Builds documentation
make html

# Local server port 8080
poetry run python -m http.server --directory build/html 8080
```

## Active development

In a secondary shell start the watchsource.py script to automatically rebuild the
documentation when a change to a source file happens.

```bash
poetry run python watchsource.py
```

