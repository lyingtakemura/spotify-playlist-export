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
