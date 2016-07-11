#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from PyQt4.QtCore import Qt, QDate
from PyQt4.QtGui import (QWidget, QLabel, QPushButton, QDateTimeEdit)

from static import Constants


class BaseWidget(QWidget):

    def __init__(self, parent=0, *args, **kwargs):
        super(QWidget, self).__init__(parent, *args, **kwargs)

    def change_main_context(self, *args, **kwargs):
        return self.parentWidget().change_context(*args, **kwargs)

    def open_dialog(self, *args, **kwargs):
        return self.parentWidget().open_dialog(*args, **kwargs)


class DateTimeEdit(QDateTimeEdit):

    def __init__(self, *args, **kwargs):
        super(DateTimeEdit, self).__init__(*args, **kwargs)
        self.setDisplayFormat(Constants.DATE_DISPLAY_FORMAT)
        self.setCalendarPopup(True)

    def setPythonDate(self, value):
        self.setDate(QDate(value))


class Label(QLabel):

    def __init__(self, text, parent=None):
        super(QLabel, self).__init__(text, parent)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)


class PushButton(QPushButton):

    def __init__(self, *args, **kwargs):
        super(PushButton, self).__init__(*args, **kwargs)
        self.setCursor(Qt.PointingHandCursor)


class CancelPushButton(PushButton):

    def __init__(self, *args, **kwargs):
        super(CancelPushButton, self).__init__(*args, **kwargs)
