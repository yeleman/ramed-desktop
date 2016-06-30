#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from PyQt4.QtGui import QIcon
from PyQt4.QtCore import Qt

from static import Constants

from ui.common import CMainWindow
from ui.statusbar import GStatusBar
from ui.home import HomeViewWidget


class MainWindow(CMainWindow):

    def __init__(self):
        CMainWindow.__init__(self)

        self.setWindowIcon(QIcon.fromTheme(
            '', QIcon(u"{}".format(Constants.APP_LOGO))))

        self.statusbar = GStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.change_context(HomeViewWidget)

    def resizeEvent(self, event):
        """lancé à chaque redimensionnement de la fenêtre"""
        # Ajustement en fonction du container
        self.wc = self.width()
        self.hc = self.height()

    def change_context(self, context_widget, *args, **kwargs):
        # instanciate context
        self.view_widget = context_widget(parent=self, *args, **kwargs)
        # attach context to window
        self.setCentralWidget(self.view_widget)

    def open_dialog(self, dialog, modal=False, opacity=0.98, *args, **kwargs):
        d = dialog(parent=self, *args, **kwargs)
        d.setModal(modal)
        d.setWindowOpacity(opacity)
        d.exec_()
