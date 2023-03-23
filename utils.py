def timeit(func):
    from datetime import datetime

    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        time = end - start
        print("{} RUN TOOK: {}".format(func.__name__.upper(), time))
        return result

    return wrapper


def set_playlist_path():
    from datetime import datetime

    now = datetime.now()
    path = "{}_{}".format(now.date(), now.time().replace(microsecond=0))
    return "/playlists/{}".format(path)
