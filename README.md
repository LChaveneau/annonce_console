# Projet webscrapping et machine learning

Le but de ce projet a été de récupérer des données sur les consoles en ventes sur les sites d'occasion pour ainsi créer une machine d'aide à la décision. 
Cette machine d'aide à la décision estime le prix et indique à l'utilisateur comment se situe le prix annoncé pour cette console par rapport au prix prédit.

Chaque utilisation d'une librairie est suivie d'un notebook pour l'aide à l'utilisation.

## TODO 

* Réussir à scrapper le site **leboncoin.fr**.
* Trouver un meilleur algorithme pour estimer le prix d'une annonce.
* Passer à la deuxième étape de la construction de la machine : indication de la position du prix par rapport au prix estimé. 
* Terminer les test des librairies.

## SCRAPPING_LEBONCOIN_FAIL

Ce dossier comprend un bout de code qui tente de rentrer sur le site **leboncoin**, en vain.

## SCRAPPING_EBAY

Ce dossier comprend l'automatisation du scrapping sur la plateforme **ebay**. Les données récupérées dans les annonces de console de jeux vidéo sont stockés dans le document *brute.json*

## Nettoyage_données

Ce dossier comprend *lib_nettoyage.py* qui en premier lieu transforme *brute.json* pour que les données brute soit lisible. Cette transformation est stocké dans le dossier *data* dans le hub sous le nom de *data.json*.

La librairie effectue ensuite le nettoyage et la transformation des données brute. Les données nettoyées sont stockés dans le dossier *data* dans le hub sous le nom *donnees_operationnel.tsv*.

Ce dossier comprend aussi plusieurs *.json* qui sont des documents de stockage des motifs regular expression utilisés lors de la phase de nettoyage

## Machine_learning

La librairie lib_modele.py permet l'automatisation de la création de modèles. Les modèles que l'on veut entrainer et même optimiser doivent être indiquer dans le dossier *modele* et dans le document *modele.json* ou *modele.yaml*. Plusieurs méthodes existent pour savoir quels modèles scikit-learn sont prise en compte dans cette librairie.

Aprés recherche de paramètres optimales et construction des modèles, les résultats sont stockées dans *modele_optimisé.yaml*. Donc à chaque modèles on récupère :

* Les paramètres optimales si demandés.
* Le mean squared error estimé par cross validation
* le score estimé par cross validation
* le mean squared error sur données d'entrainement

Une fonction permet de choisir le meilleur modèle en fonction d'un critère : MSE ou error.

Le modèle choisi est ensuite exporté dans le dossier *modele_finale* sous le nom de *fitted_modele.sav*

Durant ce processus le document *script.txt* est crée. Il contient le script à lancer lors du développement du modèle. 

## app 

Création d'un GUI simple qui prend comme entrée les différents features et renvoie l'estimation du prix. 

Il manque la partie d'aide à la décision

## test

Test des librairies. **NON COMPLET**