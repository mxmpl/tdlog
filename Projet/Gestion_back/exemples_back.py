############# Import des bibliothèques utiles
import sys
sys.path.append("..")
from Gestion_bdd import bdd
from back_prototype_bdd import *

print(bdd.return_table_attribution())
set_new_attribution_id({1:2})
print(bdd.return_table_attribution())