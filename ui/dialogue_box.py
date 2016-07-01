#!usr/bin/env python
# -*- coding: utf8 -*-
# maintainer: Fad
from __future__ import (
    unicode_literals, absolute_import, division, print_function)

import os
# from sqlite3 import IntegrityError
from PyQt4.QtGui import (QHBoxLayout, QVBoxLayout, QGridLayout, QGroupBox,
                         QPixmap, QDialog, QLabel, QTextEdit)

from static import Constants
from ui.common import (CWidget, Button, FormLabel)


class dialogueViewWidget(QDialog, CWidget):

    def __init__(self, parent=0, *args, **kwargs):
        QDialog.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        hbox = QHBoxLayout()
        self.confirmationBox()
        self.setLayout(hbox)

    def confirmationBox(self):

        self.setWindowTitle(u"ODK Aggregate indisponible")
        self.logoField = QLabel()
        pixmap = QPixmap(os.path.join(Constants.img_media, 'alert.png'))
        self.logoField.setPixmap(pixmap)

        self.intro = FormLabel(
            u"""
                <p>Impossible de joindre le serveur ODK Aggregate.</p>
                <h6>Merci de vérifier la configuration du réseau et le lancement de la machine virtuelle. </h6>
                <hr/>
                <h6> Sans le serveur ODK Aggregate; vous pourrez exporter les fiches d'enquête préremplies, </h6>
                mais vous ne pourrez pas exporter les médias.
                <h4> Voulez-vous continuer sans ODK Aggregate ?</h4>""")

        cancel_but = Button(u"Annuler")
        cancel_but.clicked.connect(self.close)
        accept_but = Button(u"Continuez sans les médias")
        accept_but.clicked.connect(self.accept)

        # grid layout
        gridBox = QGridLayout()
        gridBox.addWidget(self.logoField, 0, 0)
        gridBox.addWidget(
            FormLabel("<h3><font color='orange'>ODK Aggregate indisponible </font></h3>"), 0, 1)
        gridBox.addWidget(self.intro, 1, 1, 2, 2)
        gridBox.addWidget(cancel_but, 4, 2)
        gridBox.addWidget(accept_but, 4, 1)
        gridBox.setRowStretch(3, 2)

        vbox = QVBoxLayout()
        vbox.addLayout(gridBox)
        self.setLayout(vbox)
