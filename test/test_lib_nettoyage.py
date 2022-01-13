#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Description
Tests sur le lib_nettoyage.py
"""

import pytest
import pandas as pd
import sys

sys.path.append(
    "C:\\Users\\Lucas\\Documents\\M2\\Python\\Projet\\version_propre\\Nettoyage_données"
)
import lib_nettoyage as lib

PATH_TO_FILE = r"C:\Users\Lucas\Documents\M2\Python\Projet\version_propre"

COLUMNS = [
    "id",
    "titre",
    "prix",
    "deli_price",
    "etat",
    "couleur",
    "retour",
    "type",
    "code_region",
    "connectivite",
    "resolution",
    "marque",
    "plateforme",
    "memoire",
    "modele",
    "set_desc",
]


def supprime_doublons():
    """Supprime doublons par la var ID"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ],
        [
            "255308231040",
            "XBOX",
            "1000 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Bloupurn",
            None,
            "None",
            "Xbox",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]

    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib.supprime_doublons(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_Annonce():
    ...


def test_traite_prix1():
    """Prix en float et en euro"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            99.9,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib.traite_prix(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_traite_prix2():
    """Conversion prix en USD + présence de \xa0"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "1\xa0999,90 USD",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            1769.91,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib.traite_prix(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_traite_prix3():
    """Conversion prix en GBP"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "13,90 GBP",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            16.54,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib.traite_prix(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_traite_deli_price1():
    """Variable deli_price en valeur"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "13.90 GBP",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "13.90 GBP",
            4.90,
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib.traite_deli_price(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_traite_deli_price2():
    """Variable deli_price = 'GRATUIT' """
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "13.90 GBP",
            "GRATUIT",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "13.90 GBP",
            0.0,
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib.traite_deli_price(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_traite_deli_price3():
    """Variable deli_price = Pas de Livraison"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "13.90 GBP",
            "Pas de livraison",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "13.90 GBP",
            0.0,
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib.traite_deli_price(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_traite_retour1():
    """Si variable retour n'est pas ["Retours refusés"]"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "13.90 GBP",
            "Pas de livraison",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "13.90 GBP",
            "Pas de livraison",
            "Occasion",
            "Noir",
            "Oui",
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib.traite_retour(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_traite_retour2():
    """Variable retour =  ["Retours refusés"]"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "13.90 GBP",
            "Pas de livraison",
            "Occasion",
            "Noir",
            ["Retours refusés"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "13.90 GBP",
            "Pas de livraison",
            "Occasion",
            "Noir",
            "Non",
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib.traite_retour(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def traite_etat1():
    """etat = Trés bon état"""
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "13.90 GBP",
            "Pas de livraison",
            "Très bon état",
            "Noir",
            ["Retours refusés"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "13.90 GBP",
            "Pas de livraison",
            "Occasion",
            "Noir",
            ["Retours refusés"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib.traite_etat(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def traite_etat2():
    """etat = Comme neuf"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "13.90 GBP",
            "Pas de livraison",
            "Comme neuf",
            "Noir",
            ["Retours refusés"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "13.90 GBP",
            "Pas de livraison",
            "Occasion",
            "Noir",
            ["Retours refusés"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib.traite_etat(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def traite_etat3():
    """etat = Occasion"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "13.90 GBP",
            "Pas de livraison",
            "Occasion",
            "Noir",
            ["Retours refusés"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "13.90 GBP",
            "Pas de livraison",
            "Occasion",
            "Noir",
            ["Retours refusés"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib.traite_etat(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def traite_etat4():
    """etat = Neuf"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "13.90 GBP",
            "Pas de livraison",
            "Neuf",
            "Noir",
            ["Retours refusés"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "13.90 GBP",
            "Pas de livraison",
            "Neuf",
            "Noir",
            ["Retours refusés"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib.traite_etat(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_anomalie_type1():
    """Pas d'anomalie et anomalie"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ],
        [
            "255308231040",
            "XBOX",
            "1000 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "Cable",
            "PAL",
            None,
            None,
            "SEGA",
            "Bloupurn",
            None,
            "None",
            "Xbox",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "Console de salon",
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._anomalie_type_(
            pd.DataFrame(data=rows_entree, columns=COLUMNS), PATH_TO_FILE
        )
    )


def test_anomalie_type2():
    """'none' et anomalie"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ],
        [
            "255308231040",
            "XBOX",
            "1000 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "Screen",
            "PAL",
            None,
            None,
            "SEGA",
            "Bloupurn",
            None,
            "None",
            "Xbox",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._anomalie_type_(
            pd.DataFrame(data=rows_entree, columns=COLUMNS), PATH_TO_FILE
        )
    )


def test_anomalie_type3():
    """'none' et pas d'anomalie"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ],
        [
            "255308231040",
            "XBOX",
            "1000 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "Bloupurn",
            None,
            "None",
            "Xbox",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ],
        [
            "255308231040",
            "XBOX",
            "1000 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "Bloupurn",
            None,
            "None",
            "Xbox",
        ],
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._anomalie_type_(
            pd.DataFrame(data=rows_entree, columns=COLUMNS), PATH_TO_FILE
        ).sort_index()
    )


def test_anomalie_plateforme1():
    """Pas anomalie et anomalie"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ],
        [
            "255308231040",
            "XBOX",
            "1000 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "Bloupurn",
            None,
            "None",
            "Xbox",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._anomalie_plateforme_(
            pd.DataFrame(data=rows_entree, columns=COLUMNS), PATH_TO_FILE
        )
    )


def test_anomalie_plateforme2():
    """None et anomalie"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            "SEGA",
            None,
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ],
        [
            "255308231040",
            "XBOX",
            "1000 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "Rien_du_tout",
            None,
            "None",
            "Xbox",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            "SEGA",
            None,
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._anomalie_plateforme_(
            pd.DataFrame(data=rows_entree, columns=COLUMNS), PATH_TO_FILE
        )
    )


def test_anomalie_plateforme3():
    """'none' et pas d'anomalie"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            "SEGA",
            None,
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ],
        [
            "255308231040",
            "XBOX",
            "1000 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "None",
            "Xbox",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            "SEGA",
            None,
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ],
        [
            "255308231040",
            "XBOX",
            "1000 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "None",
            "Xbox",
        ],
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._anomalie_plateforme_(
            pd.DataFrame(data=rows_entree, columns=COLUMNS), PATH_TO_FILE
        ).sort_index()
    )


def test_anomalie_marque1():
    """Pas anomalie et anomalie"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ],
        [
            "255308231040",
            "XBOX",
            "1000 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "Hyterva",
            "Bloupurn",
            None,
            "None",
            "Xbox",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._anomalie_marque_(
            pd.DataFrame(data=rows_entree, columns=COLUMNS), PATH_TO_FILE
        )
    )


def test_anomalie_marque2():
    """None et anomalie"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ],
        [
            "255308231040",
            "XBOX",
            "1000 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "Pas_bonne_marque",
            "Rien_du_tout",
            None,
            "None",
            "Xbox",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._anomalie_marque_(
            pd.DataFrame(data=rows_entree, columns=COLUMNS), PATH_TO_FILE
        )
    )


def test_anomalie_marque3():
    """'none' et pas d'anomalie"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ],
        [
            "255308231040",
            "XBOX",
            "1000 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "None",
            "Xbox",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ],
        [
            "255308231040",
            "XBOX",
            "1000 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "None",
            "Xbox",
        ],
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._anomalie_marque_(
            pd.DataFrame(data=rows_entree, columns=COLUMNS), PATH_TO_FILE
        ).sort_index()
    )


def test_anomalie_modele1():
    """Pas anomalie et anomalie"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ],
        [
            "255308231040",
            "XBOX",
            "1000 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "Hyterva",
            "Bloupurn",
            None,
            "pas_de_modele_valable",
            "Xbox",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            "SEGA",
            "Sega Saturn",
            None,
            "Saturn",
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._anomalie_modele_(
            pd.DataFrame(data=rows_entree, columns=COLUMNS), PATH_TO_FILE
        )
    )


def test_anomalie_marque2():
    """None et anomalie"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ],
        [
            "255308231040",
            "XBOX",
            "1000 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "Pas_bonne_marque",
            "Rien_du_tout",
            None,
            "lahYtar",
            "Xbox",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._anomalie_modele_(
            pd.DataFrame(data=rows_entree, columns=COLUMNS), PATH_TO_FILE
        )
    )


def test_anomalie_marque3():
    """'none' et pas d'anomalie"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ],
        [
            "255308231040",
            "XBOX",
            "1000 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "Xbox",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            "99,90 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ],
        [
            "255308231040",
            "XBOX",
            "1000 EUR",
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "Xbox",
        ],
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._anomalie_modele_(
            pd.DataFrame(data=rows_entree, columns=COLUMNS), PATH_TO_FILE
        ).sort_index()
    )


def test_autre_anomalie1():
    """Suppression de annonce présentant comme titre "DE REDUCTION" car ce sont en réalités des jeux vidéos"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            99.90,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ],
        [
            "255308231040",
            "19836€ de REDUCTION",
            1000.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "Xbox",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            99.90,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "SEGA Saturn V2 - Console + Manette + Câbles.\nconsole testé avant la vente\ncâbles non d’origine",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie2():
    """ Suppression des annonces ayant comme description "BIENVENUE DANS NOTRE BOUTIQUE" et ayant un prix infèrieur à 10€"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "BIENVENUE DANS NOTRE BOUTIQUE\n",
        ],
        [
            "255308231040",
            "titre lambda",
            3.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "BIENVENUE DANS NOTRE BOUTIQUE\n",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "BIENVENUE DANS NOTRE BOUTIQUE\n",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie3():
    """Suppression des annonces commençant par 'notice'"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "notice de titre lambda",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie4():
    """Suppression des annonces commençant par 'book'"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "book de titre lambda",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie5():
    """Suppression des annonces contenant 'book' dans le titre et dont le prix est infèrieur à 50€"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - book Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "de book titre lambda",
            45.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - book Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie7():
    """## Suppression des annonces où le titre contient 'poster' ou 'autocollant' ou 'coque'"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "poster de titre lambda",
            38.87,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie8():
    """Suppression des annonces où le titre contient 'poster' ou 'autocollant' ou 'coque' et où prix < 40'"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "autocollant de titre lambda",
            38.87,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie9():
    """Suppression des annonces où le titre contient 'poster' ou 'autocollant' ou 'coque' et où prix < 40"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "stickers de titre lambda",
            38.87,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie10():
    """Suppression des annonces où le titre contient 'poster' ou 'autocollant' ou 'coque' et où prix < 40"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "logo de titre lambda",
            38.87,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie11():
    """Suppression des annonces où le titre contient 'poster' ou 'autocollant' ou 'coque' et où prix < 40"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "logo de titre lambda",
            38.87,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie11():
    """Suppression des annonces où le titre contient 'poster' ou 'autocollant' ou 'coque' et où prix < 40"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "badge de titre lambda",
            38.87,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie12():
    """Suppression des annonces où le titre contient 'poster' ou 'autocollant' ou 'coque' et où prix < 40"""
    rows_entree = [
        [
            "255308231040",
            "SEGA faceplate Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "faceplate de titre lambda",
            38.87,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA faceplate Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie32():
    """Suppression des annonces où le titre contient 'poster' ou 'autocollant' ou 'coque' et où prix < 40"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "coque de titre lambda",
            38.87,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie14():
    """Suppression des annonceS où le titre contien 'kit' ayant un prix infèrieur à 35€"""
    rows_entree = [
        [
            "255308231040",
            "kit SEGA Saturn V2 - book Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "kit titre lambda",
            19.90,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "kit SEGA Saturn V2 - book Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie15():
    """Suppression des annonceS où le titre commence par 'jeu' 'magazine' 'boitevide 'affiche' 'affiche' 'manettede' 'boitede' """
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "jeu de titre lambda",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie14():
    """Suppression des annonceS où le titre contien 'kit' ayant un prix infèrieur à 35€"""
    rows_entree = [
        [
            "255308231040",
            "kit SEGA Saturn V2 - book Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "kit titre lambda",
            19.90,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "kit SEGA Saturn V2 - book Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie16():
    """Suppression des annonceS où le titre commence par 'jeu' 'magazine' 'boitevide 'affiche' 'affiche' 'manettede' 'boitede' """
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "magasine de titre lambda",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie14():
    """Suppression des annonceS où le titre contien 'kit' ayant un prix infèrieur à 35€"""
    rows_entree = [
        [
            "255308231040",
            "kit SEGA Saturn V2 - book Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "kit titre lambda",
            19.90,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "kit SEGA Saturn V2 - book Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie17():
    """Suppression des annonceS où le titre commence par 'jeu' 'magazine' 'boitevide 'affiche' 'affiche' 'manettede' 'boitede' """
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "boite vide de titre lambda",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie14():
    """Suppression des annonceS où le titre contien 'kit' ayant un prix infèrieur à 35€"""
    rows_entree = [
        [
            "255308231040",
            "kit SEGA Saturn V2 - book Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "kit titre lambda",
            19.90,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "kit SEGA Saturn V2 - book Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie18():
    """Suppression des annonceS où le titre commence par 'jeu' 'magazine' 'boitevide 'affiche' 'affiche' 'manettede' 'boitede' """
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "affiche de titre lambda",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie14():
    """Suppression des annonceS où le titre contien 'kit' ayant un prix infèrieur à 35€"""
    rows_entree = [
        [
            "255308231040",
            "kit SEGA Saturn V2 - book Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "kit titre lambda",
            19.90,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "kit SEGA Saturn V2 - book Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie19():
    """Suppression des annonceS où le titre commence par 'jeu' 'magazine' 'boitevide 'affiche' 'affiche' 'manettede' 'boitede' """
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "manette de titre lambda",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie14():
    """Suppression des annonceS où le titre contien 'kit' ayant un prix infèrieur à 35€"""
    rows_entree = [
        [
            "255308231040",
            "kit SEGA Saturn V2 - book Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "kit titre lambda",
            19.90,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "kit SEGA Saturn V2 - book Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie20():
    """Suppression des annonceS où le titre commence par 'jeu' 'magazine' 'boitevide 'affiche' 'affiche' 'manettede' 'boitede' """
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "boite de titre lambda",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie14():
    """Suppression des annonceS où le titre contien 'kit' ayant un prix infèrieur à 35€"""
    rows_entree = [
        [
            "255308231040",
            "kit SEGA Saturn V2 - book Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "kit titre lambda",
            19.90,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "kit SEGA Saturn V2 - book Console + Manette + Câbles",
            100.09,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie21():
    """Suppression des annonces infèrieur à 25€ sous certaine condition"""
    rows_entree = [
        [
            "255308231040",
            "hs SEGA Saturn V2 - Console + Manette + Câbles",
            24.87,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "jeu de titre lambda",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "hs SEGA Saturn V2 - Console + Manette + Câbles",
            24.87,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie22():
    """Suppression des annonces infèrieur à 25€ sous certaine condition"""
    rows_entree = [
        [
            "255308231040",
            "SEGA seul Saturn V2 - Console + Manette + Câbles",
            24.87,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "jeu de titre lambda",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA seul Saturn V2 - Console + Manette + Câbles",
            24.87,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie23():
    """Suppression des annonces infèrieur à 25€ sous certaine condition"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2  pour pieces - Console + Manette + Câbles",
            24.87,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "jeu de titre lambda",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2  pour pieces - Console + Manette + Câbles",
            24.87,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie24():
    """Suppression des annonces infèrieur à 25€ sous certaine condition"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 hors-service - Console + Manette + Câbles",
            24.87,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "jeu de titre lambda",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 hors-service - Console + Manette + Câbles",
            24.87,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_autre_anomalie25():
    """Suppression des annonces infèrieur à 25€ sous certaine condition"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "jeu de titre lambda",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS).equals(
        lib._autre_anomalie_(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_var_console1():
    """Creation d'une var console.
    Ici prsence d'une identification d'une non identification"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "pas de console",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
            "Saturn",
        ]
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS + ["console"]).equals(
        lib.var_console(pd.DataFrame(data=rows_entree, columns=COLUMNS), PATH_TO_FILE)
    )


def test_var_console2():
    """Deux/deux identification"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "playstation3",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
            "Saturn",
        ],
        [
            "255308231040",
            "playstation3",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
            "PS3",
        ],
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS + ["console"]).equals(
        lib.var_console(pd.DataFrame(data=rows_entree, columns=COLUMNS), PATH_TO_FILE)
    )


def test_var_manette1():
    """un avec manette, l'autre sans manette"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "playstation3",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "sans manette",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
            "oui",
        ],
        [
            "255308231040",
            "playstation3",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "sans manette",
            "non",
        ],
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS + ["manette"]).equals(
        lib.var_manette(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_var_manette2():
    """un avec manette, l'autre sans manette"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Câbles",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla avec controller",
        ],
        [
            "255308231040",
            "playstation3 without controllers",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Câbles",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla avec controller",
            "oui",
        ],
        [
            "255308231040",
            "playstation3 without controllers",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blabla",
            "non",
        ],
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS + ["manette"]).equals(
        lib.var_manette(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_var_manette3():
    """un avec 'complet', l'autre sans indication"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 complet - Console + Câbles",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "playstation3",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "rien",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 complet - Console + Câbles",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
            "oui",
        ],
        [
            "255308231040",
            "playstation3",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "rien",
            "NaN",
        ],
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS + ["manette"]).equals(
        lib.var_manette(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_var_cable1():
    """un avec manette, l'autre sans manette"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "playstation3",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "sans cable",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
            "oui",
        ],
        [
            "255308231040",
            "playstation3",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "sans cable",
            "non",
        ],
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS + ["cable"]).equals(
        lib.var_cable(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_var_cable2():
    """un avec manette, l'autre sans manette"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla avec cables",
        ],
        [
            "255308231040",
            "playstation3 sans cable",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blablabla",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla avec cables",
            "oui",
        ],
        [
            "255308231040",
            "playstation3 sans cable",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "blablabla",
            "non",
        ],
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS + ["cable"]).equals(
        lib.var_cable(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_var_cable3():
    """un avec 'complet', l'autre sans indication"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 complet - Console",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "playstation3",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "rien",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 complet - Console",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
            "oui",
        ],
        [
            "255308231040",
            "playstation3",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "rien",
            "oui",
        ],
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS + ["cable"]).equals(
        lib.var_cable(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_var_nbjeu1():
    """dans titre, avec 'jeu' et 'game'"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles + 3jeux",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "playstation3 + 3 games",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "sans manette",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles + 3jeux",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
            3.0,
        ],
        [
            "255308231040",
            "playstation3 + 3 games",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "sans manette",
            3.0,
        ],
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS + ["nbjeu"]).equals(
        lib.var_jeu(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_var_nbjeu2():
    """dans description, avec 'jeu' et 'game'"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla + 3jeux",
        ],
        [
            "255308231040",
            "playstation3",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "sans manette + 3 games",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla + 3jeux",
            3.0,
        ],
        [
            "255308231040",
            "playstation3",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "sans manette + 3 games",
            3.0,
        ],
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS + ["nbjeu"]).equals(
        lib.var_jeu(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_var_nbjeu3():
    """ sans indication, et avec 'sans jeux'"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
        ],
        [
            "255308231040",
            "playstation3",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "sans manette sans jeux",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla",
            0.0,
        ],
        [
            "255308231040",
            "playstation3",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "sans manette sans jeux",
            0.0,
        ],
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS + ["nbjeu"]).equals(
        lib.var_jeu(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_var_nbjeu4():
    """avec une valeur trouvé >= 50"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla + 89jeux",
        ],
        [
            "255308231040",
            "playstation3 + 68 games",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "sans manette",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 - Console + Manette + Câbles",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla + 89jeux",
            1.0,
        ],
        [
            "255308231040",
            "playstation3 + 68 games",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "sans manette",
            1.0,
        ],
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS + ["nbjeu"]).equals(
        lib.var_jeu(pd.DataFrame(data=rows_entree, columns=COLUMNS))
    )


def test_var_edition1():
    """un oui un non"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 edition digital",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla + 89jeux",
        ],
        [
            "255308231040",
            "playstation3 edition WOW",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "sans manette",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 edition digital",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla + 89jeux",
            "non",
        ],
        [
            "255308231040",
            "playstation3 edition WOW",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "sans manette",
            "oui",
        ],
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS + ["edition"]).equals(
        lib.var_edition(pd.DataFrame(data=rows_entree, columns=COLUMNS), PATH_TO_FILE)
    )


def test_var_edition2():
    """deux non"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 edition standard",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla + 89jeux",
        ],
        [
            "255308231040",
            "playstation3 edition original",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "sans manette",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 edition standard",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla + 89jeux",
            "non",
        ],
        [
            "255308231040",
            "playstation3 edition original",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "sans manette",
            "non",
        ],
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS + ["edition"]).equals(
        lib.var_edition(pd.DataFrame(data=rows_entree, columns=COLUMNS), PATH_TO_FILE)
    )


def test_var_edition3():
    """deux non"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 edition classique",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla + 89jeux",
        ],
        [
            "255308231040",
            "playstation3 1er edition",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "sans manette",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 edition classique",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla + 89jeux",
            "non",
        ],
        [
            "255308231040",
            "playstation3 1er edition",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "sans manette",
            "non",
        ],
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS + ["edition"]).equals(
        lib.var_edition(pd.DataFrame(data=rows_entree, columns=COLUMNS), PATH_TO_FILE)
    )


def test_var_edition4():
    """Pas indiqué et un oui"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 edition no_scrap_leboncoin",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla + 89jeux",
        ],
        [
            "255308231040",
            "playstation3",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "sans manette",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 edition no_scrap_leboncoin",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla + 89jeux",
            "oui",
        ],
        [
            "255308231040",
            "playstation3",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "sans manette",
            "non",
        ],
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS + ["edition"]).equals(
        lib.var_edition(pd.DataFrame(data=rows_entree, columns=COLUMNS), PATH_TO_FILE)
    )


def test_est_correcte():
    assert lib._est_correcte_("3go")
    assert lib._est_correcte_("56go")
    assert lib._est_correcte_("3to")
    assert not lib._est_correcte_("3tb")
    assert not lib._est_correcte_("3gb")
    assert not lib._est_correcte_(" ")


def test_traite_memoire():
    assert lib._traite_memoire_("3go") == 3.0
    assert lib._traite_memoire_("56go") == 56.0
    assert lib._traite_memoire_("3to") == 3000.0


def test_var_memoire1():
    """Une saturn et une playstation sans indication mémoire"""
    rows_entree = [
        [
            "255308231040",
            "SEGA Saturn V2 edition classique",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            None,
            None,
            "blabla + 89jeux",
            "Saturn",
        ],
        [
            "255308231040",
            "playstation3 1er edition",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            None,
            "xbox360",
            "sans manette",
            "PS3",
        ],
    ]
    rows_attendu = [
        [
            "255308231040",
            "SEGA Saturn V2 edition classique",
            24.87,
            "4,90 EUR",
            "Pour pièces détachées/ne fonctionne pas",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            None,
            "PAL",
            None,
            None,
            None,
            None,
            0.0,
            None,
            "blabla + 89jeux",
            "Saturn",
        ],
        [
            "255308231040",
            "playstation3 1er edition",
            23.98,
            "4,90 EUR",
            "Occasion",
            "Noir",
            ["Remboursement sous 30\xa0jours | L'acheteur paie les frais de retour"],
            "handheld",
            "PAL",
            None,
            None,
            "SEGA",
            "PS1",
            "NaN",
            "xbox360",
            "sans manette",
            "PS3",
        ],
    ]
    assert pd.DataFrame(data=rows_attendu, columns=COLUMNS + ["console"]).equals(
        lib.var_memoire(pd.DataFrame(data=rows_entree, columns=COLUMNS + ["console"]))
    )


def test_supprime_variable():
    column_before = [
        "id",
        "titre",
        "prix",
        "deli_price",
        "etat",
        "couleur",
        "retour",
        "type",
        "code_region",
        "connectivite",
        "resolution",
        "marque",
        "plateforme",
        "memoire",
        "modele",
        "set_desc",
        "console",
        "manette",
        "cable",
        "jeu",
        "edition",
    ]
    column_after = [
        "prix",
        "deli_price",
        "etat",
        "retour",
        "memoire",
        "console",
        "manette",
        "cable",
        "jeu",
        "edition",
    ]
    assert lib.supprime_variables(pd.DataFrame(columns=column_before)).equals(
        pd.DataFrame(columns=column_after)
    )
