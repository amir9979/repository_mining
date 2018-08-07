import os
import pickle
import gzip

REPOSIROTY_DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "repository_data")
REPOSIROTY_CACHING_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "repository_caching")
assert os.path.exists(REPOSIROTY_DATA_DIR)
assert os.path.exists(REPOSIROTY_CACHING_DIR)


def assert_dir_exists(cache_dir):
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)


def cached(cache_name, cache_dir=REPOSIROTY_CACHING_DIR):
    """
    A function that creates a decorator which will use "cachefile" for caching the results of the decorated function "fn".
    """
    cache_dir = os.path.join(cache_dir, cache_name)
    assert_dir_exists(cache_dir)
    def decorator(fn):  # define a decorator for a function "fn"
        def wrapped(key='KEY', *args, **kwargs):   # define a wrapper that will finally call "fn" with all arguments
            # if cache exists -> load it and return its content
            # cachefile = os.path.abspath(os.path.join(cache_dir, key))
            gzip_cachefile = os.path.abspath(os.path.join(cache_dir, key + ".gzip"))
            # assert_dir_exists(os.path.dirname(cachefile))
            assert_dir_exists(os.path.dirname(gzip_cachefile))
            # if os.path.exists(cachefile):
            #         with open(cachefile, 'rb') as cachehandle:
            #             return pickle.load(cachehandle)
            if os.path.exists(gzip_cachefile):
                with gzip.GzipFile(gzip_cachefile, 'rb') as cachehandle:
                    return pickle.load(cachehandle)


            # execute the function with all arguments passed
            if fn.func_code.co_argcount == 0:
                res = fn(*args, **kwargs)
            else:
                res = fn(key, *args, **kwargs)

            # write to cache file
            with gzip.GzipFile(gzip_cachefile, 'wb') as cachehandle:
                pickle.dump(res, cachehandle, pickle.HIGHEST_PROTOCOL)

            return res

        return wrapped

    return decorator   # return this "customized" decorator that uses "cachefile"
