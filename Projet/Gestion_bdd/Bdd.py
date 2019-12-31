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
    "Bdd_principale", check_same_thread=False
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
    Permet d'inserer un nouveau chantier dans la base de données.
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
    Permet d'inserer un ouvrier dans la base de données.
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
):  # new_attribution = ["id_ouvrier","id_chantier"]
    """
    Permet d'inserer un couple d'id_ouvrier/id_chantier dans la base de données.
    """
    ouvriers_disponible = select_condition(
        """SELECT id
                     FROM ouvriers
                     WHERE statut = """
        + str(DISPONIBLE)
    )
    if [
            int(new_attribution[0])
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
