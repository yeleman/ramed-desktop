#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import logging

from static import Constants

# disable logging on Windows exe
if not Constants.IS_FROZEN or Constants.VERBOSE:
    logging.basicConfig(level=Constants.LOG_LEVEL)
logger = logging.getLogger('RAMED')
