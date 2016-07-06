#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import sys

from PyQt4.QtGui import QApplication

from ui.mainwindow import MainWindow

logger = logging.getLogger(__name__)
app = QApplication(sys.argv)


def main():

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
