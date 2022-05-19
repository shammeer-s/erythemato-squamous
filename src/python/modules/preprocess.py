# Created by Samar on 20-05-2022
# Filename: preprocess.py

from random import *

import pandas as pd
from sklearn.model_selection import train_test_split


class data:
    def __init__(self, raw):
        self.raw = raw
        self.features = list(self.raw.columns)
        self.data = None
        self.correlated_features = None
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None
        self.x = None
        self.y = None

    def imputer(self, method="mean"):
        self.raw.replace(to_replace="?", value=None, inplace=True)
        if method == "mean":
            self.raw["Age_linear"] = self.raw["Age_linear"].fillna(self.raw["Age_linear"].mean())
            print("Mean Imputation")
        elif method == "median":
            self.raw["Age_linear"] = self.raw["Age_linear"].fillna(self.raw["Age_linear"].median())
            print("Median Imputation")
        self.raw.to_csv(r"../../input/dataset.csv", index=False)
        print("Dataset is saved at 'input --> dataset.csv'", end="\n\n")

    def correlation(self, method="polychoric", exclude_limits=None, verbose=1):
        if exclude_limits is None:
            exclude_limits = [-0.1, 0.1]
        if method == "polychoric":
            if verbose != 0:
                print("Polychoric correlation is applied", end="\n\n")
            correlation = pd.read_csv("../../input/feature info.csv", index_col=0)

            # Selecting correlated columns
            correlation = correlation.loc[(correlation["Correlation"] <= exclude_limits[0]) | (correlation["Correlation"] >= exclude_limits[1]), :]
            cols = correlation.index
            if verbose != 0:
                print("Highly correlated features")
                if verbose >= 2:
                    print(cols, end="\n\n")

            if verbose != 0:
                print("Features and correlated features have been updated", end="\n\n")
            self.correlated_features = cols
            self.features = cols
            self.data = self.raw.loc[:, self.correlated_features | ['disease']]
            return self.data

    def split(self, random_state=None, stratify=True, size=None):
        if random_state is None:
            random_state = randint(1, 100)
        print("Data is getting split into train and test sets", end="\n\n")
        if size is None:
            size = [0.8, 0.2]

        # Dependent and independent variables separation
        self.x = self.data.loc[:, self.features]
        self.y = self.data.loc[:, 'disease']

        # Train test split
        if stratify:
            self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, stratify=self.y, random_state=random_state, test_size=size[1])
        else:
            self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, random_state=random_state, test_size=size[1])
