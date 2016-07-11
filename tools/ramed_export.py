#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import json

import ijson
import requests
import copy
import os
import datetime

from PyQt4.QtCore import QObject, pyqtSignal
from path import Path

from app_logging import logger
from static import Constants
from tools.ramed_instance import RamedInstance
from tools.ramed_form_pdf_export import gen_pdf_export


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

    # number of successful exports, number of errors
    export_ended = pyqtSignal(int, int, name='exportEnded')

    export_canceled = pyqtSignal(name='exportCanceled')

    # error message
    error_raised = pyqtSignal(str, name='ErrorRaised')

    def __init__(self, main_window):
        super(RamedExporter, self).__init__()
        self.main_window = main_window
        self.nb_instances = 0
        self.cancel_requested = None
        self.is_running = False

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
        self.export_ended.connect(main_window.export_ended)
        self.export_ended.connect(main_window.view_widget.export_ended)

        self.export_canceled.connect(main_window.view_widget.export_canceled)
        self.export_canceled.connect(main_window.export_canceled)

        self.error_raised.connect(main_window.export_error_raised)

    def path_for(self, path):
        return os.path.join(self.destination_folder, path)

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
            error_message = "Impossible de lire le fichier."
        except ValueError:
            error_message = "Le fichier n'est pas un fichier JSON valide."
        except Exception as e:
            error_message = repr(e)
        else:
            success = True
        finally:
            self.nb_instances = nb_instances
            self.parsing_ended.emit(success, nb_instances, error_message)

    def start(self):
        self.export_started.emit()
        self.is_running = True
        exported_instances = []
        counter = 1

        with open(self.fname, encoding="UTF-8", mode='r') as f:
            for instance_dict in filter(self.submission_filter,
                                        ijson.items(f, 'item')):
                if self.cancel_requested:
                    break
                instance = RamedInstance(instance_dict)
                self.exporting_instance.emit(instance.ident, counter)
                self.export_single_instance(instance)
                if self.cancel_requested:
                    break
                self.export_instance_medias(instance)
                exported_instances.append(instance_dict)
                if self.cancel_requested:
                    break
                self.instance_completed.emit(True, counter, self.nb_instances)
                counter += 1
        if self.cancel_requested:
            self.cleanup_canceled_export(exported_instances)
            self.export_canceled.emit()
            return
        # copy JSON file to destination
        fpath = os.path.join(self.destination_folder, "odk_data.json")
        with open(fpath, encoding='UTF-8', mode='w') as f:
            json.dump(exported_instances, f)
        self.is_running = False
        self.export_ended.emit(counter - 1, 0)

    def export_single_instance(self, instance):
        fname, fpath = gen_pdf_export(self.destination_folder, instance)

    def export_instance_medias(self, instance):
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
                assert self.cancel_requested is not True
                req = requests.get(url, timeout=Constants.ODK_TIMEOUT)
                assert req.status_code == 200
                with open(fpath, 'wb') as f:
                    f.write(req.content)
            except (AssertionError, IOError, Exception) as ex:
                logger.exception(ex)
                success = False
            else:
                success = True
            medias[key].update({'success': success})
        return medias

    def cancel(self):
        self.cancel_requested = True

    def cleanup_canceled_export(self, instances=[]):
        logger.debug("cleanup_canceled_export")

        # remove every instance's individual folder
        for instance_dict in instances:
            instance = RamedInstance(instance_dict)
            Path(self.path_for(instance.folder_name)).rmtree_p()

        # remove other static folders and files
        Path(self.path_for("PDF")).rmtree_p()
        Path(self.path_for('odk_data.json')).remove_p()

        # try to remove destination folder (if empty)
        Path(self.destination_folder).rmdir_p()

        self.cancel_requested = None
        self.is_running = False
