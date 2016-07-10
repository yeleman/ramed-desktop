#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import json

import ijson
import requests
import copy
import os
import datetime

from PyQt4.QtCore import QObject, pyqtSignal
from path import Path

from tools.ramed_form_pdf_export import gen_pdf_export
from tools.ramed_instance import RamedInstance
from static import Constants

logger = logging.getLogger(__name__)


class RamedExporter(QObject):

    check_started = pyqtSignal(name='checkStarted')
    check_ended = pyqtSignal(bool, str, name='checkEnded')

    parsing_started = pyqtSignal(name='parsingStarted')

    # succeeded, nbInstances, errorMesage
    parsing_ended = pyqtSignal(bool, int, str, name='parsingEnded')

    export_started = pyqtSignal(name='exportStarted')

    # succeeded, index, total
    instance_completed = pyqtSignal(bool, int, int, name='instanceCompleted')

    # ident-string, index
    exporting_instance = pyqtSignal(str, int, name='exportingInstance')

    # error message
    export_failed = pyqtSignal(str, name='exportFailed')

    # number of successful exports, number of errors
    export_ended = pyqtSignal(int, int, name='exportEnded')

    # error message
    raised_error = pyqtSignal(str, name='ErrorRaised')

    def __init__(self, main_window):
        super(RamedExporter, self).__init__()
        self.main_window = main_window
        self.nb_instances = 0

        # connect signals
        self.check_started.connect(main_window.check_started)
        self.check_ended.connect(main_window.check_ended)

        self.parsing_started.connect(main_window.parsing_started)
        self.parsing_ended.connect(main_window.parsing_ended)
        self.parsing_ended.connect(main_window.view_widget.parsing_ended)

        self.export_started.connect(main_window.export_started)
        self.exporting_instance.connect(main_window.exporting_instance)
        self.exporting_instance.connect(
            main_window.view_widget.exporting_instance)
        self.instance_completed.connect(
            main_window.view_widget.instance_completed)
        self.export_failed.connect(main_window.export_failed)
        self.export_ended.connect(main_window.export_ended)
        self.raised_error.connect(main_window.export_raised_error)

    def check_aggregate_presence(self):
        self.check_started.emit()
        try:
            req = requests.get(Constants.AGGREGATE_URL,
                               timeout=Constants.ODK_TIMEOUT)
            assert req.status_code in (200, 201, 301)
            success = True
            error_message = ""
        except Exception as e:
            error_message = repr(e)
            success = False
        finally:
            self.check_ended.emit(success, error_message)

    def parse(self, destination_folder, fname, from_date, to_date):
        self.parsing_started.emit()

        self.fname = fname
        self.destination_folder = destination_folder
        Path(destination_folder).makedirs_p()
        self.from_date = from_date
        self.to_date = to_date

        nb_instances = 0
        success = False
        error_message = ""
        try:
            with open(self.fname, encoding="UTF-8", mode='r') as f:
                items = ijson.items(f, 'item')
                nb_instances = len(list(filter(self.submission_filter, items)))
        except IOError:
            error_message = "Unable to read file"
        except ValueError:
            error_message = "File is not a valid JSON"
        except Exception as e:
            error_message = repr(e)
        else:
            success = True
        finally:
            self.nb_instances = nb_instances
            self.parsing_ended.emit(success, nb_instances, error_message)

    def submission_filter(self, instance_dict):
        try:
            instance_id = instance_dict.get('instanceID') or None
            instance_date = datetime.date(
                *[int(x) for x in instance_dict.get('date').split('-')[:3]])
            assert instance_id
            assert instance_date >= self.from_date
            assert instance_date <= self.to_date
            return True
        except:
            return False

    def start(self):
        self.export_started.emit()
        instances = []
        counter = 1
        with open(self.fname, encoding="UTF-8", mode='r') as f:
            for instance_dict in filter(self.submission_filter,
                                        ijson.items(f, 'item')):
                instance = RamedInstance(instance_dict)
                self.exporting_instance.emit(instance.ident, counter)
                self.export_single_instance(instance)
                self.export_medias(instance)
                instances.append(instance_dict)
                self.instance_completed.emit(True, counter, self.nb_instances)
                counter += 1

        # copy JSON file to destination
        fpath = os.path.join(self.destination_folder, "odk_data.json")
        with open(fpath, encoding='UTF-8', mode='w') as f:
            json.dump(instances, f)
        self.export_ended.emit(counter - 1, 0)

    def export_single_instance(self, instance):
        fname, fpath = gen_pdf_export(self.destination_folder, instance)

    def export_medias(self, instance):
        medias = copy.deepcopy(instance.medias)

        output_dir = os.path.join(self.destination_folder,
                                  instance.folder_name)
        Path(output_dir).makedirs_p()

        for key, media in medias.items():
            url = media.get('url').replace('http://aggregate.defaultdomain',
                                           Constants.AGGREGATE_URL)
            fname = "{key}_{fname}".format(key=key,
                                           fname=media.get('filename'))
            fpath = os.path.join(output_dir, fname)
            try:
                req = requests.get(url, timeout=Constants.ODK_TIMEOUT)
                assert req.status_code == 200
                with open(fpath, 'wb') as f:
                    f.write(req.content)
            except (AssertionError, IOError, Exception) as e:
                print(repr(e))
                success = False
            else:
                success = True
            medias[key].update({'success': success})
        return medias
