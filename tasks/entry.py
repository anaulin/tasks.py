"""Utilities to handle .md blog entry files, manipulate the TOML frontmatter, etc."""

import os
import toml

from slugify import slugify

TOML_SEPARATOR = "+++"


def get_file_as_str(filename):
    """Returns the content of the filename as a string."""
    with open(filename, 'r') as file:
        return file.read()


def get_toml_and_content(filename):
    """Returns a tuple with the entry TOML frontmatter and the markdown content."""
    file_str = get_file_as_str(filename)
    front_start = file_str.index(TOML_SEPARATOR) + len(TOML_SEPARATOR)
    frontmatter_end = file_str.index(TOML_SEPARATOR, front_start)
    toml_str = file_str[front_start:frontmatter_end]
    content_str = file_str[frontmatter_end + len(TOML_SEPARATOR):]
    return (toml.loads(toml_str), content_str)


def get_toml(filename):
    """Returns a dictionary representing the TOML frontmatter in the given file."""
    return get_toml_and_content(filename)[0]


def get_url(filename):
    """Given a filename, returns the corresponding blog URL."""
    slug = os.path.splitext(os.path.basename(filename))[0]
    return "https://anaulin.org/blog/{}/".format(slug)


def add_syndication_url(filename, url):
    """Adds the given URL to the syndication_urls list of the entry."""
    frontmatter = get_toml(filename)
    if "syndication_urls" in frontmatter:
        new_urls = frontmatter["syndication_urls"] + [url]
        add_to_toml(filename, {"syndication_urls": new_urls})
    else:
        add_to_toml(filename, {'syndication_urls': [url]})


def add_to_toml(filename, toml_to_add):
    """Adds the given TOML dictionary to the file's existing TOML frontmatter.

    List values items in the new toml will fully override an existing list with the same key.
    """
    existing_toml = get_toml(filename)
    write_toml(filename, {**existing_toml, **toml_to_add})


def write_toml(filename, new_toml):
    """Rewrites the given entry file, replacing the existing frontmatter TOML with the new one."""
    (_, content) = get_toml_and_content(filename)
    with open(filename, 'w') as outfile:
        outfile.write("+++\n")
        outfile.write(toml.dumps(new_toml))
        outfile.write("+++")
        outfile.write(content)


def to_slug(title):
    """Returns a slugified version of the given title"""
    return slugify(title)
