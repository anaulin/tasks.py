"""Mastodon utilities."""

import getpass
from mastodon import Mastodon

APP_NAME = "Ana's tasks.py"
API_BASE_URL = "https://social.coop"
CLIENT_SECRET_FILE = 'mastodon_clientcred.secret'
MASTODON_SECRET_FILE = 'mastodon_usercred.secret'
MASTODON_LOGIN_EMAIL = 'ana@ulin.org'


def login():
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
