"""
Fichier principale du projet TDLOG 2019-2020.
@author: Maxime Brisinger, Margot Cosson, Raphaël Lasry, Maxime Poli
"""

# Import des bibliothèques et fonctions utiles

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

import sys
sys.path.insert(0, 'control')

from get import (get_info_from_id_ouvrier,
                 get_info_from_id_chantier,
                 return_table,
                 return_table_ouvrier_avec_chantiers,
                 return_cluster_chantiers,
                 resume_chantiers,
                 get_planning_individuel)

from put import (convert_format_date,
                 set_new_ouvrier,
                 set_new_attribution,
                 declare_new_chantier,
                 FORMAT_DATE1,
                 FORMAT_DATE2)

from change import(del_data,
                   delete_chantier,
                   modify_data)


APP = Flask(__name__)
CORS(APP)  # Creation du site

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
def liste_ouvriers():
    """
    Ajout d'un nouvel ouvrier.
    """
    data = request.get_json()
    if request.method == "POST":
        set_new_ouvrier({"name_ouvrier": data["name_ouvrier"]})
    ouvriers = return_table_ouvrier_avec_chantiers()
    return jsonify(ouvriers)

@APP.route("/listeOuvriers/<id_ouvrier>", methods=["GET", "POST", "DELETE", "PUT"])
def ouvrier_id(id_ouvrier: str):
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
    affichage des noms des chantiers où il peut être affecté.
    """
    if request.method == "GET":
        chantiers_dispos = return_cluster_chantiers(id_ouvrier)
        return jsonify(chantiers_dispos)
    ouvriers = return_table_ouvrier_avec_chantiers()
    return jsonify(ouvriers)

@APP.route("/attribution/", methods=["POST"])
def nouvelles_attributions():
    """
    Nouvelle attribution d'un ouvrier sur un chantier.
    """
    liste_attributions = request.get_json()
    for attribution in liste_attributions:
        set_new_attribution(attribution)
    return jsonify(liste_attributions)

@APP.route("/attribution/<id_ouvrier>/<id_chantier>", methods=["DELETE"])
def supprimer_attribution(id_ouvrier: str, id_chantier: str):
    """
    Supprime attribution d'un ouvrier sur un chantier.
    """
    del_data("attribution", id_ouv=int(id_ouvrier), id_chant=int(id_chantier))
    return jsonify(0)

@APP.route("/listeChantiers/", methods=["GET", "POST"])
def liste_chantiers():
    """
    Renvoie la liste des chantiers.
    """
    if request.method == "GET":
        chantiers = resume_chantiers()
        liste_des_chantiers = []
        for cle in chantiers:
            chantiers[cle]["name_chantier"] = str(cle)
            liste_des_chantiers.append(chantiers[cle])
        return jsonify(liste_des_chantiers)
    elif request.method == "POST":
        data = request.get_json()
        date_start = convert_format_date(data["start"], FORMAT_DATE2, FORMAT_DATE1)
        date_end = convert_format_date(data["end"], FORMAT_DATE2, FORMAT_DATE1)
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
def chantier_par_nom(name_chantier: str):
    """
    Action sur un chantier donné : informations.
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

@APP.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    """
    Permet d'exporter dans le fichier qui se trouve dans le dossier front.
    """
    return send_from_directory('front/', path)

@APP.route('/')
def root():
    """
    Permet d'exporter dans le fichier index.html qui se trouve dans le dossier front.
    """
    return send_from_directory('front/', 'index.html')

if __name__ == "__main__":
    APP.run(host='127.0.0.1', port=5000, debug=True)
