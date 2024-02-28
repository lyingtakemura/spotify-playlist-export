import json


def save_as_json(filename, data):
    with open("playlists/" + filename + ".json", "w") as file:
        file.writelines(json.dumps(data, indent=4))
