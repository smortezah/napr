"""Preprocessing terpenes data."""

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import (
    OrdinalEncoder,
    StandardScaler,
)
from sklearn.impute import SimpleImputer


class Preprocessor:
    def __init__(
        self,
        data: pd.DataFrame,
    ):
        self.data = data
        # Defaults
        self.train_size = 0.75
        self.random_state = 777
        self.unknown_value = 9999
        self.dropped_columns = [
            "_id",
            "coconut_id",
            "name",
            "iupac_name",
            "molecular_formula",
            "textTaxa",  # extract_tax()
            "bcutDescriptor",  # split_bcutDescriptor()
            "chemicalClass",
            "chemicalSuperClass",
            "directParentClassification",  # encode()
        ]

    def preprocess(self, **kwargs):
        if "train_size" in kwargs:
            self.train_size = kwargs["train_size"]
        if "random_state" in kwargs:
            self.random_state = kwargs["random_state"]
        if "unknown_value" in kwargs:
            self.unknown_value = kwargs["unknown_value"]
        if "dropped_columns" in kwargs:
            self.dropped_columns = kwargs["dropped_columns"]

        self.split_bcutDescriptor()

        # Categorical encoding
        self.extract_tax()
        train, test = train_test_split(
            self.data,
            train_size=self.train_size,
            random_state=self.random_state,
        )
        train, test = self.encode(
            train, test, columns=["directParentClassification"]
        )

        # Imputation

        # Feature scaling

        # Join train and test into self.data

        # Drop columns
        self.data.drop(self.dropped_columns, axis=1, inplace=True)

    def split_bcutDescriptor(self):
        splitted = (
            self.data["bcutDescriptor"]
            .apply(lambda x: x[1:-1])
            .str.split(",", expand=True)
        )
        splitted.columns = ["bcutDescriptor_" + str(i) for i in range(6)]
        splitted.replace(["null", ""], np.nan, inplace=True)
        splitted = splitted.astype("float64")
        self.data = pd.concat([self.data, splitted], axis=1)

    def extract_tax(self):
        for tax in ["plants", "marine", "bacteria", "fungi"]:
            self.data.loc[:, "textTaxa_" + tax] = (
                self.data["textTaxa"].str.contains(tax).astype("int64")
            )

    def encode(self, train, test, columns):
        encoder = OrdinalEncoder(
            handle_unknown="use_encoded_value", unknown_value=self.unknown_value
        )
        encoder.fit(train[columns])
        encoded_train = pd.DataFrame(
            encoder.transform(train[columns]),
            columns=["encoded_" + col for col in columns],
            index=train[columns].index,
        )
        encoded_test = pd.DataFrame(
            encoder.transform(test[columns]),
            columns=["encoded_" + col for col in columns],
            index=test[columns].index,
        )
        train = pd.concat([train, encoded_train], axis=1)
        test = pd.concat([test, encoded_test], axis=1)
        return train, test

    def impute(self, columns):
        imputer = SimpleImputer(strategy="median")

    def feature_scale(self, columns):
        scaler = StandardScaler()

    def transform(self, transformer, train, test, prefix: str = ""):
        if not prefix:
            columns = train.columns
        else:
            columns = [prefix + "_" + col for col in train.columns]

        transformer.fit(train)
        transformed_train = pd.DataFrame(
            transformer.transform(train),
            columns=columns,
            index=train.index,
        )
        transformed_test = pd.DataFrame(
            transformer.transform(test),
            columns=columns,
            index=test.index,
        )
        return transformed_train, transformed_test
