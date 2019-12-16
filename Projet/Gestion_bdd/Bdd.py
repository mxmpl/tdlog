######################################################

'''
Projet TDLOG réalisé par Maxime BRISINGER, Margot COSSON, Raphael LASRY et Maxime POLI, 2019-2020

Le but de ce script python est de traiter les bases de données (chantiers et ouvriers principalement).

'''

###################################################### Import des bibliothèques utiles

import sqlite3

###################################################### Requetes
    
def Commit_condition(command: str):
    """
    Permet d'executer une commande.
    """
    cursor.execute(command)
    db.commit()
    
def Select_condition (command: str): # On séléctionne les lignes demandées et on les récupère sous forme de liste
    """
    Permet à partir d'une commande d'enregistrer les informations correspondantes de la base de données. 
    """
    cursor.execute(command)
    db.commit()
    rows = cursor.fetchall()
    sortie = [] # permet de ne pas obtenir une liste de tuple en sortie => voir avec raphael si on peut pas changer fetchall pour éviter cette astuce 
    for row in rows:
        sortie.append(list(row[:]))
    return sortie

def Print_condition (command: str): 
    """
    Permet à partir d'une commande d'afficher les informations correspondantes de la base de données. 
    """
    cursor.execute(command)
    db.commit()
    rows = cursor.fetchall()
    for row in rows:
        print(list(row[:]))
        
        
###################################################### Création des bases de données 
db = sqlite3.connect('Bdd_principale') # La base de données avec 3 tables (informations sur les chantiers, ouvriers et attributions)
cursor = db.cursor() # On se place sur cette bdd

cursor.execute('''CREATE TABLE IF NOT EXISTS chantiers(id INTEGER PRIMARY KEY,
                                                    name TEXT, date_debut SMALLDATETIME, date_fin SMALLDATETIME, adress TEXT)''')
# La table possède 4 arguments, la clef primaire, le nom du chantier, le jour de début du chantier, le jour de sa fin, ainsi que l'adresse du chantier

DISPONIBLE = 0
INDISPONIBLE = 1
cursor.execute('''CREATE TABLE IF NOT EXISTS ouvriers(id INTEGER PRIMARY KEY,
                                                    name TEXT, specialite TEXT, statut BIT)''') # Statut permet de dire s'il est disponible ou pas avec DISPONIBLE si oui, INDISPONIBLE si non
                                                    
cursor.execute('''CREATE TABLE IF NOT EXISTS attribution(id_ouvrier INTEGER, id_chantier INTEGER,
                                                        FOREIGN KEY(id_ouvrier) REFERENCES ouvriers(id),
                                                        FOREIGN KEY(id_chantier) REFERENCES chantiers(id))
                                                        ''')

db.commit() # On termine de creer les tables

###################################################### Ajout d'un nouveau chantier à notre base de données

def Insert_chantier(new_chantier: list):
    cursor.execute('''INSERT INTO chantiers(name, date_debut, date_fin, adress)
                      VALUES(?,?,?,?)''',(new_chantier[0], new_chantier[1], new_chantier[2], new_chantier[3]))

# chantier = get_data() # A terme pouvoir utiliser cette fct qui crée une liste comme l'exemple de la ligne suivante 
chantier = ["Paris", "2016-10-09 08:00:00", "2016-10-09 12:00:00", "20 rue des lillas"]
Insert_chantier(chantier)
                  
chantier = ["Marseille", "2018-10-09 08:00:00", "2018-10-09 12:00:00", "20 rue des lillas"]
Insert_chantier(chantier)
                  
chantier = ["Noisy", "2019-12-09 08:00:00", "2020-02-09 12:00:00", "6-8 Avenue Blaise Pascal"]
Insert_chantier(chantier)

chantier = ["Noisy", "2019-12-09 08:00:00", "2020-02-09 12:00:00", "6-8 Avenue Blaise Pascal"]
Insert_chantier(chantier) # Chantier identique

chantier = ["Paris", "2019-11-21 09:00:00", "2019-12-09 13:00:00", "3 Avenue Foch"]
Insert_chantier(chantier)

chantier = ["Boulogne", "2014-06-25 08:00:00", "2021-08-07 12:00:00", "70 rue du point du jour"]
Insert_chantier(chantier)

db.commit()

###################################################### Ajout d'un nouveau ouvrier à notre base de données

def Insert_ouvrier(new_ouvrier: list):
    cursor.execute('''INSERT INTO ouvriers(name, specialite, statut)
                      VALUES(?,?,?)''',(new_ouvrier[0], new_ouvrier[1], new_ouvrier[2]))

# ouvrier = get_data() # A terme pouvoir utiliser cette fct qui crée une liste comme l'exemple de la ligne suivante 
ouvrier = ["Jean", "horticulture", DISPONIBLE]
Insert_ouvrier(ouvrier)
                  
ouvrier = ["Lucie", "fleuriste", INDISPONIBLE]
Insert_ouvrier(ouvrier)
    
ouvrier = ["Marcel", "élagueur", DISPONIBLE]
Insert_ouvrier(ouvrier)

ouvrier = ["Julie", "cheffe de chantier", DISPONIBLE]
Insert_ouvrier(ouvrier)

db.commit()

###################################################### Ajout d'un nouveau couple à notre base de données

def Insert_attribution(new_attribution: list): #new_attribution = ["id_ouvrier","id_chantier"]
    ouvriers_disponible = Select_condition('''SELECT id
                                              FROM ouvriers 
                                              WHERE statut = 0 ''') # Idem comment mettre DISPONIBLE ici ? 
    if [int(new_attribution[0])] in ouvriers_disponible:  # manipulation avec les listes encore, à voir avec Raphael 
        cursor.execute('''INSERT INTO attribution(id_ouvrier, id_chantier)
                          VALUES(?,?)''', (new_attribution[0], new_attribution[1]))
    else : 
        print("Vous ne pouvez pas associer cet ouvrier à ce chantier car l'ouvrier n'est pas disponible")
                      
