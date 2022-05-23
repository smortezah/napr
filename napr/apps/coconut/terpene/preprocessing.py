"""Preprocessing terpenes data."""

import numpy as np
import pandas as pd

import sklearn
from sklearn.model_selection import train_test_split


class Preprocessor:
    def __init__(
        self,
        data: pd.DataFrame,
    ):
        self.TRAIN_SIZE = 0.75
        self.RANDOM_STATE = 777

        self.data = data

        self.dropped_columns: list[str] = []

        self.preprocess()

    def preprocess(self):
        self.dropped_columns += [
            "_id",
            "coconut_id",
            "name",
            "iupac_name",
            "molecular_formula",
        ]

        # Categorical encoding
        self.extract_tax()
        self.split_bcutDescriptor()

        # Train-test split
        train, test = train_test_split(
            self.data,
            train_size=self.TRAIN_SIZE,
            random_state=self.RANDOM_STATE,
        )

    def extract_tax(self):
        for tax in ["plants", "marine", "bacteria", "fungi"]:
            self.data.loc[:, "textTaxa_" + tax] = (
                self.data["textTaxa"].str.contains(tax).astype("int64")
            )

        self.dropped_columns += ["textTaxa"]

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

        self.dropped_columns += ["bcutDescriptor"]
