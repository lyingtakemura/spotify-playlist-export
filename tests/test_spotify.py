import pytest
from spotify import Spotify


@pytest.fixture
def spotify():
    return Spotify()


def test_spotify_object_setup(spotify):
    assert spotify.url is not None
    assert spotify.client_id is not None
    assert spotify.client_secret is not None


def test_to_b64_string(spotify):
    assert spotify._to_b64_string("qq", "ww") == "OWIxZjI0ZGNlNjU1NGZlOTgyNWM1ZjNlMmFlYjhmZmU6ZDMyYTA0Y2FiNjdjNGRiOTk0YmI2ODY1NDYyZTcxOTk="
