"""
Fonctions Set du back-end.
@author: Maxime Brisinger, Margot Cosson, Raphaël Lasry, Maxime Poli
"""
import datetime
import copy
import sys
import exception as ex
sys.path.append("..")
from data import bdd


HEURES_DEBUT = {
    "debut_matin": datetime.datetime(1900, 1, 1, 8, 0),
    "debut_aprem": datetime.datetime(1900, 1, 1, 14, 0),
}
# Le 1er janvier 1900 est une date fictive pour avoir un type datetime plutôt
# que time qui permet moins d'opérations
HEURES_FIN = {
    "fin_matin": datetime.datetime(1900, 1, 1, 12, 0),
    "fin_aprem": datetime.datetime(1900, 1, 1, 18, 0),
}
NB_LIMITE_JOURS = 25  # Nombre limite de jours pour un chantier
FORMAT_DATE1 = "%Y-%m-%d %H:%M:%S"
FORMAT_DATE2 = "%d/%m/%Y %H:%M:%S"


def convert_format_date(date: str, format1: str, format2: str):
    """
    Convertit une date en format1 vers le format2.
    """
    try:
        date_format1 = datetime.datetime.strptime(date, format1)
        date_format2 = datetime.datetime.strftime(date_format1, format2)
        return date_format2
    except:
        raise ex.InvalidDates(date=date)

def verif_dispo_horaire_ouvrier(
        id_ouvrier: int, id_chantier: int, planning=None, infos_chantier=None
):
    """
    Permet via l'index d'un chantier et d'un ouvrier de vérifier que
    l'ouvrier est disponible sur la plage horaire concernée pour ce
    chantier. Return True si l'ouvrier n'est pas encore occupé sur ce créneau.
    """
    if planning is None:
        planning = bdd.get_planning_individuel(id_ouvrier)
    if infos_chantier is None:
        infos_chantier = bdd.get_info_from_id_chantier(id_chantier)
    for chantier in planning:
        if (
                chantier["start"] == infos_chantier["start"]
                and chantier["end"] == infos_chantier["end"]
        ):
            raise ex.ImpossibleAssignation(
                id_ouvrier=id_ouvrier, id_chantier=id_chantier
            )
    return True


def set_new_chantier(dict_new_chantier: dict):
    """
    Permet d'inserer un nouveau chantier. Le format d'entrée
    doit être un dictionnaire de la forme
    {"name_chantier": text, "start": text, "end": text, "adress": text}.
    """
    ex.conformite_dict(
        dict_new_chantier,
        {"name_chantier": str, "start": str, "end": str, "adress": str},
    )
    bdd.insert_chantier(dict_new_chantier)


def set_new_ouvrier(dict_new_ouvrier: dict):
    """
    Permet d'inserer un nouveau ouvrier. Le format d'entrée
    doit être un dictionnaire de la forme
    {"name_ouvrier": text}.
    """
    ex.conformite_dict(dict_new_ouvrier, {"name_ouvrier": str})
    bdd.insert_ouvrier(dict_new_ouvrier)


def set_new_attribution(dict_new_attribution: dict):
    """
    Permet d'inserer un couple d'id_ouvrier/id_chantier.
    Format d'entrée : dict_new_attribution = {"id_ouvrier": int, "id_chantier": int}
    """
    ex.conformite_dict(dict_new_attribution, {"id_ouvrier": int, "id_chantier": int})
    # On vérifie si le chantier et l'ouvrier existent
    bdd.id_in_table(
        "ouvriers", id_ouv=dict_new_attribution["id_ouvrier"], id_chant=None
    )
    bdd.id_in_table(
        "chantiers", id_ouv=None, id_chant=dict_new_attribution["id_chantier"]
    )
    # Si l'ouvrier est disponible sur cette horaire
    if verif_dispo_horaire_ouvrier(
            dict_new_attribution["id_ouvrier"], dict_new_attribution["id_chantier"]
    ):
        bdd.insert_attribution(dict_new_attribution)


