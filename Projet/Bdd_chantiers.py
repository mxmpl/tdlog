######################################################

'''
Projet TDLOG réalisé par Maxime BRISINGER, Margot COSSON, Raphael LASRY et Maxime POLI, 2019-2020

Le but de ce script python est de traiter les bases de données relatives aux chantiers.

'''

###################################################### Import des bibliothèques utiles

import sqlite3

###################################################### Création de la base de données bdd_chantiers

db = sqlite3.connect('bdd_chantiers') # La base de données listant tous les chantiers
cursor = db.cursor() # On se place sur cette bdd

cursor.execute('''CREATE TABLE IF NOT EXISTS chantiers(id INTEGER PRIMARY KEY,
                                                    name TEXT, date_debut SMALLDATETIME, date_fin SMALLDATETIME, adress TEXT)''')
# La table possède 4 arguments, la clef primaire, le nom du chantier, le jour de début du chantier, le jour de sa fin, ainsi que l'adresse du chantier

db.commit() # On termine de creer la table

###################################################### Ajout d'un nouveau chantier à notre base de données

# Ici il faudrait pouvoir récupérer les données sous forme d'un tableau avec le nom, les jours (optionnel ?) et l'adresse

# new_chantier = get_data() # A terme pouvoir utiliser cette fct qui crée une liste comme l'exemple de la ligne suivante 
new_chantier = ["Paris", "2016-10-09 08:00:00", "2016-10-09 12:00:00", "20 rue des lillas"]
cursor.execute('''INSERT INTO chantiers(name, date_debut, date_fin, adress)
                  VALUES(?,?,?,?)''', (new_chantier[0], new_chantier[1], new_chantier[2], new_chantier[3]))
                  
new_chantier = ["Marseille", "2018-10-09 08:00:00", "2018-10-09 12:00:00", "20 rue des lillas"]
cursor.execute('''INSERT INTO chantiers(name, date_debut, date_fin, adress)
                  VALUES(?,?,?,?)''', (new_chantier[0], new_chantier[1], new_chantier[2], new_chantier[3]))
                  
db.commit()

###################################################### Sélection de certains chantiers particuliers
    
def Select_condition (command: str):
    cursor.execute(command)
    rows = cursor.fetchall()
    for row in rows:
        print(list(row[:]))

# list_of_days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]   
#      
# def Select_days(days: str): # Cette fonction permet
#     list_days = []
#     for day in days:
#         for day_ in list_of_days:
#             if (day!=day_):
#                 if list_of_days.index(day) < list_of_days.index(day_):
#                     list_days.append(day + " ; " + day_)
#                 else :
#                     list_days.append(day_ + " ; " + day)
#     return tuple(list_days)
        
    
print ("On renvoie tous les noms, et adresses des chantiers dans la bdd")
Select_condition('''SELECT name, adress 
                    FROM chantiers''') # On renvoie tous les noms, et adresses des chantiers dans la bdd
                    
print("\nOn renvoie le nom des chantiers ayant une adresse donnée")
Select_condition('''SELECT name 
                    FROM chantiers 
                    WHERE adress = "20 rue des lillas"''') # On renvoie le nom des chantiers ayant une adresse donnée
                    
print("\nOn renvoie toutes les infos du chantier nommé 'Marseille'")
Select_condition('''SELECT * 
                    FROM chantiers 
                    WHERE name = "Marseille"''') # On renvoie toutes les infos du chantier nommé "Marseille"

print("\nOn compte combien de chantiers sont dans la table")            
Select_condition('''SELECT COUNT(*) 
                    FROM chantiers 
                    ''') # On compte combien de chantiers sont dans la table
 
print("\nOn renvoie tous les chantiers ordonnés par nom")
Select_condition('''SELECT * 
                    FROM chantiers 
                    ORDER BY name''') # On renvoie tous les chantiers ordonnés par nom
                    
print("\nOn renvoie tous les chantiers commençant à une date donnée")
Select_condition('''SELECT * 
                    FROM chantiers 
                    WHERE date_debut = ("2018-10-09 08:00:00") ''') # On renvoie tous les chantiers commençant à une date donnée

###################################################### Supression de la table entière

# On supprime la table
cursor.execute('''DROP TABLE chantiers''')
