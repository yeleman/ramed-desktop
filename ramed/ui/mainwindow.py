#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from PyQt4.QtCore import Qt, pyqtSlot, QThread
from PyQt4.QtGui import QMainWindow, QIcon

from ramed.app_logging import logger
from ramed.static import Constants
from ramed.tools.ramed_export import RamedExporter
from ramed.ui.statusbar import StatusBar
from ramed.ui.home import HomeViewWidget
from ramed.ui.confirmation import ConfirmationWidget


class MainWindow(QMainWindow):

    def __init__(self, width=None, height=None):
        super(QMainWindow, self).__init__()

        self.requested_width = width
        self.requested_height = height
        if self.requested_width and self.requested_height:
            self.resize(self.requested_width, self.requested_height)
        self.setWindowTitle(Constants.APP_TITLE)
        self.setWindowIcon(QIcon(Constants.intpath(Constants.PNG_ICON)))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)

        self.reset()

    def change_context(self, context_widget, *args, **kwargs):
        self.view_widget = context_widget(parent=self, *args, **kwargs)
        self.setCentralWidget(self.view_widget)

    def open_dialog(self, dialog, modal=False, opacity=0.98, *args, **kwargs):
        d = dialog(parent=self, *args, **kwargs)
        d.setModal(modal)
        d.setWindowOpacity(opacity)
        d.exec_()

    # override
    def closeEvent(self, event):
        if self.exporter.is_running:
            event.ignore()

            logger.debug("exporter running, cancelling...")
            self.exporter.cancel()

            # wait for canceled signal to exit (after warning popup)
            self.is_exiting = True
            return
        super(MainWindow, self).closeEvent(event)

    def do_close(self):
        self.is_exiting = False
        self.close()

    def reset(self):
        self.statusbar = StatusBar(self)
        self.setStatusBar(self.statusbar)
        self.change_context(HomeViewWidget)

        # exporter
        self.exporter = RamedExporter(main_window=self)
        self.exporter_thread = QThread()
        self.exporter.moveToThread(self.exporter_thread)
        self.exporter.export_ended.connect(self.exporter_thread.quit)
        self.exporter.export_canceled.connect(self.exporter_thread.quit)
        self.exporter_thread.started.connect(self.exporter.start)
        self.is_exiting = False

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
        logger.debug("check started")

    @pyqtSlot(bool, str)
    def check_ended(self, succeeded, error_message):
        logger.debug("check ended: {}, {}".format(succeeded, error_message))
        if succeeded:
            self.view_widget.start_export()
        else:
            self.view_widget.display_missing_aggregate_confirmation()

    @pyqtSlot()
    def parsing_started(self):
        logger.debug("parsing started")

    @pyqtSlot(bool, int, str)
    def parsing_ended(self, succeeded, nb_instances, error_message):
        logger.debug("parsing ended: {}, {}, {}"
                     .format(succeeded, nb_instances, error_message))
        if succeeded:
            self.exporter_thread.start()

    @pyqtSlot(str)
    def export_started(self):
        logger.debug("export_started")

    @pyqtSlot(str, int)
    def exporting_instance(self, ident, index):
        logger.debug("exporting_instance")
        self.statusbar.showMessage(ident)

    @pyqtSlot(bool, int, int)
    def instance_completed(self, succeeded, index, total):
        logger.debug("instance_completed")

    @pyqtSlot(int, int)
    def export_ended(self, nb_instances_successful, nb_instances_failed):
        logger.debug("export_ended: {}, {}"
                     .format(nb_instances_successful, nb_instances_failed))
        self.statusbar.reset()
        self.change_context(ConfirmationWidget,
                            nb_instances_successful=nb_instances_successful,
                            nb_instances_failed=nb_instances_failed,
                            nb_medias_successful="?",
                            nb_medias_failed="?",
                            from_date="?", to_date="?")

    @pyqtSlot()
    def export_canceled(self):
        self.statusbar.reset()

    @pyqtSlot(str)
    def export_error_raised(self, error_message):
        logger.debug("export_error_raised: {}".format(error_message))
