"""Description.
Libraire pour un gui de la librairie ordonnancement.
"""
import ipywidgets as ipw
from IPython.display import display
from typing import List
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import sys
import pandas as pd

PATH_TO_FILE = r"C:\Users\Lucas\Documents\M2\Python\Projet\version_propre"

sys.path.append(PATH_TO_FILE + r"\Machine_learning")

from lib_modele import traite_NA_data

with open(PATH_TO_FILE + r"\modele_final\\script.txt", "r") as fichier:
    exec(fichier.read())


def _data_(new_row):
    data = pd.read_csv(PATH_TO_FILE + "\data\\donnees_operationnel.tsv", sep="\t")
    data.loc[len(data.index)] = new_row
    data = traite_NA_data(data)
    return data


def _split_(data):
    ohe = OneHotEncoder(drop="first")
    X1 = data.iloc[:, [2, 3, 5, 6, 7, 9]].to_numpy()
    X2 = data.iloc[:, [1, 4, 8]].to_numpy()
    ohe.fit(X1)
    X1 = ohe.transform(X1).toarray()
    X = np.hstack([X2, X1])
    return X[-1]


def _estimation_(valeur):
    X = _split_(_data_(valeur))
    estimation, *_ = MODELE.predict([X])
    return round(estimation, 1)


def check_modele():
    print(MODELE)


