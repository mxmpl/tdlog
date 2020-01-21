"""
Script pour la création des exceptions du projet.
@author: Maxime Brisinger, Margot Cosson, Raphaël Lasry, Maxime Poli
"""

class WrongRequest(Exception):
    def __init__(self):
        super().__init__()
        self.msg = "Mauvaise requête"

    def __str__(self):
        return self.msg


class WrongType(WrongRequest):
    """
    Ce n'est pas le bon type d'argument.
    """

    def __init__(self, typ=None, msg=None):
        super().__init__()
        if msg is None:
            if typ is None:
                msg = "Mauvais type."
            else:
                msg = "L'argument n'est pas du type requis : {}".format(typ)
        self.msg = msg

    def __str__(self):
        return self.msg


class MissingBadKey(WrongRequest):
    """
    Clef manquante dans un dictionnaire.
    """

    def __init__(self, key=None, msg=None):
        super().__init__()
        if msg is None:
            if key is None:
                msg = "Clef manquante ou erronée."
            else:
                msg = "La clef {} est manquante ou erronée.".format(key)
        self.msg = msg

    def __str__(self):
        return self.msg


class InvalidId(WrongRequest):
    """
    L'identifiant est incorrect.
    """

    def __init__(self, ide=None, msg=None):
        super().__init__()
        if msg is None:
            if ide is None:
                msg = "L'identifiant est invalide."
            else:
                msg = "L'identifiant {} est invalide.".format(ide)
        self.msg = msg

    def __str__(self):
        return self.msg

class ImpossibleAssignation(WrongRequest):
    """
    L'ouvrier est indisponible.
    """
    def __init__(self, id_ouvrier=None, id_chantier=None, msg=None):
        super().__init__()
        if msg is None:
            if id_ouvrier is None and id_chantier is None:
                msg = "L'assignation n'est pas possible."
            else:
                msg = "L'ouvrier {} n'est pas disponible pour être assigné au chantier {}.".format(
                    id_ouvrier, id_chantier
                )
        self.msg = msg

    def __str__(self):
        return self.msg

class InvalidDates(WrongRequest):
    """
    Date invalide.
    """

    def __init__(self, date=None, msg=None):
        super().__init__()
        if msg is None:
            if date is None:
                msg = "Date invalide"
            else:
                msg = "La date {} n'est pas valide.".format(date)
        self.msg = msg

    def __str__(self):
        return self.msg

class OverlimitDate(WrongRequest):
    """
    Durée supérieure à la durée limite imposée.
    """

    def __init__(self, limite_jours=None, msg=None):
        super().__init__()
        if msg is None:
            if limite_jours is None:
                msg = "La date est postérieure à la limite imposée."
            else:
                msg = "Le chantier dépasse la limite de jours établie à {} jours.".format(
                    limite_jours
                )
        self.msg = msg

    def __str__(self):
        return self.msg

def conformite_dict(dictionnaire: dict, champs: dict):
    """
    champs doit être un dictionnaire des types des values du
    dictionnaire telle que {"name" : str, "id" : int,}
    """
    if not isinstance(dictionnaire, dict):
        raise WrongType(dict)
    for clef in champs.keys():
        if clef not in dictionnaire.keys():
            raise MissingBadKey(clef)
        elif not isinstance(dictionnaire[clef], champs[clef]):
            raise WrongType(type(dictionnaire[clef]))
    return True
