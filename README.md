# Projet gestion de planning

Si c'est la première fois que vous lancez le site, exécutez le fichier requirements.py
(installation des bibliothèques python)

Pour lancer le site, exécuter main.py

L'architecture du projet est la suivante :
- Un dossier control avec les fichiers python pour le contrôleur du projet
- Un dossier data avec les fichiers python gérant la base de données
- Un dossier ui contenant les fichiers build du front-end Angular 
- Un dossier front_angular contenant les fichiers de développement Angular permettant de modifier la partie front-end du projet

Pour faire des modifications sur la partie front-end:
- Faire les changements souhaités dans front_angular
- Exécuter la commande 'ng build' avec Angular CLI
- Remplacer le contenu du dossier ui par celui de front_angular/dist

Cette branche contient le dossier prototypes_html avec les prototypes
