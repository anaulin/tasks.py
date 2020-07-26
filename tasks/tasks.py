"""Main tasks collection. Entrypoint to the shenanigans."""

import datetime

from invoke import run, task
from . import mastodon
from . import entry
from . import webmention


BLOG_DIR = "/Users/anaulin/src/github.com/anaulin/blog"


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
    print("Toot posted to: {}".format(toot_url))
    entry.add_syndication_url(entry_file, toot_url)
    _git_commit_all(_ctx)
    deploy(_ctx)


@task(help={
    'entry_file': "Path to the entry file to syndicate.",
    'sub': "Sub on indiewebxyz to syndicate to. E.g. 'hottubs'"
})
def send_to_indiewebxyz(_ctx, entry_file, sub):
    """Adds appropriate syndication URLs and submits the entry to the chosen indieweb.xyz sub."""
    xyz_url = webmention.get_indiewebxyz_sub_url(sub)
    entry.add_syndication_url(entry_file, xyz_url)
    _git_commit_all(_ctx)
    deploy(_ctx)
    webmention.send(entry.get_url(entry_file), xyz_url)


@task(help={
    'entry_file': "Path to the entry file to syndicate.",
})
def send_to_indiewebnews(_ctx, entry_file):
    """Sends webmention to news.indieweb.org, adds appropriate syndication URLs."""
    indiewebnews_url = "https://news.indieweb.org/en"
    entry.add_syndication_url(entry_file, indiewebnews_url)
    _git_commit_all(_ctx)
    deploy(_ctx)
    webmention.send(entry.get_url(entry_file), indiewebnews_url)


@task
def deploy(_ctx):
    """Deploy blog."""
    run("cd {} && make deploy".format(BLOG_DIR))


@task(help={'entry_file': "Path to the entry file to publish."})
def publish(_ctx, entry_file):
    """Publishes the given entry and deploys it."""
    entry.add_to_toml(
        entry_file, {"draft": "false", "date": datetime.datetime.now()})
    _git_commit_all(_ctx)
    deploy(_ctx)
    toot_entry(_ctx, entry_file)


@task(help={'title': "Title of book."})
def start_reading(_ctx, title):
    """Start a draft entry about this book."""
    slug = "book-notes-" + title.replace(' ', '-').lower()
    run("cd {} && make new slug={}".format(BLOG_DIR, slug))
    filename = "{}/content/blog/{}.md".format(BLOG_DIR, slug)
    entry.add_to_toml(filename, {
        "title": "Book Notes: {}".format(title),
        "draft": "true",
        "tags": ["books"],
        "book": {
            "title": title,
            "author": "",
            "url": "",
            "start": datetime.date.today(),
            "end": "",
            "rating": "",
            "image": "/img/"
        },
    })
    _git_commit_all(_ctx)


def _git_commit_all(_ctx):
    run("cd {} && git add . && git commit -m 'Autocommit from tasks.py' && git push".format(BLOG_DIR))
