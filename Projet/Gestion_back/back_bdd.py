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


HTML_CSV = True
JAVASCRIPT_BDD = not HTML_CSV
JAVASCRIPT_BDD_HTML = True 

############################ Import des bibliothèques utiles
import sys
sys.path.append("..")
from Gestion_bdd import Bdd as bdd

############################ Creation du site

APP = Flask(__name__)  # Creation du site

############################ Page principale

@APP.route("/") # a modif pour mettre un bouton nouveau planning 
#et un bouton modifier ancien planning
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
    return render_template("home.html", chantiers=bdd.get_list_of_names_chantiers())

########################### Affichage des tables, a supprimer dans le futur

a = bdd.return_table_ouvriers()
b = bdd.return_table_chantiers()
c = bdd.return_table_attribution()
print(a)
print(b)
print(c)

########################### Page principale : affectation des ouvriers et rajout d'un chantier

def set_new_attribution(new_attributions): 
    """
    new_attributions doit être un dictionnaire qui associe 
    un nom d'ouvrier à un nom de chantier
    """
    for ouvrier in new_attributions.keys(): # ouvrier est un type str
        bdd.insert_attribution([bdd.get_id_from_name_ouvrier(ouvrier),bdd.get_id_from_name_chantier(new_attributions[ouvrier])])
    c = bdd.return_table_attribution()
    print(c)
    
def set_new_chantier(dict_new_chantier): 
    """
    dict_new_chantier est un dictionnaire qui associe à " " le nom du nouveau chantier
    """
    for clef in dict_new_chantier.keys(): 
        new_chantier = [str(dict_new_chantier[clef]), "NULL", "NULL", "NULL"]
        bdd.insert_chantier(new_chantier)
    
    
@APP.route("/ouvrier", methods=["POST"])
def new_attribution(): # On suppose pour le moment que deux chantiers n'ont pas le mêmes noms
    requete = request.form 
    if (" " not in requete.keys()): # un dictionnaire avec comme clef " " est le signe d'une requete pour creer un nouveau chantier
        set_new_attribution(requete)
    else : 
        set_new_chantier(requete)
    return render_template("home.html", chantiers=bdd.get_list_of_names_chantiers())   


    
    
    
    
# À FAIRE : new_chantier ; new_ouvrier ; reset et affichage_planning 
#
#@APP.route("/ouvrier", methods=["POST"])
#def assigner_chantier_a_ouvrier():
#    """
#    Permet de coupler les ouvriers avec les chantiers.
#    """
#    chantiers = recup_chantiers()
#    # Si la personne souhaite ajouter un chantier non existant
#    chantiers_a_traiter = request.form  # On récupère les infos de la requete
#    for element in chantiers_a_traiter.keys():
#        # On suppose qu'on ne rajoute pas deux fois un chantier identique
#        if chantiers_a_traiter[element] not in LISTE_CHANTIERS:
#            indice_nouveau_chantier = len(LISTE_CHANTIERS)
#            LISTE_CHANTIERS.append(chantiers_a_traiter[element])
#            ligne_ajout = [[indice_nouveau_chantier, chantiers_a_traiter[element]]]
#            if HTML_CSV:
#                liste_dataframe = pd.DataFrame(ligne_ajout)
#                fichier = open("csv/chantiers.csv", "a")
#                fichier.write("")
#                fichier.close()
#                liste_dataframe.to_csv(
#                    "csv/liste_chantiers.csv", header=False, index=False, mode="a"
#                )
#            elif JAVASCRIPT_BDD:
#                # Pour l'instant on ne demande que le nom du chantier
#                chantier = [str(chantiers_a_traiter[element]), "NULL", "NULL", "NULL"]
#                bdd.insert_chantier(chantier)
#        if HTML_CSV:
#            # Est-ce vraiment utile d'avoir deux CSV différents ?
#            chantiers.at[chantiers_a_traiter[element], "Ouvrier"] = element
#    if HTML_CSV:
#        chantiers.to_csv("csv/chantiers.csv", sep=",")
#        return render_template("home.html", chantiers=bdd.get_list_of_names_chantiers())
#    return None

############################# Page d'affichage : on affiche le planning
#
#@APP.route("/affichage_planning")
#def affichage_planning():
#    """
#    Permet de visualiser le planning créé.
#    """
#    chantiers = recup_chantiers()
#    if HTML_CSV:
#        return chantiers.to_html()
#    # Mettre ce que l'on ferait si JAVASCRIPT_BDD était True
#    return None
#
############################# Fonction pour réinitialiser le planning
#
#@APP.route("/reset")
#def reset():
#    """
#    Permet de réinitialiser le planning.
#    """
#    chantiers = recup_chantiers()
#    if HTML_CSV:
#        for i in range(len(chantiers.loc[:, "Ouvrier"])):
#            chantiers.loc[:, "Ouvrier"][i] = " "
#        chantiers.to_csv("csv/chantiers.csv", sep=",")
#        return render_template("home.html", chantiers=LISTE_CHANTIERS)
#    # Mettre ce que l'on ferait si JAVASCRIPT_BDD était True
#        # Ici on ne supprime pas la table, on séléctionnera simplement aucun chantier
#    return None

############################# PROBLÈME : POURQUOI ÇA NE MARCHE PAS sur spyder 
#(alors que ok dans le terminal) 
# ALORS QUE appel_bdd est bien déclaré dans Bdd.py ??
# alors que ça marche avec bdd.DISPONIBLE par ex ? 
# ça marche quand Bdd.py est dans le même dossier 

#print("ICI", bdd.appel_bdd)

########################### Lancement du site

if __name__ == "__main__":
    APP.debug = False # Quand on met Debug = True, ça arrive pas en bas donc ça n'efface pas les tables, ATTENTION ! 
    APP.run()
    
# À la fin de l'utilisation, on supprime les tables 

bdd.suppression_table_chantiers()
bdd.suppression_table_ouvriers()
bdd.suppression_table_attribution()