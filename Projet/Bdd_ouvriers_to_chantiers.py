######################################################

'''
Projet TDLOG réalisé par Maxime BRISINGER, Margot COSSON, Raphael LASRY et Maxime POLI, 2019-2020

Le but de ce script python est de traiter les bases de données relatives aux liens ouvriers/chantiers.

'''

###################################################### Import des bibliothèques utiles

import sqlite3

###################################################### Création de la base de données bdd_liste_attribution

db = sqlite3.connect('bdd_liste_attribution') # La base de données listant tous les couples chantiers-ouvriers
cursor = db.cursor() # On se place sur cette bdd

cursor.execute('''CREATE TABLE IF NOT EXISTS attribution(id INTEGER PRIMARY KEY,
                                                    id_ouvrier INTEGER, id_chantier INTEGER)''')
db.commit() # On termine de creer la table

###################################################### Ajout d'un nouveau couple à notre base de données

# new_attribution = get_data() # données à récupérer depuis Python 
new_attribution = ["1", "2"]
cursor.execute('''INSERT INTO attribution(id_ouvrier, id_chantier)
                  VALUES(?,?)''', (new_attribution[0], new_attribution[1]))
                  
new_attribution = ["4", "1"]
cursor.execute('''INSERT INTO attribution(id_ouvrier, id_chantier)
                  VALUES(?,?)''', (new_attribution[0], new_attribution[1]))
db.commit()

###################################################### Sélection de certains ouvriers particuliers

def Select_condition (command: str):
    cursor.execute(command)
    rows = cursor.fetchall()
    for row in rows:
        print(list(row[:]))
    
print("On renvoie tous les couples d'attribution (ouvrier,chantier) présents dans la table.")
Select_condition('''SELECT id_ouvrier, id_chantier 
                    FROM attribution''') 
                    
print("\nOn renvoie les chantiers de l'ouvrier 1")
Select_condition('''SELECT id_chantier 
                    FROM attribution 
                    WHERE id_ouvrier = "1"''') 

print("\nOn renvoie toutes les informations de la table")
Select_condition('''SELECT * 
                    FROM attribution''') 
                    
print("\nOn renvoie le nombre de chantier de l'ouvrier 1")
Select_condition('''SELECT COUNT(*) 
                    FROM attribution 
                    WHERE id_ouvrier = "1"''') 

###################################################### Supression de la table entière

# On supprime la table
cursor.execute('''DROP TABLE attribution''')


