from Bdd import * 
############################ Remplissage des bases de données 

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

OUVRIER = ["Jean", "horticulture", DISPONIBLE]

insert_ouvrier(OUVRIER)

OUVRIER = ["Lucie", "fleuriste", INDISPONIBLE]

insert_ouvrier(OUVRIER)

OUVRIER = ["Marcel", "élagueur", DISPONIBLE]

insert_ouvrier(OUVRIER)

OUVRIER = ["Julie", "cheffe de chantier", DISPONIBLE]

insert_ouvrier(OUVRIER)

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
select_condition(
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

# Suppression des tables créées

suppression_table_test()
suppression_table_chantiers()
suppression_table_ouvriers()
suppression_table_attribution()


