#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (
    unicode_literals, absolute_import, division, print_function)

import os
import datetime

from PyQt4.QtGui import (QVBoxLayout, QProgressBar, QDialog,
                         QGridLayout, QFileDialog, QGroupBox)
from PyQt4.QtCore import QDate, pyqtSlot

from static import Constants
from ui.common import (CWidget, FormatDate, FormLabel, DeletedBtn, Button)
from ui.dialogue_box import dialogueViewWidget


class HomeViewWidget(CWidget):

    def __init__(self, parent=0, *args, **kwargs):
        super(HomeViewWidget, self).__init__(parent=parent, *args, **kwargs)

        # inputs
        self._json_fpath = None
        self._destination_folder = self.guess_destination()
        self._from_date, self._to_date = self.guess_dates()
        self.nb_instances = 0

        self.setup_ui()

    def setup_ui(self):
        # json file selector
        self.json_groupbox = QGroupBox("Export ODK Aggregate")
        layout = QGridLayout()
        self.browse_file_btn = Button(
            "Sélection fichier JSON ODK Aggregate ...", self)
        self.browse_file_btn.clicked.connect(self.json_file_selected)
        layout.addWidget(self.browse_file_btn, 1, 0)
        self.json_groupbox.setLayout(layout)

        # destination folder selector
        self.destination_groupbox = QGroupBox("Destination")
        layout = QGridLayout()
        self.destination_btn = Button(self.destination_folder, self)
        self.destination_btn.clicked.connect(self.directory_selected)
        layout.addWidget(self.destination_btn, 1, 0)
        self.destination_groupbox.setLayout(layout)

        # period calendars
        today = datetime.date.today()
        self.period_groupbox = QGroupBox("Période")
        layout = QGridLayout()
        self.from_date_selector = FormatDate(QDate(self.from_date))
        self.from_date_selector.dateChanged.connect(self.from_date_changed)
        self.from_date_selector.setMaximumDate(self.to_date)
        self.to_date_selector = FormatDate(QDate(self.to_date))
        self.to_date_selector.dateChanged.connect(self.to_date_changed)
        self.to_date_selector.setMinimumDate(self.from_date)
        self.to_date_selector.setMaximumDate(today)
        layout.addWidget(FormLabel("Du"), 2, 0)
        layout.addWidget(self.from_date_selector, 3, 0)
        layout.addWidget(FormLabel("Au"), 2, 1)
        layout.addWidget(self.to_date_selector, 3, 1)
        self.period_groupbox.setLayout(layout)

        # start button
        self.start_button = Button("Lancer")
        self.start_button.setEnabled(False)
        self.start_button.clicked.connect(self.export_requested)

        # cancel button
        self.cancel_btn = DeletedBtn("Annuler")

        # progression bar
        self.progression_groupbox = QGroupBox("...")
        layout = QGridLayout()
        self.progressbar = QProgressBar()
        self.progressbar.setMinimum(1)
        self.progressbar.setMaximum(100)
        self.progressbar.setValue(0)
        layout.addWidget(self.progressbar, 0, 1)
        self.progression_groupbox.setLayout(layout)

        # grid (list-like)
        self.gridBox = QGridLayout()
        self.gridBox.addWidget(self.json_groupbox, 0, 0)
        self.gridBox.addWidget(self.destination_groupbox, 1, 0)
        self.gridBox.addWidget(self.period_groupbox, 2, 0)
        self.gridBox.addWidget(self.start_button, 3, 0)
        self.gridBox.setRowStretch(5, 2)

        vBox = QVBoxLayout()
        vBox.addLayout(self.gridBox)
        self.setLayout(vBox)

    @property
    def json_fpath(self):
        return self._json_fpath

    @json_fpath.setter
    def json_fpath(self, value):
        self._json_fpath = value
        self.browse_file_btn.setText(value)
        self.update_start_button_state()

    @property
    def destination_folder(self):
        return self._destination_folder

    @destination_folder.setter
    def destination_folder(self, value):
        self._destination_folder = value
        self.destination_btn.setText(self.destination_folder)
        self.update_start_button_state()

    @property
    def from_date(self):
        return self._from_date

    @from_date.setter
    def from_date(self, value):
        self._from_date = value
        self.from_date_selector.setPythonDate(self.from_date)
        self.update_start_button_state()

    @property
    def to_date(self):
        return self._to_date

    @to_date.setter
    def to_date(self, value):
        self._to_date = value
        self.to_date_selector.setPythonDate(self.to_date)
        self.update_start_button_state()

    def guess_destination(self, root=None):
        home_folder = root or os.path.expanduser("~")
        return os.path.join(home_folder, Constants.DEFAULT_FOLDER_NAME)

    def guess_dates(self):
        to = datetime.date.today()
        start = to - datetime.timedelta(days=15)
        return start, to

    def update_start_button_state(self):
        self.start_button.setEnabled(
            all([self.json_fpath, self.destination_folder,
                 self.from_date, self.to_date]))

    def json_file_selected(self):
        # self.file_name_field.setText("Aucun fichier")
        self.start_button.setEnabled(False)
        fpath = QFileDialog.getOpenFileName(
            self, "Choisir le fichier d'export JSON",
            self.json_fpath or self.guess_destination(),
            "Fichiers JSON (*.json)")
        if fpath:
            self.json_fpath = fpath

    def directory_selected(self):
        path = QFileDialog.getExistingDirectory(
            self, "Sélectionner le dossier", self.destination_folder)
        if path:
            self.destination_folder = path

    def from_date_changed(self, new_date):
        self.from_date = new_date.toPyDate()

    def to_date_changed(self, new_date):
        self.to_date = new_date.toPyDate()

    def export_requested(self):
        print("export_requested")
        self.parentWidget().exporter.check_aggregate_presence()
        self.gridBox.addWidget(self.progression_groupbox, 4, 0)
        # self.gridBox.addWidget(self.cancel_btn, 4, 2)

    def display_noaggregate_confirmation(self):
        if dialogueViewWidget(parent=None).exec_() == QDialog.Accepted:
            self.start_export()

    def start_export(self):
        print("Lancement ...")
        self.parentWidget().exporter.parse(
            destination_folder=self.destination_folder,
            fname=self.json_fpath,
            from_date=self.from_date,
            to_date=self.to_date)

    def update_progress_label(self, index):
        progression_label = "Export en cours...    {index}/{total}" \
                            .format(index=index,
                                    total=self.nb_instances)
        self.progression_groupbox.setTitle(progression_label)
        print(self.progression_label)

    @pyqtSlot(bool, int, str)
    def parsing_ended(self, succeeded, nb_instances, error_message):
        if succeeded:
            self.nb_instances = nb_instances

    @pyqtSlot(str, int)
    def exporting_instance(self, ident, index):
        print("exporting_instance")
        self.update_progress_label(index)

    @pyqtSlot(bool, int, int)
    def instance_completed(self, succeeded, index, total):
        pc = index * 100 // total
        self.progressbar.setValue(pc)
        print(pc, "%")