class Application:
    def __init__(self):

        self.bouton = ipw.Button(
            description="Envoyer",
            icon="check",
            tooltip="Envoyer les données pour une estimation",
            layout=ipw.Layout(width="25%", height="40px"),
        )

        self.console = ipw.Combobox(
            options=[
                "2DSXL",
                "3DS",
                "3DS XL",
                "DSi",
                "DSi XL",
                "DSlite",
                "Atari 2600",
                "Atari 7800",
                "Dreamcast",
                "GBA",
                "GBA SP",
                "Game Boy",
                "Game Boy Color",
                "Game Gear",
                "Game cube",
                "Game&Watch",
                "Intellivision",
                "Jaguar",
                "Master System",
                "Master System II",
                "Mega Drive",
                "Mega Drive II",
                "Mega Drive mini",
                "N64",
                "NES",
                "SNES",
                "NGP",
                "NGPC",
                "Neo-Geo AES",
                "Nintendo Mini",
                "PS mini",
                "PS1",
                "PS2",
                "PS2 slim",
                "PS3",
                "PS3 slim",
                "PS3 ultra slim",
                "PS4",
                "PS4 PRO",
                "PS4 slim",
                "PS5 blu-ray",
                "PS5 digital",
                "PSP",
                "PS Vita",
                "Saturn",
                "Switch",
                "Switch OLED",
                "Switch lite",
                "TurboGrafx-16",
                "Wii",
                "Wii U",
                "Wii U Deluxe",
                "WonderSwan",
                "WonderSwan Color",
                "Xbox",
                "Xbox 360",
                "Xbox 360s",
                "Xbox One",
                "Xbox One S",
                "Xbox Series S",
                "Xbox Series X",
                "32X",
            ]
        )
        self.manette = ipw.Checkbox(value=True, description="Manette")
        self.edition = ipw.Checkbox(value=False, description="Edition speciale")
        self.cable = ipw.Checkbox(value=True, description="Cable")
        self.retour = ipw.ToggleButtons(
            options=["Sans retour", "Avec retour"],
            layout=ipw.Layout(width="50%", height="60px"),
        )
        self.etat = ipw.ToggleButtons(
            description="Etat de la console",
            options=["Occasion", "Neuf", "HS / Pour pièces détachées", "Reconditionné"],
            layout=ipw.Layout(height="80px"),
        )
        self.deli_price = ipw.FloatSlider(
            value=0,
            min=0,
            max=100,
            step=0.5,
            description="Prix de livraison:",
            continuous_update=False,
            orientation="horizontal",
            readout=True,
            readout_format=".1f",
        )
        self.nbjeu = ipw.IntSlider(
            value=0,
            min=0,
            max=49,
            step=1,
            description="Nombre de jeux vendu avec la console",
            continuous_update=False,
            orientation="horizontal",
            readout=True,
            readout_format=".1f",
        )

        self.memoire_xbox360 = ipw.Select(
            options=["Ne sait pas", "4", "20", "60", "120", "250", "320", "500"],
            value="Ne sait pas",
            # rows=10,
            description="Memoire en giga:",
            disabled=False,
        )
        self.memoire_xbox360S = ipw.Select(
            options=["Ne sait pas", "4", "120", "229", "250", "320"],
            value="Ne sait pas",
            # rows=10,
            description="Memoire en giga:",
            disabled=False,
        )
        self.memoire_xboxOneetS = ipw.Select(
            options=["Ne sait pas", "500", "1000", "2000", "320"],
            value="Ne sait pas",
            # rows=10,
            description="Memoire en giga:",
            disabled=False,
        )
        self.memoire_ps3 = ipw.Select(
            options=[
                "Ne sait pas",
                "12",
                "40",
                "60",
                "80",
                "120",
                "150",
                "160",
                "250",
                "320",
                "500",
            ],
            value="Ne sait pas",
            # rows=10,
            description="Memoire en giga:",
            disabled=False,
        )
        self.memoire_ps3slim = ipw.Select(
            options=["Ne sait pas", "12", "120", "160", "250", "298", "320", "500"],
            value="Ne sait pas",
            # rows=10,
            description="Memoire en giga:",
            disabled=False,
        )
        self.memoire_ps3ultraslim = ipw.Select(
            options=["Ne sait pas", "12", "250", "500"],
            value="Ne sait pas",
            # rows=10,
            description="Memoire en giga:",
            disabled=False,
        )
        self.memoire_ps4 = ipw.Select(
            options=["Ne sait pas", "500", "1000"],
            value="Ne sait pas",
            # rows=10,
            description="Memoire en giga:",
            disabled=False,
        )
        self.memoire_ps4SLIMetPRO = ipw.Select(
            options=["Ne sait pas", "500", "1000", "2000"],
            value="Ne sait pas",
            # rows=10,
            description="Memoire en giga:",
            disabled=False,
        )

        self.resultat = ipw.Output()

    def transforme_etat(self):
        etat = self.etat.value
        if etat == "HS / Pour pièces détachées":
            etat = "Pour pièces détachées/ne fonctionne pas"
        elif etat == "Reconditionné":
            etat = "Reconditionné par le vendeur"
        return etat

    def transforme_retour(self):
        if self.retour.value == "Sans retour":
            retour = "Oui"
        if self.retour.value == "Avec retour":
            retour = "Non"
        return retour

    def transforme_memoire(self):
        if self.console.value == "Xbox 360":
            memory = self.memoire_xbox360.value
        elif self.console.value == "Xbox 360s":
            memory = self.memoire_xbox360S.value
        elif self.console.value == "Xbox One S":
            memory = self.memoire_xboxOneetS.value
        elif self.console.value == "Xbox One":
            memory = self.memoire_xboxOneetS.value
        elif self.console.value == "PS3":
            memory = self.memoire_ps3.value
        elif self.console.value == "PS3 ultra slim":
            memory = self.memoire_ps3ultraslim.value
        elif self.console.value == "PS3 slim":
            memory = self.memoire_ps3slim.value
        elif self.console.value == "PS4 PRO":
            memory = self.memoire_ps4.value
        elif self.console.value == "PS4":
            memory = self.memoire_ps4SLIMetPRO.value
        elif self.console.value == "PS4 slim":
            memory = self.memoire_ps4SLIMetPRO.value
        else:
            memory = 0
        try:
            memoire = float(memory)
        except ValueError:
            memoire = np.nan
        return memoire

    def transforme_manette(self):
        if self.manette == True:
            manette = "oui"
        else:
            manette = "non"
        return manette

    def transforme_cable(self):
        if self.cable == True:
            cable = "oui"
        else:
            cable = "non"
        return cable

    def transforme_edition(self):
        if self.edition == True:
            edition = "oui"
        else:
            edition = "non"
        return edition

    def affichage(self):
        sortie = ipw.interactive_output(self.construction, {"valeur": self.console})
        widgets = ipw.VBox(
            [
                ipw.HBox(
                    [
                        self.console,
                        ipw.VBox([self.cable, self.manette]),
                        ipw.VBox([self.edition, self.nbjeu]),
                    ]
                ),
                self.retour,
                self.deli_price,
                self.etat,
            ]
        )

        self.bouton.on_click(self._sur_clique)
        display(widgets, sortie, self.resultat)

    def _sur_clique(self, b):
        variables = [
            0,
            self.deli_price.value,
            self.transforme_etat(),
            self.transforme_retour(),
            self.transforme_memoire(),
            self.console.value,
            self.transforme_manette(),
            self.transforme_cable(),
            self.nbjeu.value,
            self.transforme_edition(),
        ]
        string = f"Estimation pour {self.console.value} : {_estimation_(variables)}"
        with self.resultat:
            resultat = ipw.Text(value=string)
            display(resultat)

    def construction(self, valeur: str):
        if valeur == "Xbox 360":
            affichage = self.memoire_xbox360
        elif valeur == "Xbox 360s":
            affichage = self.memoire_xbox360S
        elif valeur == "Xbox One S":
            affichage = self.memoire_xboxOneetS
        elif valeur == "Xbox One":
            affichage = self.memoire_xboxOneetS
        elif valeur == "PS3":
            affichage = self.memoire_ps3
        elif valeur == "PS3 ultra slim":
            affichage = self.memoire_ps3ultraslim
        elif valeur == "PS3 slim":
            affichage = self.memoire_ps3slim
        elif valeur == "PS4 PRO":
            affichage = self.memoire_ps4
        elif valeur == "PS4":
            affichage = self.memoire_ps4SLIMetPRO
        elif valeur == "PS4 slim":
            affichage = self.memoire_ps4SLIMetPRO
        else:
            affichage = ipw.Select(options=[" "], disabled=True)
        affichage = ipw.HBox([affichage, self.bouton])
        display(affichage)
