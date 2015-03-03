#!/usr/bin/env python
# -*- coding: utf-8 -*


def attach(typ, name, value):
    setattr(typ, name, value)


def detach(typ, name):
    delattr(typ, name)
