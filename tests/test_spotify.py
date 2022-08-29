import os

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


def test_export_to_csv(spotify):
    """
    - assert file was created
    - assert file size is same as expected
    """
    spotify.playlist = {
        "items": [
            {
                "added_at": "2022-07-26T01:16:19Z",
                "added_by": {
                    "external_urls": {
                        "spotify": "https://open.spotify.com/user/-"
                    },
                    "href": "https://api.spotify.com/v1/users/-",
                    "id": "-",
                    "type": "user",
                    "uri": "spotify:user:-"
                },
                "track": {
                    "album": {
                        "album_type": "single",
                        "artists": [
                            {
                                "external_urls": {
                                    "spotify": "https://open.spotify.com/artist/-"
                                },
                                "href": "https://api.spotify.com/v1/artists/-",
                                "id": "-",
                                "name": "-",
                                "type": "artist",
                                "uri": "spotify:artist:-"
                            }
                        ],

                        "external_urls": {
                            "spotify": "https://open.spotify.com/album/-"
                        },
                        "href": "https://api.spotify.com/v1/albums/-",
                        "id": "-",

                        "name": "2077",
                        "release_date": "2022-01-06",
                        "release_date_precision": "day",
                        "total_tracks": 1,
                        "type": "album",
                        "uri": "spotify:album:-"
                    },
                    "artists": [
                        {
                            "external_urls": {
                                "spotify": "https://open.spotify.com/artist/-"
                            },
                            "href": "https://api.spotify.com/v1/artists/-",
                            "id": "-",
                            "name": "TEST_ARTIST_1",
                            "type": "artist",
                            "uri": "spotify:artist:-"
                        }
                    ],

                    "disc_number": 1,
                    "href": "https://api.spotify.com/v1/tracks/-",
                    "id": "-",
                    "name": "2077",
                    "popularity": 56,
                    "track_number": 1,
                    "type": "track",
                    "uri": "spotify:track:-"
                },
            }
        ]
    }
    spotify.export_to_csv()
    assert os.path.exists("./playlist.csv")
    assert os.path.getsize("./playlist.csv") == 25  # should be 25 bytes
