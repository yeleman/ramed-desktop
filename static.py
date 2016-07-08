#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import os


class Constants(object):

    # ---------- Application ----------- #

    WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
    NAME_MAIN = "main.py"
    APP_NAME = "RAMED Desktop"
    APP_VERSION = u"1.0"
    APP_DATE = u"06/2016"
    IMG_MEDIA = os.path.join(WORKING_DIR, "media", "img")
    APP_LOGO = os.path.join(IMG_MEDIA, "logo.png")
    APP_LOGO_ICO = os.path.join(IMG_MEDIA, "logo.ico")
    # ---------- Autor ----------------- #
    AUTOR = u"Yeleman s.a.r.l"
    EMAIL_AUT = u"reg@yeleman.com"
    TEL_AUT = u"+223 73 12 08 96"
    ADRESS_AUT = u"Hipprodrome, rue 240 porte 1068\nBPE. 3713 - Bamako, Mali"
    ORG_AUT = u"Copyright © RAMED"

    # ---------- Organization ---------- #
    NAME_ORGA = "RAMED"
    AGGREGATE_URL = "http://192.168.5.142"
