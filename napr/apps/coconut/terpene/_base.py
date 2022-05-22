"""The base class for terpenes."""

import pandas as pd

from napr import plotting
from napr.apps.coconut.terpene import explore


class Terpene:
    """The Terpene class."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

        # Default plot style is 'ggplot_classic'
        plotting.set_plt_style()

        self.plot = explore.Plot(self.data)
