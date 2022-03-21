"""Test the exploratory data analysis related functions for terpenes."""

import random
import pandas as pd

import matplotlib.pyplot as plt

import pytest

from napr.apps.coconut.terpene.explore import (
    _filter_subclasses,
    SUBCLASS_NAME,
    plot_dist_subclass_mw_logp_nplscore,
    plot_violin_mw_logp_nplscore,
    plot_lipinsky,
    plot_hbond,
)


@pytest.fixture(scope="module")
def data():
    """Return the data for the tests."""
    chemicalSubClass_21_3 = [
        "Diterpenoids",
        "Cholestane steroids",
        "Terpene glycosides",
        "Triterpenoids",
        "Sesquiterpenoids",
        "Monoterpenoids",
        "Eicosanoids",
        "Pregnane steroids",
        "Terpene lactones",
        "Steroidal glycosides",
        "Phosphosphingolipids",
        "Ergostane steroids",
        None,
        "Steroid esters",
        "Fatty acids and conjugates",
        "Steroid lactones",
        "Sesterterpenoids",
        "Fatty acyl glycosides",
        "Glycerophosphoethanolamines",
        "Gorgostanes and derivatives",
        "Fatty alcohols",
        "Fatty amides",
        "Fatty acyl thioesters",
        "Tetraterpenoids",
        "Oxosteroids",
        "Monoradylglycerols",
        "Steroidal alkaloids",
        "Diradylglycerols",
        "Cucurbitacins",
        "Glycerophosphocholines",
        "Glycosphingolipids",
        "Fatty acid esters",
        "Stigmastanes and derivatives",
        "Quinone and hydroquinone lipids",
        "Glycerophosphoglycerophosphoglycerols",
        "Cycloartanols and derivatives",
        "Bile acids, alcohols and derivatives",
        "Glycerol vinyl ethers",
        "Glycerophosphoinositols",
        "Steroid acids",
        "Hydroxysteroids",
        "Fatty aldehydes",
        "Lineolic acids and derivatives",
        "Triradylcglycerols",
        "Fatty alcohol esters",
        "Glycerophosphoserines",
        "Hopanoids",
        "Glycerophosphoglycerols",
        "Androstane steroids",
        "Polyprenols",
        "Glycosylglycerols",
        "Estrane steroids",
        "Sesquaterpenoids",
        "Delta-7-steroids",
        "Glycerophosphoinositol phosphates",
        "17-furanylsteroids and derivatives",
        "Ecdysteroids",
        "Furostanes and derivatives",
        "Glycerophosphoglycerophosphates",
        "Ceramides",
        "Vitamin D and derivatives",
        "Azasteroids and derivatives",
        "Retinoids",
        "Sulfated steroids",
        "Furospirostanes and derivatives",
        "Physalins and derivatives",
        "Acyltrehaloses",
        "Polyterpenoids",
        "Delta-5-steroids",
        "Glycerophosphates",
        "Isoprenoid phosphates",
        "5,6-epoxysteroids",
        "CDP-glycerols",
        "C24-propyl sterols and derivatives",
        "Polyprenylphenols",
        "Glycerol ethers",
        "Oxasteroids and derivatives",
        "Lysobisphosphatidic acids",
        "Semilysobisphosphatidic acids",
        "Glycerophosphonoethanolamines",
        "Halogenated steroids",
        "Glycero-3-pyrophosphates",
        "Phosphonosphingolipids",
        "Delta-1,4-steroids",
        "Glycerophosphonocholines",
    ]

    def gen_rand(N=len(chemicalSubClass_21_3)):
        return [random.random() for _ in range(N)]

    return pd.DataFrame(
        {
            "molecular_weight": gen_rand(),
            "alogp": gen_rand(),
            "npl_score": gen_rand(),
            "lipinskiRuleOf5Failures": gen_rand(),
            "hBondAcceptorCount": gen_rand(),
            "hBondDonorCount": gen_rand(),
            "chemicalSubClass": chemicalSubClass_21_3,
        }
    )


def test_filter_subclasses(data):
    """Test the filter_subclasses function."""
    filtered = _filter_subclasses(data)
    unique_subclasses = filtered["chemicalSubClass"].unique()
    subclasses = [key for key in SUBCLASS_NAME.keys() if key != "other"]
    assert set(unique_subclasses) == set(subclasses)


def test_plot_dist_subclass_mw_logp_nplscore(data):
    """Test the plot_dist_subclass_mw_logp_nplscore function."""
    fig, ax = plot_dist_subclass_mw_logp_nplscore(data)

    assert isinstance(fig, plt.Figure)
    for axis in ax:
        assert isinstance(axis, plt.Axes)

    assert len(ax) == 5


def test_plot_violin_mw_logp_nplscore(data):
    """Test the plot_violin_mw_logp_nplscore function."""
    fig, ax = plot_violin_mw_logp_nplscore(data)

    assert isinstance(fig, plt.Figure)
    for axis in ax:
        assert isinstance(axis, plt.Axes)

    assert len(ax) == 3


def test_plot_lipinsky(data):
    """Test the plot_lipinsky function."""
    fig, ax = plot_lipinsky(data)

    assert isinstance(fig, plt.Figure)
    for axis in ax:
        assert isinstance(axis, plt.Axes)

    assert len(ax) == 7


def test_plot_hbond(data):
    """Test the plot_hbond function."""
    with pytest.warns(DeprecationWarning):
        fig, ax = plot_hbond(data)

    assert isinstance(fig, plt.Figure)
    for axis in ax:
        assert isinstance(axis, plt.Axes)

    assert len(ax) == 14
