"""Nettoyage de brute.json"""

from serde import deserialize, serialize
from serde.json import from_json
import json
from dataclasses import dataclass
import pandas as pd
from typing import List
import re
from rich import print
import warnings


def rend_lisible(dossier):
    """Corrige les erreurs d'encodage de brute.json et le réenregistre."""
    with open(
        dossier + r"\SCRAPPING_EBAY\donnees\\brute.json", "r", encoding="utf-8"
    ) as fichier:
        data = fichier.read()
    data = data.replace("}", "},")
    data = data[:-1]
    data = "[" + data + "]"
    data = data.replace("\u00e9", "é")
    with open(dossier + r"\data\\data.json", "w", encoding="utf8") as fichier:
        fichier.write(data)


def transformation_dataframe(dossier):
    """Transforme data.json en dataframe pandas"""
    with open(dossier + r"\data\\data.json", "r") as fichier:
        data = fichier.read()
    annonces = from_json(List[Annonce], data)
    return pd.DataFrame(annonces)


@serialize
@deserialize
@dataclass
class Annonce:
    """Classe contenant nos observations"""

    id: str
    titre: str
    prix: str
    deli_price: str
    etat: str
    couleur: str
    retour: str
    type: str
    code_region: str
    connectivite: str
    resolution: str
    marque: str
    plateforme: str
    memoire: str
    modele: str
    retour: str
    set_desc: str


def supprime_soublons(data):
    """Supprime les doublons des annonces définit unique par la variable id"""
    return data.drop_duplicates(subset="id", keep="first")


def traite_prix(data):
    """
    Transforme la variable prix en float
    Si le prix n'est pas en euro, il est convertit grâce aux cours actuels de taux d'échange
    """
    newlist = list()
    motif_test = re.compile("(\d+,\d+)(\D+)")
    for prix in data.prix.to_list():
        prix = prix.replace("\xa0", "")
        element, *_ = motif_test.findall(prix)
        prix, devise = element
        prix = float(prix.replace(",", "."))
        if devise.replace(" ", "") == "GBP":
            prix = round(prix * 1.19, 2)
        if devise.replace(" ", "") == "USD":
            prix = round(prix * 0.885, 2)
        newlist.append(prix)
    data.prix = newlist
    return data


def traite_deli_price(data):
    """Convertit en float les prix de livraison"""
    motif = re.compile("(.*?) EUR")
    new_list = list()
    for price in data.deli_price.to_list():
        if type(price) == str:
            try:
                kd, *_ = motif.findall(price)
            except:
                kd = "0"
            kd = kd.replace(",", ".")
            new_list.append(float(kd))
    data.deli_price = new_list
    return data


def traite_retour(data):
    """Transforme la variable retour avec les modalités 'oui ou 'non'"""
    new_list = list()
    for retour in data.retour.to_list():
        element, *_ = retour
        if element == "Retours refusés":
            valeur = "Non"
        else:
            valeur = "Oui"
        new_list.append(valeur)
    data.retour = new_list
    return data


def traite_etat(data):
    """
    Certaines catégories de la variable état sont trés bien codés (affiche vraiment l'état) mais ils ne sont pas beaucoup.
    En effet beaucoup d'annonce sont classés en 'occasion'. Cela n'indique pas un réel etat de l'objet en vente.
    La décision est donc de mettre tout le monde en Occasion (sauf neuf, pour pièce ou reconditionné par le vendeur)
    """
    new_list = list()
    for etat in data.etat.to_list():
        if (
            etat == "Très bon état"
            or etat == "Bon état"
            or etat == "Etat correct"
            or etat == "Comme neuf"
            or etat == "Ouvert (jamais utilisé)"
        ):
            etat = "Occasion"
        new_list.append(etat)
    data.etat = new_list
    return data


def supprime_variables(data):
    """
    Supprime les variables inutiles pour la suite de l'analyse :
        - titre
        - id
        - couleur
        - type
        - code_region
        - connectivite
        - resolution 
        - marque
        - plateforme
        - modele
        - set_desc
    """
    data = data.reset_index(drop=True)
    return data.drop(
        [
            "titre",
            "id",
            "couleur",
            "type",
            "code_region",
            "connectivite",
            "resolution",
            "marque",
            "plateforme",
            "modele",
            "set_desc",
        ],
        axis=1,
    )


def traite_anomalie(data, path_to_file):
    """Nettoie la base de données"""
    data = _anomalie_type_(data, path_to_file)
    data = _anomalie_marque_(data, path_to_file)
    data = _anomalie_plateforme_(data, path_to_file)
    data = _anomalie_modele_(data, path_to_file)
    data = _autre_anomalie_(data)
    return data


