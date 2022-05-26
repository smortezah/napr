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
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

        # Defaults
        self.random_state = 777
        self.unknown_value = 9999
        self.dropped_columns = [
            "_id",
            "coconut_id",
            "name",
            "iupac_name",
            "molecular_formula",
            "textTaxa",  # _extract_tax()
            "bcutDescriptor",  # _split_bcutDescriptor()
            "chemicalClass",
            "chemicalSuperClass",
        ]
        self.target_columns = ["chemicalSubClass"]

    def preprocess(self, **kwargs) -> pd.DataFrame:
        """Preprocess the terpene data.

        Args:
            **kwargs: Keyword arguments passed to preprocessing functions.

        Returns:
            pd.DataFrame: The preprocessed data.
        """
        if "random_state" in kwargs:
            self.random_state = kwargs["random_state"]
        if "unknown_value" in kwargs:
            self.unknown_value = kwargs["unknown_value"]
        if "dropped_columns" in kwargs:
            self.dropped_columns = kwargs["dropped_columns"]
        if "target_columns" in kwargs:
            self.target_columns = kwargs["target_columns"]

        self._split_bcutDescriptor()
        self._extract_tax()
        train, test = train_test_split(
            self.data,
            train_size=0.75,
            random_state=self.random_state,
        )
        self._encode(train, test)
        self._impute(train, test)
        self._feature_scale(train, test)

        self.data = pd.concat([train, test], axis=0)
        # self.data.sort_index(inplace=True)
        self.data.drop(self.dropped_columns, axis=1, inplace=True)
        return self.data

    def _split_bcutDescriptor(self) -> None:
        """Split the bcutDescriptor column into multiple columns and concatenate
        to the data."""
        splitted = (
            self.data["bcutDescriptor"]
            .apply(lambda x: x[1:-1])
            .str.split(",", expand=True)
        )
        splitted.columns = ["bcutDescriptor_" + str(i) for i in range(6)]
        splitted.replace(["null", ""], np.nan, inplace=True)
        splitted = splitted.astype("float64")
        self.data = pd.concat([self.data, splitted], axis=1)

    def _extract_tax(self) -> None:
        """Extract the taxonomy from the textTaxa column and concatenate to the
        data."""
        for tax in ["plants", "marine", "bacteria", "fungi"]:
            self.data.loc[:, "textTaxa_" + tax] = (
                self.data["textTaxa"].str.contains(tax).astype("int64")
            )

    def _encode(self, train: pd.DataFrame, test: pd.DataFrame) -> None:
        """Encode the data.

        Args:
            train (pd.DataFrame): The training data.
            test (pd.DataFrame): The testing data.
        """
        columns = ["directParentClassification"]

        encoder = OrdinalEncoder(
            handle_unknown="use_encoded_value", unknown_value=self.unknown_value
        )
        train[columns] = encoder.fit_transform(train[columns])
        test[columns] = encoder.transform(test[columns])

    def _impute(self, train: pd.DataFrame, test: pd.DataFrame) -> None:
        """Impute the data.

        Args:
            train (pd.DataFrame): The training data.
            test (pd.DataFrame): The testing data.
        """
        ignored_columns = self.dropped_columns + self.target_columns
        columns = train.columns[~train.columns.isin(ignored_columns)]

        imputer = SimpleImputer(strategy="median")
        train[columns] = imputer.fit_transform(train[columns])
        test[columns] = imputer.transform(test[columns])

    def _feature_scale(self, train: pd.DataFrame, test: pd.DataFrame) -> None:
        """Feature scale the data.

        Args:
            train (pd.DataFrame): The training data.
            test (pd.DataFrame): The testing data.
        """
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
