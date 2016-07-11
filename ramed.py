#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import sys

from PyQt4.QtGui import QApplication

from app_logging import logger
from ui.mainwindow import MainWindow

app = QApplication(sys.argv)


def main():
    logger.info("startup")
    window = MainWindow(width=400, height=300)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