def _anomalie_type_(data, path_to_file):
    """Détecte et supprime certaines anomalies de la variable type.
    Les 'None' sont conservés pour un futur traitement"""
    liste_motifs = []
    with open(
        path_to_file + r"\Nettoyage_données\motif\\anomalie_type.json",
        "r",
        encoding="utf-8",
    ) as fichier:
        motifs = fichier.read()
    motifs = json.loads(motifs)
    for motif in motifs:
        liste_motifs.append(re.compile(motif))
    liste_index = list()
    liste_index_none = list()
    i = 0
    for type in data.type.to_list():
        if type:
            type = type.lower()
            type = type.replace(" ", "")
            for motif in liste_motifs:
                if motif.search(type):
                    liste_index.append(i)
                    break
        else:
            liste_index_none.append(i)
        i = i + 1
    return data.iloc[liste_index + liste_index_none]


def _anomalie_marque_(data, path_to_file):
    """Détecte et supprime certaines anomalies de la variable marque.
    Les 'None' sont conservés pour un futur traitement"""
    liste_motifs = []
    with open(
        path_to_file + r"\Nettoyage_données\motif\\anomalie_marque.json",
        "r",
        encoding="utf-8",
    ) as fichier:
        motifs = fichier.read()
    motifs = json.loads(motifs)
    for motif in motifs:
        liste_motifs.append(re.compile(motif))
    liste_index = list()
    liste_index_none = list()
    i = 0
    for marque in data.marque.to_list():
        if marque:
            marque = marque.lower()
            marque = marque.replace(" ", "")
            for motif in liste_motifs:
                if motif.search(marque):
                    liste_index.append(i)
                    break
        else:
            liste_index_none.append(i)
        i = i + 1
    return data.iloc[liste_index + liste_index_none]


def _anomalie_plateforme_(data, path_to_file):
    """Détecte et supprime certaines anomalies de la variable plateforme.
    Les 'None' sont conservés pour un futur traitement"""
    liste_motifs = []
    with open(
        path_to_file + r"\Nettoyage_données\motif\\anomalie_plateforme.json",
        "r",
        encoding="utf-8",
    ) as fichier:
        motifs = fichier.read()
    motifs = json.loads(motifs)
    for motif in motifs:
        liste_motifs.append(re.compile(motif))
    liste_index = list()
    liste_index_none = list()
    i = 0
    for plat in data.plateforme.to_list():
        if plat:
            plat = plat.lower()
            plat = plat.replace(" ", "")
            for motif in liste_motifs:
                if motif.search(plat):
                    liste_index.append(i)
                    break
        else:
            liste_index_none.append(i)
        i = i + 1
    return data.iloc[liste_index + liste_index_none]


def _anomalie_modele_(data, path_to_file):
    """Détecte et supprime certaines anomalies de la variable modele.
    Les 'None' sont conservés pour un futur traitement"""
    liste_motifs = []
    with open(
        path_to_file + r"\Nettoyage_données\motif\\anomalie_modele.json",
        "r",
        encoding="utf-8",
    ) as fichier:
        motifs = fichier.read()
    motifs = json.loads(motifs)
    for motif in motifs:
        liste_motifs.append(re.compile(motif))
    liste_index = list()
    liste_index_none = list()
    i = 0
    for modele in data.modele.to_list():
        if modele:
            modele = modele.lower()
            modele = modele.replace(" ", "")
            for motif in liste_motifs:
                if motif.search(modele):
                    liste_index.append(i)
                    break
        else:
            liste_index_none.append(i)
        i = i + 1
    return data.iloc[liste_index + liste_index_none]


