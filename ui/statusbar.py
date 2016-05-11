#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from PyQt4.QtGui import QStatusBar

from static import Constants


class GStatusBar(QStatusBar):

    def __init__(self, parent):

        QStatusBar.__init__(self, parent)
        self.showMessage(u"Bienvenue sur {}.".format(Constants.APP_NAME))
