#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import os

ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))


class Constants(object):

    def __init__(self):
        CConstants.__init__(self)

    # ---------- Application ----------- #

    NAME_MAIN = "main.py"
    APP_NAME = "Example app"
    APP_VERSION = u"1.0"
    APP_DATE = u"02/2013"
    img_media = os.path.join(ROOT_DIR, "media", "img")
    APP_LOGO = os.path.join(img_media, "logo.png")
    APP_LOGO_ICO = os.path.join(img_media, "logo.ico")
    # ---------- Autor ----------------- #
    AUTOR = u"Yeleman s.a.r.l"
    EMAIL_AUT = u""
    TEL_AUT = u""
    ADRESS_AUT = u""
    ORG_AUT = u"Copyright © xxxx"

    # ---------- Organization ---------- #
    NAME_ORGA = "Example s.a.r.l"
