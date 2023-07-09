# -*- coding: utf-8 -*-

"""Top-level package for heliostrome."""

__author__ = "Stephan Smit"
__email__ = "stephansmit@hotmail.com"
# Do not edit this string manually, always use bumpversion
# Details in CONTRIBUTING.md
__version__ = "0.0.2"


def get_module_version():
    return __version__


from .example import Example  # noqa: F401
