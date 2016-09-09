#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import subprocess
import os

from ramed.static import Constants


def launch_without_console(command, args):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return subprocess.Popen([command] + args, startupinfo=startupinfo).wait()


def create_shortcut(source, destination):
    program = os.path.join(Constants.WORKING_DIR, 'Shortcut.exe')

    args = ["/f:{}".format(destination),
            "/a:c",
            "/t:{}".format(source)]
    if Constants.IS_FROZEN:
        launch_without_console(program, args)
    else:
        subprocess.call("{} {}".format(program, " ".join(args)))
