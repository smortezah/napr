"""The base class for terpenes."""

import pandas as pd

from napr import plotting
from . import explore
from .preprocessing import DataCleanse, DimReduce
from napr.utils.decorators import info


class Terpene:
    """The Terpene class."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

        # Default plot style is 'ggplot_classic'
        plotting.set_plt_style()
        self.plot = explore.Plot(self.data)

    @info(message="Data cleansing")
    def data_cleanse(self, **kwargs) -> None:
        """Cleansing the terpene data.

        Args:
            **kwargs:
                random_state: The random state for train_test_split.
                unknown_value: The unknown value for encoding.
                dropped_columns: The dropped columns.
                target_columns: The target columns.
        """
        cleanser = DataCleanse(data=self.data)
        self.data = cleanser.data_cleanse(**kwargs)

    def dim_reduce(self, **kwargs) -> None:
        dim_reducer = DimReduce(data=self.data)
        self.data = dim_reducer.dim_reduce(**kwargs)
