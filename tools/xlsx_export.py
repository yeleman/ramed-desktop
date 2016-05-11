#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from openpyxl import Workbook
from openpyxl.compat import range


def xlsx_example():
    # print("make_xlsx_example")
    wb = Workbook()
    dest_filename = 'xlsx_example.xlsx'
    ws1 = wb.active
    ws1.title = "Sheet example"
    for row in range(1, 20):
        ws1.append(range(600))
    wb.save(filename=dest_filename)
