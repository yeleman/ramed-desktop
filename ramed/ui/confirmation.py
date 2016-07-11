#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from PyQt4.QtGui import (QVBoxLayout, QGridLayout, QLabel, QPixmap,
                         QSizePolicy)

from ramed.static import Constants
from ramed.ui.common import (BaseWidget, PushButton, Label)


class ConfirmationWidget(BaseWidget):

    def __init__(self, parent,
                 nb_instances_successful,
                 nb_instances_failed,
                 nb_medias_successful,
                 nb_medias_failed,
                 from_date, to_date, *args, **kwargs):
        super(ConfirmationWidget, self).__init__(parent=parent)

        title_label = Label(
            "<h2><font color='green'>Félicitations !</font></h2>")
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap(Constants.intpath(
            [Constants.IMAGES_FOLDER, 'success.png'])))

        nb_submissions_total = nb_instances_successful + nb_instances_failed
        message_label = Label(
            "<p>L'ensemble des données de la collecte "
            "({nb_submissions_total} enregistrements entre {from_date} "
            "et {to_date})<br /> ont été exportées avec succes.</p>"
            "<h6>Nombre enregistrements : {nb_instances_successful} </h6>"
            "<h6> Nombre de médias : {nb_medias_successful} </h6>"
            .format(nb_submissions_total=nb_submissions_total,
                    from_date=from_date, to_date=to_date,
                    nb_instances_successful=nb_instances_successful,
                    nb_medias_successful=nb_medias_successful))

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            message_label.sizePolicy().hasHeightForWidth())
        message_label.setSizePolicy(size_policy)

        reset_button = PushButton("Nouvel export")
        reset_button.clicked.connect(self.parentWidget().reset)

        quit_button = PushButton("Quitter")
        quit_button.clicked.connect(self.parentWidget().close)

        gridBox = QGridLayout()
        gridBox.addWidget(icon_label, 0, 1)
        gridBox.addWidget(title_label, 0, 2)
        gridBox.addWidget(message_label, 1, 1, 3, 2)
        gridBox.addWidget(reset_button, 4, 1)
        gridBox.addWidget(quit_button, 4, 2)
        gridBox.setRowStretch(1, 3)

        vBox = QVBoxLayout()
        vBox.addLayout(gridBox)
        self.setLayout(vBox)
