"""The base class for terpenes."""

import pandas as pd

from napr import plotting
from . import explore
from .preprocessing import Preprocessor


class Terpene:
    """The Terpene class."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

        # Default plot style is 'ggplot_classic'
        plotting.set_plt_style()
        self.plot = explore.Plot(self.data)

    def preprocess(self, **kwargs) -> None:
        """Preprocess the terpene data.

        Args:
            **kwargs:
                random_state: The random state for train_test_split.
                unknown_value: The unknown value for OrdinalEncoder.
                dropped_columns: The dropped columns.
                target_columns: The target columns.
        """
        preprocessor = Preprocessor(data=self.data)
        self.data = preprocessor.preprocess(**kwargs)
