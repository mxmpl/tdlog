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
import doctest

############################ Création des bases de données

DB = sqlite3.connect(
    "Bdd_principale"
)  
# La base de données avec 3 tables 
# (informations sur les chantiers, ouvriers et attributions)
CURSOR = DB.cursor()  # On se place sur cette bdd

CURSOR.execute(
    """CREATE TABLE IF NOT EXISTS test(id INTEGER PRIMARY KEY,
                                                    name TEXT,
                                                    data TEXT)"""
)

# La table test va nous permettre d'effectuer des test sur nos requetes

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

############################ Requetes


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


############################ Ajout d'un nouveau test à notre base de données


def insert_test(new_test: list):
    """
    Permet d'inserer un nouveau test dans la base de données.
    """
    CURSOR.execute(
        """INSERT INTO test(name, data)
                      VALUES(?,?)""",
        (new_test[0], new_test[1]),
    )


TEST = ["Margot COSSON", "Test pour vérifier la fonction insert_condition"]

insert_test(TEST)

TEST = ["Maxime BRISINGER", "Test pour vérifier la fonction select_condition"]

insert_test(TEST)

TEST = ["Maxime POLI", "Test pour vérifier la fonction print_condition"]

insert_test(TEST)

############################ Test des fonctions


def test_insert():
    """
    On va tester ici la fonction insert_test.

    >>> test_insert()
    True
    """
    nombre_elements_initial = select_condition(
        """SELECT COUNT(*)
                                                            FROM test"""
    )
    test = ["Nom", "Donnée"]
    insert_test(test)
    nombre_elements_final = select_condition(
        """SELECT COUNT(*)
                                                        FROM test"""
    )
    return nombre_elements_final[0][0] == nombre_elements_initial[0][0] + 1


test_insert()


def test_select():
    """
    On va tester ici la fonction select_condition.

    >>> test_select()
    True
    """
    donnee = select_condition(
        '''SELECT data
                                        FROM test
                                        WHERE name = "Maxime BRISINGER"'''
    )
    return donnee[0][0] == "Test pour vérifier la fonction select_condition"


test_select()


def test_print():
    """
    On va tester ici la fonction print_condition.

    >>> test_print()
    ['Maxime POLI']
    """
    print_condition(
        """SELECT name
                            FROM test
                            WHERE data like "%print_condition%" """
    )


if __name__ == "__main__":
    doctest.testmod()

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


# CHANTIER = get_data() # A terme pouvoir utiliser cette fct
# Qui crée une liste comme l'exemple de la ligne suivante

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


# OUVRIER = get_data() # A terme pouvoir utiliser cette fct qui crée une liste
# Comme l'exemple de la ligne suivante

OUVRIER = ["Jean", "horticulture", DISPONIBLE]

insert_ouvrier(OUVRIER)

OUVRIER = ["Lucie", "fleuriste", INDISPONIBLE]

insert_ouvrier(OUVRIER)

OUVRIER = ["Marcel", "élagueur", DISPONIBLE]

insert_ouvrier(OUVRIER)

OUVRIER = ["Julie", "cheffe de chantier", DISPONIBLE]

insert_ouvrier(OUVRIER)

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


# new_attribution = get_data() # données à récupérer depuis Python
ATTRIBUTION = [1, 2]

insert_attribution(ATTRIBUTION)

ATTRIBUTION = [4, 1]

insert_attribution(ATTRIBUTION)

ATTRIBUTION = [3, 1]  # Attribution impossible (ouvrier non disponible)

insert_attribution(ATTRIBUTION)

ATTRIBUTION = [1, 5]

insert_attribution(ATTRIBUTION)

ATTRIBUTION = [2, 2]

insert_attribution(ATTRIBUTION)

ATTRIBUTION = [3, 3]

insert_attribution(ATTRIBUTION)


DB.commit()

############################ Exemple de requetes sur les chantiers

print("On renvoie tous les noms, et adresses des chantiers dans la bdd")
print_condition(
    """SELECT name, adress
                    FROM chantiers"""
)  # On renvoie tous les noms, et adresses des chantiers dans la bdd

print("\nOn renvoie le nom des chantiers ayant une adresse donnée")
print_condition(
    '''SELECT name
                    FROM chantiers
                    WHERE adress = "20 rue des lillas"'''
)  # On renvoie le nom des chantiers ayant une adresse donnée

print("\nOn renvoie toutes les infos du chantier nommé 'Marseille'")
print_condition(
    '''SELECT *
                    FROM chantiers
                    WHERE name = "Marseille"'''
)  # On renvoie toutes les infos du chantier nommé "Marseille"

