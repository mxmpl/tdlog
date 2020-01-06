############################

"""
Projet TDLOG réalisé par Maxime BRISINGER, Margot COSSON, Raphael LASRY et
Maxime POLI, 2019-2020

Le but de ce script python est de traiter la partie back du site.
Ce scrit gère uniquement le prototype du site en HTML-CSV.

Fichier conforme à la norme PEP8.
"""

############################ Module Flask

from flask import Flask, request, render_template  # Bibliothèque permettant de
# génerer le site

############################ Import des bibliothèques utiles

import pandas as pd  # Bibliothèque permettant de gérer les CSV

############################ Creation du site

APP = Flask(__name__)  # Creation du site

############################ Utilisation de csv

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

############################ Page principale

@APP.route("/")
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
    return render_template("home.html", chantiers=LISTE_CHANTIERS)

############################ Page principale : affectation des ouvriers

def recup_chantiers():
    """
    Permet de récupere les chantiers sous forme : [nom_chantier, nom_ouvrier].
    """
    # On récupère les couples chantiers/ouvriers
    return pd.read_csv("csv/chantiers.csv", index_col="Nom", sep=",")

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
            liste_dataframe = pd.DataFrame(ligne_ajout)
            fichier = open("csv/chantiers.csv", "a")
            fichier.write("")
            fichier.close()
            liste_dataframe.to_csv(
                "csv/liste_chantiers.csv", header=False, index=False, mode="a"
            )
        chantiers.at[chantiers_a_traiter[element], "Ouvrier"] = element
    chantiers.to_csv("csv/chantiers.csv", sep=",")
    return render_template("home.html", chantiers=LISTE_CHANTIERS)

############################ Page d'affichage : on affiche le planning

@APP.route("/affichage_planning")
def affichage_planning():
    """
    Permet de visualiser le planning créé.
    """
    chantiers = recup_chantiers()
    return chantiers.to_html()

############################ Fonction pour réinitialiser le planning

@APP.route("/reset")
def reset():
    """
    Permet de réinitialiser le planning.
    """
    chantiers = recup_chantiers()
    for i in range(len(chantiers.loc[:, "Ouvrier"])):
        chantiers.loc[:, "Ouvrier"][i] = " "
    chantiers.to_csv("csv/chantiers.csv", sep=",")
    return render_template("home.html", chantiers=LISTE_CHANTIERS)

########################### Lancement du site

if __name__ == "__main__":
    APP.debug = False
    APP.run()
