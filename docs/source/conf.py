# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'KinielaGPT'
copyright = '2025, Ricardo Moya'
author = 'Ricardo Moya'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'myst_parser',
    'sphinx_copybutton'
]

# -- Pygments (syntax highlighting) style -----------------------------------
# https://pygments.org/styles/
pygments_style = 'emacs'
pygments_dark_style = 'dracula'

# MyST-Parser configuration
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

templates_path = ['_templates']
exclude_patterns = []

language = 'es'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_css_files = [
    'https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=Roboto+Mono&family=Merriweather:wght@700;900&display=swap',
    'custom.css'
]

# Furo theme options
html_theme_options = {
    "source_repository": "https://github.com/RicardoMoya/KinielaGPT/",
    "source_branch": "main",
    "source_directory": "docs/source/",
    "light_css_variables": {
        "color-brand-primary": "#2196F3",
        "color-brand-content": "#1976D2",
        "color-link": "#1976D2",
        "color-link--hover": "#0D47A1",
    },
    "dark_css_variables": {
        "color-brand-primary": "#64B5F6",
        "color-brand-content": "#42A5F5",
        "color-link": "#42A5F5",
        "color-link--hover": "#90CAF9",
    },
    "sidebar_hide_name": True,
    "navigation_with_keys": True,
    "globaltoc_collapse": True,
    "globaltoc_includehidden": False,
    "globaltoc_maxdepth": 2,
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/RicardoMoya/KinielaGPT",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
}

html_title = "KinielaGPT"
html_short_title = "KinielaGPT"

# Additional HTML options
html_favicon = "_static/favicon.ico"
html_logo = "_static/logo.png"

# Custom JavaScript files
html_js_files = [
    'sidebar-collapse.js',
]
