#!/usr/bin/env python
# -*- coding: utf-8 -*

from itertools import chain, imap


def iflatmap(iterable, f):
    return imap(f, iflatten(iterable))


def iflatten(iterable):
    return chain.from_iterable(iterable)


def itake(iterable, n):
    for i in iterable:
        if n > 0:
            n -= 1
            yield i
        else:
            return


# NOT USED
# original source code is here: http://www.ibm.com/developerworks/linux/library/l-cpyiter/
def ireduce(*args):
    f, iterable, initializer = args
    iterable = iter(iterable)
    curr = iterable.next() if initializer is None else initializer

    for j in iterable:
        curr = f(curr, j)
        yield curr


# NOT USED
def ifoldl(f, iterable, initializer=None):
    return ireduce(f, iterable, initializer)
