# VOLTTRON documentation

This repository contains code and documentation that generate modular VOLTTRON core documentation and 
documentation of agent developed and maintained by core VOLTTRON team. The documents are main available 
on https://eclipse-volttron.readthedocs.io

## Building documents locally

```bash
# Install documentation dependencies
poetry install

# Builds documentation
make html

# Local server port 8080
poetry run python -m http.server --directory build/html 8080
```

## Linking agent or library documentation

### Pulling in agent/library documentation

This repository only contains the documentation for modular volttron core available at 
https://github.com/eclipse-volttron/volttron-core. Documentation for different agents and libraries are stored in the 
corresponding agent/library repository. However when building the readthedocs pages for a specific version of 
volttron-core, documentation of a configured set of agents/libraries are pulled in from the various agent/libraries 
repositories and build along with volttron-core documentation. 

List of agents/libraries are configured in the file  [external_docs.yml](source/external_docs.yml). It contains one or 
more entries of the below format for each of the external repository from which documentation is pulled in

```yaml
name: 
    # optional path to repo.
    # if not provided default would be "https://github.com/eclipse-volttron/" + agent/library/project name(parent element)
    repo: https://github.com/username/repo_name
    # branch or tag that should get pulled. should be valid value to be used wtih git checkout. ex. branch, tag
    version: main
    # optional docs directory. defaults to "docs/source" under root
    docs_dir: docs/source
```

For example, 
```yaml
volttron-lib-base-historian:
    repo: https://github.com/eclipse-volttron/volttron-lib-base-historian
    version: develop
```
If you are repository has multiple sub-projects, each with its own documentation, you can create multiple entries in 
external_docs.yml, one for each sub-project. Each entry can have a unique logical name as key and point to the 
same repository and different docs_dir. 

For example, 
```yaml

volttron-boptest-agent:
    repo: https://github.com/eclipse-volttron/volttron-boptest
    version: main
    docs_dir: volttron-boptest-agent/docs/source

volttron-lib-boptest-integration:
    repo: https://github.com/eclipse-volttron/volttron-boptest
    version: main
    docs_dir: volttron-lib-boptest-integration/docs/source
```

### Linking to agent/library document from volttron-core documents

When you add a new entry in external_docs.yml, please also make sure you provide a link to the documentation from the 
volttron-core documentation. All external documentation will be available at external-docs/<yaml entry key for the repo>

Example entry in external_docs.yml

```yaml
volttron-lib-boptest-integration:
    repo: https://github.com/eclipse-volttron/volttron-boptest
    version: main
    docs_dir: volttron-lib-boptest-integration/docs/source
```

Reference to index page generated from (https://github.com/eclipse-volttron/volttron-boptest/blob/main/volttron-lib-boptest-integration/docs/source/index.rst)
use 

```rst
BOPTestIntegrationLibrary <external-docs/volttron-lib-boptest-integration/index>
```
Another way to handle links to external agent/library documentation from volttron-core documentation is to use 
`(a custom anchor)[https://sublime-and-sphinx-guide.readthedocs.io/en/latest/references.html#use-a-custom-anchor]`

## Active development

In a secondary shell start the watchsource.py script to automatically rebuild the
documentation when a change to a source file happens.

```bash
poetry run python watchsource.py
```

