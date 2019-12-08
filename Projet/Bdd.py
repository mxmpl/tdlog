import sqlite3

db = sqlite3.connect('liste_chantiers') # La base de données listant tous les chantiers
cursor = db.cursor() # On se place sur cette bdd

cursor.execute('''
    CREATE TABLE IF NOT EXISTS chantiers(id INTEGER PRIMARY KEY, name TEXT,
                       day TEXT, adress TEXT)
''') # La table possède 4 arguments, la clef primaire, le nom du chantier, le jour où l'on souhaite y aller, ainsi que l'adresse du chantier

db.commit() # On termine de creer la table

# Ici il faudrait pouvoir récupérer les données sous forme d'un tableau avec le nom, les jours (optionnel ?) et l'adresse

# new_chantier = get_data() # A terme pouvoir utiliser cette fct qui crée une liste comme l'exemple de la ligne suivante 
new_chantier = ["Paris", "Lundi ; Mercredi", "20 rue des lillas"]

cursor.execute('''INSERT INTO chantiers(name, day, adress)
                  VALUES(?,?,?)''', (new_chantier[0], new_chantier[1], new_chantier[2]))
                  
db.commit()

cursor.execute('''SELECT name, day, adress FROM chantiers''')
for row in cursor:
    # row[0] returns the first column in the query (name), row[1] returns email column.
    print('{0} : {1}, {2}'.format(row[0], row[1], row[2]))
    
# On supprime la table
cursor.execute('''DROP TABLE chantiers''')
