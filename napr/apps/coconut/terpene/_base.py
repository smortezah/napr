"""The base class for terpenes."""

import pandas as pd

from napr.plotting import set_plt_style
from . import explore


class Terpene:
    """The Terpene class."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

        # Default plot style is 'ggplot_classic'
        set_plt_style()

    def plot_dist_subclass_mw_logp_nplscore(
        data: pd.DataFrame, figsize: tuple[float, float] = (9, 8)
    ) -> tuple[figure.Figure, list[axes.Axes]]:
        explore._plot_dist_subclass_mw_logp_nplscore(data, figsize)

    def plot_violin_mw_logp_nplscore(
        data: pd.DataFrame, figsize: tuple[float, float] = (8.5, 3.5)
    ) -> tuple[figure.Figure, list[axes.Axes]]:
        explore._plot_violin_mw_logp_nplscore(data, figsize)

    def plot_lipinsky(
        data: pd.DataFrame, figsize: tuple[float, float] = (6, 8)
    ) -> tuple[figure.Figure, list[axes.Axes]]:
        explore._plot_lipinsky(data, figsize)

    def plot_hbond(
        data: pd.DataFrame, figsize: tuple[float, float] = (7, 10)
    ) -> tuple[figure.Figure, list[axes.Axes]]:
        explore._plot_hbond(data, figsize)
