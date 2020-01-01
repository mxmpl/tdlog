############################

"""
Projet TDLOG réalisé par Maxime BRISINGER, Margot COSSON, Raphael LASRY et
Maxime POLI, 2019-2020

Le but de ce script python est de traiter les bases de données
(chantiers et ouvriers principalement).

Fichier conforme à la norme PEP8.
"""

############################ Import des bibliothèques utiles

import sqlite3

############################ Création des bases de données

DB = sqlite3.connect(
    "bdd_principale", check_same_thread=False
)  
# La base de données avec 3 tables 
# (informations sur les chantiers, ouvriers et attributions)
CURSOR = DB.cursor()  # On se place sur cette bdd

CURSOR.execute(
    """CREATE TABLE IF NOT EXISTS chantiers(id INTEGER PRIMARY KEY,
                                                    name TEXT,
                                                    date_debut SMALLDATETIME,
                                                    date_fin SMALLDATETIME,
                                                    adress TEXT)"""
)
# La table possède 4 arguments, la clef primaire, le nom du chantier,
# Le jour de début du chantier, le jour de sa fin,
# Ainsi que l'adresse du chantier

DISPONIBLE = 0
INDISPONIBLE = 1
appel_bdd = 2 # à supprimer après, c'est un essai 
CURSOR.execute(
    """CREATE TABLE IF NOT EXISTS ouvriers(id INTEGER PRIMARY KEY,
                                                    name TEXT,
                                                    specialite TEXT,
                                                    statut BIT)"""
)  # Statut permet de dire s'il est disponible ou pas
# Avec DISPONIBLE si oui, INDISPONIBLE si non

CURSOR.execute(
    """CREATE TABLE IF NOT EXISTS attribution(id_ouvrier INTEGER,
                                                        id_chantier INTEGER,
                                                        FOREIGN KEY(id_ouvrier)
                                                        REFERENCES ouvriers(id),
                                                        FOREIGN KEY(id_chantier)
                                                        REFERENCES chantiers(id)
                                                        )
                                                        """
)

DB.commit()  # On termine de creer les tables

############################ Fonctions de requetes

def commit_condition(command: str):
    """
    Permet d'executer une commande.
    """
    CURSOR.execute(command)
    DB.commit()


def select_condition(
        command: str
):  # On séléctionne les lignes demandées et on les récupère sous forme de liste
    """
    Permet à partir d'une commande d'enregistrer les informations
    correspondantes de la base de données.
    """
    commit_condition(command)
    rows = CURSOR.fetchall()
    sortie = []  # Permet de ne pas obtenir une liste de tuple en sortie 
    for row in rows:
        sortie.append(list(row[:]))
    return sortie


def print_condition(command: str):
    """
    Permet à partir d'une commande d'afficher les informations correspondantes
    de la base de données.
    """
    commit_condition(command)
    rows = CURSOR.fetchall()
    for row in rows:
        print(list(row[:]))


############################ Ajout d'un nouveau chantier à notre base de données


def insert_chantier(new_chantier: list):
    """
    Permet d'inserer un nouveau chantier dans la base de données. Le format d'entrée 
    doit être de la forme [nom, date_debut, date_fin, adresse]. 
    """
    CURSOR.execute(
        """INSERT INTO chantiers(name, date_debut, date_fin, adress)
                      VALUES(?,?,?,?)""",
        (new_chantier[0], new_chantier[1], new_chantier[2], new_chantier[3]),
    )
    DB.commit()

############################ Ajout d'un nouveau ouvrier à notre base de données


def insert_ouvrier(new_ouvrier: list):
    """
    Permet d'inserer un ouvrier dans la base de données. Le format d'entrée doit 
    être de la forme [nom, specialite, statut]. 
    """
    CURSOR.execute(
        """INSERT INTO ouvriers(name, specialite, statut)
                      VALUES(?,?,?)""",
        (new_ouvrier[0], new_ouvrier[1], new_ouvrier[2]),
    )
    DB.commit()

############################ Ajout d'un nouveau couple à notre base de données


def insert_attribution(
        new_attribution: list
):
    """
    Permet d'inserer un couple d'id_ouvrier/id_chantier dans la base de données.
    Format d'entrée : new_attribution = [id_ouvrier,id_chantier]
    """
    # À FAIRE : un test qui vérifie le format de new_attribution cad [int, int]
    ouvriers_disponible = select_condition(
        """SELECT id
                     FROM ouvriers
                     WHERE statut = """
        + str(DISPONIBLE)
    )
    if [
            new_attribution[0]
    ] in ouvriers_disponible:  
        CURSOR.execute(
            """INSERT INTO attribution(id_ouvrier, id_chantier)
                          VALUES(?,?)""",
            (new_attribution[0], new_attribution[1]),
        )
    else:
        print(
            "Vous ne pouvez pas associer cet ouvrier à ",
            "ce chantier car l'ouvrier n'est pas disponible",
        )
    DB.commit()

