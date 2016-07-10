#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import os
import sys
import platform


class Constants(object):

    SYSTEM = platform.system()
    IS_FROZEN = hasattr(sys, 'frozen')
    WORKING_DIR = os.path.dirname(os.path.abspath(sys.executable
                                  if IS_FROZEN else __file__))
    NAME_MAIN = "ramed.py"
    APP_NAME = "RAMED Desktop"
    APP_TITLE = "Export des fichiers de collecte RAMED"
    APP_VERSION = u"1.0"
    APP_DATE = u"07/2016"
    IMG_MEDIA = os.path.join(WORKING_DIR, "media", "img")
    APP_LOGO = os.path.join(IMG_MEDIA, "logo.png")
    APP_LOGO_ICO = os.path.join(IMG_MEDIA, "logo.ico")

    AUTOR = u"yɛlɛman s.à.r.l"
    EMAIL_AUT = u"info@yeleman.com"
    TEL_AUT = u"(223) 76 33 30 05"
    ADRESS_AUT = u"Hipprodrome, rue 240 porte 1068\nBPE. 3713 - Bamako, Mali"
    ORG_AUT = u"© RAMED/UNICEF/YELEMAN"

    NAME_ORGA = "RAMED"
    AGGREGATE_URL = "http://192.168.0.10"
    DEFAULT_FOLDER_NAME = "Données Collecte"
    ODK_TIMEOUT = 1
