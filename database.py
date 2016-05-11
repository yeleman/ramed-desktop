#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import, division,
                        print_function)

from models import User


def setup(drop_tables=False):
    """ Create table if not exit """
    did_create = False

    for model in [User, ]:
        if drop_tables:
            model.droptable()
        if not model.table_exists():
            model.create_table()
            did_create = True

setup()
