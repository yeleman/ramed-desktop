#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import sys

from PyQt4.QtGui import QApplication

from ramed.app_logging import logger
from ramed.ui.mainwindow import MainWindow

app = QApplication(sys.argv)


def main():
    logger.info("startup")
    window = MainWindow(width=400, height=300)
    window.show()
    ret_code = app.exec_()
    app.deleteLater()
    sys.exit(ret_code)

if __name__ == '__main__':
    main()
