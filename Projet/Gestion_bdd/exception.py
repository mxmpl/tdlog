class wrong_type(Exception): 
    """
    Ce n'est pas le bon type d'argument.
    """
    def __init__(self, typ, msg=None): 
        if msg is None:
            # Set some default useful message
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
            # Set some default useful message
            msg = "La clef {} est manquante.".format(key)
        self.msg = msg
    def __str__(self):
        return self.msg

class invalid_id(Exception): 
    """
    L'identifiant est incorrect.
    """
    pass

class id_ouvrier_not_available_for_assignation(Exception): 
    """
    L'ouvrier est indisponible.
    """
    pass

class invalid_dates(Exception):
    """
    Date invalide.
    """
    pass

class overlimit_date(Exception): 
    """
    Durée supérieure à la durée limite imposée.
    """
    def __str__(self):
        return "Invalid date"

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

if __name__ == '__main__':
    dico = {"name" : "Marcel", "age" : 20}
    liste = [1,2,3]
    champs = {"name" : str, "age": int}
    conformite_dict(dico, champs)
    

"""à faire : faire exception quand on essaye de get dans une table vide"""