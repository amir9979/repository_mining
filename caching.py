import os
import pickle
import gzip

from config import Config


REPOSITORY_DATA_DIR = Config.get_work_dir_path(Config().config['CACHING']['RepositoryData'])
REPOSITORY_CACHING_DIR = Config.get_work_dir_path(Config().config['CACHING']['RepositoryCaching'])


def assert_dir_exists(cache_dir):
    if not cache_dir.exists():
        cache_dir.mkdir()
    return cache_dir


assert REPOSITORY_DATA_DIR and assert_dir_exists(REPOSITORY_DATA_DIR)
assert REPOSITORY_CACHING_DIR and assert_dir_exists(REPOSITORY_CACHING_DIR)


def cached(cache_name, cache_dir=REPOSITORY_CACHING_DIR):
    """
    A function that creates a decorator which will use "cachefile" for caching the results of the decorated function "fn".
    """
    cache_dir = cache_dir.joinpath(cache_name)
    assert_dir_exists(cache_dir)

    def decorator(fn):  # define a decorator for a function "fn"
        def wrapped(key='KEY', *args, **kwargs):   # define a wrapper that will finally call "fn" with all arguments
            key_ = key
            if type(key) != type(''):
                key_ = key.github_name
            gzip_cachefile = cache_dir.joinpath(key_ + ".gzip")
            assert_dir_exists(gzip_cachefile.parent)
            if gzip_cachefile.exists():
                try:
                    with gzip.GzipFile(gzip_cachefile, 'rb') as cachehandle:
                        print(f"read {key} from cache")
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
                with gzip.GzipFile(os.path.join(*gzip_cachefile.parts), 'wb') as cachehandle:
                    pickle.dump(res, cachehandle, pickle.HIGHEST_PROTOCOL)
            except Exception as e:
                raise e
            return res

        return wrapped

    return decorator   # return this "customized" decorator that uses "cachefile"
