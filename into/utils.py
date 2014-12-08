from __future__ import absolute_import, division, print_function

from contextlib import contextmanager
import tempfile
import os


def expand_tuples(L):
    """

    >>> expand_tuples([1, (2, 3)])
    [(1, 2), (1, 3)]

    >>> expand_tuples([1, 2])
    [(1, 2)]
    """
    if not L:
        return [()]
    elif not isinstance(L[0], tuple):
        rest = expand_tuples(L[1:])
        return [(L[0],) + t for t in rest]
    else:
        rest = expand_tuples(L[1:])
        return [(item,) + t for t in rest for item in L[0]]

@contextmanager
def tmpfile(extension=''):
    extension = '.' + extension.lstrip('.')
    handle, filename = tempfile.mkstemp(extension)

    yield filename

    try:
        if os.path.exists(filename):
            os.remove(filename)
    except OSError:  # Sometimes Windows can't close files
        if os.name == 'nt':
            os.close(handle)
            try:
                os.remove(filename)
            except OSError:  # finally give up
                pass