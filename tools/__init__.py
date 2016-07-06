#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import subprocess
import os

from static import Constants

logger = logging.getLogger(__name__)


def create_shortcut(source, destination):
    program = os.path.join(Constants.WORKING_DIR, 'Shortcut.exe')
    cmd = '{program} /f:"{destination}" /a:c /t:"{source}"'.format(
        program=program, source=source, destination=destination)
    subprocess.call(cmd)
