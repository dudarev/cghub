import atexit
from cProfile import Profile


class Profiler(object):
    def __init__(self, fn, filename, skip):
        self.fn = fn
        self.filename = filename
        self.skip = skip
        self.profiler = Profile()
        atexit.register(self.dump_stats)

    def __call__(self, *args, **kwargs):
        if self.skip:
            return self.fn(*args, **kwargs)
        return self.profiler.runcall(self.fn, *args, **kwargs)

    def dump_stats(self):
        if self.filename and not self.skip:
            self.profiler.dump_stats(self.filename)


def profile(fn=None, filename=None, skip=False):
    if fn is None:
        def decorator(fn):
            return profile(fn, filename, skip)

        return decorator

    profiler = Profiler(fn, filename, skip)

    def wrapper(*args, **kwargs):
        return profiler(*args, **kwargs)

    wrapper.__doc__ = fn.__doc__
    wrapper.__name__ = fn.__name__
    wrapper.__dict__ = fn.__dict__
    wrapper.__module__ = fn.__module__
    return wrapper
