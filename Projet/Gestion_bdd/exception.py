class wrong_type(Exception): 
    """
    Ce n'est pas le bon type d'argument.
    """
    def __init__(self, typ, msg=None): 
        if msg is None:
            msg = "L'argument n'est pas du type requis : {}".format(typ)
        self.msg = msg
    def __str__(self):
        return self.msg

class missing_or_bad_key(Exception): 
    """
    Clef manquante dans un dictionnaire.
    """
    def __init__(self, key, msg=None): 
        if msg is None:
            msg = "La clef {} est manquante.".format(key)
        self.msg = msg
    def __str__(self):
        return self.msg

class invalid_id(Exception): 
    """
    L'identifiant est incorrect.
    """
    def __init__(self, ide=None, msg=None): 
        if msg is None:
            if ide is None:
                msg = "L'identifiant est invalide."
            else:
                msg = "L'identifiant {} est invalide.".format(ide)
        self.msg = msg
    def __str__(self):
        return self.msg

class id_ouvrier_not_available_for_assignation(Exception): 
    """
    L'ouvrier est indisponible.
    """
    def __init__(self, id_ouvrier, id_chantier, msg=None):
        if msg is None:
            msg = "L'ouvrier {} n'est pas disponible pour être assigné au chantier {}.".format(id_ouvrier, id_chantier)
        self.msg = msg
    def __str__(self):
        return self.msg

class invalid_dates(Exception):
    """
    Date invalide.
    """
    def __init__(self, date, msg=None): 
        if msg is None:
            msg = "La date {} n'est pas valide.".format(date)
        self.msg = msg
    def __str__(self):
        return self.msg

class overlimit_date(Exception): 
    """
    Durée supérieure à la durée limite imposée.
    """
    def __init__(self, limite_jours, msg=None): 
        if msg is None:
            msg = "Le chantier dépasse la limite de jours établie à {} jours.".format(limite_jours)
        self.msg = msg
    def __str__(self):
        return self.msg

def conformite_dict(dictionnaire: dict, champs):
    """
    champs doit être un dictionnaire des types des values du 
    dictionnaire telle que {"name" : str, "id" : int,}
    """
    if type(dictionnaire) != dict:
        raise wrong_type(dict)
    for clef in champs.keys():
        if clef not in dictionnaire.keys(): 
            raise missing_or_bad_key(clef)
        elif type(dictionnaire[clef]) != champs[clef]:
            raise wrong_type(type(dictionnaire[clef]))
    return True

if __name__ == '__main__':
    dico = {"name" : "Marcel", "age" : 20}
    liste = [1,2,3]
    champs = {"name" : str, "age": int}
    conformite_dict(dico, champs)
    

"""à faire : faire exception quand on essaye de get dans une table vide"""