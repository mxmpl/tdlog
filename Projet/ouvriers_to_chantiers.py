import sqlite3

db = sqlite3.connect('liste_attribution') # La base de données listant tous les chantiers
cursor = db.cursor() # On se place sur cette bdd

cursor.execute('''CREATE TABLE IF NOT EXISTS attribution(id INTEGER PRIMARY KEY,
                                                    id_ouvrier INTEGER, id_chantier INTEGER)''')
db.commit() # On termine de creer la table

# new_attribution = get_data() # données à récupérer depuis Python 
new_attribution = ["1", "2"]
cursor.execute('''INSERT INTO attribution(id_ouvrier, id_chantier)
                  VALUES(?,?)''', (new_attribution[0], new_attribution[1]))
                  
new_attribution = ["4", "1"]
cursor.execute('''INSERT INTO attribution(id_ouvrier, id_chantier)
                  VALUES(?,?)''', (new_attribution[0], new_attribution[1]))
db.commit()


def Select_condition (command: str):
    cursor.execute(command)
    rows = cursor.fetchall()
    for row in rows:
        print(list(row[:]))
    
Select_condition('''SELECT id_ouvrier, id_chantier 
                    FROM attribution''') 
                    
Select_condition('''SELECT id_chantier 
                    FROM attribution 
                    WHERE id_ouvrier = "1"''') 
                    
Select_condition('''SELECT * 
                    FROM attribution''') 
                    
Select_condition('''SELECT COUNT(*) 
                    FROM attribution 
                    WHERE id_ouvrier = "1"''') 

###################################################### Supression de la table entière

# On supprime la table
cursor.execute('''DROP TABLE attribution''')


