from io import StringIO

import pytest
from spotify import Spotify


@pytest.fixture
def spotify():
    spotify = Spotify()
    return spotify


urls = [
        ("https://open.spotify.com/playlist/qqqqqqqq?si=qqqqqqqq", "qqqqqqqq"),
        ("https://open.spotify.com/playlist/qqqqqqqqqq", "qqqqqqqqqq"),
        ("https://open.spotify.com/playlist/000000000000", "000000000000"),
        ("https://open.spotify.com/playlist/0000000?si=0000000", "0000000")
    ]


@pytest.mark.parametrize("url, expected", urls)
def test_parse_playlist_id(spotify, mocker, url, expected):
    playlist_url = StringIO(url)
    mocker.patch('sys.stdin', playlist_url)
    spotify._parse_playlist_id()
    assert spotify.playlist_id == expected
