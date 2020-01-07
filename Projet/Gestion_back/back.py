#############

"""
Projet TDLOG réalisé par Maxime BRISINGER, Margot COSSON, Raphael LASRY et
Maxime POLI, 2019-2020

Le but de ce script python est de traiter la partie back du site.

Fichier conforme à la norme PEP8.
"""

############# Module sys

import sys

############# Module Flask

from flask import Flask, request, render_template

############# Import des bibliothèques utiles

sys.path.append("..")
from Gestion_bdd import bdd

############# Creation du site

APP = Flask(__name__)  # Creation du site

#%% Fonctions du back


def set_new_attribution_name(dict_new_attributions: dict):
    """
    dict_new_attributions doit être un dictionnaire qui associe
    un nom d'ouvrier à un nom de chantier.
    Discuter du fait que si on déclare une nouvelle attribution avec les noms
    du chantier et de l'ouvrier, cela peut etre problematique en cas de doublons
    de noms.
    """
    for ouvrier in dict_new_attributions.keys():  # ouvrier est un type str
        id_ouvrier = bdd.get_id_from_name_ouvrier(ouvrier)
        id_chantier = bdd.get_id_from_name_chantier(dict_new_attributions[ouvrier])
        if verif_dispo_horaire_ouvrier(id_ouvrier, id_chantier):
            bdd.insert_attribution([id_ouvrier, id_chantier])

def set_new_attribution_id(dict_new_attributions: dict): 
    """
    dict_new_attributions doit être un dictionnaire qui associe
    un id d'ouvrier à un id de chantier.
    """
    for id_ouvrier in dict_new_attributions.keys():  # id est un type int
        id_chantier = dict_new_attributions[id_ouvrier]
        if verif_dispo_horaire_ouvrier(id_ouvrier, id_chantier):
            bdd.insert_attribution([id_ouvrier, id_chantier])



def set_new_chantier(dict_new_chantier: dict):
    """
    dict_new_chantier est un dictionnaire qui associe à " "
    le nom du nouveau chantier.
    """
    for clef in dict_new_chantier.keys():
        new_chantier = [str(dict_new_chantier[clef]), "NULL", "NULL", "NULL"]
        bdd.insert_chantier(new_chantier)


def set_new_ouvrier(dict_new_ouvrier: dict):
    """
    dict_new_ouvrier est un dictionnaire qui associe à " "
    le nom du nouvel ouvrier.
    """
    for clef in dict_new_ouvrier.keys():
        new_ouvrier = [str(dict_new_ouvrier[clef]), "NULL", bdd.DISPONIBLE]
        bdd.insert_ouvrier(new_ouvrier)


def get_planning():
    """
    Cette fonction permet de renvoyer une liste de listes telles que
    [[nom_ouvrier1, nom_chantier1, date_debut, date_fin],
    [nom_ouvrier2, nom_chantier2, date_debut, date_fin], ...]
    Attention, si aucune information n'a été remplie, cela renvoie une liste vide
    telle que [].
    """
    return bdd.get_all_attribution()

def conversion_liste_dict(liste: list): 
    """
    Cette fonction permet de convertir une liste d'attribution [nom_ouvrier1, 
    nom_chantier1, date_debut, date_fin] en dictionnaire 
    """
    pass

def verif_dispo_horaire_ouvrier(id_ouvrier: int, id_chantier: int):
    """
    Permet via l'index d'un chantier et d'un ouvrier de vérifier que
    l'ouvrier est disponible sur la plage horaire concernée pour ce
    chantier. Return true si l'ouvrier n'est pas encore occupé sur ce créneau.
    """
    if bdd.get_dates_from_id_chantier(
            id_chantier
    ) not in bdd.get_attribution_hours_one_ouvrier(id_ouvrier):
        return True
    return False



if __name__ == "__main__":
    APP.debug = False  
    APP.run()

# À la fin de l'utilisation, on supprime les tables

#bdd.suppression_table_chantiers()
#bdd.suppression_table_ouvriers()
#bdd.suppression_table_attribution()
#bdd.reset_table("chantiers")
#bdd.reset_table("ouvriers")
#bdd.reset_table("attribution")
