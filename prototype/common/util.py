#!/usr/bin/env python
# -*- coding: utf-8 -*


def to_gen(f):
    def to_generator(*args, **kwargs):
        return (i for i in f(*args, **kwargs))
    return to_generator


def swap_arg12(*args):
    return ((args[1],) + (args[0],) + args[2:])
