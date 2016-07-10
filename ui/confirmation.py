#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (
    unicode_literals, absolute_import, division, print_function)

import os

from PyQt4.QtGui import (QVBoxLayout, QGridLayout, QLabel, QPixmap,
                         QSizePolicy)
from PyQt4.QtCore import Qt

from ui.common import (CWidget, Button, DeletedBtn, FormLabel)

from static import Constants

try:
    unicode
except:
    unicode = str


class ConfirmationViewWidget(CWidget):

    def __init__(self, parent,
                 nb_instances_successful,
                 nb_instances_failed,
                 nb_medias_successful,
                 nb_medias_failed,
                 from_date, to_date, *args, **kwargs):
        super(ConfirmationViewWidget, self).__init__(parent=parent)

        self.logoField = QLabel()
        pixmap = QPixmap(os.path.join(Constants.IMG_MEDIA, 'success.png'))
        self.logoField.setPixmap(pixmap)

        nb_submissions_total = nb_instances_successful + nb_instances_failed
        self.msgLabel = FormLabel(
            "<p>L'ensemble des données de la collecte "
            "({nb_submissions_total} enregistrements entre {from_date} "
            "et {to_date})<br /> ont été exportées avec succes.</p>"
            "<h6>Nombre enregistrements : {nb_instances_successful} </h6>"
            "<h6> Nombre de médias : {nb_medias_successful} </h6>"
            .format(nb_submissions_total=nb_submissions_total,
                    from_date=from_date, to_date=to_date,
                    nb_instances_successful=nb_instances_successful,
                    nb_medias_successful=nb_medias_successful))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.msgLabel.sizePolicy().hasHeightForWidth())
        self.msgLabel.setSizePolicy(sizePolicy)

        self.newExportBtn = Button("Nouvel export")
        # self.newExportBtn.setEnabled(False)
        self.newExportBtn.clicked.connect(self.parentWidget().reset)

        self.cancelBtn = Button("Quiter")
        self.cancelBtn.clicked.connect(self.parentWidget().close)

        gridBox = QGridLayout()
        gridBox.addWidget(self.logoField, 0, 1)
        gridBox.addWidget(FormLabel(
            "<h2><font color='green'> Félicitations !</font></h2>"), 0, 2)
        gridBox.addWidget(self.msgLabel, 1, 1, 3, 2)
        gridBox.addWidget(self.newExportBtn, 4, 1)
        gridBox.addWidget(self.cancelBtn, 4, 2)
        gridBox.setRowStretch(1, 3)

        vBox = QVBoxLayout()
        vBox.addLayout(gridBox)
        self.setLayout(vBox)
