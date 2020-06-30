"""Main tasks collection. Entrypoint to the shenanigans."""

from invoke import task
from . import mastodon
from . import entry


@task
def mastodon_login(_ctx):
    """Logs into Mastodon and creates local credentials files."""
    mastodon.login()


@task(help={'entry_file': "Path to the entry file to toot."})
def toot_entry(_ctx, entry_file):
    """Posts a toot about the given blog entry."""
    meta = entry.get_toml(entry_file)
    tags = " ".join(["#{}".format(tag) for tag in meta['tags']])
    content = "I just published {}: {} \n{}".format(
        meta['title'], entry.get_url(entry_file), tags
    )
    toot_url = mastodon.toot(content)
    print("Posted to: {}".format(toot_url))
