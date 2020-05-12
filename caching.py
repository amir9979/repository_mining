import os
import pickle
import gzip

from config import Config


REPOSITORY_DATA_DIR = Config.get_work_dir_path(Config().config['CACHING']['RepositoryData'])
REPOSITORY_CACHING_DIR = Config.get_work_dir_path(Config().config['CACHING']['RepositoryCaching'])

assert os.path.exists(REPOSITORY_DATA_DIR)
assert os.path.exists(REPOSITORY_CACHING_DIR)


def assert_dir_exists(cache_dir):
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)
    return cache_dir


def cached(cache_name, cache_dir=REPOSITORY_CACHING_DIR):
    """
    A function that creates a decorator which will use "cachefile" for caching the results of the decorated function "fn".
    """
    cache_dir = os.path.join(cache_dir, cache_name)
    assert_dir_exists(cache_dir)

    def decorator(fn):  # define a decorator for a function "fn"
        def wrapped(key='KEY', *args, **kwargs):   # define a wrapper that will finally call "fn" with all arguments
            gzip_cachefile = os.path.abspath(os.path.join(cache_dir, key + ".gzip"))
            assert_dir_exists(os.path.dirname(gzip_cachefile))
            if os.path.exists(gzip_cachefile):
                try:
                    with gzip.GzipFile(gzip_cachefile, 'rb') as cachehandle:
                        return pickle.load(cachehandle)
                except:
                    pass
            # execute the function with all arguments passed
            if fn.__code__.co_argcount == 0:
                res = fn(*args, **kwargs)
            else:
                res = fn(key, *args, **kwargs)

            # write to cache file
            try:
                with gzip.GzipFile(gzip_cachefile, 'wb') as cachehandle:
                    pickle.dump(res, cachehandle, pickle.HIGHEST_PROTOCOL)
            except:
                pass
            return res

        return wrapped

    return decorator   # return this "customized" decorator that uses "cachefile"
