#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from PyQt4.QtGui import QStatusBar


class StatusBar(QStatusBar):

    DEFAULT_MESSAGE = ""

    def __init__(self, parent):
        super(QStatusBar, self).__init__(parent)
        self.reset()

    def reset(self):
        self.showMessage(self.DEFAULT_MESSAGE)
