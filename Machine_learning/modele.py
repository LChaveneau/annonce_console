"""
Description.
Modèle de soutien a lib_modele.py créant la connexion entre utilisateur et sklearn
"""

import numpy as np
import pandas as pd
import re

from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import (
    LinearRegression,
    ElasticNet,
    ARDRegression,
    GammaRegressor,
    SGDRegressor,
    Lasso,
)
from sklearn.kernel_ridge import KernelRidge
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.cross_decomposition import PLSRegression, PLSCanonical
from sklearn.tree import DecisionTreeRegressor, ExtraTreeRegressor
from sklearn.ensemble import (
    RandomForestRegressor,
    ExtraTreesRegressor,
    GradientBoostingRegressor,
    AdaBoostRegressor,
)
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.model_selection import cross_val_score

MODELE_ACCEPTE = {
    "LinearRegression": LinearRegression(),
    "SVR": SVR(),
    "ElasticNet": ElasticNet(),
    "ARDRegression": ARDRegression(),
    "GammaRegressor": GammaRegressor(),
    "StochasticGradientDescent": SGDRegressor(),
    "Lasso": Lasso(),
    "KernelRidge": KernelRidge(),
    "KNN": KNeighborsRegressor(),
    "GaussianProcessRegressor": GaussianProcessRegressor(),
    "PLSRegression": PLSRegression(),
    "PLSCanonical": PLSCanonical(),
    "DecisionTreeRegressor": DecisionTreeRegressor(),
    "RandomForestRegressor": RandomForestRegressor(),
    "ExtraTreeRegressor": ExtraTreeRegressor(),
    "ExtraTreesRegressor": ExtraTreesRegressor(),
    "MLPRegressor": MLPRegressor(),
    "GradientBoostingRegressor": GradientBoostingRegressor(),
    "AdaBoostDecisionTreeRegressor": AdaBoostRegressor(
        base_estimator=DecisionTreeRegressor()
    ),
}


def _renvoie_apprentissage_(modele, parametre, data):
    """
    Créer et optimise si besoin un modèle.
    Renvoie:
        - un score
        - les paramètres optimaux
        - le mean squared error évalué par CrossValidation
        - le mean squared error de l'échantillon test
    """

    print(f"Construction du modèle {modele} ... Please wait ...")
    algo, parametre = _tri_(modele, parametre)
    X_tr, X_te, y_tr, y_te = _split_(data)
    if parametre:
        par = GridSearchCV(algo, param_grid=parametre, cv=7)
        par.fit(X_tr, y_tr)
        MSE = cross_val_score(
            estimator=algo.set_params(**par.best_params_),
            X=X_tr,
            y=y_tr,
            cv=7,
            scoring="neg_mean_squared_error",
        ).mean()
        MSE_tr = mean_squared_error(y_te, par.predict(X_te))
        score = par.best_score_
        parametre = par.best_params_
    else:
        par = algo.fit(X_tr, y_tr)
        score = cross_val_score(estimator=algo, X=X_tr, y=y_tr, cv=7).mean()
        MSE = cross_val_score(
            estimator=algo, X=X_tr, y=y_tr, scoring="neg_mean_squared_error", cv=7
        ).mean()
        MSE_tr = mean_squared_error(y_te, par.predict(X_te))
        parametre = None
    return parametre, float(score), -float(MSE), float(MSE_tr)


def _est_valide_(algo, parametre):
    """Check si la liste des paramètres est valide"""
    if parametre:
        for param in parametre.keys():
            if param not in algo.get_params().keys():
                raise ValueError(
                    f"Le parametre {param} du modèle {algo} n'est pas reconnu \n {algo} contient comme parametre {algo.get_params().keys()}"
                )


def _tri_(modele, parametre):
    """Check si le modèle est correct et est accepté et renvoie la class sklearn associé """
    if modele not in MODELE_ACCEPTE.keys():
        raise ValueError(
            "Le modèle est incorrect ou le modèle ne fait pas partie des modèles acceptés"
        )
    algo = MODELE_ACCEPTE[modele]
    if modele != "AdaBoostRegressor":
        _est_valide_(algo, parametre)
    return (algo, parametre)


def construit_meilleur_modele(modele, parametre, data):
    """
    Construction d'un modele.
    """
    _upload_class_(modele)

    algo, parametre = _tri_(modele, parametre)
    ohe = OneHotEncoder(drop="first")
    y = data.prix.to_numpy()
    X1 = data.iloc[:, [2, 3, 5, 6, 7, 9]].to_numpy()
    X2 = data.iloc[:, [1, 4, 8]].to_numpy()
    ohe.fit(X1)
    X1 = ohe.transform(X1).toarray()
    X = np.hstack([X2, X1])
    if parametre:
        machine = algo.set_params(**parametre)
    else:
        machine = algo
    return machine.fit(X, y)


def _upload_class_(modele):
    """import la fonction sklearn"""
    docstring = MODELE_ACCEPTE[modele].__doc__
    motif = re.compile(">>>.*(from sklearn\..*?)\n")
    doc, *_ = motif.findall(docstring)
    exec(doc)


def _split_(data):
    """Encode les variables modalités et création d'échantillon test et train"""
    ohe = OneHotEncoder(drop="first")
    ## Var à prédire
    y = data.prix.to_numpy()
    ##features
    X1 = data.iloc[:, [2, 3, 5, 6, 7, 9]].to_numpy()
    X2 = data.iloc[:, [1, 4, 8]].to_numpy()
    ohe.fit(X1)
    X1 = ohe.transform(X1).toarray()
    X = np.hstack([X2, X1])

    return train_test_split(X, y)
