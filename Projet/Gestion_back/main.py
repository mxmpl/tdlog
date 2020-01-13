"""
Projet TDLOG réalisé par Maxime BRISINGER, Margot COSSON, Raphael LASRY et
Maxime POLI, 2019-2020

Le but de ce script python est de traiter la partie back du site.

Fichier conforme à la norme PEP8.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import Api

from back import (resume_chantiers, set_new_ouvrier, return_table_ouvrier_avec_chantiers, get_info_from_id_ouvrier,
                  get_planning_individuel, modify_data, del_data, return_cluster_chantiers, set_new_attribution, convert_format_date,
                  return_table, delete_chantier, get_info_from_id_chantier, declare_new_chantier)

APP = Flask(__name__)
CORS(APP)  # Creation du site


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
def nouvelles_attributions():
    """
  Nouvelle attribution d'un ouvrier sur un chantier
  """
    liste_attributions = request.get_json()
    for attribution in liste_attributions:
        set_new_attribution(attribution)
    return jsonify(liste_attributions)


@APP.route("/attribution/<id_ouvrier>/<id_chantier>", methods=["DELETE"])
def delete_attribution(id_ouvrier: str, id_chantier: str):
    """
  Supprime attribution d'un ouvrier sur un chantier
  """
    del_data("attribution", id_ouv=int(id_ouvrier), id_chant=int(id_chantier))
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

if __name__ == "__main__":
    APP.run(debug=True)