"""Utilities for the terpene data."""

import pandas as pd

from napr.plotting import set_plt_style
from ._plot import (
    _plot_dist_subclass_mw_logp_nplscore,
    _plot_violin_mw_logp_nplscore,
    _plot_lipinsky,
    _plot_hbond
)


class Terpene():
    """The Terpene class."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

        # Default plot style is 'ggplot_classic'
        set_plt_style()

    def plot_dist_subclass_mw_logp_nplscore(self):
        """Plot the distribution of terpene subclasses, molecular weight, logP
        and NPL-score.
        """
        return _plot_dist_subclass_mw_logp_nplscore(self.data)

    def plot_violin_mw_logp_nplscore(self):
        """Plot the distribution of molecular weight, logP and NPL-score for
        each terpene subclass.
        """
        return _plot_violin_mw_logp_nplscore(self.data)

    def plot_lipinsky(self):
        """Plot the Lipinsky's rule of five violations."""
        return _plot_lipinsky(self.data)

    def plot_hbond(self):
        """Plot the distribution of hydrogen bond acceptors and donors."""
        return _plot_hbond(self.data)
