#############%%

"""
Projet TDLOG réalisé par Maxime BRISINGER, Margot COSSON, Raphael LASRY et
Maxime POLI, 2019-2020

Le but de ce script python est de traiter la partie back du site.

Fichier conforme à la norme PEP8.
"""
#############%% Module utiles

import datetime
import copy

#############%% Module sys

import sys

#############%% Module Flask

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import Api

#############%% Import des bibliothèques utiles

sys.path.append("..")
from Gestion_bdd import bdd
from Gestion_bdd import exception as ex

#############%% Creation du site

APP = Flask(__name__)
CORS(APP)  # Creation du site

#############%% Constantes

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
FORMAT_DATE = "%Y-%m-%d %H:%M:%S"
FORMAT_DATE_ANGULAR = "%d/%m/%Y %H:%M:%S"

#############%% Fonctions du back


def convert_format_date(date_angular: str):
    """
    Convertit une date en format angular en format classique.
    """
    date_angular = datetime.datetime.strptime(date_angular, FORMAT_DATE_ANGULAR)
    date_classique = datetime.datetime.strftime(date_angular, FORMAT_DATE)
    return date_classique


########%% SET & DEL


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
    else:
        raise ex.id_ouvrier_not_available_for_assignation


def del_data(name_table: str, id_ouv=None, id_chant=None):
    """
    Permet de supprimer un élément de la table à partir de son id.
    """
    if bdd.id_in_table(name_table, id_ouv=id_ouv, id_chant=id_chant):
        bdd.del_data(name_table, id_ouv=id_ouv, id_chant=id_chant)
        return
    raise ex.invalid_id


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
    date_debut = datetime.datetime.strptime(dict_new_chantier["start"], FORMAT_DATE)
    date_fin = datetime.datetime.strptime(dict_new_chantier["end"], FORMAT_DATE)
    # Liste de dictionnaires renvoyée à la fin
    list_dict_new_chantiers = (
        []
    )  # correspond à la liste des dictionnaires du chantier découpé en demi-journées
    # Vérification de la conformité des entrées
    if date_debut >= date_fin:
        raise ex.invalid_dates("Mauvaise date")
    if (
            date_debut.hour != HEURES_DEBUT["debut_matin"].hour
            and date_debut.hour != HEURES_DEBUT["debut_aprem"].hour
    ):
        raise ex.invalid_dates("Mauvaise date")
    if (
            date_fin.hour != HEURES_FIN["fin_matin"].hour
            and date_fin.hour != HEURES_FIN["fin_aprem"].hour
    ):
        raise ex.invalid_dates("Mauvaise date")
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
            dic_chantier["start"] = date_debut.strftime(FORMAT_DATE)
            if date_debut.hour == HEURES_DEBUT["debut_matin"].hour:
                dic_chantier["end"] = (date_debut + duree_matin).strftime(FORMAT_DATE)
                date_debut += transition_matin_aprem
            elif date_debut.hour == HEURES_DEBUT["debut_aprem"].hour:
                dic_chantier["end"] = (date_debut + duree_aprem).strftime(FORMAT_DATE)
                date_debut += transition_aprem_matin
            list_dict_new_chantiers.append(dic_chantier)
        break
    if date_debut == heure_fin_fin:
        return list_dict_new_chantiers
    raise ex.overlimit_date


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


def delete_chantier(name_chantier: str):
    """
    Permet de supprimer un chantier au sens du nom.
    """
    chantiers = return_table("chantiers")
    attributions = return_table("attribution")
    for chantier in chantiers:
        if chantier["name_chantier"] == name_chantier:
            id_chantier = chantier["id_chantier"]
            for attribution in attributions:
                if attribution["id_chantier"] == id_chantier:
                    del_data(
                        "attribution",
                        id_ouv=attribution["id_ouvrier"],
                        id_chant=attribution["id_chantier"],
                    )
            del_data("chantiers", id_ouv=None, id_chant=id_chantier)


########%% GET


