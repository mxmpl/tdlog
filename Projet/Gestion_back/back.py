#############%%

"""
Projet TDLOG réalisé par Maxime BRISINGER, Margot COSSON, Raphael LASRY et
Maxime POLI, 2019-2020

Le but de ce script python est de traiter la partie back du site.

Fichier conforme à la norme PEP8.
"""

#############%% Module sys

import sys

#############%% Module Flask

from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from flask_restful import Api

#############%% Import des bibliothèques utiles

sys.path.append("..")
from Gestion_bdd import bdd
from Gestion_bdd import exception as ex

#############%% Creation du site

APP = Flask(__name__)
CORS(APP)  # Creation du site

#############%% Fonctions du back

########%% SET & DEL

def set_new_chantier(dict_new_chantier: dict):
    """
    Permet d'inserer un nouveau chantier. Le format d'entrée
    doit être un dictionnaire de la forme
    {"name_chantier": text, "start": text, "end": text, "adress": text}.
    """
    # Gestion d'erreur à faire dessus : chantier pas déjà existant
    # Exception levée si l'argument n'est pas conforme
    ex.conformite_dict(dict_new_chantier, {"name_chantier": str, "start": str, "end": str, "adress": str})
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
    ex.conformite_dict(dict_new_attribution, {"id_ouvrier": int, "id_chantier": int })
    if verif_dispo_horaire_ouvrier(dict_new_attribution["id_ouvrier"],
                                   dict_new_attribution["id_chantier"]):
        bdd.insert_attribution(dict_new_attribution)
    else:
        raise ex.id_ouvrier_not_available_for_assignation

def del_data(name_table: str, id_ouv = None, id_chant = None):
    """
    Permet de supprimer un élément de la table à partir de son id.
    """
    if bdd.id_in_table(name_table, id_ouv = id_ouvrier, id_chant = id_chantier):
        bdd.del_data(name_table, id_ouv = id_ouvrier, id_chant = id_chantier)
        return
    raise ex.invalid_id

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
    
def return_cluster_chantiers(id_ouv: int):
    """
    Renvoie un dictionnaire
    {"Boulogne":[{"id_chantier": 1, "name_chantier":"Boulogne", "start":...},],
    "Marseille":[{"id_chantier": 2, "name_chantier":"Marseille", "start":...},],}
    """
    chantiers = return_chantiers_possibles(id_ouv)
    dictionnaire = {}
    for chantier in chantiers:
        if chantier["name_chantier"] in dictionnaire.keys(): 
            dictionnaire[chantier["name_chantier"]].append(chantier)
        else:
             dictionnaire[chantier["name_chantier"]] = [chantier]
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
        try :
            verif_dispo_horaire_ouvrier(id_ouv, chantier["id_chantier"], planning = chantier_attribues, infos_chantier = chantier)
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

def modify_data(name_table: str, champs: str, value: str, id_ouv = None, id_chant = None):
    """
    Permet de modifier une donnée dans une table.
    """
    # Gestion d'erreur à faire : vérifier que champs est bien un champs
    bdd.modify_data(name_table, champs, value, id_ouv, id_chant)

########%% CHECK

def verif_dispo_horaire_ouvrier(id_ouvrier: int, id_chantier: int, planning = None, infos_chantier = None):
    """
    Permet via l'index d'un chantier et d'un ouvrier de vérifier que
    l'ouvrier est disponible sur la plage horaire concernée pour ce
    chantier. Return True si l'ouvrier n'est pas encore occupé sur ce créneau.
    """
    if planning == None:
        planning = bdd.get_planning_individuel(id_ouvrier)
    if infos_chantier == None:
        infos_chantier = bdd.get_info_from_id_chantier(id_chantier)
    for chantier in planning:
        # Bien qu'inutile dans notre modèle, on vérifie le début et la fin de l'horaire.
        if(chantier["start"] == infos_chantier["start"]
           and chantier["end"] == infos_chantier["end"]):
            raise ex.id_ouvrier_not_available_for_assignation
    return True

#if __name__ == "__main__":
#    APP.debug = False
#    APP.run()

# À la fin de l'utilisation, on supprime les tables

#bdd.suppression_table_chantiers()
#bdd.suppression_table_ouvriers()
#bdd.suppression_table_attribution()
#bdd.reset_table("chantiers")
#bdd.reset_table("ouvriers")
#bdd.reset_table("attribution")

#############%% Gestion du site

@APP.route("/", methods=['GET'])
def index():
   """
   Page d'accueil.
   """
   return "Welcome"

@APP.route("/listeChantiers/", methods=['GET'])
def ListeChantiers(): # NOM A CHANGER
   """
   Associe les chantiers aux ouvriers.
   """
   attribution = get_planning()
   for dico in attribution:
       dico["title"] = dico["name_ouvrier"] + " a " + dico["name_chantier"]
   return jsonify(attribution)

@APP.route("/listeOuvriers/", methods=['GET', 'POST', 'DELETE', 'PUT'])
def ListeOuvriers(): # NOM A CHANGER
   """
   Ajout d'un nouvel ouvrier.
   """
   data = request.get_json()
   if request.method == "POST":
       set_new_ouvrier({"name_ouvrier":data["name_ouvrier"]})
   ouvriers = return_table_ouvrier_avec_chantiers()
   return jsonify(ouvriers)

@APP.route("/listeOuvriers/<id_ouvrier>", methods=['GET', 'POST', 'DELETE', 'PUT'])
def OuvrierId(id_ouvrier: str): # MODIFIER ET PRENDRE UN INT + NOM A CHANGER
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
       modify_data("ouvrier", "name", data["name_ouvrier"], id_ouv = int(id_ouvrier))
   elif request.method == "DELETE":
       del_data("ouvriers", id_ouv = int(id_ouvrier))
   ouvriers = return_table_ouvrier_avec_chantiers()
   return jsonify(ouvriers)

@APP.route("/listeOuvriers/<id_ouvrier>/chantiersdispos", methods=['GET', 'POST', 'DELETE', 'PUT'])
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


# @APP.route("/addOuvriers/", methods = ['POST'])
# def addOuvrier():
#     """
#     Attribue un ouvrier à un chantier.
#     """
#     data = request.get_json()
#     new_evenement = {"start":"2020-01-07", "title":data["nom"]+" est a Paris", "end":"2020-01-07"}
#     global attribution
#     attribution.append(new_evenement)
#     return jsonify(attribution)

if __name__ == '__main__':
   APP.run(debug=True)
