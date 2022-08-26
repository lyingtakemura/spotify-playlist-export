import pytest
from spotify import Spotify


@pytest.fixture
def spotify():
    spotify = Spotify()
    return spotify


playlist_urls = [
    ("https://open.spotify.com/playlist/60S2Vw5q3DPjrYMbLezJa3?si=7c1573053a35455e"),
    ("https://open.spotify.com/playlist/60S2Vw5q3DPjrYMbLezJa3"),
]

@pytest.mark.parametrize("url", playlist_urls)
def test_get_playlist_by_url(spotify, mocker, url):
    mocker.patch('builtins.input', lambda _: url)
    spotify.get_playlist_by_url()
    assert "items" in spotify.playlist.keys()