def get_info_from_id_ouvrier(id_ouv: int):
    """
    Récupère toutes les informations d'un ouvrier à partir de son identifiant.
    Renvoie un dictionnaire de la forme
    {"id_ouvrier": int, "name_ouvrier": text}.
    """
    return bdd.get_info_from_id_ouvrier(id_ouv)


def get_info_from_id_chantier(id_chan: int):
    """
    Récupère toutes les informations d'un chantier à partir de son identifiant.
    Renvoie un dictionnaire de la forme
    {"id_chantier": int, "name_chantier": text, "start": text, "end": text, "adress": text}.
    """
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
    # faire gestion d'erreur si ni chantiers, ni ouvriers, ni attribution


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
    # liste_chantier = []
    dictionnaire = {}
    for name_chantier in chantiers_possibles:
        # dictionnaire_chantier["name_chantier"] = name_chantier
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
                            dict = dictionnaire_chantier["ouvriers"][i]
                            if (
                                    "name_ouvrier" in dict.keys()
                                    and dico["name_ouvrier"] == dict["name_ouvrier"]
                            ):
                                dictionnaire_chantier["ouvriers"][i][
                                    "id_chantier"
                                ].append(chantier["id_chantier"])
                                test = False
                                break
                        if test:
                            dico["id_chantier"] = [chantier["id_chantier"]]
                            dictionnaire_chantier["ouvriers"].append(dico)
        # liste_chantier.append(dictionnaire_chantier)
        dictionnaire[name_chantier] = dictionnaire_chantier
    # return liste_chantier
    return dictionnaire


def return_chantiers_possibles(id_ouv: int):
    """
    Renvoie la liste des chantiers où un ouvrier donné peut être attribué en
    fonction des chantiers auxquels il a déjà été attribué
    (gestion des conflits horaires).
    """
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


########%% MODIFY


def modify_data(name_table: str, champs: str, value: str, id_ouv=None, id_chant=None):
    """
    Permet de modifier une donnée dans une table.
    """
    # Gestion d'erreur à faire : vérifier que champs est bien un champs
    bdd.modify_data(name_table, champs, value, id_ouv, id_chant)


########%% CHECK


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
            raise ex.id_ouvrier_not_available_for_assignation
    return True


# if __name__ == "__main__":
#    APP.debug = False
#    APP.run()

# À la fin de l'utilisation, on supprime les tables

# bdd.suppression_table_chantiers()
# bdd.suppression_table_ouvriers()
# bdd.suppression_table_attribution()
# bdd.reset_table("chantiers")
# bdd.reset_table("ouvriers")
# bdd.reset_table("attribution")

#############%% Gestion du site


@APP.route("/", methods=["GET"])
def index():
    """
   Page d'accueil.
   """
    return "Welcome"


@APP.route("/planning/", methods=["GET"])
def planning():
    """
   Associe les chantiers aux ouvriers.
   """
    planning_chantiers = []
    chantiers = resume_chantiers()
    for cle in chantiers:
        planning_chantiers.append(
            {
                "title": cle,
                "start": chantiers[cle]["start"],
                "end": chantiers[cle]["end"],
            }
        )
    return jsonify(planning_chantiers)


@APP.route("/listeOuvriers/", methods=["GET", "POST", "DELETE", "PUT"])
def liste_ouvriers():  # NOM A CHANGER
    """
   Ajout d'un nouvel ouvrier.
   """
    data = request.get_json()
    if request.method == "POST":
        set_new_ouvrier({"name_ouvrier": data["name_ouvrier"]})
    ouvriers = return_table_ouvrier_avec_chantiers()
    return jsonify(ouvriers)


@APP.route("/listeOuvriers/<id_ouvrier>", methods=["GET", "POST", "DELETE", "PUT"])
def ouvrier_id(id_ouvrier: str):  # MODIFIER ET PRENDRE UN INT + NOM A CHANGER
    """
   Actions sur un ouvrier donné :
   informations, modification du nom ou suppression.
   """
    if request.method == "GET":
        ouvrier = get_info_from_id_ouvrier(int(id_ouvrier))
        ouvrier["chantiers"] = get_planning_individuel(ouvrier["id_ouvrier"])
        return jsonify(ouvrier)
    if request.method == "PUT":
        data = request.get_json()
        modify_data(
            "ouvriers", "name_ouvrier", data["name_ouvrier"], id_ouv=int(id_ouvrier)
        )
    elif request.method == "DELETE":
        del_data("ouvriers", id_ouv=int(id_ouvrier))
    ouvriers = return_table_ouvrier_avec_chantiers()
    return jsonify(ouvriers)


