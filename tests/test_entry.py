import os

from .context import entry

TEST_ENTRY = os.path.join(os.path.dirname(__file__), "test_entry.md")


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
