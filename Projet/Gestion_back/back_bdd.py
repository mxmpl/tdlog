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

############# Choix de la maniere dont on gere les données

HTML_CSV = True
JAVASCRIPT_BDD = not HTML_CSV
JAVASCRIPT_BDD_HTML = True

############# Import des bibliothèques utiles

sys.path.append("..")
from Gestion_bdd import Bdd as bdd

############# Creation du site

APP = Flask(__name__)  # Creation du site

#%% Fonctions du back 

def set_new_attribution(dict_new_attributions: dict):
    """
    dict_new_attributions doit être un dictionnaire qui associe
    un nom d'ouvrier à un nom de chantier
    """
    for ouvrier in dict_new_attributions.keys():  # ouvrier est un type str
        bdd.insert_attribution(
            [
                bdd.get_id_from_name_ouvrier(ouvrier),
                bdd.get_id_from_name_chantier(dict_new_attributions[ouvrier]),
            ]
        )
    print(bdd.return_table_attribution()) # a supprimer après, pour afficher pour l'instant 


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

#%% Liens avec le front en HTML 


############# Page principale

@APP.route("/")  # a modif pour mettre un bouton nouveau planning
# Et un bouton modifier ancien planning
def home():
    """
    Permet de creer la page d'accueil.
    """
    user = {"username": "Bernard"}
    return render_template("bienvenue.html", user=user)

############# Page home

@APP.route("/home")
def editer():
    """
    Permet de d'afficher la page home.
    """
    return render_template("home.html", chantiers=bdd.get_list_of_names_chantiers())

############# Liens avec le front 
        
@APP.route("/ouvrier", methods=["POST"])
def new_attribution():
    """
    On suppose pour le moment que deux chantiers n'ont pas le mêmes noms.
    On créer une nouvelle attribution.
    """
    requete = request.form
    if (
            " " not in requete.keys()
    ):  # Un dictionnaire avec comme clef " " est le signe d'une requete
        # pour creer un nouveau chantier
        set_new_attribution(requete)
    else:
        set_new_chantier(requete)
    return render_template("home.html", chantiers=bdd.get_list_of_names_chantiers())


############# Page d'affichage : on affiche le planning
    
@APP.route("/affichage_planning")
def affichage_planning():
    """
    Permet de visualiser le planning créé.
    """
    return render_template("planning.html", planning=get_planning())

############# Fonction pour réinitialiser le planning

@APP.route("/reset")
def reset():
    """
    Permet de réinitialiser le planning.
    """
    bdd.reset_table("attribution")
    return render_template("home.html", chantiers=bdd.get_list_of_names_chantiers())

############# PROBLÈME (mail envoyé à clémentine) : POURQUOI ÇA NE MARCHE PAS sur spyder 
# (alors que ok dans le terminal)
# ALORS QUE appel_bdd est bien déclaré dans Bdd.py ??
# alors que ça marche avec bdd.DISPONIBLE par ex ?
# ça marche quand Bdd.py est dans le même dossier

# print("ICI", bdd.appel_bdd)

############# Lancement du site

if __name__ == "__main__":
    APP.debug = (
        False
    )  # Quand on met Debug = True,
        # ça arrive pas en bas donc ça n'efface pas les tables, ATTENTION !
    APP.run()

# À la fin de l'utilisation, on supprime les tables

bdd.suppression_table_chantiers()
bdd.suppression_table_ouvriers()
bdd.suppression_table_attribution()
