"""Test the base plotting functions."""

import matplotlib as mpl
import matplotlib.pyplot as plt

from napr.plotting._base import (
    label_subplot,
    reset_plt_style,
    set_plt_style
)


def test_label_subplot():
    """Test the label_subplot function."""
    fig, ax = plt.subplots()
    label = label_subplot(fig, ax, 'a')

    assert label.get_text() == 'a'
    assert label.get_position() == (0, 1)


def test_plt_style():
    """Test the set_plt_style and reset_plt_style functions."""
    set_plt_style()
    assert mpl.rcParams != mpl.rcParamsDefault

    reset_plt_style()
    assert mpl.rcParams == mpl.rcParamsDefault

    set_plt_style('ggplot_bw')
    assert mpl.rcParams['axes.grid'] is True

    set_plt_style('dark_background')
    assert mpl.rcParams['axes.facecolor'] == 'black'
