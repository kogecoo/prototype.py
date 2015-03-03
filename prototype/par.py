#!/usr/bin/env python
# -*- coding: utf-8 -*

from common import builtin_patcher, trivial_patcher
from common.util import swap_arg12
from parallel import parallel
from parallel.parallel_collections import ParallelGen
from types import GeneratorType


# TODO: make it use it with lambda. the limitation caused by multiprocessing will be resolved by followings:
# http://stackoverflow.com/questions/19984152/what-can-multiprocessing-and-dill-do-together
# http://stackoverflow.com/questions/3288595/multiprocessing-using-pool-map-on-a-function-defined-in-a-class
# http://matthewrocklin.com/blog/work/2013/12/05/Parallelism-and-Serialization/

# seq.par().foreach(func) may be confusing.
#  In this writing style, seq seems to be modified but in reallity,
# nothing happens to seq.
#  If users want to obtain the result by foreach, it is contained in
# seq.par() so it need to be written as follows.
# >>> s = seq.par()
# >>> s.foreach(func) # s is ParallelGen instance which contains modified seq
#
#  We now have 2 options to tackle this issue.
# 1. Write wrapper function for foreach and it changes seq directly.
#  - We don't study its feasibility.
# 2. Delete foreach attribute when patch() is called.
#  - We think foreach is unnecessary functionality for this library.

attrs = {
    'fold': lambda *args: reduce(*swap_arg12(*args)),
    'to_single': lambda self: (x for x in self.data)
}

attrs_for_bltins = {
    'par': lambda it: parallel(it)
}


def attach_to_builtins():

    for k, v in attrs_for_bltins.items():
        builtin_patcher.attach(list, k, v)
        builtin_patcher.attach(tuple, k, v)
        builtin_patcher.attach(GeneratorType, k, v)


def detach_to_builtins():
    for k in attrs_for_bltins.keys():
        builtin_patcher.detach(list, k)
        builtin_patcher.detach(tuple, k)
        builtin_patcher.detach(GeneratorType, k)


def attach_to_par():
    for k, v in attrs.items():
        trivial_patcher.attach(ParallelGen, k, v)


def detach_to_par():
    for k in attrs.keys():
        trivial_patcher.detach(ParallelGen, k)


def attach():
    attach_to_builtins()
    attach_to_par()


def detach():
    detach_to_builtins()
    detach_to_par()
