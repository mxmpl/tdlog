"""
Fonctions Delete et Modify du back-end.
@author: Maxime Brisinger, Margot Cosson, Raphaël Lasry, Maxime Poli
"""

import sys
sys.path.append("..")
from Gestion_bdd import bdd
from Gestion_bdd import exception as ex

def del_data(name_table: str, id_ouv=None, id_chant=None):
    """
    Permet de supprimer un élément de la table à partir de son id.
    """
    if bdd.id_in_table(name_table, id_ouv=id_ouv, id_chant=id_chant):
        bdd.del_data(name_table, id_ouv=id_ouv, id_chant=id_chant)
        return
    raise ex.invalid_id(msg = "Il n'est pas possible de supprimer la donnée correspondante à cet/ces identifiant(s) car elle n'existe pas.")

def delete_chantier(name_chantier: str):
    """
    Permet de supprimer un chantier au sens du nom.
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
    # Gestion d'erreur à faire : vérifier que champs est bien un champs
    bdd.modify_data(name_table, champs, value, id_ouv, id_chant)

