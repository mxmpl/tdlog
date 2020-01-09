############################%%

"""
Projet TDLOG réalisé par Maxime BRISINGER, Margot COSSON, Raphael LASRY et
Maxime POLI, 2019-2020

Le but de ce script python est de traiter les bases de données
(chantiers et ouvriers principalement).

Fichier conforme à la norme PEP8.
"""

############################%% Import des bibliothèques utiles

import sqlite3

############################%% Création des bases de données

DB = sqlite3.connect("bdd", check_same_thread=False)
# La base de données avec 3 tables
# (informations sur les chantiers, ouvriers et attributions)
CURSOR = DB.cursor()  # On se place sur cette bdd

CURSOR.execute(
    """CREATE TABLE IF NOT EXISTS chantiers(id_chantier INTEGER PRIMARY KEY,
                                                    name_chantier TEXT,
                                                    start TEXT,
                                                    end TEXT,
                                                    adress TEXT)"""
)
# La table possède 4 arguments, la clef primaire, le nom du chantier,
# Le jour de début du chantier, le jour de sa fin,
# Ainsi que l'adresse du chantier

CURSOR.execute(
    """CREATE TABLE IF NOT EXISTS ouvriers(id_ouvrier INTEGER PRIMARY KEY,
                                                    name_ouvrier TEXT
                                                    )"""
)

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

############################%% Fonctions

