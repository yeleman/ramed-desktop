#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import re

logger = logging.getLogger(__name__)


class RamedInstance(dict):

    def __init__(self, *args, **kwargs):
        super(RamedInstance, self).__init__(*args, **kwargs)
        self.parse()

    @classmethod
    def clean_prenoms(cls, prenoms):
        return prenoms.strip().title() if prenoms else None

    @classmethod
    def clean_nom(cls, nom):
        return nom.strip().upper() if nom else None

    @classmethod
    def clean_name(cls, nom, prenoms):
        if prenoms and nom:
            return "{nom} {prenoms}".format(prenoms=prenoms, nom=nom)
        elif prenoms:
            return prenoms
        return nom

    def parse(self):
        self._medias = self.get_medias()

    @property
    def prenom(self):
        return self.clean_prenoms(self.get('prenoms'))

    @property
    def nom(self):
        return self.clean_nom(self.get('nom'))

    @property
    def name(self):
        if self.prenom and self.nom:
            return "{nom} {prenom}".format(prenom=self.prenom, nom=self.nom)
        elif self.prenom:
            return self.prenom
        return self.nom

    @property
    def uuids(self):
        return self.get("instanceID")[5:13]

    @property
    def folder_name(self):
        return "{nom}-{uuid}".format(
            nom=re.sub(r'\[\]/\;,\>\<\&\*\:\%\=\+\@\!\#\^\(\)\|\?',
                       '', self.name),
            uuid=self.uuids)

    @property
    def region(self):
        return self.get('region').strip().upper() or None

    @property
    def cercle(self):
        return self.get('cercle').strip().upper() or None

    @property
    def commune(self):
        return self.get('commune').strip().upper() or None

    @property
    def location(self):
        return "/".join([part for part
                         in (self.commune, self.cercle, self.region)
                        if part is not None])

    def get_medias(self):
        medias = {}
        keys = ("filename", "type", "url")
        is_media = lambda d: sum([1 for k in keys
                                  if k in d.keys()]) == len(keys)

        def walk_dict(adict, parent_key=[]):
            for key, value in adict.items():
                new_parent_key = parent_key + [key]
                if isinstance(value, dict):
                    if is_media(value):
                        medias.update({"/".join(new_parent_key): value})
                    else:
                        walk_dict(value, parent_key=new_parent_key)
                elif isinstance(value, list):
                    walk_list(value, parent_key=new_parent_key)

        def walk_list(alist, parent_key=[]):
            for value in alist:
                if isinstance(value, dict):
                    walk_dict(value, parent_key=parent_key)
                elif isinstance(value, list):
                    walk_list(value, parent_key=parent_key)

        walk_dict(self)
        return medias

    @property
    def medias(self):
        return self._medias
