#!/usr/bin/env python
# -*- coding: utf-8 -*

# The code in this file is written under the influence of Pipe and Python-Parallel-Collections
# https://github.com/JulienPalard/Pipe
# https://github.com/gterzian/Python-Parallel-Collections

from itertools import ifilter, imap, izip, takewhile
from common.util import swap_arg12, to_gen
from common.itertools_more import itake, iflatten, iflatmap
from types import GeneratorType
from common import builtin_patcher


# make it be able to patching with 'with' statement.
# http://qiita.com/yamaneko1212/items/93dfbb74c97bd69b8e0c


_tailor = lambda f, args: to_gen(f)(*swap_arg12(*args))


attrs = {
    'map':       lambda *args: _tailor(imap, args),
    'reduce':    lambda *args: reduce(*swap_arg12(*args)),
    'filter':    lambda *args: _tailor(ifilter, args),
    'zip':       to_gen(izip),
    'takewhile': lambda *args: _tailor(takewhile, args),
    'take':      itake,
    'flatmap':   to_gen(iflatmap),
    'flatten':   to_gen(iflatten),
    'foldl':     lambda *args: reduce(*swap_arg12(*args)),
    'len':       lambda self: len(self),
    'to_iter':   lambda self: iter(self),
    'to_list':   lambda self: list(self)
}


def attach():
    for k, v in attrs.items():
        builtin_patcher.attach(tuple, k, v)
        builtin_patcher.attach(list, k, v)
        builtin_patcher.attach(GeneratorType, k, v)


def detach():
    for k in attrs.keys():
        builtin_patcher.detach(tuple, k)
        builtin_patcher.detach(list, k)
        builtin_patcher.detach(GeneratorType, k)
