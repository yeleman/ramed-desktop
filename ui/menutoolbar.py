# !/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from PyQt4.QtGui import (QIcon, QToolBar, QFont, QCursor)
from PyQt4.QtCore import Qt, QSize

from ui.common import CWidget

from static import Constants

from ui.example import ExampleViewWidget


class MenuToolBar(QToolBar, CWidget):

    def __init__(self, parent=None, *args, **kwargs):
        QToolBar.__init__(self, parent, *args, **kwargs)

        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        menu = [{"name": u"Tableau de bord", "icon": 'example',
                 "admin": False, "goto": ExampleViewWidget}, ]

        for m in menu:
            self.addAction(QIcon("{}{}.png".format(Constants.img_media, m.get(
                'icon'))), m.get('name'), lambda m=m: self.goto(m.get('goto')))
            self.addSeparator()

    def goto(self, goto):
        self.change_main_context(goto)
