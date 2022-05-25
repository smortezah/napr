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
        self.target_columns = ["chemicalSubClass"]

    def preprocess(self, **kwargs):
        if "train_size" in kwargs:
            self.train_size = kwargs["train_size"]
        if "random_state" in kwargs:
            self.random_state = kwargs["random_state"]
        if "unknown_value" in kwargs:
            self.unknown_value = kwargs["unknown_value"]
        if "dropped_columns" in kwargs:
            self.dropped_columns = kwargs["dropped_columns"]
        if "target_columns" in kwargs:
            self.target_columns = kwargs["target_columns"]

        self._split_bcutDescriptor()

        # self._extract_tax()

        # train, test = train_test_split(
        #     self.data,
        #     train_size=self.train_size,
        #     random_state=self.random_state,
        # )

        # self._encode(train, test)

        # # Imputation
        # self._impute(train, test)

        # # Feature scaling
        # self._feature_scale(train, test)

        # # Concatenate train and test into self.data
        # self.data = pd.concat([train, test], axis=0)
        # self.data.sort_index(inplace=True)

        # print(self.data.info())
        # # Drop columns
        # self.data = self.data.drop(self.dropped_columns, axis=1)
        # print(self.data.info())
        return self.data

    def _split_bcutDescriptor(self):
        splitted = (
            self.data["bcutDescriptor"]
            .apply(lambda x: x[1:-1])
            .str.split(",", expand=True)
        )
        splitted.columns = ["bcutDescriptor_" + str(i) for i in range(6)]
        splitted.replace(["null", ""], np.nan, inplace=True)
        splitted = splitted.astype("float64")
        self.data = pd.concat([self.data, splitted], axis=1)

    def _extract_tax(self):
        for tax in ["plants", "marine", "bacteria", "fungi"]:
            self.data.loc[:, "textTaxa_" + tax] = (
                self.data["textTaxa"].str.contains(tax).astype("int64")
            )

    def _fit_transform(self, transformer, train, test, prefix: str = ""):
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

    def _encode(self, train, test):
        columns = ["directParentClassification"]
        encoder = OrdinalEncoder(
            handle_unknown="use_encoded_value", unknown_value=self.unknown_value
        )
        train[columns] = encoder.fit_transform(train[columns])
        test[columns] = encoder.transform(test[columns])

    def _impute(self, train, test):
        ignored_columns = self.dropped_columns + self.target_columns
        columns = train.columns[~train.columns.isin(ignored_columns)]
        imputer = SimpleImputer(strategy="median")
        train[columns] = imputer.fit_transform(train[columns])
        test[columns] = imputer.transform(test[columns])

    def _feature_scale(self, train, test):
        ignored_columns = (
            self.dropped_columns
            + self.target_columns
            + list(train.columns[train.columns.str.contains("textTaxa")])
            + ["contains_sugar"]
        )
        columns = train.columns[~train.columns.isin(ignored_columns)]
        scaler = StandardScaler()
        train[columns] = scaler.fit_transform(train[columns])
        test[columns] = scaler.transform(test[columns])
