############################

"""
Projet TDLOG réalisé par Maxime BRISINGER, Margot COSSON, Raphael LASRY et
Maxime POLI, 2019-2020

Le but de ce script python est de montrer quelques exemples de requetes SQL.

Fichier conforme à la norme PEP8.
"""

############################ Modules et fonctions

from bdd import *


############################ Remplissage des bases de données
#
#CHANTIER = {"name_chantier": "Paris", "start": "2016-10-09 08:00:00", "end": "2016-10-09 12:00:00", "adress": "20 rue des lillas"}
#
#insert_chantier(CHANTIER)
#
#CHANTIER = {"name_chantier": "Marseille", "start": "2018-10-09 08:00:00", "end": "2018-10-09 12:00:00", "adress": "20 rue des lillas"}
#
#insert_chantier(CHANTIER)
#
#CHANTIER = {"name_chantier": "Noisy", "start": "2019-12-09 08:00:00", "end": "2020-02-09 12:00:00", "adress": "6-8 Avenue Blaise Pascal"}
#
#insert_chantier(CHANTIER)
#
#OUVRIER = {"name_ouvrier" :"Maxime"}
#
#insert_ouvrier(OUVRIER)
#
#OUVRIER = {"name_ouvrier" :"Margot"}
#
#insert_ouvrier(OUVRIER)
#
#OUVRIER = {"name_ouvrier" :"Raphael"}
#
#insert_ouvrier(OUVRIER)
#
#ATTRIBUTION = {"id_ouvrier": 1, "id_chantier": 2}
#
#insert_attribution(ATTRIBUTION)
#
#ATTRIBUTION = {"id_ouvrier": 2, "id_chantier": 1}
#
#insert_attribution(ATTRIBUTION)
#
#ATTRIBUTION = {"id_ouvrier": 3, "id_chantier": 1}
#
#insert_attribution(ATTRIBUTION)
#
#ATTRIBUTION = {"id_ouvrier": 1, "id_chantier": 3}
#
#insert_attribution(ATTRIBUTION)

############################ Exemple de requetes sur les chantiers

#print("On retourne les tables")
#print(return_table("ouvriers"))
#print(return_table("chantiers"))
#print(return_table("attribution"))
#
#print("get_info_from_id_chantier", get_info_from_id_chantier(1))
#print("get_info_from_id_ouvrier", get_info_from_id_ouvrier(1))
#print("get_all_attribution", get_all_attribution())
#print("get_list_of_names_chantiers", get_list_of_names_chantiers())
#print("get_planning_individuel", get_planning_individuel(2))
#
#
#reset_table("chantiers")
#reset_table("ouvriers")
#reset_table("attribution")

print(id_in_table("ouvriers", id_ouv = 1))
