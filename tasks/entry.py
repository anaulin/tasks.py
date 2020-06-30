"""Utilities to handle .md blog entry files, manipulate the TOML frontmatter, etc."""

import os
import re
import toml

RE_TOML_SEPARATOR = r"\+\+\+"


def get_toml(filename):
    """Returns a dictionary representing the TOML frontmatter in the given file."""
    with open(filename, 'r') as file:
        file_str = file.read()
        splits = re.split(RE_TOML_SEPARATOR, file_str)
        return toml.loads(splits[1].strip())


def get_url(filename):
    """Given a filename, returns the corresponding blog URL."""
    slug = os.path.splitext(os.path.basename(filename))[0]
    return "https://anaulin.org/blog/{}/".format(slug)
