"""Webmention-related operations."""

import ronkyuu


def get_indiewebxyz_sub_url(sub):
    return "https://indieweb.xyz/en/{}".format(sub)


def send(src, tgt):
    """Sends a webmention from the src URL to the tgt URL.

    Returns the status code of the webmention request.
    """
    response = ronkyuu.sendWebmention(src, tgt)
    if not response:
        print("Error sending mention: {}".format(response.text))
    return response