def _autre_anomalie_(data):
    """Suppression de d'autre anomalies aprés étude minutieuse de la base de données"""

    ## Suppression de annonce présentant comme titre "DE REDUCTION" car ce sont en réalités des jeux vidéos
    motif_regex = re.compile("de REDUCTION")
    liste_garder = list()
    i = 0
    for titre in data.titre.to_list():
        if motif_regex.search(titre):
            pass
        else:
            liste_garder.append(i)
        i = i + 1
    data = data.iloc[liste_garder]

    ## Suppression des annonces ayant comme description "BIENVENUE DANS NOTRE BOUTIQUE" et ayant un prix infèrieur à 10€
    motif_regex = re.compile("BIENVENUE DANS NOTRE BOUTIQUE\n")
    liste_garder = list()
    i = 0
    for titre, prix in zip(data.set_desc.to_list(), data.prix.to_list()):
        if titre:
            if motif_regex.search(titre):
                if prix >= 10:
                    liste_garder.append(i)
            else:
                liste_garder.append(i)
        else:
            liste_garder.append(i)
        i = i + 1
    data = data.iloc[liste_garder]

    ## Suppression des annonces commençant par "notice"
    motif_regex = re.compile("^notice.*?|^book.*?")
    liste_supprimer = list()
    liste_garder = list()
    i = 0
    for titre in data.titre.to_list():
        titre = titre.replace(" ", "").lower()
        if motif_regex.findall(titre):
            ...
        else:
            liste_garder.append(i)
        i = i + 1
    data = data.iloc[liste_garder]

    ## Suppression des annonces contenant 'notice' dans le titre et dont le prix est infèrieur à 50€
    motif_regex = re.compile("notice(s).?|book.?")
    liste_garder = list()
    i = 0
    for titre, prix in zip(data.titre.to_list(), data.prix.to_list()):
        titre = titre.replace(" ", "")
        titre = titre.lower()
        if motif_regex.findall(titre):
            if prix < 50:
                ...
            else:
                liste_garder.append(i)
        else:
            liste_garder.append(i)
        i = i + 1
    data = data.iloc[liste_garder]

    ## Suppression des annonces où le titre contient 'poster' ou 'autocollant' ou 'coque' et où priw < 40
    motifs_regex = [
        re.compile("coque"),
        re.compile("autocollant|sticker|logo|badge|faceplate"),
        re.compile("poster"),
    ]
    liste_garder = list()
    i = 0
    for titre, prix in zip(data.titre.to_list(), data.prix.to_list()):
        titre = titre.lower()
        trouver = False
        if prix <= 40:
            for motif in motifs_regex:
                if motif.search(titre):
                    trouver = True
                    break
            if trouver == False:
                liste_garder.append(i)
        else:
            liste_garder.append(i)
        i = i + 1
    data = data.iloc[liste_garder]

    ## Suppression des annonceS où le titre contien 'kit' ayant un prix infèrieur à 35€
    motif_regex = re.compile("kit")
    liste_garder = list()
    i = 0
    for titre, prix in zip(data.titre.to_list(), data.prix.to_list()):
        titre = titre.replace(" ", "").lower()
        if prix < 35.0:
            if motif_regex.search(titre):
                ...
            else:
                liste_garder.append(i)
        else:
            liste_garder.append(i)
        i = i + 1
    data = data.iloc[liste_garder]

    ## Suppression des annonceS où le titre commence par 'jeu' 'magazine'
    motif_regex = re.compile(
        "^jeu|^magazine|^magasine|^boitevide|^affiche|^manettede|^boitede"
    )
    liste_garder = list()
    i = 0
    for titre in data.titre.to_list():
        titre = titre.replace(" ", "").lower()
        if motif_regex.search(titre):
            ...
        else:
            liste_garder.append(i)
        i = i + 1
    data = data.iloc[liste_garder]

    ## Suppression des annonces infèrieur à 25€ sous certaine condition
    liste_motifs = [
        re.compile(".*?seul.*?"),
        re.compile("hs"),
        re.compile("pourpi[eè]ce"),
        re.compile("hors.?service"),
    ]
    liste_garder = list()
    i = 0
    for titre, etat, prix in zip(
        data.titre.to_list(), data.etat.to_list(), data.prix.to_list()
    ):
        titre = titre.replace(" ", "").lower()
        if prix < 25.0:
            for motif in liste_motifs:
                if etat == "Pour pièces détachées/ne fonctionne pas":
                    liste_garder.append(i)
                    break
                elif motif.search(titre):
                    liste_garder.append(i)
                    break
        else:
            liste_garder.append(i)
        i = i + 1
    data = data.iloc[liste_garder]
    return data


def creer_var(data, path_to_file):
    """
    Créer plusieurs variables :
        - console : représente le nom de la console
        - manette : si la console est vendue avec une ou des manettes
        - cable :  si la console est vendue avec ses cables
        - nbjeu : le nombre de jeux vendus avec la console
        - memoire : indique la mémoire de la console. Attention pour les 
                    consoles ne présentant pas de différence de mémoire (SNES),
                    la variable memoire est égale à 0. 
        - edition : si la console est une édition spéciale
    """
    warnings.filterwarnings("ignore")
    data = var_console(data, path_to_file)
    data = var_manette(data)
    data = var_cable(data)
    data = var_jeu(data)
    data = var_memoire(data)
    data = var_edition(data, path_to_file)
    return data


