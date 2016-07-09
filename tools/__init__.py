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


def launch_without_console(command, args):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return subprocess.Popen([command] + args, startupinfo=startupinfo).wait()


def create_shortcut(source, destination):
    program = os.path.join(Constants.WORKING_DIR, 'Shortcut.exe')
    # cmd = '{program} /f:"{destination}" /a:c /t:"{source}"'.format(
    #     program=program, source=source, destination=destination)
    args = ["/f:{}".format(destination),
            "/a:c",
            "/t:{}".format(source)]
    if Constants.SYSTEM.lower() == "windows":
        launch_without_console(program, args)
    else:
        subprocess.call(program + " ".join(args))
