#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from PyQt4.QtCore import Qt, QSize
from PyQt4.QtGui import (QMainWindow, QWidget, QTabBar, QIcon)

from static import Constants


class CMainWindow(QMainWindow):

    def __init__(self, parent=0, *args, **kwargs):
        QMainWindow.__init__(self)

        self.setWindowIcon(QIcon.fromTheme('logo', QIcon(
            u"{}logo.png".format(Constants.img_media))))

        self.wc = self.width()
        self.hc = self.height()
        self.resize(self.wc, self.hc)
        self.setWindowTitle(Constants.NAME_ORGA)
        self.setWindowIcon(QIcon(Constants.APP_LOGO))

    def resizeEvent(self, event):
        """lancé à chaque redimensionnement de la fenêtre"""
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


class CWidget(QWidget):

    def __init__(self, parent=0, *args, **kwargs):

        QWidget.__init__(self, parent=parent, *args, **kwargs)

    def refresh(self):
        pass

    def change_main_context(self, context_widget, *args, **kwargs):
        # print("change_main_context")
        return self.parentWidget().change_context(context_widget, *args, **kwargs)

    def open_dialog(self, dialog, modal=False, *args, **kwargs):
        return self.parentWidget().open_dialog(dialog, modal=modal, *args, **kwargs)