def var_console(data, path_to_file):
    """Créer la variable console depuis la colonne titre."""
    dict_motifs = {}
    with open(
        path_to_file + r"\Nettoyage_données\motif\\var_console.json",
        "r",
        encoding="utf-8",
    ) as fichier:
        motifs = fichier.read()
    motifs = json.loads(motifs)
    for motif in motifs.keys():
        dict_motifs[re.compile(motif)] = motifs[motif]
    liste_index = list()
    liste_console = list()
    i = 0
    for titre in data.titre.to_list():
        titre = titre.lower()
        titre = titre.replace(" ", "")
        for motif in dict_motifs.keys():
            if motif.search(titre):
                liste_index.append(i)
                liste_console.append(dict_motifs[motif])
                break
        i = i + 1
    data = data.iloc[liste_index]
    data["console"] = liste_console
    return data


def var_manette(data):
    """
    Créer la variable manette.
    Si la présence de manette n'est pas indiqué par le titre ou la description, l'observation est remplis par NaN. Les NaN seront traités ultèrieurement.
    """
    motif_regex1 = re.compile("sans.?manette|without.?controller|sans.?controller")
    motif_regex2 = re.compile("manette|controller")
    motif_regex3 = re.compile("complet")
    liste_manette = list()
    for titre, desc in zip(data.titre.to_list(), data.set_desc.to_list()):
        if desc == None:
            desc = " "
        if motif_regex1.search(titre.lower()):
            liste_manette.append("non")
        elif motif_regex1.search(desc.lower()):
            liste_manette.append("non")
        elif motif_regex2.search(titre.lower()):
            liste_manette.append("oui")
        elif motif_regex2.search(desc.lower()):
            liste_manette.append("oui")
        elif motif_regex3.search(titre.lower()):
            liste_manette.append("oui")
        elif motif_regex3.search(desc.lower()):
            liste_manette.append("oui")
        else:
            liste_manette.append("NaN")
    data["manette"] = liste_manette
    return data


def var_cable(data):
    """
    Créer la variable cable.
    Si le môt cable n'est pas détecter dans l'annonce, l'annonce est considérée avec câble(s)
    """
    motif_regex1 = re.compile("sans.?c[aâ]ble")
    motif_regex4 = re.compile("without.?c[aâ]ble")
    motif_regex2 = re.compile("c[aâ]ble")
    motif_regex3 = re.compile("complet")
    liste_cable = list()
    for titre, desc in zip(data.titre.to_list(), data.set_desc.to_list()):
        if desc == None:
            desc = " "
        if motif_regex1.search(titre.lower()):
            liste_cable.append("non")
        elif motif_regex1.search(desc.lower()):
            liste_cable.append("non")
        elif motif_regex4.search(titre.lower()):
            liste_cable.append("non")
        elif motif_regex4.search(desc.lower()):
            liste_cable.append("non")
        elif motif_regex2.search(titre.lower()):
            liste_cable.append("oui")
        elif motif_regex2.search(desc.lower()):
            liste_cable.append("oui")
        elif motif_regex3.search(titre.lower()):
            liste_cable.append("oui")
        elif motif_regex3.search(desc.lower()):
            liste_cable.append("oui")
        else:
            liste_cable.append("oui")
    data["cable"] = liste_cable
    return data


def var_jeu(data):
    """Détermine le nombre de jeu vendu avec la console"""
    motif_regex1 = re.compile(".*? (\d+).?jeu.*?")
    motif_regex2 = re.compile(".*? (\d+).?game.*?")
    liste_jeu = list()
    for titre, desc in zip(data.titre.to_list(), data.set_desc.to_list()):
        if desc == None:
            desc = " "
        if motif_regex1.findall(titre.lower()):
            valeur, *_ = motif_regex1.findall(titre.lower())
        elif motif_regex1.findall(desc.lower()):
            valeur, *_ = motif_regex1.findall(desc.lower())
        elif motif_regex2.findall(titre.lower()):
            valeur, *_ = motif_regex2.findall(titre.lower())
        elif motif_regex2.findall(desc.lower()):
            valeur, *_ = motif_regex2.findall(desc.lower())
        else:
            valeur = "0"
        if float(valeur) >= 50:
            valeur = "1"
        liste_jeu.append(float(valeur))
    data["nbjeu"] = liste_jeu
    return data


