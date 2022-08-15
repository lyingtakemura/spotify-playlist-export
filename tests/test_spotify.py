import pytest
from spotify import Spotify


@pytest.fixture
def spotify_object():
    spotify = Spotify()
    return spotify


def test_spotify_object_setup(spotify_object):
    assert spotify_object.url is not None
    assert spotify_object.client_id is not None
    assert spotify_object.client_secret is not None


def test_to_b64_string(spotify_object):
    assert spotify_object._to_b64_string("qq", "ww") == "OWIxZjI0ZGNlNjU1NGZlOTgyNWM1ZjNlMmFlYjhmZmU6ZDMyYTA0Y2FiNjdjNGRiOTk0YmI2ODY1NDYyZTcxOTk="

