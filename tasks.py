import getpass
import os
import re
import toml
from invoke import task
from mastodon import Mastodon

# Mastodon constants.
APP_NAME = "Ana's tasks.py"
API_BASE_URL = "https://social.coop"
CLIENT_SECRET_FILE = 'mastodon_clientcred.secret'
MASTODON_SECRET_FILE = 'mastodon_usercred.secret'
MASTODON_LOGIN_EMAIL = 'ana@ulin.org'

RE_TOML_SEPARATOR = r"\+\+\+"


@task
def mastodon_login(_ctx):
    """Logs into Mastodon and creates local credentials files."""
    password = getpass.getpass("Enter Mastodon password: ")
    Mastodon.create_app(
        APP_NAME,
        api_base_url=API_BASE_URL,
        to_file=CLIENT_SECRET_FILE
    )
    mastodon = Mastodon(
        client_id=CLIENT_SECRET_FILE,
        api_base_url=API_BASE_URL
    )
    mastodon.log_in(
        MASTODON_LOGIN_EMAIL,
        password,
        to_file=MASTODON_SECRET_FILE
    )
    print("Created credential files: {}, {}".format(
        CLIENT_SECRET_FILE, MASTODON_SECRET_FILE))


def toot(content):
    """Toots content. Returns resulting url."""
    mastodon = Mastodon(access_token=MASTODON_SECRET_FILE,
                        api_base_url=API_BASE_URL)
    result = mastodon.toot(content)
    return result['url']


def get_toml_from_file(filename):
    """Returns a dictionary representing the TOML frontmatter in the given file."""
    with open(filename, 'r') as file:
        file_str = file.read()
        splits = re.split(RE_TOML_SEPARATOR, file_str)
        return toml.loads(splits[1].strip())


def get_url_from_filename(filename):
    """Given a filename, returns the corresponding blog URL."""
    slug = os.path.splitext(os.path.basename(filename))[0]
    return "https://anaulin.org/blog/{}".format(slug)


@task(help={'entry': "Path to the entry file to toot."})
def toot_entry(_ctx, entry):
    """Posts a toot about the given blog entry."""
    meta = get_toml_from_file(entry)
    tags = " ".join(["#{}".format(tag) for tag in meta['tags']])
    content = "I just published {}: {} \n{}".format(
        meta['title'], get_url_from_filename(entry), tags
    )
    toot_url = toot(content)
    print("Posted to: {}".format(toot_url))