def var_edition(data, path_to_file):
    """Détermine si la console est une édition spéciale."""
    motif_tri = re.compile("[ée]dition")
    liste_motifs = []
    with open(
        path_to_file + r"\Nettoyage_données\motif\\var_edition.json",
        "r",
        encoding="utf-8",
    ) as fichier:
        motifs = fichier.read()
    motifs = json.loads(motifs)
    for motif in motifs:
        liste_motifs.append(re.compile(motif))
    liste_edition = list()
    for titre in data.titre.to_list():
        trouver = False
        if motif_tri.search(titre.lower()):
            for motif in liste_motifs:
                if motif.search(titre.lower()):
                    liste_edition.append("non")
                    trouver = True
                    break
            if trouver == False:
                liste_edition.append("oui")
        else:
            liste_edition.append("non")
    data["edition"] = liste_edition
    return data

    return data


def var_memoire(data):
    """
    Créer la variable memoire.
    Pour les consoles n'ayant pas de différence en terme de mémoire, la variable mémoire prend comme input le numéro 0
    """
    motif_ps3 = re.compile("PS3")
    motif_ps4 = re.compile("PS4")
    motif_xbox360 = re.compile("Xbox 360")
    motif_xboxOne = re.compile("Xbox One")
    liste_memoire = list()

    for console, memoire, titre, desc in zip(
        data.console.to_list(),
        data.memoire.to_list(),
        data.titre.to_list(),
        data.set_desc.to_list(),
    ):
        if desc == None:
            desc = " "
        if (
            motif_ps3.search(console)
            or motif_ps4.search(console)
            or motif_xbox360.search(console)
            or motif_xboxOne.search(console)
        ):
            if _est_correcte_(memoire):
                liste_memoire.append(_traite_memoire_(memoire))
            else:
                liste_memoire.append(_cherche_memoire_(titre, desc))
        else:
            liste_memoire.append(0.0)
    data["memoire"] = liste_memoire
    data.loc[data.memoire == 30000, "memoire"] = "NaN"
    return data


def _est_correcte_(memoire):
    """Regarde si la mémoire est correcte"""
    motif = re.compile("go")
    motif2 = re.compile("to")
    if memoire:
        if motif.search(memoire.lower()):
            return True
        if motif2.search(memoire.lower()):
            return True
        else:
            return False
    else:
        return False


def _cherche_memoire_(titre, desc):
    """Cherche la capacité de stockage pour une console dans sa description ou dans son titre."""
    motif_to = re.compile(".*? (\d+).?to.*?")
    motif_go = re.compile(".*? (\d+).?go.*?")
    motif_gb = re.compile(".*? (\d+).?gb.*?")
    if motif_to.findall(titre.lower()):
        valeur, *_ = motif_to.findall(titre.lower())
        return float(valeur) * 1000
    elif motif_to.findall(desc.lower()):
        valeur, *_ = motif_to.findall(desc.lower())
        return float(valeur) * 1000
    elif motif_go.findall(titre.lower()):
        valeur, *_ = motif_go.findall(titre.lower())
        return float(valeur)
    elif motif_go.findall(desc.lower()):
        valeur, *_ = motif_go.findall(desc.lower())
        return float(valeur)
    elif motif_gb.findall(titre.lower()):
        valeur, *_ = motif_gb.findall(titre.lower())
        return float(valeur)
    elif motif_gb.findall(desc.lower()):
        valeur, *_ = motif_gb.findall(desc.lower())
        return float(valeur)
    else:
        return "NaN"


def _traite_memoire_(memory):
    """Transforme en float la mémoire et convertit en go"""
    motif_to = re.compile(".*?(\d+).?to.*?")
    motif_go = re.compile(".*?(\d+).?go.*?")
    try:
        memoire, *_ = motif_to.findall(memory.lower())
        memoire = float(memoire) * 1000
    except:
        memoire, *_ = motif_go.findall(memory.lower())
        memoire = float(memoire)
    return memoire


def write_tsv(data, path_to_file):
    """
    Ecrit la nouvelle base de données retravaillé en document .tsv
    """
    with open(
        path_to_file + r"\data\\donnees_operationnel.tsv", "w", encoding="utf-8"
    ) as fichier:
        fichier.write(
            "prix\tlivraison\tetat\tretour\tmemoire\tconsole\tmanette\tcable\tnbjeu\tedition\n"
        )
        for observation in data.iloc():
            fichier.write(
                f"{observation.prix}\t{observation.deli_price}\t{observation.etat}\t{observation.retour}\t{observation.memoire}\t{observation.console}\t{observation.manette}\t{observation.cable}\t{observation.nbjeu}\t{observation.edition}\n"
            )
