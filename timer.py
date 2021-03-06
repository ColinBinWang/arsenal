import numpy as np
from time import time
from contextlib import contextmanager
from arsenal.humanreadable import htime

class Timer(object):
    """
    >>> from time import sleep
    >>> a = Timer('A')
    >>> b = Timer('B')
    >>> with a:
    ...     sleep(0.5)
    >>> with b:
    ...     sleep(1)
    >>> a.compare(b)          #doctest:+SKIP
    A is 2.0018x faster

    """
    def __init__(self, name):
        self.name = name
        self.times = []
        self.b4 = None
    def __enter__(self):
        self.b4 = time()
    def __exit__(self, *_):
        self.times.append(time() - self.b4)
    def __str__(self):
        return 'Timer(name=%s, avg=%g, std=%g)' % (self.name, self.avg, self.std)
    @property
    def avg(self):
        return np.mean(self.times)
    @property
    def std(self):
        return np.std(self.times, ddof=1)
    def compare(self, other):
        if self.avg <= other.avg:
            print '%s is %gx faster' % (self.name, other.avg / self.avg)
        else:
            other.compare(self)


@contextmanager
def timeit(msg="%.4f seconds", header=None):
    """Context Manager which prints the time it took to run code block."""
    if header is not None:
        print header
    b4 = time()
    yield

    t = time() - b4
    ht = htime(t)
    if t < 60:
        ht = t
    try:
        print msg % ht
    except TypeError:
        print msg, ht

timesection = lambda x: timeit(header='%s...' % x,
                               msg=' -> %s took %%.2f seconds' % x)
