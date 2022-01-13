#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Procédure de test pour modele.py"""

import pytest
import pandas as pd
import sys

sys.path.append(
    "C:\\Users\\Lucas\\Documents\\M2\\Python\\Projet\\version_propre\\Machine_learning"
)
import modele as lib
from sklearn.ensemble import RandomForestRegressor


def test_est_valide():
    parametre = {
        "bootstrap": True,
        "max_depth": 100,
        "max_features": 20,
        "max_leaf_nodes": 100,
        "min_samples_leaf": 6,
        "min_samples_split": 4,
    }
    parametre_non_valide = {"dhsi": "HGTD", "bootstrap": True}
    lib._est_valide_(RandomForestRegressor(), parametre)
    with pytest.raises(ValueError):
        lib._est_valide_(RandomForestRegressor(), parametre_non_valide)
