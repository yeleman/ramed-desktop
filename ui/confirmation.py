#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (
    unicode_literals, absolute_import, division, print_function)

import os

from PyQt4.QtGui import (QVBoxLayout, QGridLayout, QLabel, QPixmap)
from PyQt4.QtCore import Qt

from ui.common import (CWidget, Button, DeletedBtn, FormLabel)

from static import Constants

try:
    unicode
except:
    unicode = str


class ConfirmationViewWidget(CWidget):

    def __init__(self, parent=0, *args, **kwargs):
        super(ConfirmationViewWidget, self).__init__(
            parent=parent)
        self.parentWidget().setWindowTitle("Export des fichier de collect RAMED")

        sumission_totals = 342
        succes_nb_record = 342
        period = "le 16 juin 2016 et le 30 juin 2016"
        nb_media = 856
        self.logoField = QLabel()
        pixmap = QPixmap(os.path.join(Constants.IMG_MEDIA, 'success.png'))
        self.logoField.setPixmap(pixmap)

        self.msgLabel = FormLabel("""
        <p>L'ensemble des données de la collecte ({sumission_totals}
           enregistrements entre {period}) ont été exportées avec succes.
           <h6>Nombre enregistrements : {succes_nb_record} </h6>
		   <h6> Nombre de médias : {nb_media} </h6></p>""".format(
            sumission_totals=sumission_totals, period=period,
            succes_nb_record=succes_nb_record, nb_media=nb_media))

        self.newExportBtn = Button("Nouvel export")
        self.newExportBtn.clicked.connect(self.new_export)

        self.cancelBtn = Button("Quiter")
        self.cancelBtn.clicked.connect(self.parentWidget().close)

        gridBox = QGridLayout()
        gridBox.addWidget(self.logoField, 0, 0)
        gridBox.addWidget(self.logoField, 0, 3)
        gridBox.addWidget(
            FormLabel("<h2><font color='green'> Félicitations !</font></h2>"), 0, 1)
        gridBox.addWidget(self.msgLabel, 1, 1, 2, 2)
        gridBox.addWidget(self.newExportBtn, 3, 1)
        gridBox.addWidget(self.cancelBtn, 3, 2)
        gridBox.setRowStretch(2, 1)
        gridBox.setRowStretch(4, 1)

        vBox = QVBoxLayout()
        vBox.addLayout(gridBox)
        self.setLayout(vBox)

    def new_export(self):
        print("III")
