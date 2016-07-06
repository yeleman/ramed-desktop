#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import os
import shutil

# from reportlab.platypus import BaseDocTemplate, Paragraph, SimpleDocTemplate
# from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfFileWriter, PdfFileReader
from path import Path

from static import Constants
from tools import create_shortcut

TEMPLATE_PATH = os.path.join(Constants.WORKING_DIR,
                             "templates", "ramed-template.pdf")

logger = logging.getLogger(__name__)


def gen_pdf_export(export_folder, instance):

    output_folder = os.path.join(export_folder, instance.folder_name)
    Path(output_folder).makedirs_p()
    fname = "{name}.pdf".format(name=instance.name)
    fpath = os.path.join(output_folder, fname)

    # shutil.copyfile(TEMPLATE_PATH, fpath)

    input_fp = open(TEMPLATE_PATH, "rb")
    template = PdfFileReader(input_fp)
    output = PdfFileWriter()

    # nb_pages = template.getNumPages()

    # writting data
    c = canvas.Canvas(fpath, pagesize=A4)
    c.setLineWidth(.3)
    c.setFont('Helvetica', 12)
    c.drawString(30, 750, instance.get('nom-enquete'))

    # saving to buffer
    c.save()

    # merging template and data
    output_ro = open(fpath, u"rb")
    template_page = template.getPage(0)
    document = PdfFileReader(output_ro)
    template_page.mergePage(document.getPage(0))
    output.addPage(template_page)

    # writing output to file
    output_fp = open(fpath, u"wb")
    output.write(output_fp)
    output_fp.close()

    # create shortcut
    shortcut_folder = os.path.join(export_folder, "PDF")
    Path(shortcut_folder).makedirs_p()
    shortcut_fname = "{}.lnk".format(fname.rsplit('.', 1)[0])
    create_shortcut(fpath, os.path.join(shortcut_folder, shortcut_fname))

    return fname, fpath