# new_attribution = get_data() # données à récupérer depuis Python 
attribution = [1, 2]
Insert_attribution(attribution)
                  
attribution = [4, 1]
Insert_attribution(attribution)

attribution = [3, 1] #Attribution impossible (ouvrier non disponible)
Insert_attribution(attribution)

attribution = [1, 5]
Insert_attribution(attribution)

attribution = [2, 2]
Insert_attribution(attribution)

attribution = [3, 3]
Insert_attribution(attribution)


db.commit()

###################################################### Exemple de requetes sur les chantiers
    
print ("On renvoie tous les noms, et adresses des chantiers dans la bdd")
Print_condition('''SELECT name, adress 
                    FROM chantiers''') # On renvoie tous les noms, et adresses des chantiers dans la bdd
                    
print("\nOn renvoie le nom des chantiers ayant une adresse donnée")
Print_condition('''SELECT name 
                    FROM chantiers 
                    WHERE adress = "20 rue des lillas"''') # On renvoie le nom des chantiers ayant une adresse donnée
                    
print("\nOn renvoie toutes les infos du chantier nommé 'Marseille'")
Print_condition('''SELECT * 
                    FROM chantiers 
                    WHERE name = "Marseille"''') # On renvoie toutes les infos du chantier nommé "Marseille"

print("\nOn compte combien de chantiers sont dans la table")            
Print_condition('''SELECT COUNT(*) 
                    FROM chantiers''') # On compte combien de chantiers sont dans la table
 
print("\nOn renvoie tous les chantiers ordonnés par nom")
Print_condition('''SELECT * 
                    FROM chantiers 
                    ORDER BY name''') # On renvoie tous les chantiers ordonnés par nom
                    
print("\nOn renvoie tous les chantiers commençant à une date donnée")
Print_condition('''SELECT * 
                    FROM chantiers 
                    WHERE date_debut = "2018-10-09 08:00:00" ''') # On renvoie tous les chantiers commençant à une date donnée

###################################################### Exemple de requetes sur les ouvriers
                    
print("\nOn renvoie tous les noms et spécialités des ouvriers dans la bdd")
Print_condition('''SELECT name, specialite
                    FROM ouvriers''') # On renvoie tous les noms et spécialités des ouvriers dans la bdd
                    
print("\nOn renvoie tous les noms des ouvriers ayant une spécialité donnée")
Print_condition('''SELECT name 
                    FROM ouvriers 
                    WHERE specialite = "horticulture"''') # On renvoie tous les noms des ouvriers ayant une spécialité donnée
                    
print("\nOn renvoie toutes les infos d'un ouvrier ayant un nom donné")
Print_condition('''SELECT * 
                    FROM ouvriers 
                    WHERE name = "Jean"''') # On renvoie toutes les infos d'un ouvrier ayant un nom donné
                
print("\nOn compte combien d'ouvriers sont dans la table")
Print_condition('''SELECT COUNT(*) 
                    FROM ouvriers 
                    ''') # On compte combien d'ouvriers sont dans la table

print("\nOn renvoie tous les ouvriers triés par noms")
Print_condition('''SELECT * 
                    FROM ouvriers 
                    ORDER BY name''') # On renvoie tous les ouvriers triés par noms
                
####################################################### Exemple de requetes sur les ouvriers/chantiers

print("\nOn renvoie tous les id des ouvriers/chantiers dans la bdd")
Print_condition('''SELECT id_ouvrier, id_chantier 
                    FROM attribution''') 
                
print("\nOn renvoie tous les chantiers de l'ouvrier 1")
Print_condition('''SELECT id_chantier 
                    FROM attribution 
                    WHERE id_ouvrier = 1''') 
                 
print("\nOn renvoie toute la table")    
Print_condition('''SELECT * 
                    FROM attribution''') 
                    
print("\nOn compte le nombre de chantiers où est présent l'ouvrier 1")
Print_condition('''SELECT COUNT(*) 
                    FROM attribution 
                    WHERE id_ouvrier = 1''') 
                    
####################################################### Exemple de requetes couplées sur les tables

print("\nOn renvoie les noms et spécialités des ouvriers étant affectés à des chantiers") 
Print_condition('''SELECT DISTINCT name, specialite
                    FROM ouvriers
                    JOIN attribution
                    ON id = id_ouvrier''')
                
print("\nOn renvoie toutes les informations sur les chantiers d'un ouvrier, sorte de planning en texte")
Print_condition('''SELECT DISTINCT chantiers.id, chantiers.name, chantiers.date_debut, chantiers.date_fin, chantiers.adress
                    FROM chantiers
                    JOIN attribution
                    ON chantiers.id = attribution.id_chantier
                    JOIN ouvriers 
                    ON (attribution.id_ouvrier = ouvriers.id AND ouvriers.name = "Jean") ''')
                    
# print("\nOn renvoie tous les ouvriers à un chantier en particulier")
    
####################################################### Modification d'une ligne d'une des tables

print("\nModification d'une ligne")
Commit_condition('''UPDATE ouvriers 
                    SET name = 'Jeanne' 
                    WHERE id = 1''')
                    
Print_condition('''SELECT * 
                   FROM ouvriers''')

###################################################### Supression de la table entière

# On supprime les table
cursor.execute('''DROP TABLE IF EXISTS attribution''')
cursor.execute('''DROP TABLE IF EXISTS chantiers''')
cursor.execute('''DROP TABLE IF EXISTS ouvriers''')