@APP.route(
    "/listeOuvriers/<id_ouvrier>/chantiersdispos",
    methods=["GET", "POST", "DELETE", "PUT"],
)
def chantiers_dispos_ouvrier_id(id_ouvrier: str):
    """
   Actions sur un ouvrier donné :
   affichage des noms des chantiers où il peut s'affilier
   """
    if request.method == "GET":
        chantiers_dispos = return_cluster_chantiers(id_ouvrier)
        return jsonify(chantiers_dispos)

    ouvriers = return_table_ouvrier_avec_chantiers()
    return jsonify(ouvriers)


@APP.route("/attribution/", methods=["POST"])
def nouvelle_attribution():
    """
  Nouvelle attribution d'un ouvrier sur un chantier
  """
    attribution = request.get_json()
    set_new_attribution(attribution)
    return jsonify(attribution)


@APP.route("/attribution/<id_ouvrier>/<id_chantier>", methods=["DELETE"])
def delete_attribution(id_ouvrier: str, id_chantier: str):
    """
  Supprime attribution d'un ouvrier sur un chantier
  """
    del_data("attribution", id_ouv=id_ouvrier, id_chant=id_chantier)
    return jsonify(0)


@APP.route("/listeChantiers/", methods=["GET", "POST"])
def liste_chantiers():
    """
   Renvoie la liste des chantiers
   """
    if request.method == "GET":
        chantiers = resume_chantiers()
        liste_chantiers = []
        for cle in chantiers:
            chantiers[cle]["name_chantier"] = str(cle)
            liste_chantiers.append(chantiers[cle])
        return jsonify(liste_chantiers)
    elif request.method == "POST":
        data = request.get_json()
        date_start = convert_format_date(
            data["start"]
        )  # data["start"][6:10] + "-" + data["start"][3:5] + "-" +
            # data["start"][0:2] + data["start"][10:]
        date_end = convert_format_date(
            data["end"]
        )  # data["end"][6:10] + "-" + data["end"][3:5] + "-"
            # + data["end"][0:2] + data["end"][10:]
        declare_new_chantier(
            {
                "name_chantier": data["name_chantier"],
                "start": date_start,
                "end": date_end,
                "adress": data["adress"],
            }
        )
    chantiers = resume_chantiers()
    return jsonify(chantiers)


@APP.route("/listeChantiers/<name_chantier>", methods=["GET", "POST", "DELETE", "PUT"])
def chantier_name(name_chantier: str):
    """
   Action sur un chantier donné :
   informations.
   """
    if request.method == "GET":
        chantier = resume_chantiers()[name_chantier]
        chantier["name_chantier"] = name_chantier
        for dico_ouvrier in chantier["ouvriers"]:
            dico_ouvrier["chantiers"] = []
            for id_chant in dico_ouvrier["id_chantier"]:
                dico_ouvrier["chantiers"].append(get_info_from_id_chantier(id_chant))
        return jsonify(chantier)
    elif request.method == "DELETE":
        delete_chantier(name_chantier)
    chantiers = return_table("chantiers")
    return jsonify(chantiers)


@APP.route("/addOuvriers/", methods=["POST"])
def add_ouvrier():
    """
    Attribue un ouvrier à un chantier.
    """
    data = request.get_json()
    new_evenement = {
        "start": "2020-01-07",
        "title": data["nom"] + " est a Paris",
        "end": "2020-01-07",
    }
    global ATTRIBUTION
    ATTRIBUTION.append(new_evenement)
    return jsonify(attribution)


if __name__ == "__main__":
    APP.run(debug=True)
