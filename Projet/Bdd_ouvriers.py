######################################################

""" Gestion de la base de données Chantiers"""

###################################################### Import des bibliothèques utiles

import sqlite3

###################################################### Création de la base de données liste_chantiers

db = sqlite3.connect('bbd_ouvriers') # La base de données listant tous les chantiers
cursor = db.cursor() # On se place sur cette bdd

cursor.execute('''CREATE TABLE IF NOT EXISTS ouvriers(id INTEGER PRIMARY KEY,
                                                    name TEXT, specialite TEXT, statut BIT)''') #statut permet de dire s'il est disponible ou pas avec 0 si oui, 1 si non

db.commit() # On termine de creer la table

###################################################### Ajout d'un nouveau ouvrier à notre base de données

# Ici il faudrait pouvoir récupérer les données depuis le site

# new_ouvrier = get_data() # A terme pouvoir utiliser cette fct qui crée une liste comme l'exemple de la ligne suivante 
new_ouvrier = ["Jean", "horticulture", "0"]
cursor.execute('''INSERT INTO ouvriers(name, specialite, statut)
                  VALUES(?,?,?)''', (new_ouvrier[0], new_ouvrier[1], new_ouvrier[2]))
                  
new_ouvrier = ["Lucie", "fleuriste", "1"]
cursor.execute('''INSERT INTO ouvriers(name, specialite, statut)
                  VALUES(?,?,?)''', (new_ouvrier[0], new_ouvrier[1], new_ouvrier[2]))
                  
db.commit()

###################################################### Sélection de certains chantiers particuliers
    
def Select_condition (command: str):
    cursor.execute(command)
    rows = cursor.fetchall()
    for row in rows:
        print(list(row[:]))
    
Select_condition('''SELECT name, specialite 
                    FROM ouvriers''')
                    
Select_condition('''SELECT name 
                    FROM ouvriers 
                    WHERE specialite = "horticulture"''')
                    
Select_condition('''SELECT * 
                    FROM ouvriers 
                    WHERE name = "Jean"''')
                    
Select_condition('''SELECT COUNT(*) 
                    FROM ouvriers 
                    WHERE name = "Jean"''')
                    
Select_condition('''SELECT * 
                    FROM ouvriers 
                    ORDER BY name''')

###################################################### Supression de la table entière

# On supprime la table
cursor.execute('''DROP TABLE ouvriers''')
