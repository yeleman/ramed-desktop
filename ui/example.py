#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from PyQt4.QtGui import QHBoxLayout, QGridLayout, QPushButton

from static import Constants

from tools.xlsx_export import xlsx_example
from tools.pdf_export import pdf_example
from ui.common import (CWidget)

try:
    unicode
except:
    unicode = str


class ExampleViewWidget(CWidget):

    def __init__(self, parent=0, *args, **kwargs):
        super(ExampleViewWidget, self).__init__(parent=parent, *args, **kwargs)
        self.parentWidget().setWindowTitle("Hello hello how low")

        self.btt_xlsx_export = QPushButton(u"Export xlsx", self)
        self.btt_xlsx_export.clicked.connect(xlsx_example)
        self.btt_pdf_export = QPushButton(u"Export pdf", self)
        self.btt_pdf_export.clicked.connect(pdf_example)

        hbox = QHBoxLayout(self)

        editbox = QGridLayout()

        editbox.addWidget(self.btt_xlsx_export, 0, 0)
        editbox.addWidget(self.btt_pdf_export, 0, 1)
        hbox.addLayout(editbox)
        self.setLayout(hbox)
