#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from PyQt4.QtGui import QStatusBar


class GStatusBar(QStatusBar):

    DEFAULT_MESSAGE = ""

    def __init__(self, parent):

        QStatusBar.__init__(self, parent)
        self.reset()

    def reset(self):
        self.showMessage(self.DEFAULT_MESSAGE)
