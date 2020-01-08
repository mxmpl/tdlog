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

from flask import Flask, request, render_template

#############%% Import des bibliothèques utiles

sys.path.append("..")
from Gestion_bdd import bdd

#############%% Creation du site

#APP = Flask(__name__)  # Creation du site

#############%% Fonctions du back

########%% SET & DEL

def set_new_chantier(dict_new_chantier: dict):
    """
    Permet d'inserer un nouveau chantier. Le format d'entrée
    doit être un dictionnaire de la forme
    {"name_chantier": text, "start": text, "end": text, "adress": text}.
    """
    # Gestion d'erreur à faire dessus : conformité de l'entrée + chantier non existant
    bdd.insert_chantier(dict_new_chantier)

def del_chantier(id_chantier: int):
    """
    Permet de supprimer un chantier de la table chantiers à partir de son id.
    """
    chantiers = return_table_chantier()
    for chantier in chantiers:
        if id_chantier == chantier["id_chantier"]:
            bdd.del_chantier(id_chantier)
    raise Exception ("Attention, vous essayez de supprimer un chantier qui n'existe pas")

def set_new_ouvrier(dict_new_ouvrier: dict):
    """
    Permet d'inserer un nouveau ouvrier. Le format d'entrée
    doit être un dictionnaire de la forme
    {"name_ouvrier": text}.
    """
    # Gestion d'erreur à faire dessus : conformité de l'entrée + ouvrier non existant
    bdd.insert_ouvrier(dict_new_ouvrier) 
    
def del_ouvrier(id_ouvrier: int):
    """
    Permet de supprimer un ouvrier de la table ouvriers à partir de son id.
    """
    ouvriers = return_table_ouvrier()
    for ouvrier in ouvriers:
        if id_ouvrier == ouvrier["id_ouvrier"]:
            bdd.del_ouvrier(id_ouvrier)
    raise Exception ("Attention, vous essayez de supprimer un ouvrier qui n'existe pas")

def set_new_attribution(dict_new_attribution: dict): 
    """
    Permet d'inserer un couple d'id_ouvrier/id_chantier.
    Format d'entrée : dict_new_attribution = {"id_ouvrier": int, "id_chantier": int}
    """
    # Gestion d'erreur à faire : conformité de l'entrée + vérification que les id_ouvrier et id_chantier existent
    if verif_dispo_horaire_ouvrier(dict_new_attribution["id_ouvrier"], dict_new_attribution["id_chantier"]):
        bdd.insert_attribution(dict_new_attribution)
    else: 
        raise Exception("L'ouvrier {} ne peut être attribué au chantier {} car il est déjà occupé".format(dict_new_attribution["id_ouvrier"], dict_new_attribution["id_chantier"])

def del_attribution(id_ouv: int, id_chan: int):
    """
    Permet de supprimer une attribution de la table attribution à partir d'un
    couple d'id_ouvrier/id_chantier.
    """
    attributions = return_table_attribution()
    for attribution in attributions:
        if id_ouv == attribution["id_ouvrier"] and id_chan == attribution["id_chantier"]:
            bdd.del_attribution(id_ouv, id_chan)
    raise Exception ("Attention, vous essayez de supprimer une attribution qui n'existe pas")
    
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

def return_table_chantier():
    """
    Renvoie toute la table chantiers sous forme d'une liste de dictionnaire :
    [{"id_chantier": int, "name_chantier": text, "start": text, "end": text, "adress": text},].
    """
    return bdd.return_table_chantier()

def return_table_ouvrier():
    """
    Renvoie toute la table ouvriers sous forme d'une liste de dictionnaire :
    [{"id_ouvrier": int, "name_ouvrier": text},].
    """
    return bdd.return_table_ouvrier()

def return_table_attribution():
    """
    Renvoie toute la table attribution sous forme d'une liste de dictionnaire :
    [{"id_ouvrier": int, "id_chantier": text},].
    """
    return bdd.return_table_attribution()

def get_planning():
    """
    Renvoie toutes les attributions et les informations sur les ouvriers et
    les chantiers correspondantes sous la forme d'une liste de dictionnaires
    telle que [{"id_ouvrier": int, "name_ouvrier": text, "id_chantier": int,
    "name_chantier": text, "start": text, "end": text, "adress": text},]
    """
    return bdd.get_all_attribution()

########%% MODIFY

def modify_name_ouvrier(id_ouv: int, new_name: str):
    """
    Permet de modifier le nom d'un ouvrier.
    """
    ouvriers = return_table_ouvrier()
    for ouvrier in ouvriers:
        if id_ouv == ouvrier["id_ouvrier"]:
            bdd.modify_name_ouvrier(id_ouv, new_name)
    raise Exception("Attention, vous essayez de modifier le nom d'un ouvrier qui n'existe pas")
    
def modify_name_chantier(id_chan: int, new_name: str):
    """
    Permet de modifier le nom d'un chantier.
    """
    chantiers = return_table_chantier()
    for chantier in chantiers:
        if id_chan == chantier["id_chantier"]:
            bdd.modify_name_chantier(id_chan, new_name)
    raise Exception("Attention, vous essayez de modifier le nom d'un chantier qui n'existe pas")
    
########%% CHECK

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
