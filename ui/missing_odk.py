#!/urs/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from PyQt4.QtGui import (QVBoxLayout, QGridLayout, QPixmap,
                         QDialog, QLabel, QIcon)

from static import Constants
from ui.common import (BaseWidget, PushButton, Label)


class MissingODKConfirmationWidget(QDialog, BaseWidget):

    def __init__(self, parent=None, *args, **kwargs):
        super(QDialog, self).__init__(parent)
        super(BaseWidget, self).__init__(parent)

        self.setWindowTitle("ODK Aggregate indisponible")
        self.setWindowIcon(QIcon(Constants.intpath(Constants.PNG_ICON)))

        icon_label = QLabel()
        icon_label.setPixmap(
            QPixmap(Constants.intpath([Constants.IMAGES_FOLDER, 'alert.png'])))
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

        continue_button = PushButton("Continuez sans les médias")
        continue_button.clicked.connect(self.accept)

        cancel_button = PushButton("Annuler l'export")
        cancel_button.clicked.connect(self.close)
        cancel_button.setFocus()

        # grid layout
        gridBox = QGridLayout()
        gridBox.addWidget(icon_label, 0, 0)
        gridBox.addWidget(title, 0, 1)
        gridBox.addWidget(message, 1, 1, 2, 2)
        gridBox.addWidget(cancel_button, 4, 2)
        gridBox.addWidget(continue_button, 4, 1)
        gridBox.setRowStretch(3, 2)

        vbox = QVBoxLayout()
        vbox.addLayout(gridBox)
        self.setLayout(vbox)
