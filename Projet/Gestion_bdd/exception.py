class wrong_type_dict(Exception): 
    pass

class missing_or_bad_key(Exception): 
    pass

class bad_type(Exception): 
    pass

        
def conformite_dict(dictionnaire: dict, champs):
    """
    champs doit être un dictionnaire des types des values du 
    dictionnaire telle que {"name" : str, "id" : int,}
    """
    if type(dictionnaire) != dict:
        raise wrong_type_dict
    for clef in champs.keys():
        if clef not in dictionnaire.keys(): 
            raise missing_or_bad_key
        elif type(dictionnaire[clef]) != champs[clef]:
            raise bad_type

if __name__ == '__main__':
    dico = {"name" : "Marcel", "age" : 20}
    liste = [1,2,3]
    champs = {"name" : str, "age": int}
    conformite_dict(liste,champs)

"""à faire : faire exception quand on essaye de get dans une table vide"""