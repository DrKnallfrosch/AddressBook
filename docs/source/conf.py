# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

# Add AddressPack module to the system path
sys.path.insert(0, os.path.abspath('../..'))

project = 'AddressPack'
copyright = '2024, Tim Schuette, Dominik Elias Hase'
author = 'Tim Schuette, Dominik Elias Hase'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',        # Automatically generate documentation from docstrings
    'sphinx.ext.napoleon',       # For Google/NumPy style docstrings
    'sphinx_autodoc_typehints',  # Add type hints to docs
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# Set the HTML theme to python_docs_theme
html_theme = 'python_docs_theme'

# The master toctree document.
master_doc = 'index'
html_static_path = ['_static']
