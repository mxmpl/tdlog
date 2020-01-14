############################

"""
Projet TDLOG réalisé par Maxime BRISINGER, Margot COSSON, Raphael LASRY et
Maxime POLI, 2019-2020

Le but de ce script python est de télécharger les bibliothèques utiles

Fichier conforme à la norme PEP8.
"""

############################ Import de la bibliothèque os

import os

############################ Telechargement des bibliothèques liées au back

os.system("pip install flask")
# os.system("pip install render_template")
# os.system("pip install request")

############################ Telechargement des bibliothèques liées aux bdd

os.system("pip install pysqlite3") # Normalement il est installé de base
os.system("pip install doctest-cli")
os.system("pip install pandas")
