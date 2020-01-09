class wrong_type(Exception): 
    """
    Ce n'est pas le bon type d'argument.
    """
    pass

class missing_or_bad_key(Exception): 
    """
    Clef manquante dans un dictionnaire.
    """
    pass

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

def conformite_dict(dictionnaire: dict, champs):
    """
    champs doit être un dictionnaire des types des values du 
    dictionnaire telle que {"name" : str, "id" : int,}
    """
    if type(dictionnaire) != dict:
        raise wrong_type
    for clef in champs.keys():
        if clef not in dictionnaire.keys(): 
            raise missing_or_bad_key
        elif type(dictionnaire[clef]) != champs[clef]:
            raise wrong_type

#if __name__ == '__main__':
#    dico = {"name" : "Marcel", "age" : 20}
#    liste = [1,2,3]
#    champs = {"name" : str, "age": int}
#    conformite_dict(liste,champs)
    

"""à faire : faire exception quand on essaye de get dans une table vide"""