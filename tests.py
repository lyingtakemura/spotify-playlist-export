import json

import pytest

from main import Spotify


@pytest.fixture(scope="module")
def spotify():
    _ = Spotify()
    with open("input.json") as file:
        _.playlist = json.load(file)
        _.playlist = _.playlist["items"]
    return _


def test_parse_playlist(spotify):
    """
    - check if result is list
    - check if list items are tuples with 3 items each
    """
    spotify.parse_playlist()
    assert isinstance(spotify.playlist, list)
    assert isinstance(spotify.playlist[0], tuple)
    assert len(spotify.playlist[0]) == 3


def test_export_to_csv(spotify, tmp_path, mocker):
    """
    - check if exported file exists in tmp directory
    - check if first line is not empty
    - check if first line is in appropriate format
    """
    path = str(tmp_path) + "/test_file"
    mocker.patch.object(spotify, "playlist_filepath", return_value=path)
    spotify.export_to_csv()
    with open(path + ".csv", "r") as file:
        line = file.readline()
        assert len(line) > 1
        assert len(line.split('"')) == 3
