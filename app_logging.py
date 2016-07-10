#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import sys
import logging

# disable logging on Windows exe
if not hasattr(sys, 'frozen'):
    logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('RAMED')
