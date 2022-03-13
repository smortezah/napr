"""The base class for terpenes."""

import pandas as pd

from napr.plotting import set_plt_style


class Terpene:
    """The Terpene class."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

        # Default plot style is 'ggplot_classic'
        set_plt_style()
