#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import logging

from ramed.static import Constants

# disable logging on Windows exe
if not Constants.IS_FROZEN or Constants.VERBOSE:
    logging.basicConfig(level=Constants.LOG_LEVEL)
else:
    # disable requests
    pass
for log_id in ('requests.packages.urllib3',
               'requests.exceptions.ConnectTimeout',
               'socket.timeout'):
    verbose_logger = logging.getLogger(log_id)
    verbose_logger.propagate = False
    verbose_logger.disabled = True
logger = logging.getLogger('RAMED')
