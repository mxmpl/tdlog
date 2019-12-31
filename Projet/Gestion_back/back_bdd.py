############################

"""
Projet TDLOG réalisé par Maxime BRISINGER, Margot COSSON, Raphael LASRY et
Maxime POLI, 2019-2020

Le but de ce script python est de traiter la partie back du site.

Fichier conforme à la norme PEP8.
"""

############################ Module Flask

from flask import Flask, request, render_template

############################ Choix de la maniere dont on gere les données

# Variables globales

global HTML_CSV 
HTML_CSV = True
global JAVASCRIPT_BDD 
JAVASCRIPT_BDD = not HTML_CSV
global JAVASCRIPT_BDD_HTML
JAVASCRIPT_BDD_HTML = True 

############################ Import des bibliothèques utiles
import sys
sys.path.append("..")
from Gestion_bdd import Bdd as bdd

import pandas as pd  # Bibliothèque permettant de gérer les CSV

############################ Creation du site

APP = Flask(__name__)  # Creation du site

############################ Utilisation de bdd

def get_id_names_dates_chantiers(): 
    """
    Renvoie une liste de listes telles que [index, nom, date_debut, date_fin]
    """
    return bdd.select_condition("""SELECT id, name, date_debut, date_fin
                                                FROM chantiers""")
def get_list_of_names_chantiers():
    """
    Renvoie la liste des noms des chantiers telle que ["chantier1", "chantier2", ...]
    """
    list_of_list_names = bdd.select_condition("""SELECT name FROM chantiers""")
    names = []
    for list_names in list_of_list_names: 
        names.append(list_names[0])
    return names
    
def get_id_names_ouvriers(): 
    """
    Renvoie une liste de listes telles que [index, nom]
    """
    return bdd.select_condition(
        """SELECT id, name FROM ouvriers""") 


print(bdd.test2())


############################ Page principale

@APP.route("/") # a modif pour mettre un bouton nouveau planning et un bouton modifier ancien planning
def home():
    """
    Permet de creer la page d'accueil.
    """
    user = {"username": "Bernard"}
    return render_template("bienvenue.html", user=user)

############################ Page home

@APP.route("/home")
def editer():
    """
    Permet de d'afficher la page home.
    """
    return render_template("home.html", chantiers=get_list_of_names_chantiers())

############################ Page principale : affectation des ouvriers

def recup_chantiers():
    """
    Permet de récupere les chantiers sous forme : [nom_chantier, nom_ouvrier].
    """
    # On récupère les couples chantiers/ouvriers
    if HTML_CSV:
        chantiers = pd.read_csv("csv/chantiers.csv", index_col="Nom", sep=",")
    elif JAVASCRIPT_BDD:
        chantiers = bdd.select_condition(
            """SELECT DISTINCT c.name,
                            o.name
                            FROM chantiers AS c, ouvriers AS o
                            JOIN attribution
                            ON c.id = attribution.id_chantier
                            JOIN ouvriers
                            ON (attribution.id_ouvrier = o.id) """
        )  # Attention aux alias
    return chantiers

@APP.route("/ouvrier", methods=["POST"])
def assigner_chantier_a_ouvrier():
    """
    Permet de coupler les ouvriers avec les chantiers.
    """
    chantiers = recup_chantiers()
    # Si la personne souhaite ajouter un chantier non existant
    chantiers_a_traiter = request.form  # On récupère les infos de la requete
    for element in chantiers_a_traiter.keys():
        # On suppose qu'on ne rajoute pas deux fois un chantier identique
        if chantiers_a_traiter[element] not in LISTE_CHANTIERS:
            indice_nouveau_chantier = len(LISTE_CHANTIERS)
            LISTE_CHANTIERS.append(chantiers_a_traiter[element])
            ligne_ajout = [[indice_nouveau_chantier, chantiers_a_traiter[element]]]
            if HTML_CSV:
                liste_dataframe = pd.DataFrame(ligne_ajout)
                fichier = open("csv/chantiers.csv", "a")
                fichier.write("")
                fichier.close()
                liste_dataframe.to_csv(
                    "csv/liste_chantiers.csv", header=False, index=False, mode="a"
                )
            elif JAVASCRIPT_BDD:
                # Pour l'instant on ne demande que le nom du chantier
                chantier = [str(chantiers_a_traiter[element]), "NULL", "NULL", "NULL"]
                bdd.insert_chantier(chantier)
        if HTML_CSV:
            # Est-ce vraiment utile d'avoir deux CSV différents ?
            chantiers.at[chantiers_a_traiter[element], "Ouvrier"] = element
    if HTML_CSV:
        chantiers.to_csv("csv/chantiers.csv", sep=",")
        return render_template("home.html", chantiers=LISTE_CHANTIERS)
    # Mettre ce que l'on ferait si JAVASCRIPT_BDD était True
    return None

############################ Page d'affichage : on affiche le planning

@APP.route("/affichage_planning")
def affichage_planning():
    """
    Permet de visualiser le planning créé.
    """
    chantiers = recup_chantiers()
    if HTML_CSV:
        return chantiers.to_html()
    # Mettre ce que l'on ferait si JAVASCRIPT_BDD était True
    return None

############################ Fonction pour réinitialiser le planning

@APP.route("/reset")
def reset():
    """
    Permet de réinitialiser le planning.
    """
    chantiers = recup_chantiers()
    if HTML_CSV:
        for i in range(len(chantiers.loc[:, "Ouvrier"])):
            chantiers.loc[:, "Ouvrier"][i] = " "
        chantiers.to_csv("csv/chantiers.csv", sep=",")
        return render_template("home.html", chantiers=LISTE_CHANTIERS)
    # Mettre ce que l'on ferait si JAVASCRIPT_BDD était True
        # Ici on ne supprime pas la table, on séléctionnera simplement aucun chantier
    return None

########################### Lancement du site

if __name__ == "__main__":
    APP.debug = False
    APP.run()
