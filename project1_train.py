# -*- coding: utf-8 -*-

# Import des modules pour le projet
import pandas as pd
import numpy as np
import os
import math
import pickle

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from scipy import stats
from sklearn.linear_model import LogisticRegression

from collections import Counter
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, f1_score

from sklearn.ensemble import RandomForestRegressor
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import chi2_contingency
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score, StratifiedKFold
import lightgbm as lgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.preprocessing import StandardScaler, OneHotEncoder
import warnings

from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.compose import make_column_transformer, make_column_selector
from sklearn.impute import SimpleImputer


def clean_rows(rains_data: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    """
    Remove column and rows that are not relevant for predictions
    """

    rains_data = rains_data.drop(["Date"], axis=1)
    rains_data = rains_data.drop(["Location"], axis=1)

    rains_data = rains_data.dropna(
        axis=0, how="any", subset=["RainToday", "RainTomorrow"]
    )

    # rains = rains.dropna(axis=0, how="any", subset=["Temp9am", "Temp3pm"])

    return rains_data


def get_preprocessor(X_train=None, y_train=None, create=False):
    """
    Return a preprocessing pipeline
    """

    # Load trained pipeline if exists
    if not create and os.path.exists("preprocessor"):

        with open("preprocessor", "rb") as file:
            preprocessor = pickle.load(file)

    # Create a preprocessing pipeline and save it
    else:

        # If data have not been provided retrieve
        # with get_data function
        if X_train is None or y_train is None:
            X_train, X_test, y_train, y_test = get_data()

        num = make_column_selector(dtype_include=np.number)
        cat = make_column_selector(dtype_exclude=np.number)

        num_pipeline = make_pipeline(
            SimpleImputer(strategy="mean"), StandardScaler()
        )
        cat_pipeline = make_pipeline(
            SimpleImputer(strategy="most_frequent"), OneHotEncoder()
        )

        preprocessor = make_column_transformer(
            (num_pipeline, num), (cat_pipeline, cat)
        )

        preprocessor.fit(X_train, y_train)

        with open("preprocessor", "wb") as file:
            pickle.dump(preprocessor, file)

    return preprocessor


def get_data():
    """
    Retrieve train and test data for rains dataset
    """

    # Chargement du fichier rains dans le dataframe rains
    rains = pd.read_csv(
        "https://assets-datascientest.s3-eu-west-1.amazonaws.com"
        + "/de/total/rains.csv"
    )

    rains = clean_rows(rains)

    X = rains.drop(["RainTomorrow"], axis=1)
    y = rains["RainTomorrow"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=2, stratify=y
    )

    return (
        X_train,
        X_test,
        y_train,
        y_test,
    )


def get_processed_data():
    """
    Return processed data to use for model training
    """

    X_train, X_test, y_train, y_test = get_data()

    preprocessor = get_preprocessor(X_train, y_train)

    X_train_processed = preprocessor.transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    return X_train_processed, X_test_processed, y_train, y_test


if __name__ == "__main__":

    X_train_processed, X_test_processed, y_train, y_test = get_processed_data()

    params_lgb = {
        "colsample_bytree": 0.95,
        "max_depth": 16,
        "min_split_gain": 0.1,
        "n_estimators": 200,
        "num_leaves": 50,
        "reg_alpha": 1.2,
        "reg_lambda": 1.2,
        "subsample": 0.95,
        "subsample_freq": 20,
    }

    models = [
        LogisticRegression(),
        LinearDiscriminantAnalysis(),
        KNeighborsClassifier(),
        GaussianNB(),
        DecisionTreeClassifier(),
        SVC(),
        lgb.LGBMClassifier(**params_lgb),
        RandomForestClassifier(n_estimators=100, max_depth=4, random_state=0),
    ]

    # Train models and save them to files
    for model in models:
        print(f"Model: {type(model).__name__}")
        model.fit(X_train_processed, y_train)
        print(model.score(X_test_processed, y_test))
        with open(f"{type(model).__name__}_trained", "wb") as file:
            pickle.dump(model, file)
