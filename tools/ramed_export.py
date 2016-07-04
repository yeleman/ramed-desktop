#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

import ijson
import requests

from PyQt4.QtCore import QObject, pyqtSignal

from static import Constants

logger = logging.getLogger(__name__)


class RamedExporter(QObject):

    check_started = pyqtSignal(name='checkStarted')
    check_ended = pyqtSignal(bool, str, name='checkEnded')

    parsing_started = pyqtSignal(name='parsingStarted')

    # succeeded, nbInstances, errorMesage
    parsing_ended = pyqtSignal(bool, int, str, name='parsingEnded')

    export_started = pyqtSignal(name='exportStarted')

    # error message
    export_failed = pyqtSignal(str, name='exportFailed')

    # number of successful exports, number of errors
    export_ended = pyqtSignal(int, int, name='exportEnded')

    # error message
    raised_error = pyqtSignal(str, name='ErrorRaised')

    def __init__(self, main_window):
        super(RamedExporter, self).__init__()
        self.main_window = main_window

        # connect signals
        self.check_started.connect(main_window.check_started)
        self.check_ended.connect(main_window.check_ended)

        self.parsing_started.connect(main_window.parsing_started)
        self.parsing_ended.connect(main_window.parsing_ended)

        self.export_started.connect(main_window.export_started)
        self.export_failed.connect(main_window.export_failed)
        self.export_ended.connect(main_window.export_ended)
        self.raised_error.connect(main_window.export_raised_error)

    def check_aggregate_presence(self):
        self.check_started.emit()
        try:
            req = requests.get(Constants.AGGREGATE_URL, timeout=2)
            assert req.status_code in (200, 201, 301)
            success = True
            error_message = ""
        except Exception as e:
            error_message = repr(e)
            success = False
        finally:
            self.check_ended.emit(success, error_message)

    def parse(self, fname):
        self.parsing_started.emit()
        self.fname = fname
        success = False
        nb_instances = 0
        error_message = ""
        try:
            items = ijson.items(open(self.fname, 'r'), 'item')
            nb_instances = len([i for i in items
                                if isinstance(i, dict)
                                and i.get('instanceID')])
        except IOError:
            error_message = "Unable to read file"
        except ValueError:
            error_message = "File is not a valid JSON"
        except Exception as e:
            print(e)
            error_message = repr(e)
        else:
            success = True
        finally:
            self.parsing_ended.emit(success, nb_instances, error_message)

    def start(self):
        self.export_started.emit()
        self.export_ended.emit(1, 3)