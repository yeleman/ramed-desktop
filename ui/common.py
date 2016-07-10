#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from PyQt4.QtCore import Qt, QDate
from PyQt4.QtGui import (QMainWindow, QWidget, QLabel, QPushButton,
                         QIcon, QDateTimeEdit)

from static import Constants


class CMainWindow(QMainWindow):

    def __init__(self, parent=0, *args, **kwargs):
        QMainWindow.__init__(self)

        self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        self.setWindowIcon(QIcon.fromTheme('logo', QIcon(
            u"{}logo.png".format(Constants.IMG_MEDIA))))
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
        return self.parentWidget().change_context(
            context_widget, *args, **kwargs)

    def open_dialog(self, dialog, modal=False, *args, **kwargs):
        return self.parentWidget().open_dialog(
            dialog, modal=modal, *args, **kwargs)


class FormatDate(QDateTimeEdit):

    def __init__(self, *args, **kwargs):
        super(FormatDate, self).__init__(*args, **kwargs)
        self.setDisplayFormat(u"dd/MM/yyyy")
        self.setCalendarPopup(True)

    def setPythonDate(self, value):
        self.setDate(QDate(value))


class FormLabel(QLabel):

    def __init__(self, text, parent=None):
        QLabel.__init__(self, text, parent)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)


class Button(QPushButton):

    def __init__(self, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        self.setAutoDefault(True)
        self.setIcon(QIcon.fromTheme('', QIcon('')))
        self.setCursor(Qt.PointingHandCursor)


class CancelButton(Button):

    def __init__(self, *args, **kwargs):
        super(CancelButton, self).__init__(*args, **kwargs)
