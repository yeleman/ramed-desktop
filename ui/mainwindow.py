#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from PyQt4.QtGui import QIcon
from PyQt4.QtCore import Qt, pyqtSlot

from static import Constants

from ui.common import CMainWindow
from ui.statusbar import GStatusBar
from ui.home import HomeViewWidget
from ui.confirmation import ConfirmationViewWidget
from tools.ramed_export import RamedExporter


class MainWindow(CMainWindow):

    def __init__(self):
        CMainWindow.__init__(self)

        self.setWindowIcon(QIcon.fromTheme(
            '', QIcon(u"{}".format(Constants.APP_LOGO))))

        self.statusbar = GStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.change_context(HomeViewWidget)

        # exporter
        self.exporter = RamedExporter(main_window=self)

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

    @pyqtSlot()
    def check_started(self):
        print("check started")

    @pyqtSlot(bool, str)
    def check_ended(self, succeeded, error_message):
        print("check ended", succeeded, error_message)
        if succeeded:
            self.view_widget.launch_export()
        else:
            self.view_widget.display_noaggregate_confirmation()

    @pyqtSlot()
    def parsing_started(self):
        print("parsing started")

    @pyqtSlot(bool, int, str)
    def parsing_ended(self, succeeded, nb_instances, error_message):
        print("parsing ended", succeeded, nb_instances, error_message)
        if succeeded:
            self.exporter.start()

    @pyqtSlot(str)
    def export_started(self):
        print("export_started")

    @pyqtSlot(str)
    def export_failed(self, error_message):
        print("export_failed", error_message)

    @pyqtSlot(int, int)
    def export_ended(self, nb_instances_successful, nb_instances_failed):
        print("export_ended", nb_instances_successful, nb_instances_failed)
        self.change_context(ConfirmationViewWidget,
                            nb_instances_successful=nb_instances_successful,
                            nb_instances_failed=nb_instances_failed)

    @pyqtSlot(str)
    def export_raised_error(self, error_message):
        print("export_raised_error", error_message)
