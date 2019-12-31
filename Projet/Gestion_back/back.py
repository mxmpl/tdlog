############################

"""
Projet TDLOG réalisé par Maxime BRISINGER, Margot COSSON, Raphael LASRY et
Maxime POLI, 2019-2020

Le but de ce script python est de traiter la partie back du site.

Fichier conforme à la norme PEP8.
"""

############################ Module Flask

from flask import Flask, request, render_template  # Bibliothèque permettant de
# génerer le site

############################ Choix de la maniere dont on gere les données

# Variables globales

global HTML_CSV 
HTML_CSV = False
global JAVASCRIPT_BDD 
JAVASCRIPT_BDD = not HTML_CSV
global JAVASCRIPT_BDD_HTML
JAVASCRIPT_BDD_HTML = False 

############################ Import des bibliothèques utiles
if HTML_CSV:
    import pandas as pd  # Bibliothèque permettant de gérer les CSV
elif JAVASCRIPT_BDD:
    import sys
    sys.path.append("..")
    from Gestion_bdd import Bdd as bdd  # Fichier permettant de gérer les requetes SQL
# Probleme pour PEP8 lié à la localisation du fichier

############################ Creation du site

APP = Flask(__name__)  # Creation du site

############################ Utilisation de csv

if HTML_CSV:
    DICTIONNAIRE_CHANTIERS = pd.read_csv(
        "csv/liste_chantiers.csv", index_col=None, sep=","
    )  # Lecture du CSV et recuperation des éléments
    LISTE_CHANTIERS = []
    # Creation d'une liste listant tous les noms des chantiers
    for index in DICTIONNAIRE_CHANTIERS["Index"]:
        LISTE_CHANTIERS.append(DICTIONNAIRE_CHANTIERS["Noms"][index])

    DICTIONNAIRE_OUVRIERS = pd.read_csv(
        "csv/liste_ouvriers.csv", index_col=None, sep=","
    )  # Lecture du CSV et recuperation des éléments
    LISTE_OUVRIERS = []
    # Creation d'une liste listant tous les noms des ouvriers
    for index in DICTIONNAIRE_OUVRIERS["Index"]:
        LISTE_OUVRIERS.append(DICTIONNAIRE_OUVRIERS["Noms"][index])

############################ Utilisation de bdd

if JAVASCRIPT_BDD:
    DICTIONNAIRE_CHANTIERS = bdd.select_condition(
        """SELECT id, name
                                                FROM chantiers"""
    )  # Lecture de la table et recuperation de l'id et du nom des chantiers
    LISTE_CHANTIERS = []
    for index in DICTIONNAIRE_CHANTIERS:
        # Creation d'une liste listant tous les noms des chantiers
        LISTE_CHANTIERS.append(DICTIONNAIRE_CHANTIERS[index][1])

    DICTIONNAIRE_OUVRIERS = bdd.select_condition(
        """SELECT id, name
                                                FROM ouvriers"""
    )  # Lecture de la table et recuperation de l'id et du nom des ouvriers
    LISTE_OUVRIERS = []
    for index in DICTIONNAIRE_OUVRIERS:
        # Creation d'une liste listant tous les noms des ouvriers
        LISTE_OUVRIERS.append(DICTIONNAIRE_OUVRIERS[index][1])

############################ Page principale

@APP.route("/")
def home():
    """
    Permet de creer la page d'accueil.
    """
    if HTML_CSV:
        user = {"username": "Bernard"}
        return render_template("bienvenue.html", user=user)
    # Mettre ce que l'on ferait si JAVASCRIPT_BDD était True
    return None

############################ Page home

@APP.route("/home")
def editer():
    """
    Permet de d'afficher la page home.
    """
    if HTML_CSV:
        return render_template("home.html", chantiers=LISTE_CHANTIERS)
    # Mettre ce que l'on ferait si JAVASCRIPT_BDD était True
    return None

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
