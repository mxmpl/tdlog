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

#APP = Flask(__name__)  # Creation du site

#%% Fonctions du back

#%% SET 

def set_new_chantier(dict_new_chantier: dict):
    """
    Permet d'inserer un nouveau chantier. Le format d'entrée
    doit être un dictionnaire de la forme
    {"name_chantier": text, "start": text, "end": text, "adress": text}.
    """
    bdd.insert_chantier(dict_new_chantier)
    # Gestion d'erreur à faire dessus 

def set_new_ouvrier(dict_new_ouvrier: dict):
    """
    Permet d'inserer un nouveau ouvrier. Le format d'entrée
    doit être un dictionnaire de la forme
    {"name_ouvrier": text}.
    """
    bdd.insert_ouvrier(dict_new_ouvrier)
    # Gestion d'erreur à faire dessus 

def set_new_attribution(dict_new_attribution: dict): 
    """
    Permet d'inserer un couple d'id_ouvrier/id_chantier.
    Format d'entrée : dict_new_attribution = {"id_ouvrier": int, "id_chantier": int}
    """
    if verif_dispo_horaire_ouvrier(dict_new_attribution["id_ouvrier"], dict_new_attribution["id_chantier"]):
        bdd.insert_attribution(dict_new_attribution)
    else: 
        pass #Gestion d'erreur à faire 

def get_planning():
    """
    Renvoie toutes les attributions et les informations sur les ouvriers et
    les chantiers correspondantes sous la forme d'une liste de dictionnaires
    telle que [{"id_ouvrier": int, "name_ouvrier": text, "id_chantier": int,
    "name_chantier": text, "start": text, "end": text, "adress": text},]
    """
    return bdd.get_all_attribution()

def verif_dispo_horaire_ouvrier(id_ouvrier: int, id_chantier: int):
    """
    Permet via l'index d'un chantier et d'un ouvrier de vérifier que
    l'ouvrier est disponible sur la plage horaire concernée pour ce
    chantier. Return true si l'ouvrier n'est pas encore occupé sur ce créneau.
    """
    planning = bdd.get_planning_individuel(id_ouvrier)
    infos_chantier = bdd.get_info_from_id_chantier(id_chantier)
    for chantier in planning: 
        if(chantier["start"] == infos_chantier["start"] and chantier["end"] == infos_chantier["end"]): 
            raise Exception("L'ouvrier {} est déjà occupé sur la période {}-{}".format(bdd.get_info_id_ouvrier(id_ouvrier)["name_ouvrier"], infos_chantier["start"], infos_chantier["end"]))
            return False 
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
