#!/sur/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from peewee import (CharField, DateTimeField,
                    SqliteDatabase, Model, __version__)
print("Peewee version : " + __version__)

DB_FILE = "database.db"

dbh = SqliteDatabase(DB_FILE)
dbh.connect()


class BaseModel(Model):

    class Meta:
        database = dbh

    @classmethod
    def all(cls):
        return list(cls.select())

    def get_or_none(self, obj):
        try:
            return obj.get()
        except Exception as e:
            print("get_or_none : ", e)
            return None


class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    email = CharField()
    join_date = DateTimeField()

    class Meta:
        order_by = ('username',)
