# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/stable/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import subprocess
import sys
import os
import yaml

# -- Project information -----------------------------------------------------

project = 'Eclipse VOLTTRON'
copyright = '2022, The VOLTTRON Community'
author = 'The VOLTTRON Community'

# The short X.Y version
version = 'modular'
# The full version, including alpha/beta/rc tags
release = 'modular'


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    # https://www.sphinx-doc.org/en/master/usage/extensions/autosectionlabel.html
    'sphinx.ext.autosectionlabel',
    # http://www.sphinx-doc.org/en/master/usage/extensions/todo.html
    'sphinx.ext.todo'
]

# prefix sections with the document so that we can cross link
# sections from different pages.
autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = 5

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ['.rst', '.md']

# The top-level toctree document.
main_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# #
# html_theme_options = {
#     'style_nav_header_background': '#0c5404',
# }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = ["custom.css"]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'VOLTTRONdoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (main_doc, 'VOLTTRON.tex', 'VOLTTRON Documentation',
     'The VOLTTRON Community', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (main_doc, 'volttron', 'VOLTTRON Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (main_doc, 'VOLTTRON', 'VOLTTRON Documentation',
     author, 'VOLTTRON', 'One line description of project.',
     'Miscellaneous'),
]


# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/3.6': None,
                       'volttron-ansible': ('https://volttron.readthedocs.io/projects/volttron-ansible/en/main/',
                                            None)}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# -- Custom code generation ----------------------------------------------


# Custom event handlers for Volttron #
def setup(app):
    """
    Registers callback method on sphinx events. callback method used to
    dynamically generate api-docs rst files which are then converted to html
    by readthedocs
    :param app:
    """
    # app.connect('builder-inited', generate_apidoc)
    #app.connect('builder-inited', generate_agent_docs)

    # app.connect('build-finished', clean_api_rst)
    #app.connect('build-finished', clean_agent_docs_rst)


script_dir = os.path.dirname(os.path.realpath(__file__))
external_docs_root = os.path.join(script_dir, "external-docs")

def _read_config(filename):
    data = {}
    try:
        with open(filename, 'r') as yaml_file:
            data = yaml.safe_load(yaml_file)
    except IOError as exc:
        print("Error reading from file: {}".format(filename))
        raise exc
    except yaml.YAMLError as exc:
        print("Yaml Error: {}".format(filename))
        raise exc
    return data


def generate_agent_docs(app):
    os.makedirs(external_docs_root)
    external_data = _read_config(filename=os.path.join(script_dir, "external_docs.yml"))
    repo_prefix = "https://github.com/eclipse-volttron/"
    for project_name in external_data:
        agent_repo = external_data[project_name].get("repo")
        if not agent_repo:
            agent_repo = repo_prefix + project_name
        subprocess.check_call(["git", "clone", "--no-checkout", agent_repo, project_name + "_docs_root"],
                              cwd=external_docs_root)
        # for 1st version not doing api-docs. If doing api-docs do full checkout, install requirements, run api-docs
        clone_dir = os.path.join(external_docs_root, project_name + "_docs_root")
        docs_source_dir = external_data[project_name].get("docs_dir", "docs/source")
        subprocess.check_call(["git", "sparse-checkout", "set", docs_source_dir], cwd=clone_dir)
        agent_version = external_data[project_name]["version"]
        subprocess.check_call(["git", "checkout", agent_version], cwd=clone_dir)
        doc_index_dir = os.path.join(clone_dir, docs_source_dir)
        os.symlink(doc_index_dir, os.path.join(external_docs_root, project_name))


def clean_agent_docs_rst(app, exception):
    """
    Deletes folder containing all auto generated .rst files at the end of
    sphinx build immaterial of the exit state of sphinx build.
    :param app:
    :param exception:
    """
    global external_docs_root
    import shutil
    if os.path.exists(external_docs_root):
        print("Cleanup: Removing agent docs clone directory {}".format(external_docs_root))
        shutil.rmtree(external_docs_root)
