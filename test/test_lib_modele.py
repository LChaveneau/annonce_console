#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Procédure de test pour lib_modele.py"""

import pytest
import pandas as pd
import sys

sys.path.append(
    "C:\\Users\\Lucas\\Documents\\M2\\Python\\Projet\\version_propre\\Machine_learning"
)
import lib_modele as lib
import numpy as np


def test_meilleur_modele():
    entree = [
        lib.Metrics(modele="1", parametre={}, error=0.19, mse=120.0, mse_tr=45.0),
        lib.Metrics(modele="2", parametre={}, error=0.45, mse=256.0, mse_tr=45.0),
        lib.Metrics(modele="3", parametre={}, error=0.67, mse=678.0, mse_tr=45.0),
        lib.Metrics(modele="4", parametre={}, error=0.1, mse=123.0, mse_tr=45.0),
        lib.Metrics(modele="5", parametre={}, error=0.6, mse=456.0, mse_tr=45.0),
    ]

    attendu_error = lib.Modele("3", {})
    attendu_mse = lib.Modele("1", {})

    assert lib.meilleur_modele(resultats=entree, by="error") == attendu_error
    assert lib.meilleur_modele(resultats=entree, by="mse") == attendu_mse


"""def test_traite_na():
    'Supprime doublons par la var ID'
    columns = ['prix', 'livraison', 'etat', 'retour', 'memoire', 'console', 'manette', 'cable', 'nbjeu', 'edition']
    rows_entree = [
        [780.0, 19.9, 'Neuf', 'Oui', 4.0, 'Xbox 360', np.nan, 'oui', 2, 'non'],
        [65.0, 5.0, 'Occasion', 'Non', 4.0, 'Xbox 360', np.nan, 'oui', 2, 'non'],
        [65.0, 5.0, 'Occasion', 'Non', np.nan, 'Xbox 360', 'oui', 'oui', 2, 'non'],
        [65.0, 5.0, 'Occasion', 'Non', 3.0, 'Xbox 360', 'non', 'oui', 3, 'non'],
        [780.0, 19.9, 'Neuf', 'Oui', 1.0, 'PS3', np.nan, 'oui', 4, 'non'],
        [65.0, 5.0, 'Occasion', 'Non', 1.0, 'PS3', np.nan, 'oui', 3, 'non'],
        [65.0, 5.0, 'Occasion', 'Non', 5.0, 'PS3', 'oui', 'oui', 4, 'non'],
        [65.0, 5.0, 'Occasion', 'Non', np.nan, 'PS3', 'non', 'oui', 4, 'non']
    ]
    rows_attendu = [
        [780.0, 19.9, 'Neuf', 'Oui', 4.0, 'Xbox 360', 'oui', 'oui', 2, 'non'],
       [65.0, 5.0, 'Occasion', 'Non', 4.0, 'Xbox 360', 'oui', 'oui', 2, 'non'],
       [65.0, 5.0, 'Occasion', 'Non', 3.0, 'Xbox 360', 'oui', 'oui', 2, 'non'],
       [65.0, 5.0, 'Occasion', 'Non', 3.0, 'Xbox 360', 'non', 'oui', 3, 'non'],
       [780.0, 19.9, 'Neuf', 'Oui', 1.0, 'PS3', 'oui', 'oui', 4, 'non'],
       [65.0, 5.0, 'Occasion', 'Non', 1.0, 'PS3', 'oui', 'oui', 3, 'non'],
       [65.0, 5.0, 'Occasion', 'Non', 5.0, 'PS3', 'oui', 'oui', 4, 'non'],
       [65.0, 5.0, 'Occasion', 'Non', 5.0, 'PS3', 'non', 'oui', 4, 'non']
    ]
    
    assert pd.DataFrame(data = rows_attendu, columns = columns).equals(lib.traite_NA_data(pd.DataFrame(data = rows_entree, columns = columns)))"""
