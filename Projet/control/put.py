"""
Fonctions Set du back-end.
@author: Maxime Brisinger, Margot Cosson, Raphaël Lasry, Maxime Poli
"""
import sys
import exception as ex
sys.path.append("..")
from data import bdd
import datetime
import copy

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
NB_LIMITE_JOURS = 25
FORMAT_DATE1 = "%Y-%m-%d %H:%M:%S"
FORMAT_DATE2 = "%d/%m/%Y %H:%M:%S"
FORMAT_DATE3 = "%d-%m-%Y %H:%M:%S"

def convert_format_date(date: str, format1: str, format2: str):
    """
    Convertit une date en format angular en format classique.
    """
    date_format1 = datetime.datetime.strptime(date, format1)
    date_format2 = datetime.datetime.strftime(date_format1, format2)
    return date_format2

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
        # Bien qu'inutile dans notre modèle, on vérifie le début et la fin de l'horaire.
        if (
                chantier["start"] == infos_chantier["start"]
                and chantier["end"] == infos_chantier["end"]
        ):
            raise ex.impossible_assignation(id_ouvrier = id_ouvrier, id_chantier = id_chantier)
    return True


def set_new_chantier(dict_new_chantier: dict):
    """
    Permet d'inserer un nouveau chantier. Le format d'entrée
    doit être un dictionnaire de la forme
    {"name_chantier": text, "start": text, "end": text, "adress": text}.
    """
    # Gestion d'erreur à faire dessus : chantier pas déjà existant
    # Exception levée si l'argument n'est pas conforme
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
    # Gestion d'erreur à faire dessus : ouvrier non existant
    # Exception levée si l'argument n'est pas conforme
    ex.conformite_dict(dict_new_ouvrier, {"name_ouvrier": str})
    bdd.insert_ouvrier(dict_new_ouvrier)


def set_new_attribution(dict_new_attribution: dict):
    """
    Permet d'inserer un couple d'id_ouvrier/id_chantier.
    Format d'entrée : dict_new_attribution = {"id_ouvrier": int, "id_chantier": int}
    """
    # Gestion d'erreur à faire :
    # vérification que les id_ouvrier et id_chantier existent
    # Exception levée si l'argument n'est pas conforme
    ex.conformite_dict(dict_new_attribution, {"id_ouvrier": int, "id_chantier": int})
    if verif_dispo_horaire_ouvrier(
            dict_new_attribution["id_ouvrier"], dict_new_attribution["id_chantier"]
    ):
        bdd.insert_attribution(dict_new_attribution)
    # verif_dispo_horaire_ouvrier raise une exception s'il n'est pas disponible
    
def decoup_new_chantier(dict_new_chantier: dict):
    """
    Permet à partir d'un dictionnaire d'informations d'un chantier
    {"name_chantier": text, "start": text, "end": text, "adress": text},
    de découper ce chantier en demi-journées et de
    renvoyer une liste de dictionnaire
    [{"name_chantier": text, "start": text, "end": text, "adress": text},]
    de ce chantier par demi-journées.
    """
    # Dates ou durées utiles
    transition_matin_aprem = HEURES_DEBUT["debut_aprem"] - HEURES_DEBUT["debut_matin"]
    transition_aprem_matin = datetime.timedelta(days=1) - transition_matin_aprem
    duree_matin = HEURES_FIN["fin_matin"] - HEURES_DEBUT["debut_matin"]
    duree_aprem = HEURES_FIN["fin_aprem"] - HEURES_DEBUT["debut_aprem"]
    date_debut = datetime.datetime.strptime(dict_new_chantier["start"], FORMAT_DATE1)
    date_fin = datetime.datetime.strptime(dict_new_chantier["end"], FORMAT_DATE1)
    # Liste de dictionnaires renvoyée à la fin
    list_dict_new_chantiers = (
        []
    )  # correspond à la liste des dictionnaires du chantier découpé en demi-journées
    # Vérification de la conformité des entrées
    if date_debut >= date_fin:
        raise ex.invalid_dates(msg = "La date de fin ne peut être antérieure à la date de fin.")
    if (
            date_debut.hour != HEURES_DEBUT["debut_matin"].hour
            and date_debut.hour != HEURES_DEBUT["debut_aprem"].hour
    ):
        raise ex.invalid_dates(date = date_debut.strftime(FORMAT_DATE1))
    if (
            date_fin.hour != HEURES_FIN["fin_matin"].hour
            and date_fin.hour != HEURES_FIN["fin_aprem"].hour
    ):
        raise ex.invalid_dates(date = date_fin.strftime(FORMAT_DATE1))
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
    raise ex.overlimit_date(limite_jours = NB_LIMITE_JOURS)


def declare_new_chantier(dict_new_chantier: dict):
    """
    Prend en argument un dictionnaire d'un chantier
    tel que {"name_chantier": text, "start": text, "end": text, "adress": text}.
    Le chantier peut être étendu sur plusieurs journées, il est redécoupé
    en demi-journées et enregistré dans la base de données.
    """
    list_new_chantiers = decoup_new_chantier(dict_new_chantier)
    for chantier in list_new_chantiers:
        set_new_chantier(chantier)