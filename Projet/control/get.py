"""
Fonctions Get du back-end.
@author: Maxime Brisinger, Margot Cosson, Raphaël Lasry, Maxime Poli
"""
from put import verif_dispo_horaire_ouvrier
import sys
sys.path.append("..")
from data import bdd

def get_info_from_id_ouvrier(id_ouv: int):
    """
    Récupère toutes les informations d'un ouvrier à partir de son identifiant.
    Renvoie un dictionnaire de la forme
    {"id_ouvrier": int, "name_ouvrier": text}.
    """
    # On vérifie si l'identifiant existe
    bdd.id_in_table("ouvriers", id_ouv=id_ouv, id_chant=None)
    return bdd.get_info_from_id_ouvrier(id_ouv)


def get_info_from_id_chantier(id_chan: int):
    """
    Récupère toutes les informations d'un chantier à partir de son identifiant.
    Renvoie un dictionnaire de la forme
    {"id_chantier": int, "name_chantier": text, "start": text, "end": text, "adress": text}.
    """
    # On vérifie si l'identifiant existe
    bdd.id_in_table("chantiers", id_ouv=None, id_chant=id_chan)
    return bdd.get_info_from_id_chantier(id_chan)

def return_table(name_table: str):
    """
    Renvoie toute la table name_table sous forme d'une liste de dictionnaire :
    [{"id": int, "name": text, etc.},].
    """
    if name_table == "chantiers":
        return bdd.return_table_chantier()
    elif name_table == "ouvriers":
        return bdd.return_table_ouvrier()
    elif name_table == "attribution":
        return bdd.return_table_attribution()
    raise Exception("Nom de table erroné.")

def return_table_ouvrier_avec_chantiers():
    """
    Renvoie la liste de tous les ouvriers affecté à leur chantiers de la forme
    [{"id_ouvrier": int, "name_ouvrier": text, "chantiers": list},]
    """
    ouvriers = return_table("ouvriers")
    for ouvrier in ouvriers:
        ouvrier["chantiers"] = get_planning_individuel(ouvrier["id_ouvrier"])
    return ouvriers

def return_cluster_chantiers(id_ouv=None):
    """
    Renvoie un dictionnaire
    {"Boulogne":[{"id_chantier": 1, "name_chantier":"Boulogne", "start":...},],
    "Marseille":[{"id_chantier": 2, "name_chantier":"Marseille", "start":...},],}.
    On précise id_ouv si on veut seulement les clusters de chantiers
    pour les chantiers possibles pour l'ouvrier id_ouv. Sinon on a tous les clusters
    de tous les chantiers.
    """
    if id_ouv is None:
        chantiers = return_table("chantiers")
    else:
        chantiers = return_chantiers_possibles(id_ouv)
    dictionnaire = {}
    for chantier in chantiers:
        if chantier["name_chantier"] in dictionnaire.keys():
            dictionnaire[chantier["name_chantier"]].append(chantier)
        else:
            dictionnaire[chantier["name_chantier"]] = [chantier]
    return dictionnaire

def resume_chantiers():
    """
    Revoie une liste de dictionnaires de la forme :
    {"name_chantier": text, "adress": text, "start":"2016-10-10 08:00:00",
    "end":"2016-10-15 18:00:00", "ouvriers":[{ "name_ouvrier", "id_ouvrier": int,
    "id_chantier": [int]},]}
    """
    chantiers_possibles = return_cluster_chantiers(id_ouv=None)
    ouvriers = return_table("ouvriers")
    chantiers = return_table("chantiers")
    attribution = return_table("attribution")
    dictionnaire = {}
    for name_chantier in chantiers_possibles:
        dictionnaire_chantier = {}
        dictionnaire_chantier["adress"] = chantiers_possibles[name_chantier][0][
            "adress"
        ]
        dictionnaire_chantier["start"] = sorted(
            chantiers_possibles[name_chantier], key=lambda element: element["start"]
        )[0]["start"]
        dictionnaire_chantier["end"] = sorted(
            chantiers_possibles[name_chantier], key=lambda element: element["end"]
        )[-1]["end"]
        dictionnaire_chantier["ouvriers"] = []
        for chantier in chantiers:
            if chantier["name_chantier"] == name_chantier:
                for ouvrier in ouvriers:
                    dico = {
                        "id_ouvrier": ouvrier["id_ouvrier"],
                        "id_chantier": chantier["id_chantier"],
                    }
                    if dico in attribution:
                        dico["name_ouvrier"] = ouvrier["name_ouvrier"]
                        test = True
                        for i in range(len(dictionnaire_chantier["ouvriers"])):
                            dic = dictionnaire_chantier["ouvriers"][i]
                            if (
                                    "name_ouvrier" in dic.keys()
                                    and dico["name_ouvrier"] == dic["name_ouvrier"]
                            ):
                                dictionnaire_chantier["ouvriers"][i][
                                    "id_chantier"
                                ].append(chantier["id_chantier"])
                                test = False
                                break
                        if test:
                            dico["id_chantier"] = [chantier["id_chantier"]]
                            dictionnaire_chantier["ouvriers"].append(dico)
        dictionnaire[name_chantier] = dictionnaire_chantier
    return dictionnaire

def return_chantiers_possibles(id_ouv: int):
    """
    Renvoie la liste des chantiers où un ouvrier donné peut être attribué en
    fonction des chantiers auxquels il a déjà été attribué
    (gestion des conflits horaires).
    """
    bdd.id_in_table("ouvriers", id_ouv=id_ouv, id_chant=None)
    chantiers = return_table("chantiers")
    chantier_attribues = get_planning_individuel(id_ouv)
    liste_chantiers_possibles = []
    for chantier in chantiers:
        try:
            verif_dispo_horaire_ouvrier(
                id_ouv,
                chantier["id_chantier"],
                planning=chantier_attribues,
                infos_chantier=chantier,
            )
            liste_chantiers_possibles.append(chantier)
        except:
            pass
    return liste_chantiers_possibles

def get_planning():
    """
    Renvoie toutes les attributions et les informations sur les ouvriers et
    les chantiers correspondantes sous la forme d'une liste de dictionnaires
    telle que [{"id_ouvrier": int, "name_ouvrier": text, "id_chantier": int,
    "name_chantier": text, "start": text, "end": text, "adress": text},]
    """
    return bdd.get_all_attribution()

def get_planning_individuel(id_ouv: int):
    """
    Renvoie toutes les attributions d'un ouvrier (à partir de son index) sous
    la forme d'une liste de dictionnaires telle que
    [{"id_chantier": int, "name_chantier": text, "start": text, "end": text,
    "adress": text},]
    """
    return bdd.get_planning_individuel(id_ouv)