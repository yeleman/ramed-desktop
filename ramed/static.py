#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import os
import sys
import platform
import json
import logging

IS_FROZEN = hasattr(sys, 'frozen')
WORKING_DIR = os.path.dirname(os.path.abspath(sys.executable
                              if IS_FROZEN
                              else os.path.dirname(__file__)))
print(WORKING_DIR)

try:
    with open(os.path.join(WORKING_DIR, 'ramed.config'),
              encoding='UTF-8', mode='r') as f:
        CONFIG = json.load(f)
except Exception as ex:
    if not isinstance(ex, IOError):
        print(repr(ex))
    CONFIG = {}


def get_log_level(value):
    level = value.upper()
    if level in ('DEBUG', 'INFO', 'WARNING', 'CRITICAL'):
        return getattr(logging, level)
    return logging.DEBUG


class Constants(object):

    SYSTEM = platform.system()
    IS_FROZEN = IS_FROZEN

    WORKING_DIR = WORKING_DIR
    MAIN_SCRIPT = "ramed.py"

    APP_NAME = "RAMED Desktop"
    APP_TITLE = "Export des fichiers de collecte RAMED"

    APP_VERSION = "1.0"
    APP_DATE = "juillet 2016"

    IMAGES_FOLDER = os.path.join("media", "img")
    PNG_ICON = os.path.join(IMAGES_FOLDER, "logo.png")
    ICO_ICON = os.path.join(IMAGES_FOLDER, "logo.ico")

    DATE_DISPLAY_FORMAT = "dd/MM/yyyy"

    AUTHOR = "yɛlɛman s.à.r.l"
    AUTHOR_EMAIL = "info@yeleman.com"
    AUTHOR_PHONE = "(223) 76 33 30 05"
    AUTHOR_COPY = "© RAMED/UNICEF/YELEMAN"

    VERBOSE = CONFIG.get('VERBOSE', False)
    LOG_LEVEL = get_log_level(CONFIG.get('LOG_LEVEL', 'DEBUG'))

    AGGREGATE_URL = CONFIG.get('AGGREGATE_URL', "http://192.168.0.10")
    DEFAULT_FOLDER_NAME = CONFIG.get('DEFAULT_FOLDER_NAME', "Données Collecte")
    ODK_TIMEOUT = CONFIG.get('ODK_TIMEOUT', 1)

    @classmethod
    def intpath(cls, path):
        # assume path is either a str path or a list of components
        if not isinstance(path, str):
            path = os.path.join(*path)
        return os.path.join(cls.WORKING_DIR, path)