################%% REQUEST


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
    de la base de données. A supprimer à la fin du projet en meme temps que
    le fichier python exemples.
    """
    commit_condition(command)
    rows = CURSOR.fetchall()
    for row in rows:
        print(list(row[:]))


###############%% SET & DEL


def insert_chantier(new_chantier: dict):
    """
    Permet d'inserer un nouveau chantier dans la base de données. Le format d'entrée
    doit être un dictionnaire de la forme
    {"name_chantier": text, "start": text, "end": text, "adress": text}.
    """
    CURSOR.execute(
        """INSERT INTO chantiers(name_chantier, start, end, adress)
                      VALUES(?,?,?,?)""",
        (
            new_chantier["name_chantier"],
            new_chantier["start"],
            new_chantier["end"],
            new_chantier["adress"],
        ),
    )
    DB.commit()

def del_chantier(id_chan: int):
    """
    Permet de supprimer un chantier de la table chantiers à partir de son id.
    """
    commit_condition(
        """DELETE FROM chantiers
                    WHERE id_chantier = """
        + str(id_chan)
    )


def insert_ouvrier(new_ouvrier: dict):
    """
    Permet d'inserer un nouveau ouvrier dans la base de données. Le format d'entrée
    doit être un dictionnaire de la forme
    {"name_ouvrier": text}.
    """
    CURSOR.execute(
        """INSERT INTO ouvriers(name_ouvrier)
                      VALUES(?)""",
        (new_ouvrier["name_ouvrier"],),
    )
    DB.commit()

def del_ouvrier(id_ouv: int):
    """
    Permet de supprimer un ouvrier de la table ouvriers à partir de son id.
    """
    commit_condition(
        """DELETE FROM ouvriers
                    WHERE id_ouvrier = """
        + str(id_ouv)
    )


def insert_attribution(new_attribution: dict):
    """
    Permet d'inserer un couple d'id_ouvrier/id_chantier dans la base de données.
    Format d'entrée : new_attribution = {"id_ouvrier": int, "id_chantier": int}
    """
    CURSOR.execute(
        """INSERT INTO attribution(id_ouvrier, id_chantier) VALUES(?,?)""",
        (new_attribution["id_ouvrier"], new_attribution["id_chantier"]),
    )
    DB.commit()

def del_attribution(id_ouv: int, id_chan: int):
    """
    Permet de supprimer une attribution de la table attribution à partir d'un
    couple d'id_ouvrier/id_chantier.
    """
    commit_condition(
        """DELETE FROM attribution
                    WHERE id_ouvrier = """
        + str(id_ouv)
        + """ AND id_chantier = """
        + str(id_chan)
    )

###############%% CHECK
    
def id_in_table(name_table: str, id_ouv = False, id_chant = False): 
    """
    Pour savoir si un identifiant est dans la table.
    """
    if id_ouv != False and id_chant != False: # On veut alors vérifier une attribution
        commande = "id_ouvrier IN " + str(id_ouv) + " AND id_chantier = " + str(id_chant)
    elif id_ouv == False: # On veut alors vérifier l'indice d'un chantier
        commande = "id_chantier IN " + str(id_chant)
    else: # On veut alors vérifier l'indice d'un ouvrier
        commande = "id_ouvrier IN " + str(id_ouv)
        print(""" SELECT * FROM """ + '"' + name_table + '"' + """ WHERE EXISTS (
                                    SELECT * 
                                    FROM """ + '"' + name_table + '"' +
                                    """ WHERE """ + commande + ')')
#    return commit_condition(""" SELECT COUNT(*) FROM """ + '"' + name_table + '"' + """ WHERE """ + commande)
        return commit_condition(""" SELECT COUNT(*) FROM ouvriers WHERE id_ouvrier IN ('1')""")

###############%% MODIFY


def modify_name_ouvrier(id_ouv: int, new_name: str):
    """
    Permet de modifier le nom d'un ouvrier.
    """
    commit_condition(
        """ UPDATE ouvriers
                    SET name_ouvrier = """
        + '"'
        + new_name
        + '"'
        + """ WHERE id_ouvrier = """
        + str(id_ouv)
    )


def modify_name_chantier(id_chan: int, new_name: str):
    """
    Permet de modifier le nom d'un chantier.
    """
    commit_condition(
        """ UPDATE chantiers
                    SET name_chantier = """
        + '"'
        + new_name
        + '"'
        + """ WHERE id_chantier = """
        + str(id_chan)
    )


###############%% GET


def get_info_from_id_chantier(id_chan: int):
    """
    Récupère toutes les informations d'un chantier à partir de son identifiant.
    Renvoie un dictionnaire de la forme
    {"id_chantier": int, "name_chantier": text, "start": text, "end": text, "adress": text}.
    """
    information = select_condition(
        """SELECT *
                                                FROM chantiers
                                                WHERE id_chantier = """
        + str(id_chan)
    )[0]
    return {
        "id_chantier": information[0],
        "name_chantier": information[1],
        "start": information[2],
        "end": information[3],
        "adress": information[4],
    }


def get_info_from_id_ouvrier(id_ouv: int):
    """
    Récupère toutes les informations d'un ouvrier à partir de son identifiant.
    Renvoie un dictionnaire de la forme
    {"id_ouvrier": int, "name_ouvrier": text}.
    """
    information = select_condition(
        """SELECT *
                                                FROM ouvriers
                                                WHERE id_ouvrier = """
        + str(id_ouv)
    )[0]
    return {"id_ouvrier": information[0], "name_ouvrier": information[1]}


def get_all_attribution():
    """
    Renvoie toutes les attributions et les informations sur les ouvriers et
    les chantiers correspondantes sous la forme d'une liste de dictionnaires
    telle que [{"id_ouvrier": int, "name_ouvrier": text, "id_chantier": int,
    "name_chantier": text, "start": text, "end": text, "adress": text},]
    """
    attributions = select_condition(
        """ SELECT *
                                                FROM attribution """
    )
    liste_attribution = []
    for attribution in attributions:
        dict_attribution = get_info_from_id_ouvrier(attribution[0])
        dict_chantier = get_info_from_id_chantier(attribution[1])
        dict_attribution.update(dict_chantier)
        liste_attribution.append(dict_attribution)
    return liste_attribution


def get_list_of_names_chantiers():
    """
    Renvoie la liste des noms des chantiers telle que ["chantier1", "chantier2", ...]
    """
    list_of_list_names = select_condition("""SELECT name_chantier FROM chantiers""")
    names = []
    for list_names in list_of_list_names:
        names.append(list_names[0])
    return names


def get_planning_individuel(id_ouv: int):
    """
    Renvoie toutes les attributions d'un ouvrier (à partir de son index) sous
    la forme d'une liste de dictionnaires telle que
    [{"id_chantier": int, "name_chantier": text, "start": text, "end": text,
    "adress": text},]
    """
    attributions = select_condition(
        """SELECT DISTINCT c.id_chantier
                            FROM chantiers AS c
                            JOIN attribution
                            ON c.id_chantier = attribution.id_chantier
                            WHERE attribution.id_ouvrier = """
        + str(id_ouv)
    )
    liste_attribution = []
    for attribution in attributions:
        liste_attribution.append(get_info_from_id_chantier(attribution[0]))
    return liste_attribution


def return_table_chantier():
    """
    Renvoie toute la table chantiers sous forme d'une liste de dictionnaire :
    [{"id_chantier": int, "name_chantier": text, "start": text, "end": text, "adress": text},].
    """
    informations = select_condition(
        """SELECT *
                    FROM chantiers"""
    )
    table_chantier = []
    for information in informations:
        table_chantier.append(
            {
                "id_chantier": information[0],
                "name_chantier": information[1],
                "start": information[2],
                "end": information[3],
                "adress": information[4],
            }
        )
    return table_chantier


def return_table_ouvrier():
    """
    Renvoie toute la table ouvriers sous forme d'une liste de dictionnaire :
    [{"id_ouvrier": int, "name_ouvrier": text},].
    """
    informations = select_condition(
        """SELECT *
                    FROM ouvriers"""
    )
    table_ouvrier = []
    for information in informations:
        table_ouvrier.append(
            {"id_ouvrier": information[0], "name_ouvrier": information[1]}
        )
    return table_ouvrier


def return_table_attribution():
    """
    Renvoie toute la table attribution sous forme d'une liste de dictionnaire :
    [{"id_ouvrier": int, "id_chantier": text},].
    """
    informations = select_condition(
        """SELECT *
                    FROM attribution"""
    )
    table_attribution = []
    for information in informations:
        table_attribution.append(
            {"id_ouvrier": information[0], "id_chantier": information[1]}
        )
    return table_attribution


###############%% RESET & SUPRESS


def suppression_table(name_table: str):
    """
    Supprime la table, attention ne la reset pas seulement.
    """
    commit_condition("""DROP TABLE IF EXISTS """ + name_table)


def reset_table(name_table: str):
    """
    Reset la table, attention ne la supprime pas.
    """
    commit_condition("""DELETE FROM """ + name_table)


reset_table("chantiers")
reset_table("ouvriers")
reset_table("attribution")

#############################%% BDD provisoire, à effacer dans le futur

CHANTIER = {
    "name_chantier": "Paris",
    "start": "2016-10-09 08:00:00",
    "end": "2016-10-09 12:00:00",
    "adress": "20 rue des lillas",
}

insert_chantier(CHANTIER)

CHANTIER = {
    "name_chantier": "Marseille",
    "start": "2018-10-09 08:00:00",
    "end": "2018-10-09 12:00:00",
    "adress": "20 rue des lillas",
}

insert_chantier(CHANTIER)

CHANTIER = {
    "name_chantier": "Noisy",
    "start": "2020-01-09 08:00:00",
    "end": "2020-01-11 12:00:00",
    "adress": "6-8 Avenue Blaise Pascal",
}

insert_chantier(CHANTIER)

OUVRIER = {"name_ouvrier": "Leo"}

insert_ouvrier(OUVRIER)

OUVRIER = {"name_ouvrier": "Margot"}

insert_ouvrier(OUVRIER)

OUVRIER = {"name_ouvrier": "Raphael"}

insert_ouvrier(OUVRIER)

ATTRIBUTION = {"id_ouvrier": 1, "id_chantier": 3}

insert_attribution(ATTRIBUTION)

ATTRIBUTION = {"id_ouvrier": 1, "id_chantier": 2}

insert_attribution(ATTRIBUTION)

ATTRIBUTION = {"id_ouvrier": 2, "id_chantier": 2}

insert_attribution(ATTRIBUTION)

ATTRIBUTION = {"id_ouvrier": 3, "id_chantier": 1}

insert_attribution(ATTRIBUTION)
###############%%

#print(return_table_chantier())
# modify_name_chantier(1, "St-Maur")
# print(return_table_chantier())
