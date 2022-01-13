#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Webscrapping step

Utilisation de selenium pour la navigation dans le browser.
"""

from selenium import webdriver
from bs4 import BeautifulSoup as BF
from rich import print
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep, time
import re
from pathlib import Path
import json
from numpy import random


class Session:
    """
    Session webscrapping
    """

    def __init__(self, depart):
        self.navigateur = webdriver.Chrome()
        self.navigateur.get(depart)
        sleep(5)

    def _accepte_cookies_(self):
        """Accepte les cookies"""
        soupe = self.navigateur.page_source
        soupe = BF(soupe, features="lxml")
        fenetre_cookie = soupe.find_all(attrs={"id": ["gdpr-banner-accept"]})[0]
        cliquer = self.navigateur.find_element(By.ID, fenetre_cookie.attrs["id"])
        if cliquer.screenshot("Accepter_les_cookies.png"):
            cliquer.click()
        else:
            raise ValueError(
                "Impossible de trouver le bouton d'acceptation des cookies"
            )
        sleep(5)

    def _barre_de_recherche_(self):
        """Clique sur la barre de recherche et envoie la recherche"""
        soupe = self.navigateur.page_source
        soupe = BF(soupe, features="lxml")
        barre_recherches = soupe.find_all(attrs={"type": ["text"]})
        barre_recherche = barre_recherches[0]
        cliquer = self.navigateur.find_element(
            By.CLASS_NAME, barre_recherche.attrs["class"][1]
        )
        if cliquer.screenshot("Barre_recherche.png"):
            cliquer.send_keys("Console")
        else:
            raise ValueError("Impossible de trouver la barre de recherche")
        sleep(5)

    def _selection_barre_recherche_(self):
        """Selectionne le bon resultat de la recherche"""
        soupe = self.navigateur.page_source
        soupe = BF(soupe, features="lxml")
        for click_console in soupe.find_all(
            attrs={"class": ["ui-menu-item ghAC_visible"]}
        ):
            if click_console.find_all(
                attrs={
                    "aria-label": ["console dans la catégorie Consoles de jeux vidéo"]
                }
            ):
                bon_click = click_console
        for element in self.navigateur.find_elements(
            By.CLASS_NAME, bon_click.attrs["class"][0]
        ):
            if element.text == "console – Consoles de jeux vidéo":
                bon_click = element
        if bon_click.screenshot("Bouton_console.png"):
            bon_click.click()
        else:
            raise ValueError(f"Impossible de trouver la selection {bon_click.text}")
        sleep(5)

    def _OPT_bon_pays_(self, country: str = "France"):
        """Check si les annonces sont sur le bon pays de livraison"""
        soupe = self.navigateur.page_source
        soupe = BF(soupe, features="lxml")
        resultats = soupe.find_all(attrs={"class": ["srp-controls_row-cells", "right"]})
        bon_resultat = resultats[1]
        elements = self.navigateur.find_elements(
            By.CLASS_NAME, bon_resultat.attrs["class"][0]
        )
        motif_regex = re.compile("Livraison vers: (.+)")
        if motif_regex.findall == "France":
            return
        for element in elements:
            if motif_regex.findall(element.text):
                bon_element = element
        pays, *_ = motif_regex.findall(bon_element.text)
        if pays.upper != country.upper:
            if bon_element.screenshot("Clique_livraison.png"):
                bon_element.click()
                sleep(5)
                self._choix_pays_(country)
            else:
                raise ValueError("Impossible de trouver la barre 'Livraison vers'")

    def _choix_pays_(self, country: str = "France"):
        """Change de pays si on est pas situé sur le bon pays"""
        soupe = self.navigateur.page_source
        soupe = BF(soupe, features="lxml")
        cliques = soupe.find_all(attrs={"class": ["select"]})
        clique = cliques[0]
        elements = self.navigateur.find_elements(
            By.CLASS_NAME, clique.attrs["class"][0]
        )
        element = elements[0]
        if element.screenshot("Clique_liste_pays_disponible.png"):
            element.click()
            sleep(5)
            element.find_element(
                By.XPATH, "//select/option[text()='France - FRA']"
            ).click()
            sleep(5)
        else:
            raise ValueError("Impossible de trouver la barre des pays")
        elements_ok = self.navigateur.find_elements(
            By.XPATH,
            "//*[@class='srp-shipping-location__form--inline btn btn--small btn--primary']",
        )
        clique_ok = elements_ok[0]
        if clique_ok.screenshot("bouton_ok_pays.png"):
            clique_ok.click()
            sleep(5)
        else:
            raise ValueError(
                "Impossible de trouver le bouton ok de la partie instentation du pays"
            )

    def _OPT_achat_immediat_(self):
        """Sélectionne l'option achat immédiat"""
        boutons_selection = self.navigateur.find_elements(
            By.XPATH, "//*[@class='fake-tabs__item btn']"
        )
        for bouton in boutons_selection:
            if bouton.text == "Achat immédiat":
                bon_bouton = bouton
        if bon_bouton.screenshot("Bouton_achat_immediat.png"):
            bon_bouton.click()
            sleep(5)
        else:
            raise ValueError("Le bouton achat immédiat est introuvable")

    def _stop_(self):
        """Stop et ferme le webdriver"""
        self.navigateur.quit()

    def bon_setup(self):
        """Introduction pour trouver les bonnes annonces"""
        self._accepte_cookies_()
        self._barre_de_recherche_()
        self._selection_barre_recherche_()
        self._OPT_bon_pays_()
        self._OPT_achat_immediat_()

    def traite_annonces(self, annonces: list, path):
        """Itère sur les annonces d'une page"""
        for annonce in annonces:
            sleep(abs(random.normal(1, 0.2)))
            clique, *_ = annonce.find_elements(By.CLASS_NAME, "s-item__image")
            if clique.screenshot("photo_cliquable.png"):
                clique.click()
                windows = self.navigateur.window_handles
                self.navigateur.switch_to.window(windows[1])
                element = WebDriverWait(self.navigateur, 10).until(
                    EC.presence_of_element_located((By.ID, "Body"))
                )
                sleep(abs(random.normal(0.2, 0.15)))
                self.traite_donnees(path)
                self.navigateur.close()
                self.navigateur.switch_to.window(windows[0])
            else:
                raise ValueError("Error")

    def par_page(self):
        """Traite toutes les annonces"""
        i = 0
        fichier = Path(".").resolve() / "donnees/brute.json"
        debut = time()
        while True:
            main, *_ = self.navigateur.find_elements(By.ID, "mainContent")
            elements = main.find_elements(By.CLASS_NAME, "s-item")
            bon_elements = elements[1::]
            i = i + len(bon_elements)
            self.traite_annonces(annonces=bon_elements, path=fichier)
            try:
                self.page_suivante()
            except NoSuchElementException:
                break
            print(f"{i} annonces traités en {time() - debut} secondes")
        self._stop_()

    def page_suivante(self):
        """Page suivante."""
        page_suivante, *_ = self.navigateur.find_elements(
            By.CLASS_NAME, "pagination__next"
        )
        page_suivante.click()
        sleep(4)

    def traite_donnees(self, path):
        """Ecrit les données en JSON"""
        with open(path, "a", encoding="utf-8") as f:
            ann = Annonce(self)
            f.write(ann.to_json())
            f.write("\n")


