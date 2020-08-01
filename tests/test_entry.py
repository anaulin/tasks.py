import filecmp
import shutil
import tempfile
import os

from .context import entry

TEST_ENTRY = os.path.join(os.path.dirname(__file__), "test_entry.md")

TEST_ENTRY_CONTENT = """

Some content.

## A section in the content

Content that looks like frontmatter:
```
+++
but this is
not really frontmatter
+++
```

More content.
"""


def test_get_toml_and_content():
    (toml, content) = entry.get_toml_and_content(TEST_ENTRY)
    assert toml == {
        'title': "Book Notes: The Sorcerer of the Wildeeps",
        'tags': ["books", "stuff"],
        'book': {'title': 'The Sorcerer of the Wildeeps', 'rating': 4}
    }
    assert content == TEST_ENTRY_CONTENT


def test_get_toml():
    toml = entry.get_toml(TEST_ENTRY)
    assert toml == {
        'title': "Book Notes: The Sorcerer of the Wildeeps",
        'tags': ["books", "stuff"],
        'book': {'title': 'The Sorcerer of the Wildeeps', 'rating': 4}
    }


def test_get_url():
    url = entry.get_url("../foo/bar/this-is-the-slug.md")
    assert url == "https://anaulin.org/blog/this-is-the-slug/"

    url = entry.get_url("this-is-another-slug.md")
    assert url == "https://anaulin.org/blog/this-is-another-slug/"


def test_add_to_toml():
    with tempfile.NamedTemporaryFile() as temp:
        shutil.copy2(TEST_ENTRY, temp.name)
        entry.add_to_toml(temp.name, {'new_key': 'new_value'})
        new_toml = entry.get_toml(temp.name)
        assert new_toml == {
            'title': "Book Notes: The Sorcerer of the Wildeeps",
            'tags': ["books", "stuff"],
            'book': {'title': 'The Sorcerer of the Wildeeps', 'rating': 4},
            'new_key': 'new_value'
        }


def test_add_to_toml_list():
    with tempfile.NamedTemporaryFile() as temp:
        shutil.copy2(TEST_ENTRY, temp.name)
        entry.add_to_toml(temp.name, {'tags': ['new_tag']})
        new_toml = entry.get_toml(temp.name)
        assert new_toml == {
            'title': "Book Notes: The Sorcerer of the Wildeeps",
            'tags': ["new_tag"],
            'book': {'title': 'The Sorcerer of the Wildeeps', 'rating': 4}
        }


def test_write_toml():
    with tempfile.NamedTemporaryFile() as temp:
        shutil.copy2(TEST_ENTRY, temp.name)
        entry.write_toml(temp.name, {'new_key': 'new_value'})
        (new_toml, new_content) = entry.get_toml_and_content(temp.name)
        (_, old_content) = entry.get_toml_and_content(TEST_ENTRY)
        assert new_toml == {'new_key': 'new_value'}
        assert new_content == old_content


def test_add_syndication_url():
    with tempfile.NamedTemporaryFile() as temp:
        shutil.copy2(TEST_ENTRY, temp.name)
        entry.add_syndication_url(temp.name, "new_url")
        assert entry.get_toml(temp.name)["syndication_urls"] == ["new_url"]
        entry.add_syndication_url(temp.name, "another_url")
        assert entry.get_toml(temp.name)["syndication_urls"] == [
            "new_url", "another_url"]
