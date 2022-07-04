"""Test the exploratory data analysis-related functions for terpenes."""

import random
import pandas as pd

from matplotlib import figure, axes

import pytest

from napr.apps.coconut.terpene.explore import (
    _filter_subclasses,
    SUBCLASS_NAME,
    Plot,
)


def test_filter_subclasses(data):
    """Test the filter_subclasses function."""
    filtered = _filter_subclasses(data)
    unique_subclasses = filtered["chemicalSubClass"].unique()
    subclasses = [key for key in SUBCLASS_NAME.keys() if key != "other"]
    assert set(unique_subclasses) == set(subclasses)


def test_plot_dist_subclass_mw_logp_nplscore(data):
    """Test the plot_dist_subclass_mw_logp_nplscore function."""
    plot = Plot(data)
    fig, ax = plot.dist_subclass_mw_logp_nplscore()

    assert isinstance(fig, figure.Figure)
    for axis in ax:
        assert isinstance(axis, axes.Axes)

    assert len(ax) == 5


def test_plot_violin_mw_logp_nplscore(data):
    """Test the plot_violin_mw_logp_nplscore function."""
    plot = Plot(data)
    fig, ax = plot.violin_mw_logp_nplscore()

    assert isinstance(fig, figure.Figure)
    for axis in ax:
        assert isinstance(axis, axes.Axes)

    assert len(ax) == 3


def test_plot_lipinsky(data):
    """Test the plot_lipinsky function."""
    plot = Plot(data)
    fig, ax = plot.lipinsky()

    assert isinstance(fig, figure.Figure)
    for axis in ax:
        assert isinstance(axis, axes.Axes)

    assert len(ax) == 7


def test_plot_hbond(data):
    """Test the plot_hbond function."""
    plot = Plot(data)
    fig, ax = plot.hbond()

    assert isinstance(fig, figure.Figure)
    for axis in ax:
        assert isinstance(axis, axes.Axes)

    assert len(ax) == 14
