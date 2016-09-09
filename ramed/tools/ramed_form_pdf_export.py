#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import os
import datetime

from path import Path
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (Paragraph, Table, TableStyle, Image,
                                SimpleDocTemplate)

from ramed.app_logging import logger
from ramed.tools.ramed_instance import RamedInstance
from ramed.tools import create_shortcut

BLANK = "néant"


def gen_pdf_export(export_folder, instance):

    story = []
    styles = getSampleStyleSheet()
    b_style = styles["BodyText"]
    h3 = styles["Heading3"]
    h4 = styles["Heading4"]

    output_folder = os.path.join(export_folder, instance.folder_name)

    Path(output_folder).makedirs_p()

    fname = "{name}.pdf".format(name=instance.name)
    fpath = os.path.join(output_folder, fname)
    # writting data

    def format_location(parts):
        return " / ".join([part for part in parts if part])

    def concat(parts, sep=" / "):
        return sep.join([part for part in parts if part])

    def get_lieu_naissance(data, key, village=False):
        region = data.get('{}region'.format(key))
        cercle = data.get('{}cercle'.format(key))
        commune = data.get('{}commune'.format(key))
        lieu_naissance = format_location([commune, cercle, region])
        return region, cercle, commune, lieu_naissance

    def get_lieu(data, key):
        region, cercle, commune, _ = get_lieu_naissance(data, key)
        village = data.get('{}village'.format(key))
        lieu = format_location([village, commune, cercle, region])
        return region, cercle, commune, village, lieu

    def get_other(data, key):
        profession = data.get(key)
        profession_other = data.get('{}_other'.format(key))
        return profession_other if profession == 'other' else profession

    def get_int(data, key, default=0):
        try:
            return int(data.get(key, default))
        except:
            return default

    def get_date(data, key):
        try:
            return datetime.date(*[int(x) for x in data.get(key).split('-')])
        except:
            return None

    def get_dob(data, key, female=False):
        type_naissance = data.get('{}type-naissance'.format(key), 'ne-vers')
        annee_naissance = get_int(data, '{}annee-naissance'.format(key), None)
        ddn = get_date(data, '{}ddn'.format(key))
        human = "Né{f} ".format(f="e" if female else "")
        if type_naissance == 'ddn':
            human += "le {}".format(ddn.strftime("%d-%m-%Y"))
        else:
            human += "vers {}".format(annee_naissance)

        return type_naissance, annee_naissance, ddn, human

    def get_bool(data, key, default='non'):
        text = data.get(key, default)
        return text == 'oui', text

    def get_nom(data, p='', s=''):
        nom = RamedInstance.clean_lastname(
            data.get('{p}nom{s}'.format(p=p, s=s)))
        prenoms = RamedInstance.clean_firstnames(data.get('{p}prenoms{s}'
                                                          .format(p=p, s=s)))
        name = RamedInstance.clean_name(nom, prenoms)
        return nom, prenoms, name

    def draw_String_title(text):
        return """<para align=center spaceb=5><b><font size=11>{}</font>
                  </b></para>""".format(text)

    def draw_String(label, text):
        # if len(text) == 0:
        #     text = BLANK
        return """<para align=left spaceb=5><font size=9><u>{label}</u></font>
                   : {text}</para>""".format(label=label, text=text)

    # lieu (pas sur papier)
    lieu_region, lieu_cercle, lieu_commune, lieu_village, lieu = get_lieu(
        instance, 'lieu_')
    numero_enquete = instance.get('numero') or ""
    objet_enquete = instance.get('objet') or instance.get('objet_other')
    identifiant_enqueteur = instance.get('enqueteur') or BLANK
    demandeur = instance.get('demandeur') or BLANK

    # enquêté
    nom, prenoms, name = get_nom(instance)
    sexe = instance.get('sexe') or 'masculin'
    is_female = sexe == 'feminin'
    type_naissance, annee_naissance, ddn, naissance = get_dob(
        instance, '', is_female)
    region_naissance, cercle_naissance, commune_naissance, lieu_naissance = get_lieu_naissance(
        instance, '')

    # enquêté / instance
    nom_pere, prenoms_pere, name_pere = get_nom(instance, s='-pere')
    nom_mere, prenoms_mere, name_mere = get_nom(instance, s='-mere')

    situation_matrioniale = instance.get('situation-matrimoniale', BLANK)
    profession = get_other(instance, 'profession')
    adresse = instance.get('adresse') or ""
    nina_text = instance.get('nina_text') or ""
    telephones = [str(tel.get('numero'))
                  for tel in instance.get('telephones', [])]

    nb_epouses = get_int(instance, 'nb_epouses', 0)

    # enfants
    logger.info("enfants")
    nb_enfants = get_int(instance, 'nb_enfants')
    nb_enfants_handicapes = get_int(instance, 'nb_enfants_handicapes')
    nb_enfants_acharge = get_int(instance, 'nb_enfants_acharge')

    # ressources
    salaire = get_int(instance, 'salaire')
    pension = get_int(instance, 'pension')
    allocations = get_int(instance, 'allocations')
    has_autres_revenus = get_bool(instance, 'autres-sources-revenu')
    autres_revenus = [
        (revenu.get('source-revenu'), get_int(revenu, 'montant-revenu'))
        for revenu in instance.get('autres_revenus', [])]
    total_autres_revenus = get_int(instance, 'total_autres_revenus')

    # charges
    loyer = get_int(instance, 'loyer')
    impot = get_int(instance, 'impot')
    dettes = get_int(instance, 'dettes')
    aliments = get_int(instance, 'aliments')
    sante = get_int(instance, 'sante')
    autres_charges = get_int(instance, 'autres_charges')

    # habitat
    type_habitat = get_other(instance, 'type')
    materiau_habitat = get_other(instance, 'materiau')

    # antecedents
    antecedents_personnels = instance.get('personnels')
    antecedents_personnels_details = instance.get(
        'personnels-details') or BLANK
    antecedents_familiaux = instance.get('familiaux')
    antecedents_familiaux_details = instance.get('familiaux-details') or BLANK
    antecedents_sociaux = instance.get('sociaux')
    antecedents_sociaux_details = instance.get('sociaux-details') or BLANK
    situation_actuelle = instance.get('situation-actuelle') or BLANK
    diagnostic = instance.get('diagnostic') or BLANK
    diagnostic_details = instance.get('diagnostic-details') or BLANK
    recommande_assistance = get_bool(instance, 'observation') or BLANK

    doc = SimpleDocTemplate(fpath, pagesize=A4, fontsize=3)
    logger.info("Headers")
    headers = [["MINISTÈRE DE LA SOLIDARITÉ", "",  "    REPUBLIQUE DU MALI"],
               ["DE L’ACTION HUMANITAIRE", "", "UN PEUPLE UN BUT UNE FOI"],
               ["ET DE LA RECONSTRUCTION DU NORD", "", ""],
               ["AGENCE NATIONALE D’ASSISTANCE MEDICALE (ANAM)", "", ""]]
    # headers_t = Table(headers, colWidths=(160))
    headers_t = Table(headers, colWidths=150, rowHeights=11)
    story.append(headers_t)
    headers_t.setStyle(TableStyle([('SPAN', (1, 30), (1, 13)),
                                   ('ALIGN', (0, 0), (-1, -1), 'LEFT'), ]))
    story.append(Paragraph(draw_String_title("CONFIDENTIEL"), styles["Title"]))

    numero_enquete_t = Table([["FICHE D’ENQUETE SOCIALE N°.............../{year}"
                               .format(year=datetime.datetime.now().year), ]],)
    numero_enquete_t.setStyle(TableStyle(
        [('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))
    story.append(numero_enquete_t)
    story.append(Paragraph(draw_String("Identifiant enquêteur", numero_enquete),
                           b_style))
    story.append(Paragraph(draw_String("Objet de l’enquête", objet_enquete),
                           b_style))
    story.append(Paragraph(draw_String("Enquête demandée par", demandeur),
                           b_style))
    story.append(Paragraph("Enquêté", h3))
    logger.info("Enquêté")
    story.append(Paragraph(draw_String("Concernant", concat(
        [name, sexe, situation_matrioniale])), b_style))
    story.append(Paragraph(draw_String(
        naissance, "à {}".format(lieu_naissance)), b_style))
    logger.info("Parent")
    story.append(Paragraph(draw_String("Père", name_pere), b_style))
    story.append(Paragraph(draw_String("Mère", name_mere), b_style))
    story.append(Paragraph(draw_String("Profession", profession), b_style))
    story.append(Paragraph(draw_String("Adresse", adresse), b_style))
    logger.info("NINA CARD")
    story.append(Paragraph(draw_String("N° NINA", nina_text), b_style))
    story.append(Paragraph(draw_String(
        "Téléphones", concat(telephones)), b_style))
    story.append(Paragraph("COMPOSITION DE LA FAMILLE", h3))
    story.append(Paragraph("Situation des Epouses", h4))
    epouses = instance.get('epouses', [])
    logger.info("Epouses")
    if epouses == []:
        story.append(Paragraph(BLANK, b_style))
    for nb, epouse in enumerate(epouses):
        nom_epouse, prenoms_epouse, name_epouse = get_nom(epouse, p='e_')
        nom_pere_epouse, prenoms_pere_epouse, name_pere_epouse = get_nom(
            epouse, p='e_p_')
        nom_mere_epouse, prenoms_mere_epouse, name_mere_epouse = get_nom(
            epouse, p='e_m_')

        region_epouse, cercle_epouse, commune_epouse, lieu_naissance_epouse = get_lieu_naissance(
            epouse, 'e_')
        type_naissance_epouse, annee_naissance_epouse, \
            ddn_epouse, naissance_epouse = get_dob(epouse, 'e_', True)
        profession_epouse = get_other(epouse, 'e_profession')
        nb_enfants_epouse = get_int(epouse, 'e_nb_enfants', 0)

        story.append(Paragraph(draw_String(
            "EPOUSE", "{}".format(nb + 1)), b_style))
        epouses = concat([name_epouse, str(nb_enfants_epouse) +
                          " enfant{p}".format(p="s" if nb_enfants_epouse > 1 else "")])
        story.append(Paragraph(epouses, b_style))
        dob = "{naissance} à {lieu_naissance}".format(
            naissance=naissance_epouse, lieu_naissance=lieu_naissance_epouse)
        story.append(Paragraph(dob, b_style))
        story.append(Paragraph(draw_String("Père", name_pere_epouse), b_style))
        story.append(Paragraph(draw_String("Mère", name_mere_epouse), b_style))
        story.append(Paragraph(draw_String(
            "Profession", profession_epouse), b_style))
    story.append(Paragraph("Situation des Enfants", h4))
    # c.setFont('Courier', 10)
    # row -= interligne
    # enfants
    logger.debug("Child")
    enfants = instance.get('enfants', [])
    if enfants == []:
        story.append(Paragraph(BLANK, b_style))
    for nb, enfant in enumerate(enfants):
        nom_enfant, prenoms_enfant, name_enfant = get_nom(
            enfant, p='enfant_')
        nom_autre_parent, prenoms_autre_parent, name_autre_parent = get_nom(
            instance, s='-autre-parent')
        region_enfant, cercle_enfant, commune_enfant, \
            lieu_naissance_enfant = get_lieu_naissance(enfant, 'enfant_')
        type_naissance_enfant, annee_naissance_enfant, \
            ddn_enfant, naissance_enfant = get_dob(enfant, 'enfant_')
        # situation
        scolarise, scolarise_text = get_bool(enfant, 'scolarise')
        handicape, handicape_text = get_bool(enfant, 'handicape')
        acharge, acharge_text = get_bool(enfant, 'acharge')
        nb_enfant_handicap = get_int(enfant, 'nb_enfant_handicap')
        nb_enfant_acharge = get_int(enfant, 'nb_enfant_acharge')

        story.append(Paragraph("{nb}. {enfant}".format(
            nb=nb + 1, enfant=concat([name_enfant or BLANK, naissance_enfant,
                                      "à {lieu}".format(
                                          lieu=lieu_naissance_enfant),
                                      scolarise_text, handicape_text,
                                      name_autre_parent])), b_style))

    story.append(Paragraph("AUTRES PERSONNES à la charge de l’enquêté", h4))

    # # autres
    autres = instance.get('autres', [])

    if autres == []:
        story.append(Paragraph(BLANK, b_style))

    logger.debug("Other")
    for nb, autre in enumerate(autres):
        nom_autre, prenoms_autre, name_autre = get_nom(autre, p='autre_')

        region_autre, cercle_autre, commune_autre, \
            lieu_naissance_autre = get_lieu_naissance(autre, 'autre_')
        type_naissance_autre, annee_naissance_autre, \
            ddn_autre, naissance_autre = get_dob(autre, 'autre_')
        parente_autre = get_other(autre, 'autre_parente')
        profession_autre = get_other(autre, 'autre_profession')
        story.append(Paragraph("{nb}. {enfant}".format(nb=nb + 1, enfant=concat(
            [name_autre or BLANK, naissance_autre, "à {lieu}".format(lieu=lieu_naissance_autre), parente_autre, profession_autre])), b_style))

    # ressources
    logger.debug("Ressources")
    story.append(
        Paragraph("RESSOURCES ET CONDITIONS DE VIE DE L’ENQUETE (E)", h4))

    story.append(Paragraph(
        concat(["Salaire : {}/mois".format(salaire),
                "Pension : {}/mois".format(pension),
                "Allocations : {}/mois".format(allocations)], sep=". "), b_style))
    autres_revenus_f = ["[{}/{}]".format(source_revenu, montant_revenu)
                        for source_revenu, montant_revenu in autres_revenus]
    story.append(Paragraph(draw_String("Autre", concat(
        autres_revenus_f, sep=". ")), b_style))
    story.append(Paragraph(
        "LES CHARGES DE L’ENQUETE (Préciser le montant et la période)", h4))
    story.append(Paragraph(concat(["Loyer : {}".format(loyer), "Impot : {}".format(impot), "Dettes : {}".format(dettes), "Aliments : {}".format(aliments),
                                   "Santé : {}".format(sante), ], sep=". "), b_style))
    story.append(Paragraph(draw_String(
        "Autres Charges", autres_charges), b_style))
    story.append(Paragraph(draw_String("HABITAT", concat(
        [type_habitat, materiau_habitat])), b_style))
    story.append(Paragraph("EXPOSER DETAILLE DES FAITS", h4))
    # antecedents
    logger.debug("Antecedents")
    story.append(Paragraph(draw_String("Antécédents personnels",
                                       concat(antecedents_personnels)), b_style))
    story.append(Paragraph(draw_String("Détails Antécédents personnels",
                                       antecedents_personnels_details), b_style))
    story.append(Paragraph(draw_String("Antécédents familiaux",
                                       antecedents_familiaux), b_style))
    story.append(Paragraph(draw_String("Détails Antécédents familiaux",
                                       antecedents_familiaux_details), b_style))
    story.append(Paragraph(draw_String("Antécédents sociaux",
                                       antecedents_sociaux), b_style))
    story.append(Paragraph(draw_String("Détails Antécédents sociaux",
                                       antecedents_sociaux_details), b_style))
    story.append(Paragraph(draw_String("Situation actuelle",
                                       concat(situation_actuelle)), b_style))
    story.append(Paragraph(draw_String("Diagnostic", diagnostic), b_style))
    story.append(Paragraph(draw_String(
        "Diagnostic details", diagnostic_details), b_style))
    signature_dict = instance.get("signature")
    img = ""
    if signature_dict:
        dir_media = os.path.join(output_folder, "signature_{}".format(
            signature_dict.get("filename")))
        img = Image(dir_media, width=80, height=82)

    signature = [["SIGNATURE DE L’ENQUÊTEUR", "",
                  "VISA DU CHEF DU SERVICE SOCIAL"], [img, ""]]
    signature_t = Table(signature, colWidths=150, rowHeights=90)
    signature_t.setStyle(TableStyle([('FONTSIZE', (0, 0), (-1, -1), 8), ]))
    story.append(signature_t)

    # Fait le 01-06-2016 à cercle-de-mopti
    # VISA DU CHEF DU SERVICE SOCIAL
    # SIGNATURE DE L’ENQUÊTEUR
    doc.build(story)
    logger.info("Save")

    # create shortcut
    shortcut_folder = os.path.join(export_folder, "PDF")
    Path(shortcut_folder).makedirs_p()
    shortcut_fname = "{}.lnk".format(instance.folder_name)
    create_shortcut(fpath, os.path.join(shortcut_folder, shortcut_fname))

    return fname, fpath
