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
    '''
    - mock playlist url as user input
    - invoke get_playlist_by_url on spotify object fixture to make api request
    - set tracks total and their objects from response to spotify.playlist dict
    - assert track objects have expected key in it
    - assert playlist track objects quantity equals to expected total quantity
    '''
    mocker.patch('builtins.input', lambda _: url)
    spotify.get_playlist_by_url()
    for _ in spotify.playlist["items"]:
        assert "track" in _.keys()

    assert len(spotify.playlist["items"]) == spotify.playlist["total"]
