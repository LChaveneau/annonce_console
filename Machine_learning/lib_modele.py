"""Description.

Création et optimisation de modèle.
La librairie sklearn est utilisé 
Les modèles à optimiser et à construire doivent être remplis dans le document modele.yaml ou modele.json
"""

from typing import List
from dataclasses import dataclass
from serde import deserialize, serialize
from serde.json import from_json
from serde.yaml import from_yaml
import yaml
import modele as mod
import re
from rich.table import Table
import warnings
import pickle
from pathlib import Path


@serialize
@deserialize
@dataclass
class Modele:
    """Stockage d'un modèle"""
    modele: str
    parametre: dict


def entraine_modeles(data, extension="json"):
    """
    Construit les modèles depuis un fichier .json ou .yaml présent dans le dossier modele.
    Renvoie un yaml des modèles, leurs paramètres optimaux, et leurs erreurs
    """
    modeles = _traite_fichier_(extension)
    for modele in modeles:
        with open(
            Path(".").resolve() / "modele\\modele_optimise.yaml", "a", encoding="utf-8"
        ) as f:
            resultats = _optimise_et_build_(modele, data)
            yaml.dump(resultats, f, sort_keys=False)
    print("Construction et optimisation des modèles terminée !")


def _traite_fichier_(extension):
    """Créer la liste des modeles à créer et optimiser"""
    if extension == "json":
        with open(
            Path(".").resolve() / "modele\\modele.json", "r", encoding="utf-8"
        ) as fichier:
            entree = fichier.read()
        modeles = from_json(List[Modele], entree)
    elif extension == "yaml":
        with open(
            Path(".").resolve() / "modele\\modele.yaml", "r", encoding="utf-8"
        ) as fichier:
            entree = fichier.read()
        modeles = from_yaml(List[Modele], entree)
    return modeles


def _optimise_et_build_(modele, data):
    """Envoie un modele et la base de données au module modele.py
    Cette fonction renvoie des métriques sur ce modèle et si besoin, les paramètres optimisés."""
    parametre_opti, error, mse, mse_tr = mod._renvoie_apprentissage_(
        modele.modele, modele.parametre, data
    )
    return [
        {
            "modele": modele.modele,
            "parametre": parametre_opti,
            "error": error,
            "mse": mse,
            "mse_tr": mse_tr,
        }
    ]


def load_resultats(path_to_file):
    """
    Upload les résultats de l'étape construction et optimisation des modèles.
    Vous devez indiqué le path du dossier des stockages des modèles entrainés.
    Le dossier doit être un yaml intitulé 'modele_optimise'. Ce processus est automatisé si vous êtes passés par la fonction entraine_modeles().
    """
    with open(path_to_file + "modele_optimise.yaml", "r", encoding="utf-8") as f:
        entree = f.read()
    modeles = from_yaml(List[Metrics], entree)
    return modeles


@serialize
@deserialize
@dataclass
class Metrics:
    """Classe qui sert de stockage aux métriques et aux paramètres d'un modèle fitted."""

    modele: str
    parametre: dict
    error: float
    mse: float
    mse_tr: float

    def presente_parametre(self):
        """Renvoi un string des paramètres pour la présentation sous forme de tableau"""
        output = ""
        if self.parametre:
            for parametre in self.parametre.keys():
                output += f"{parametre} = {self.parametre[parametre]}\n"
        return output


def modele_accepte():
    """Fonction indiquant les modèles gérés par le module."""
    for modele in mod.MODELE_ACCEPTE.keys():
        print(modele)


def get_params(modele: str, description: bool = False):
    """Fonction retournant les paramètres d'un modèle.
    L'argument modele doit être un str présent dans modele_accepte()
    """
    if modele != "AdaBoostDecisionTreeRegressor":
        if not description:
            return mod.MODELE_ACCEPTE[modele].get_params()
        else:
            motif = re.compile("([\s\S]+)\n\n\s+Attributes\n.*?")
            doc, *_ = motif.findall(mod.MODELE_ACCEPTE[modele].__doc__)
            return print(doc)
    else:
        if not description:
            dicte_ada = mod.MODELE_ACCEPTE[modele].get_params()
            del dicte_ada["base_estimator"]
            for parametre in (
                mod.MODELE_ACCEPTE["DecisionTreeRegressor"].get_params().keys()
            ):
                dicte_ada["base_estimator__" + parametre] = mod.MODELE_ACCEPTE[
                    "DecisionTreeRegressor"
                ].get_params()[parametre]
            return dicte_ada
        else:
            motif = re.compile("([\s\S]+)\n\n\s+Attributes\n.*?")
            doc_ada, *_ = motif.findall(mod.MODELE_ACCEPTE[modele].__doc__)
            doc_tree, *_ = motif.findall(
                mod.MODELE_ACCEPTE["DecisionTreeRegressor"].__doc__
            )
            return print(
                f"Doc pour le Boosting: \n{doc_ada}\n-------------------------------\nDoc pour l'arbre de régression: \nMerci de rajouter 'base_estimator__' avant d'entrer un paramètre de l'arbre de régression \n{doc_tree}"
            )


