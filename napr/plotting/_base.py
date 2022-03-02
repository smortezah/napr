"""Utility functions for plotting."""

import os

import matplotlib as mpl
import matplotlib.pyplot as plt


def label_subplot(
        fig: mpl.figure.Figure,
        ax: mpl.axes.Axes,
        label: str,
        translate: tuple[float, float] = (0, 0),
        **kwargs) -> mpl.text.Text:
    """Label a subplot.

    Args:
        fig (matplotlib.figure.Figure): The figure instance.
        ax (matplotlib.axes.Axes): Axis of the subplot to label.
        label (str): Label of the subplot.
        translate (tuple[float, float], optional): Translation of the label
            position, considering the figure's dpi. Defaults to (0, 0).
        **kwargs: Additional keyword arguments passed to Text.

    Returns:
        matplotlib.text.Text: An instance of Text.
    """
    trans = mpl.transforms.ScaledTranslation(
        translate[0], translate[1], fig.dpi_scale_trans)
    text = ax.text(
        0, 1, label, transform=ax.transAxes+trans, fontsize=15,
        fontweight='bold', **kwargs)
    return text


def reset_plt_style() -> None:
    """Set matplotlib plot style to default."""
    mpl.rcParams.update(mpl.rcParamsDefault)


def set_plt_style(style: str = 'ggplot_classic') -> None:
    """Set matplotlib plot style.

    Args:
        style (str, optional): Style sheet. Defaults to 'ggplot_classic'.
    """
    curr_dir = os.path.dirname(__file__)
    if style == 'ggplot_classic':
        stylesheet = os.path.join(curr_dir, 'ggplot_classic.mplstyle')
    elif style == 'ggplot_bw':
        stylesheet = os.path.join(curr_dir, 'ggplot_bw.mplstyle')
    else:
        stylesheet = style

    plt.style.use(stylesheet)
