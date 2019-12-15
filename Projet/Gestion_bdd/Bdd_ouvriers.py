
######################################################

'''
Projet TDLOG réalisé par Maxime BRISINGER, Margot COSSON, Raphael LASRY et Maxime POLI, 2019-2020

Le but de ce script python est de traiter les bases de données relatives aux ouvriers.

'''

###################################################### Import des bibliothèques utiles

import sqlite3

###################################################### Création de la base de données bdd_ouvriers

db = sqlite3.connect('bdd_ouvriers') # La base de données listant tous les ouvriers
cursor = db.cursor() # On se place sur cette bdd

DISPONIBLE = 0
INDISPONIBLE = 1
cursor.execute('''CREATE TABLE IF NOT EXISTS ouvriers(id INTEGER PRIMARY KEY,
                                                    name TEXT, specialite TEXT, statut BIT)''') # Statut permet de dire s'il est disponible ou pas avec DISPONIBLE si oui, INDISPONIBLE si non

db.commit() # On termine de creer la table

###################################################### Ajout d'un nouveau ouvrier à notre base de données

# Ici il faudrait pouvoir récupérer les données depuis le site

# new_ouvrier = get_data() # A terme pouvoir utiliser cette fct qui crée une liste comme l'exemple de la ligne suivante 
new_ouvrier = ["Jean", "horticulture", DISPONIBLE]
cursor.execute('''INSERT INTO ouvriers(name, specialite, statut)
                  VALUES(?,?,?)''', (new_ouvrier[0], new_ouvrier[1], new_ouvrier[2]))
                  
new_ouvrier = ["Lucie", "fleuriste", INDISPONIBLE]
cursor.execute('''INSERT INTO ouvriers(name, specialite, statut)
                  VALUES(?,?,?)''', (new_ouvrier[0], new_ouvrier[1], new_ouvrier[2]))
                  
db.commit()

###################################################### Sélection de certains ouvriers particuliers
    
def Select_condition (command: str):
    cursor.execute(command)
    rows = cursor.fetchall()
    for row in rows:
        print(list(row[:]))
    
print("On renvoie tous les noms et spécialités des ouvriers dans la bdd")
Select_condition('''SELECT name, specialite
                    FROM ouvriers''') # On renvoie tous les noms et spécialités des ouvriers dans la bdd
                    
print("\nOn renvoie tous les noms des ouvriers ayant une spécialité donnée")
Select_condition('''SELECT name 
                    FROM ouvriers 
                    WHERE specialite = "horticulture"''') # On renvoie tous les noms des ouvriers ayant une spécialité donnée
                    
print("\nOn renvoie toutes les infos d'un ouvrier ayant un nom donné")
Select_condition('''SELECT * 
                    FROM ouvriers 
                    WHERE name = "Jean"''') # On renvoie toutes les infos d'un ouvrier ayant un nom donné
                
print("\nOn compte combien d'ouvriers sont dans la table")
Select_condition('''SELECT COUNT(*) 
                    FROM ouvriers 
                    ''') # On compte combien d'ouvriers sont dans la table

print("\nOn renvoie tous les ouvriers triés par noms")
Select_condition('''SELECT * 
                    FROM ouvriers 
                    ORDER BY name''') # On renvoie tous les ouvriers triés par noms

print("\nOn renvoie tous les ouvriers disponibles")
Select_condition('''SELECT * 
                    FROM ouvriers 
                    WHERE statut = 0''') # Comment mettre DISPONIBLE ici ? 

###################################################### Supression de la table entière

# On supprime la table
cursor.execute('''DROP TABLE ouvriers''')