def presente_resultats(resultats: List[Metrics]):
    """Présente sous forme de tableau les résultats de la construction et optimisation des modèles"""
    tableau = Table(title="Résultats et paramètres optimaux des modèles")
    tableau.add_column("Modèle")
    tableau.add_column("Paramètre")
    tableau.add_column("Error by CV")
    tableau.add_column("MSE by CV")
    tableau.add_column("train MSE")
    for metrics in resultats:
        tableau.add_row(
            metrics.modele,
            metrics.presente_parametre(),
            str(round(metrics.error, 3)),
            str(round(metrics.mse)),
            str(round(metrics.mse_tr)),
        )
    return tableau


def traite_NA_data(data):
    """
    Traite les valeurs manquantes de la base de données
    Traitement simple :
        - NaN de la variable memoire sont remplacés par la valeur de la fréquence max de leurs catégories console
        - NaN de la variable manette sont remplacés par oui.
    """
    warnings.filterwarnings("ignore")
    gg = data.memoire.isna()

    def valeur_freq_max(element):
        frequence_max = (
            data.loc[~gg]
            .loc[data.console == element]
            .groupby(data.memoire)
            .size()
            .max()
        )
        for valeur in (
            data.loc[~gg]
            .loc[data.console == element]
            .groupby(data.memoire)
            .size()
            .keys()
        ):
            if (
                data.loc[~gg]
                .loc[data.console == element]
                .groupby(data.memoire)
                .size()[valeur]
                == frequence_max
            ):
                return valeur

    for element in data.console[data.memoire.isna()].value_counts().keys():
        for ligne in data.memoire[data.memoire.isna()][data.console == element].keys():
            data.memoire.iloc[ligne] = valeur_freq_max(element)
    cond = data.manette.isna()
    data.manette.loc[cond] = "oui"
    return data


def meilleur_modele(resultats: List[Metrics], by: str = "error") -> Modele:
    """
    Renvoie le meilleur modèle, parmis une liste de Metrics, selon une métrique.
    L'argument by prend comme argument 'error' ou 'mse'
    """
    max_intermediaire = float("inf")
    min_intermediaire = -float("inf")
    for resultat in resultats:
        if by == "error":
            if resultat.error > min_intermediaire:
                min_intermediaire = resultat.error
                meilleur_modele = Modele(
                    modele=resultat.modele, parametre=resultat.parametre
                )
        elif by == "mse":
            if resultat.mse < max_intermediaire:
                max_intermediaire = resultat.mse
                meilleur_modele = Modele(
                    modele=resultat.modele, parametre=resultat.parametre
                )
        else:
            raise ValueError("L'argument by prend comme entrée 'error' ou 'mse'.")
    return meilleur_modele


def construit_meilleur_modele(modele: Modele, data):
    """Construit un modèle depuis la class Modele.
    Les paramètres doivent être unique."""
    return mod.construit_meilleur_modele(modele.modele, modele.parametre, data)


def upload_modele(algo, path_to_file):
    """Enregistre un fitted modèle scikit-learn dans le dossier modèle_final et créer un txt contenant le script a lancer pour importer le modèle et les modules associés. A l'éxécution de ce script le modèle sera contenu dans une variable MODELE.
    """
    pickle.dump(algo, open(path_to_file + r"\modele_final\\fitted_modele.sav", "wb"))
    docstring = algo.__doc__
    motif = re.compile(">>>.*(from sklearn\..*?)\n")
    doc, *_ = motif.findall(docstring)
    with open(path_to_file + r"\modele_final\\script.txt", "w") as fichier:
        fichier.write(doc + "\n")
        fichier.write("import numpy as np\n")
        fichier.write(
            f"import pickle\nMODELE = pickle.load(open(r'{path_to_file}' + r'\modele_final\\fitted_modele.sav', 'rb'))"
        )
