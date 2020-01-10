from back import *


#print(return_table_ouvrier_avec_chantiers())


print(return_table("ouvriers"))
#print(get_planning_individuel(1))
#print(return_cluster_chantiers(1))


modify_data("ouvriers", "name_ouvrier", "Max", id_ouv = 1)
print(return_table("ouvriers"))