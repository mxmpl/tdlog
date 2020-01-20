"""
Ce script permet de télécharger les bibliothèques utiles pour lancer le projet.
@author: Maxime BRISINGER, Margot COSSON, Raphael LASRY et Maxime POLI
"""

# Import de la bibliothèque os

import os

# Telechargement des bibliothèques liées au back

os.system("pip install flask")
os.system("pip install flask_cors")

# Telechargement des bibliothèques liées aux bdd

os.system("pip install pysqlite3") # Normalement il est installé de base
os.system("pip install doctest-cli")
os.system("pip install pandas")