############################ Fonctions utiles pour le back 

def get_id_names_dates_chantiers(): 
    """
    Renvoie une liste de listes telles que [index, nom, date_debut, date_fin]
    """
    return select_condition("""SELECT id, name, date_debut, date_fin
                                                FROM chantiers""")
def get_list_of_names_chantiers():
    """
    Renvoie la liste des noms des chantiers telle que ["chantier1", "chantier2", ...]
    """
    list_of_list_names = select_condition("""SELECT name FROM chantiers""")
    names = []
    for list_names in list_of_list_names: 
        names.append(list_names[0])
    return names
    
def get_id_names_ouvriers(): 
    """
    Renvoie une liste de listes telles que [index, nom]
    """
    return select_condition(
        """SELECT id, name FROM ouvriers""") 

def get_all_attribution(): 
    """ 
    Renvoie les attributions sous la forme [nom_chantier, nom_ouvrier]
    """
    return select_condition(
            """SELECT DISTINCT c.name,
                            o.name
                            FROM chantiers AS c, ouvriers AS o
                            JOIN attribution
                            ON c.id = attribution.id_chantier
                            JOIN ouvriers
                            ON (attribution.id_ouvrier = o.id) """
        )

def get_id_from_name_ouvrier(name: str): 
    """
    Renvoie l'id d'un ouvrier avec un nom donné. Le [0][0] permet de renvoyer l'entier 
    directement et non pas une liste. 
    """
    return select_condition(
            """SELECT id
                    FROM ouvriers
                    WHERE name = '""" + name + "'"
        )[0][0]
    
def get_id_from_name_chantier(name :str): 
    """
    Renvoie l'id d'un chantier avec un nom donné. Le [0][0] permet de renvoyer l'entier 
    directement et non pas une liste. 
    """
    return select_condition(
            """SELECT id
                    FROM chantiers
                    WHERE name = '""" + name + "'" 
        )[0][0]
        
def return_table_attribution(): 
    return select_condition(
    """SELECT *
                    FROM attribution"""
                    )
def return_table_ouvriers(): 
    return select_condition(
    """SELECT name
                    FROM ouvriers"""
                    )
    
def return_table_chantiers(): 
    return select_condition(
    """SELECT name
                    FROM chantiers"""
                    )
    
############################ A effacer

CHANTIER = ["Paris", "2016-10-09 08:00:00", "2016-10-09 12:00:00", "20 rue des lillas"]

insert_chantier(CHANTIER)

CHANTIER = [
    "Marseille",
    "2018-10-09 08:00:00",
    "2018-10-09 12:00:00",
    "20 rue des lillas",
]

insert_chantier(CHANTIER)

CHANTIER = [
    "Noisy",
    "2019-12-09 08:00:00",
    "2020-02-09 12:00:00",
    "6-8 Avenue Blaise Pascal",
]

insert_chantier(CHANTIER)

CHANTIER = [
    "Noisy",
    "2019-12-09 08:00:00",
    "2020-02-09 12:00:00",
    "6-8 Avenue Blaise Pascal",
]

insert_chantier(CHANTIER)  # Chantier identique

CHANTIER = ["Paris", "2019-11-21 09:00:00", "2019-12-09 13:00:00", "3 Avenue Foch"]

insert_chantier(CHANTIER)

CHANTIER = [
    "Boulogne",
    "2014-06-25 08:00:00",
    "2021-08-07 12:00:00",
    "70 rue du point du jour",
]

insert_chantier(CHANTIER)

OUVRIER = ["Maxime", "horticulture", DISPONIBLE]

insert_ouvrier(OUVRIER)

OUVRIER = ["Margot", "fleuriste", DISPONIBLE]

insert_ouvrier(OUVRIER)

OUVRIER = ["Raph", "élagueur", DISPONIBLE]

insert_ouvrier(OUVRIER)
    

############################ Supression 
    
def suppression_table_chantiers():
    CURSOR.execute("""DROP TABLE IF EXISTS chantiers""")

def suppression_table_ouvriers():
    CURSOR.execute("""DROP TABLE IF EXISTS ouvriers""")

def suppression_table_attribution():
    CURSOR.execute("""DROP TABLE IF EXISTS attribution""")
    
#suppression_table_chantiers()
#suppression_table_ouvriers()
#suppression_table_attribution()