print("\nOn compte combien de chantiers sont dans la table")
print_condition(
    """SELECT COUNT(*)
                    FROM chantiers"""
)  # On compte combien de chantiers sont dans la table

print("\nOn renvoie tous les chantiers ordonnés par nom")
print_condition(
    """SELECT *
                    FROM chantiers
                    ORDER BY name"""
)  # On renvoie tous les chantiers ordonnés par nom

print("\nOn renvoie tous les chantiers commençant à une date donnée")
print_condition(
    """SELECT *
                    FROM chantiers
                    WHERE date_debut = "2018-10-09 08:00:00" """
)  # On renvoie tous les chantiers commençant à une date donnée

############################ Exemple de requetes sur les ouvriers

print("\nOn renvoie tous les noms et spécialités des ouvriers dans la bdd")
print_condition(
    """SELECT name, specialite
                    FROM ouvriers"""
)  # On renvoie tous les noms et spécialités des ouvriers dans la bdd

print("\nOn renvoie tous les noms des ouvriers ayant une spécialité donnée")
print_condition(
    '''SELECT name
                    FROM ouvriers
                    WHERE specialite = "horticulture"'''
)  # On renvoie tous les noms des ouvriers ayant une spécialité donnée

print("\nOn renvoie toutes les infos d'un ouvrier ayant un nom donné")
print_condition(
    '''SELECT *
                    FROM ouvriers
                    WHERE name = "Jean"'''
)  # On renvoie toutes les infos d'un ouvrier ayant un nom donné

print("\nOn compte combien d'ouvriers sont dans la table")
print_condition(
    """SELECT COUNT(*)
                    FROM ouvriers
                    """
)  # On compte combien d'ouvriers sont dans la table

print("\nOn renvoie tous les ouvriers triés par noms")
print_condition(
    """SELECT *
                    FROM ouvriers
                    ORDER BY name"""
)  # On renvoie tous les ouvriers triés par noms

############################ Exemple de requetes sur les ouvriers/chantiers

print("\nOn renvoie tous les id des ouvriers/chantiers dans la bdd")
print_condition(
    """SELECT id_ouvrier, id_chantier
                    FROM attribution"""
)

print("\nOn renvoie tous les chantiers de l'ouvrier 1")
print_condition(
    """SELECT id_chantier
                    FROM attribution
                    WHERE id_ouvrier = 1"""
)

print("\nOn renvoie toute la table")
print_condition(
    """SELECT *
                    FROM attribution"""
)

print("\nOn compte le nombre de chantiers où est présent l'ouvrier 1")
print_condition(
    """SELECT COUNT(*)
                    FROM attribution
                    WHERE id_ouvrier = 1"""
)

############################ Exemple de requetes couplées sur les tables

print(
    "\nOn renvoie les noms et spécialités des ouvriers étant affectés à des chantiers"
)
print_condition(
    """SELECT DISTINCT name, specialite
                    FROM ouvriers
                    JOIN attribution
                    ON id = id_ouvrier"""
)

print(
    "\nOn renvoie toutes les informations sur les chantiers d'un ouvrier, ",
    "sorte de planning en texte",
)
print_condition(
    """SELECT DISTINCT chantiers.id,
                    chantiers.name,
                    chantiers.date_debut,
                    chantiers.date_fin,
                    chantiers.adress
                    FROM chantiers
                    JOIN attribution
                    ON chantiers.id = attribution.id_chantier
                    JOIN ouvriers
                    ON (attribution.id_ouvrier = ouvriers.id
                    AND
                    ouvriers.name = "Jean") """
)

print(
    "\nOn renvoie toutes les informations sur les chantiers de tous les ouvrier, ",
    "sorte de planning en texte",
)
print_condition(
    """SELECT DISTINCT c.name,
                    o.name
                    FROM chantiers AS c, ouvriers AS o
                    JOIN attribution
                    ON c.id = attribution.id_chantier
                    JOIN ouvriers
                    ON (attribution.id_ouvrier = o.id) """
)  # Attention aux alias

# print("\nOn renvoie tous les ouvriers à un chantier en particulier")

############################ Modification d'une ligne d'une des tables

print("\nModification d'une ligne")
commit_condition(
    """UPDATE ouvriers
                    SET name = 'Jeanne'
                    WHERE id = 1"""
)

print_condition(
    """SELECT *
                   FROM ouvriers"""
)

############################ Supression de la table entière

# On supprime les table
CURSOR.execute("""DROP TABLE IF EXISTS attribution""")
CURSOR.execute("""DROP TABLE IF EXISTS chantiers""")
CURSOR.execute("""DROP TABLE IF EXISTS ouvriers""")
CURSOR.execute("""DROP TABLE IF EXISTS test""")
