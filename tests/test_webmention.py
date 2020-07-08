from unittest import mock

from .context import webmention


def test_get_indiewebxyz_sub_url():
    assert webmention.get_indiewebxyz_sub_url(
        "hottubs") == "https://indieweb.xyz/en/hottubs"


def test_send():
    with mock.patch('tasks.webmention.ronkyuu') as ronkyuu_mock:
        ronkyuu_mock.sendWebmention.return_value = 666
        assert webmention.send('http://src', 'https://tgt') == 666
        ronkyuu_mock.sendWebmention.assert_called_once_with(
            'http://src', 'https://tgt')
