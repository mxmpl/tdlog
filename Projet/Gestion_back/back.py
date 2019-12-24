############################

"""
Projet TDLOG réalisé par Maxime BRISINGER, Margot COSSON, Raphael LASRY et
Maxime POLI, 2019-2020

Le but de ce script python est de traiter les bases de données
(chantiers et ouvriers principalement).

Fichier conforme à la norme PEP8.
"""

############################ Import des bibliothèques utiles

from flask import Flask, request, render_template
import pandas as pd

############################ Creation du site

APP = Flask(__name__)

############################ Utilisation de csv

DICTIONNAIRE_CHANTIERS = pd.read_csv("csv/liste_chantiers.csv", index_col=None, sep=",")
LISTE_CHANTIERS = []
for index in DICTIONNAIRE_CHANTIERS["Index"]:
    LISTE_CHANTIERS.append(DICTIONNAIRE_CHANTIERS["Noms"][index])

DICTIONNAIRE_OUVRIERS = pd.read_csv("liste_ouvriers.csv", index_col=None, sep=",")
LISTE_OUVRIERS = []
for index in DICTIONNAIRE_OUVRIERS["Index"]:
    LISTE_OUVRIERS.append(DICTIONNAIRE_OUVRIERS["Noms"][index])


@APP.route("/")

def home():
    """
    Permet de creer la page d'accueil.
    """
    user = {"username": "Bernard"}
    return render_template("bienvenue.html", user=user)


@APP.route("/home")

def editer():
    """
    Permet de d'afficher la page home.
    """
    return render_template("home.html", chantiers=LISTE_CHANTIERS)


@APP.route("/ouvrier", methods=["POST"])

def assigner_chantier_a_ouvrier():
    """
    Permet de coupler les ouvriers avec les chantiers.
    """
    chantiers = pd.read_csv("chantiers.csv", index_col="Nom", sep=",")
    chantiers_a_traiter = request.form
    for element in chantiers_a_traiter.keys():
        if chantiers_a_traiter[element] not in LISTE_CHANTIERS:
            indice_nouveau_chantier = len(LISTE_CHANTIERS)
            LISTE_CHANTIERS.append(chantiers_a_traiter[element])
            ligne_ajout_csv = [[indice_nouveau_chantier, chantiers_a_traiter[element]]]
            liste_dataframe = pd.DataFrame(ligne_ajout_csv)
            fichier = open("chantiers.csv", "a")
            fichier.write("")
            fichier.close()
            liste_dataframe.to_csv(
                "csv/liste_chantiers.csv", header=False, index=False, mode="a"
            )
        chantiers.at[chantiers_a_traiter[element], "Ouvrier"] = element
    chantiers.to_csv("chantiers.csv", sep=",")
    return render_template("home.html", chantiers=LISTE_CHANTIERS)


@APP.route("/affichage_planning")

def affichage_planning():
    """
    Permet de visualiser le planning créé.
    """
    chantiers = pd.read_csv("chantiers.csv", index_col=False, sep=",")
    return chantiers.to_html()


@APP.route("/reset")

def reset():
    """
    Permet de réinitialiser le planning.
    """
    chantiers = pd.read_csv("csv/chantiers.csv", index_col="Nom", sep=",")
    for i in range(len(chantiers.loc[:, "Ouvrier"])):
        chantiers.loc[:, "Ouvrier"][i] = " "
    chantiers.to_csv("chantiers.csv", sep=",")
    return render_template("home.html", chantiers=LISTE_CHANTIERS)


########################### Utilisation des bases de données


########################### Lancement du site

if __name__ == "__main__":
    APP.debug = False
    APP.run()
