"""Main tasks collection. Entrypoint to the shenanigans."""

import datetime
import os
import sys

from invoke import run, task
from . import mastodon
from . import entry
from . import webmention
from . import goodreads


BLOG_DIR = "/Users/anaulin/src/github.com/anaulin/blog"


@task
def mastodon_login(_ctx):
    """Logs into Mastodon and creates local credentials files."""
    mastodon.login()


@task(help={'entry_file': "Path to the entry file to toot."})
def toot_entry(_ctx, entry_file):
    """Posts a toot about the given blog entry."""
    meta = entry.get_toml(entry_file)
    tags = " ".join(["#{}".format(tag.replace(" ", "-"))
                     for tag in meta['tags']])
    tags += " #blog"
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


@task(optional=['notoot'], help={'entry_file': "Path to the entry file to publish."})
def publish(_ctx, entry_file, notoot=False):
    """Publishes the given entry and deploys it."""
    entry.add_to_toml(
        entry_file, {"draft": "false", "date": datetime.datetime.now()})
    _git_commit_all(_ctx)
    deploy(_ctx)
    if not notoot:
        toot_entry(_ctx, entry_file)


@task(help={'title': "Title of book."})
def start_reading(_ctx, title):
    """Start a draft entry about this book."""
    slug = "book-notes-" + entry.to_slug(title)
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


CLIPPINGS_PY_DIR = "/Users/anaulin/src/github.com/anaulin/clippings.py"
KINDLE_CLIPPINGS = "/Volumes/Kindle/documents/My Clippings.txt"
BACKUPS_DIR = "/Users/anaulin/Google Drive/backups/"


@task
def extract_clippings(_ctx):
    """
    Use the local clippings.py installation to extract clippings from the attached Kindle.
    Includes clearing the Kindle file, making backups.
    """
    backup(_ctx, KINDLE_CLIPPINGS)
    with _ctx.cd(CLIPPINGS_PY_DIR):
        with _ctx.prefix("source .venv/bin/activate"):
            backup(_ctx, "clippings.csv")
            _ctx.run(
                f"./clippings/clippings.py extract {_escape_filename(KINDLE_CLIPPINGS)} --no-title",
                echo=True)
    with open(KINDLE_CLIPPINGS, 'w') as clippings_f:
        clippings_f.truncate(0)


@task(help={'origin_file': "Path to file to backup."})
def backup(_ctx, origin_file):
    """Copies the origin_file into the backups directory, adding a timestamp suffix to the filename"""
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    (base_filename, ext) = os.path.splitext(os.path.basename(origin_file))
    dst_file = os.path.join(
        BACKUPS_DIR, f"{base_filename}-{timestamp_str}{ext}")
    _ctx.run(
        f"cp {_escape_filename(origin_file)} {_escape_filename(dst_file)}", echo=True)


@task(help={'goodreads_csv': "Goodreads CSV to import."})
def import_goodreads(_ctx, goodreads_csv):
    """Imports the given Goodreads library export into blog format."""
    goodreads.import_to_blog(goodreads_csv)


@task(help={'goodreads_csv': "Goodreads CSV to import."})
def import_goodreads_list(_ctx, goodreads_csv):
    """Imports the given Goodreads library export into blog list format."""
    goodreads.import_to_blog_list(goodreads_csv)


def _escape_filename(filename):
    """Escapes spaces in the given filename, Unix-style."""
    return filename.replace(" ", "\\ ")


def _git_commit_all(_ctx):
    run("cd {} && git add . && git commit -m 'Autocommit from tasks.py' && git push".format(BLOG_DIR))