class Annonce:
    """Classe pour gérer les données d'une annonce"""

    def __init__(self, annonce):
        soupe = BF(annonce.navigateur.page_source, features="lxml")
        self.set_id(soupe)
        self.set_titre(soupe)
        self.set_prix(soupe)
        self.set_deli_price(soupe)
        self.set_etat(soupe)
        self.set_reste(soupe)
        self.set_retour(soupe)
        self.set_desc(annonce)

    def __str__(self):
        return f"""
titre           : {self.titre}
id              : {self.id}
etat            : {self.etat}
deli_price      : {self.deli_price}
prix            : {self.prix}
description     : {self.desc}
retour          : {self.retour}
couleur         : {self.couleur}
type            : {self.type}
marque          : {self.marque}
connectivite    : {self.connectivite}
plateforme      : {self.plateforme}
code_region     : {self.code_region}
resolution      : {self.resolution}
modele          : {self.modele}
memoire_stock   : {self.memoire}
"""

    def set_titre(self, annonce):
        """Affecte le titre de l'annonce"""
        info, *_ = annonce.find_all(attrs={"class": ["it-ttl"]})
        self.titre = list(info.childGenerator())[1]

    def set_id(self, annonce):
        """Affecte l'identifiant unique de l'annonce"""
        info, *_ = annonce.find_all(attrs={"class": ["iti-act-num"]})
        self.id = info.get_text()

    def set_etat(self, annonce):
        """Affecte l'etat de l'annonce"""
        info, *_ = annonce.find_all(attrs={"class": ["u-f1L", "condText"]})
        self.etat = info.get_text()

    def set_prix(self, annonce):
        """Affecte prix de l'annonce"""
        info, *_ = annonce.find_all(attrs={"class": ["mainPrice"]})
        try:
            prix, *_ = info.find_all(attrs={"id": ["prcIsum"]})
        except ValueError:
            prix, *_ = info.find_all(attrs={"class": ["notranslate"]})
        self.prix = prix.get_text()

    def set_deli_price(self, annonce):
        """Affecte le prix de livraison de l'annonce"""
        try:
            info, *_ = annonce.find_all(attrs={"id": ["fshippingCost"]})
            motif_regex = re.compile("\n(.*?)\n")
            self.deli_price, *_ = motif_regex.findall(info.get_text())
        except ValueError:
            try:
                info, *_ = annonce.find_all(attrs={"class": ["vi-fnf-ship-txt"]})
                self.deli_price, *_ = info.get_text()
            except ValueError:
                self.deli_price = "No shipping"

    def set_retour(self, annonce):
        """Affecte les conditions de retour"""
        infos, *_ = annonce.find_all(attrs={"class": ["ux-layout-section--returns"]})
        info, *_ = infos.find_all(attrs={"class": ["ux-labels-values__values-content"]})
        motif_regex = re.compile("(.*?) \| Afficher les détails")
        self.retour = motif_regex.findall(info.get_text())

    def set_reste(self, annonce):
        """Affecte le reste de la description du produit"""
        infos, *_ = annonce.find_all(
            attrs={"class": ["ux-layout-section__item--table-view"]}
        )
        titres = infos.find_all(attrs={"class": ["ux-labels-values__labels"]})[1::]
        valeurs = infos.find_all(attrs={"class": ["ux-labels-values__values"]})[1::]

        self.couleur = None
        self.type = None
        self.code_region = None
        self.connectivite = None
        self.resolution = None
        self.marque = None
        self.plateforme = None
        self.memoire = None
        self.modele = None

        for titre, valeur in zip(titres, valeurs):
            self.tri_reste(titre.get_text(), valeur.get_text())

    def tri_reste(self, titre, valeur):
        if titre.replace(" ", "") == "Couleur:":
            self.couleur = valeur.strip()
        elif titre.replace(" ", "") == "Type:":
            self.type = valeur.strip()
        elif titre.replace(" ", "") == "Codederégion:":
            self.code_region = valeur.strip()
        elif titre.replace(" ", "") == "Connectivité:":
            self.connectivite = valeur.strip()
        elif titre.replace(" ", "") == "Résolution:":
            self.resolution = valeur.strip()
        elif titre.replace(" ", "") == "Marque:":
            self.marque = valeur.strip()
        elif titre.replace(" ", "") == "Plateforme:":
            self.plateforme = valeur.strip()
        elif titre.replace(" ", "") == "Capacitédestockage:":
            self.memoire = valeur.strip()
        elif titre.replace(" ", "") == "Modèle:":
            self.modele = valeur.strip()
        else:
            pass

    def set_desc(self, annonce: Session):
        """Affecte la description vendeur"""
        try:
            element, *_ = annonce.navigateur.find_elements(By.ID, "desc_div")
            iframe, *_ = element.find_elements(By.CSS_SELECTOR, "iframe")
            annonce.navigateur.switch_to.frame(iframe)
            description, *_ = annonce.navigateur.find_elements(By.ID, "ds_div")
            self.set_desc = description.text
        except ValueError:
            self.set_desc = None

    def to_json(self):
        """Renvoit une chaine pour stocker le résultat en json."""
        return json.dumps(self.__dict__)


def lance_webscrapping(depart):
    """lance la récupération des données"""
    nav = Session(depart)
    nav.bon_setup()
    nav.par_page()
    nav._stop_()
