"""The base class for terpenes."""

from typing import Optional

import pandas as pd

from napr import plotting
from . import explore
from .preprocessing import Preprocess, DimReduce
from napr.utils.decorators import info


class Terpene:
    """The Terpene class."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

        # Default plot style is 'ggplot_classic'
        plotting.set_plt_style()
        self.plot = explore.Plot(self.data)

    @info(message="Data preprocessing")
    def preprocess(self, **kwargs) -> None:
        """Preprocessing the terpene data.

        Args:
            **kwargs:
                random_state: The random state for train_test_split. Defaults to
                    777.
                unknown_value: The unknown value for encoding. Defaults to 9999.
                dropped_columns: The dropped columns.
                target_columns: The target columns. Defaults to
                    ['chemicalSubClass'].
        """
        preprocessor = Preprocess(data=self.data)
        self.data = preprocessor.preprocess(**kwargs)

    @info(message="Dimension reduction")
    def dim_reduce(
        self, inplace: bool = True, **kwargs
    ) -> Optional[pd.DataFrame]:
        """Dimension reduction of the terpene data.

        Args:
            inplace: Whether to perform the dimension reduction inplace.
            **kwargs:
                model: The model to use for dimension reduction. Defaults to PCA
                    keeping 95% of the variance.

        Returns:
            pd.DataFrame|None: The dimension reduced data, or None if inplace is
                True.
        """
        dim_reducer = DimReduce(data=self.data)
        if inplace:
            self.data = dim_reducer.dim_reduce(**kwargs)
        else:
            return dim_reducer.dim_reduce(**kwargs)
