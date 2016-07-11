#!/urs/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from PyQt4.QtGui import (QVBoxLayout, QGridLayout, QPixmap, QDialog, QLabel)

from static import Constants
from ui.common import (BaseWidget, PushButton, Label)


class MissingODKConfirmationWidget(QDialog, BaseWidget):

    def __init__(self, parent=0, *args, **kwargs):
        super(QDialog, self).__init__(parent)
        super(BaseWidget, self).__init__(parent)

        self.setWindowTitle("ODK Aggregate indisponible")

        logoField = QLabel()
        logoField.setPixmap(
            QPixmap(Constants.intpath([Constants.IMG_MEDIA, 'alert.png'])))
        title = Label(
            "<h3><font color='orange'>ODK Aggregate indisponible</font></h3>")
        message = Label(
            "<p>Impossible de joindre le serveur ODK Aggregate.</p>"
            "<h6>Merci de vérifier la configuration du réseau et le lancement "
            "de la machine virtuelle. </h6>"
            "<hr/>"
            "<h6> Sans le serveur ODK Aggregate; vous pourrez exporter les "
            "fiches d'enquête préremplies, </h6>"
            "mais vous ne pourrez pas exporter les médias."
            "<h4> Voulez-vous continuer sans ODK Aggregate ?</h4>")

        accept_but = PushButton("Continuez sans les médias")
        accept_but.clicked.connect(self.accept)

        cancel_but = PushButton("Annuler l'export")
        cancel_but.clicked.connect(self.close)
        cancel_but.setFocus()

        # grid layout
        gridBox = QGridLayout()
        gridBox.addWidget(logoField, 0, 0)
        gridBox.addWidget(title, 0, 1)
        gridBox.addWidget(message, 1, 1, 2, 2)
        gridBox.addWidget(cancel_but, 4, 2)
        gridBox.addWidget(accept_but, 4, 1)
        gridBox.setRowStretch(3, 2)

        vbox = QVBoxLayout()
        vbox.addLayout(gridBox)
        self.setLayout(vbox)
