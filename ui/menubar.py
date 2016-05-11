#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from PyQt4.QtGui import (QMenuBar, QMessageBox, QIcon, QAction, QPixmap)
from PyQt4.QtCore import SIGNAL

from static import Constants
from ui.common import CWidget
from ui.example import ExampleViewWidget


class MenuBar(QMenuBar, CWidget):

    def __init__(self, parent=None, *args, **kwargs):
        QMenuBar.__init__(self, parent=parent, *args, **kwargs)

        self.setWindowIcon(QIcon(QPixmap("{}".format(Constants.APP_LOGO))))
        self.parent = parent

        menu = [{"name": u"Tableau de bord", "icon": 'example',
                 "shortcut": "Ctrl+T", "goto": ExampleViewWidget}, ]

        # Menu aller à
        goto_ = self.addMenu(u"&Aller a")

        for m in menu:
            el_menu = QAction(QIcon("{}{}.png".format(
                Constants.img_media, m.get('icon'))), m.get('name'), self)
            el_menu.setShortcut(m.get("shortcut"))
            self.connect(el_menu, SIGNAL("triggered()"),
                         lambda m=m: self.goto(m.get('goto')))
            goto_.addSeparator()
            goto_.addAction(el_menu)

        # Menu Aide
        help_ = self.addMenu(u"Aide")
        help_.addAction(QIcon("{}info.png".format(Constants.img_media)),
                        u"À propos", self.goto_about)

    def goto(self, goto):
        self.change_main_context(goto)

    # About
    def goto_about(self):
        QMessageBox.about(self, u"À propos",
                          u""" <h2>Version : {version_app} </h2>
                            <hr>
                            <h4><i>Logiciel {app_name}.</i></h4>
                            <ul><li></li> <li><b>Developpé par</b> : {autor} </li>
                                <li><b>Adresse : </b>{adress} </li>
                                <li><b>Tel: </b> {phone} </li>
                                <li><b>E-mail : </b> {email} <br/></li>
                                <li>{org_out}</li>
                            </ul>
                            """.format(email=Constants.EMAIL_AUT,
                                       app_name=Constants.APP_NAME,
                                       adress=Constants.ADRESS_AUT,
                                       autor=Constants.AUTOR,
                                       version_app=Constants.APP_VERSION,
                                       phone=Constants.TEL_AUT,
                                       org_out=Constants.ORG_AUT,
                                       )
                          )
