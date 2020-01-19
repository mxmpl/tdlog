############################

"""
Projet TDLOG réalisé par Maxime BRISINGER, Margot COSSON, Raphael LASRY et
Maxime POLI, 2019-2020

Le but de ce script python est de realiser quelques test sur nos fonctions.

Fichier conforme à la norme PEP8.
"""

############################ Modules et fonctions

import doctest
import sqlite3
from bdd import (
    print_condition,
    select_condition,
)

############################ Creation de la table test

DB = sqlite3.connect("bdd", check_same_thread=False)
CURSOR = DB.cursor()

CURSOR.execute(
    """CREATE TABLE IF NOT EXISTS test(id INTEGER PRIMARY KEY,
                                                    name TEXT,
                                                    data TEXT)"""
)

# La table test va nous permettre d'effectuer des test sur nos requetes
DB.commit()

############################ Remplissage de la table test


def insert_test(new_test: list):
    """
    Permet d'inserer un nouveau test dans la base de données.
    """
    CURSOR.execute(
        """INSERT INTO test(name, data)
                      VALUES(?,?)""",
        (new_test[0], new_test[1]),
    )
    DB.commit()


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


test_print()

############################ Test

if __name__ == "__main__":
    doctest.testmod(verbose=True)

CURSOR.execute("""DROP TABLE IF EXISTS test""")  # Suppression
DB.commit()
