from back import *

if __name__ == '__main__': 
    
    #%% On retourne les tables 
    
    print("Table ouvriers")
    print(return_table("ouvriers"))
    print("Table chantiers")
    print(return_table("chantiers"))
    print("Table attribution")
    print(return_table("attribution"))
    
    #%% On insert 
    
    print("\n-----------INSERTIONS------------")
    
    set_new_chantier({
        "name_chantier": "TEST",
        "start": "2020-10-09 08:00:00",
        "end": "2020-10-09 12:00:00",
        "adress": "TEST",
    })
    
    set_new_ouvrier({"name_ouvrier": "TEST"})
    
    set_new_attribution({"id_ouvrier": 1, "id_chantier": 4})
    
    print("Table ouvriers")
    print(return_table("ouvriers"))
    print("Table chantiers")
    print(return_table("chantiers"))
    print("Table attribution")
    print(return_table("attribution"))
    
    #%% On supprime 
    
    print("\n-----------SUPPRESSION------------")
    
    del_data("ouvriers", id_ouv = 4)
    del_data("chantiers", id_chant = 6) 
    del_data("attribution", id_ouv = 1, id_chant = 4)
    
    print("Table ouvriers")
    print(return_table("ouvriers"))
    print("Table chantiers")
    print(return_table("chantiers"))
    print("Table attribution")
    print(return_table("attribution"))
    
    #%% On modifie 
    
    print("\n-----------MODIFICATION------------")
    
    modify_data("chantiers", "name_chantier", "TEST2", id_chant = 1)
    modify_data("ouvriers", "name_ouvrier", "TEST2", id_ouv = 1)
    
    print("Table ouvriers")
    print(return_table("ouvriers"))
    print("Table chantiers")
    print(return_table("chantiers"))
    print("Table attribution")
    print(return_table("attribution"))
    
    #%% On récupère les plannings 
    
    print("\n-----------PLANNINGS------------")
    
    print(get_planning())
    print(get_planning_individuel(1))
    
    #%% On récupère les informations
    
    print("\n-----------GET INFO------------")
    
    print(get_info_from_id_ouvrier(1))
    print(get_info_from_id_chantier(1))
    print(return_cluster_chantiers(1))
    print(return_cluster_chantiers())
    print(resume_chantiers())