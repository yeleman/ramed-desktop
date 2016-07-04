#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from os.path import expanduser
from datetime import date

from PyQt4.QtGui import (QHBoxLayout, QVBoxLayout, QProgressBar, QDialog,
                         QGridLayout, QFileDialog, QGroupBox, QWidget)
from PyQt4.QtCore import Qt, QDate

from static import Constants

from ui.common import (CWidget, FormatDate, FormLabel, Deleted_btn, Button)

from ui.dialogue_box import dialogueViewWidget
try:
    unicode
except:
    unicode = str


class HomeViewWidget(CWidget):

    def __init__(self, parent=0, *args, **kwargs):
        super(HomeViewWidget, self).__init__(parent=parent, *args, **kwargs)
        self.parentWidget().setWindowTitle("Export des fichier de collect RAMED")

        self.createDestinationGroupBox()
        self.createPeriodeGroupBox()
        self.createProgressGroupBox()

        self.browse_file_btn = Button(
            "Sélection fichier JSON ODK Aggregate ...", self)
        self.browse_file_btn.clicked.connect(self.getJsonFile)
        self.file_name_field = FormLabel("Aucun fichier")
        self.run_btn = Button("Lancer")
        self.run_btn.setEnabled(False)
        self.run_btn.clicked.connect(self.run_generation)
        self.cancel_btn = Deleted_btn("Annuler")

        gridBox = QGridLayout()
        gridBox.addWidget(self.browse_file_btn, 0, 0)
        gridBox.addWidget(self.file_name_field, 1, 0)
        gridBox.addWidget(self.destinationGroupBox, 2, 0)
        gridBox.addWidget(self.periodGroupBox, 3, 0)
        gridBox.addWidget(self.run_btn, 3, 2)
        gridBox.addWidget(self.progressGroupBox, 4, 0)
        gridBox.addWidget(self.cancel_btn, 4, 2)
        # gridBox.setColumnStretch(3, 1)
        gridBox.setRowStretch(5, 2)

        vBox = QVBoxLayout()
        vBox_ = QVBoxLayout()
        vBox_.addLayout(gridBox)
        vBox.addLayout(vBox_)
        self.setLayout(vBox)

    def run_generation(self):
        print("run_generation")
        self.parentWidget().exporter.check_aggregate_presence()

    def display_noaggregate_confirmation(self):
        if dialogueViewWidget(parent=None).exec_() == QDialog.Accepted:
            self.launch_export()

    def launch_export(self):
        print("Lancement ...")
        self.parentWidget().exporter.parse(self.file_name_field.text())

    def getJsonFile(self):
        self.file_name_field.setText("Aucun fichier")
        self.run_btn.setEnabled(False)
        name_select_f = QFileDialog.getOpenFileName(
            QWidget(), "Open Data File", "", "Json data files (*.json)")
        if name_select_f != "":
            self.file_name_field.setText(name_select_f)
            self.run_btn.setEnabled(True)

    def selectDirectory(self):
        self.destFolder = str(
            QFileDialog.getExistingDirectory(self, "Selection dossier"))
        self.destination_btn.setText(self.destFolder)

    def createDestinationGroupBox(self):
        self.destinationGroupBox = QGroupBox("Destination")
        layout = QGridLayout()
        self.destFolder = expanduser("~")
        self.destination_btn = Button(self.destFolder, self)
        self.destination_btn.clicked.connect(self.selectDirectory)
        layout.addWidget(self.destination_btn, 1, 0)

        self.destinationGroupBox.setLayout(layout)

    def createPeriodeGroupBox(self):
        self.periodGroupBox = QGroupBox("Periode")
        layout = QGridLayout()
        self.on_date = FormatDate(
            QDate(date.today().year, date.today().month, 1))
        # self.on_date.setMaximumWi(20)
        self.end_date = FormatDate(QDate.currentDate())
        layout.addWidget(FormLabel("Date debut"), 2, 0)
        layout.addWidget(self.on_date, 3, 0)
        layout.addWidget(FormLabel("Date fin"), 2, 1)
        layout.addWidget(self.end_date, 3, 1)

        self.periodGroupBox.setLayout(layout)

    def createProgressGroupBox(self):
        self.progressbarLabel = "Export en cours...  34/403"
        self.progressGroupBox = QGroupBox(self.progressbarLabel)
        layout = QGridLayout()

        self.progressbar = QProgressBar()
        self.progressbar.setMinimum(1)
        self.progressbar.setMaximum(100)
        self.progressbar.setValue(20)
        layout.addWidget(self.progressbar, 0, 1)

        self.progressGroupBox.setLayout(layout)
