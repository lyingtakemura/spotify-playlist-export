import datetime


def timeit(func):

    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        result = func(*args, **kwargs)
        end = datetime.datetime.now()
        time = end - start
        print("{} RUN TOOK: {}".format(func.__name__.upper(), time))
        return result
    return wrapper
