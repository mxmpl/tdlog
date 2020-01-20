"""
Fonctions Delete et Modify du back-end.
@author: Maxime Brisinger, Margot Cosson, Raphaël Lasry, Maxime Poli
"""

import sys
from get import return_table
sys.path.append("..")
from data import bdd

def del_data(name_table: str, id_ouv=None, id_chant=None):
    """
    Permet de supprimer un élément de la table à partir de son id.
    """
    # On vérifie d'abord que cette donnée existe
    bdd.id_in_table(name_table, id_ouv=id_ouv, id_chant=id_chant)
    bdd.del_data(name_table, id_ouv=id_ouv, id_chant=id_chant)

def delete_chantier(name_chantier: str):
    """
    Permet de supprimer des chantiers (qui correspondent à une demi-journée)
    qui partagent le même nom.
    """
    chantiers = return_table("chantiers")
    attributions = return_table("attribution")
    for chantier in chantiers:
        if chantier["name_chantier"] == name_chantier:
            id_chantier = chantier["id_chantier"]
            for attribution in attributions:
                if attribution["id_chantier"] == id_chantier:
                    del_data(
                        "attribution",
                        id_ouv=attribution["id_ouvrier"],
                        id_chant=attribution["id_chantier"],
                    )
            del_data("chantiers", id_ouv=None, id_chant=id_chantier)

def modify_data(name_table: str, champs: str, value: str, id_ouv=None, id_chant=None):
    """
    Permet de modifier une donnée dans une table.
    """
    bdd.modify_data(name_table, champs, value, id_ouv, id_chant)
