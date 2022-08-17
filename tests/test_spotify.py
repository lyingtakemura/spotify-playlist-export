from io import StringIO

import pytest
from spotify import Spotify


@pytest.fixture
def spotify():
    return Spotify()


urls = [
        ("https://open.spotify.com/playlist/60S2Vw5q3DPjrYMbLezJa3?si=1658078b7f1846d4", "60S2Vw5q3DPjrYMbLezJa3"),
        ("https://open.spotify.com/playlist/60S2Vw5q3DPjrYMbLezJa3", "60S2Vw5q3DPjrYMbLezJa3"),
        ("https://open.spotify.com/playlist/00000000000000000", "00000000000000000"),
        ("https://open.spotify.com/playlist/000000000?si=0000000000", "000000000")
    ]


@pytest.mark.parametrize("url, expected", urls)
def test_parse_playlist_id(spotify, monkeypatch, url, expected):
    playlist_url = StringIO(url)
    monkeypatch.setattr('sys.stdin', playlist_url)
    assert spotify._parse_playlist_id() == expected


def test_to_b64_string(spotify):
    assert spotify._to_b64_string("qq", "ww") == "OWIxZjI0ZGNlNjU1NGZlOTgyNWM1ZjNlMmFlYjhmZmU6ZDMyYTA0Y2FiNjdjNGRiOTk0YmI2ODY1NDYyZTcxOTk="