def decoup_new_chantier(dict_new_chantier: dict):
    """
    Permet à partir d'un dictionnaire d'informations d'un chantier
    {"name_chantier": text, "start": text, "end": text, "adress": text},
    de découper ce chantier en demi-journées et de
    renvoyer une liste de dictionnaire
    [{"name_chantier": text, "start": text, "end": text, "adress": text},]
    de ce chantier par demi-journées.
    """
    ex.conformite_dict(
        dict_new_chantier,
        {"name_chantier": str, "start": str, "end": str, "adress": str},
    )
    # Dates ou durées utiles
    transition_matin_aprem = HEURES_DEBUT["debut_aprem"] - HEURES_DEBUT["debut_matin"]
    transition_aprem_matin = datetime.timedelta(days=1) - transition_matin_aprem
    duree_matin = HEURES_FIN["fin_matin"] - HEURES_DEBUT["debut_matin"]
    duree_aprem = HEURES_FIN["fin_aprem"] - HEURES_DEBUT["debut_aprem"]
    date_debut = datetime.datetime.strptime(dict_new_chantier["start"], FORMAT_DATE1)
    date_fin = datetime.datetime.strptime(dict_new_chantier["end"], FORMAT_DATE1)
    # Liste de dictionnaires du chantier découpé en demi-journées renvoyée à la fin
    list_dict_new_chantiers = []
    # Vérification de la conformité des entrées
    if date_debut >= date_fin:
        raise ex.InvalidDates(
            msg="La date de fin ne peut être antérieure à la date de début."
        )
    if (
            date_debut.hour != HEURES_DEBUT["debut_matin"].hour
            and date_debut.hour != HEURES_DEBUT["debut_aprem"].hour
    ):
        raise ex.InvalidDates(date=date_debut.strftime(FORMAT_DATE1))
    if (
            date_fin.hour != HEURES_FIN["fin_matin"].hour
            and date_fin.hour != HEURES_FIN["fin_aprem"].hour
    ):
        raise ex.InvalidDates(date=date_fin.strftime(FORMAT_DATE1))
    # On enregistre l'heure de début de la dernière matinée
    if date_fin.hour == HEURES_FIN["fin_matin"].hour:
        heure_debut_fin = date_fin - duree_matin
        heure_fin_fin = heure_debut_fin + transition_matin_aprem
    elif date_fin.hour == HEURES_FIN["fin_aprem"].hour:
        heure_debut_fin = date_fin - duree_aprem
        heure_fin_fin = heure_debut_fin + transition_aprem_matin
    # On découpe
    for i in range(1, 2 * NB_LIMITE_JOURS + 1):
        dic_chantier = copy.deepcopy(dict_new_chantier)
        if date_debut <= heure_debut_fin:
            dic_chantier["start"] = date_debut.strftime(FORMAT_DATE1)
            if date_debut.hour == HEURES_DEBUT["debut_matin"].hour:
                dic_chantier["end"] = (date_debut + duree_matin).strftime(FORMAT_DATE1)
                date_debut += transition_matin_aprem
            elif date_debut.hour == HEURES_DEBUT["debut_aprem"].hour:
                dic_chantier["end"] = (date_debut + duree_aprem).strftime(FORMAT_DATE1)
                date_debut += transition_aprem_matin
            list_dict_new_chantiers.append(dic_chantier)
        else:
            break
    if date_debut == heure_fin_fin:
        return list_dict_new_chantiers
    raise ex.OverlimitDate(limite_jours=NB_LIMITE_JOURS)


def declare_new_chantier(dict_new_chantier: dict):
    """
    Prend en argument un dictionnaire d'un chantier
    tel que {"name_chantier": text, "start": text, "end": text, "adress": text}.
    Le chantier peut être étendu sur plusieurs journées, il est redécoupé
    en demi-journées et enregistré dans la base de données.
    """
    ex.conformite_dict(
        dict_new_chantier,
        {"name_chantier": str, "start": str, "end": str, "adress": str},
    )
    try:
        # On vérifie que le nom ne soit pas déjà utilisé par un autre chantier
        bdd.name_in_table("chantiers", dict_new_chantier["name_chantier"])
        list_new_chantiers = decoup_new_chantier(dict_new_chantier)
        for chantier in list_new_chantiers:
            set_new_chantier(chantier)
    except:
        raise ex.NameAlreadyExists(dict_new_chantier["name_chantier"])
