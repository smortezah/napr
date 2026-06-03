"""Utility functions for plotting."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.text import Text
from matplotlib.transforms import ScaledTranslation


def label_subplot(
    fig: Figure, ax: Axes, label: str, translate: tuple[float, float] = (0, 0), **kwargs
) -> Text:
    """Label a subplot.

    Args:
        fig: The figure instance.
        ax: Axis of the subplot to label.
        label: Label of the subplot.
        translate: Translation of the label position, considering the figure's dpi.
            Defaults to (0, 0).
        **kwargs: Additional keyword arguments passed to Text.

    Returns:
        A label.
    """
    trans = ScaledTranslation(translate[0], translate[1], fig.dpi_scale_trans)
    text = ax.text(
        0, 1, label, transform=ax.transAxes + trans, fontsize=15, fontweight="bold", **kwargs
    )
    return text


def reset_plt_style() -> None:
    """Set matplotlib plot style to default."""
    plt.style.use("default")


def set_plt_style(style: str = "ggplot_classic") -> None:
    """Set matplotlib plot style.

    Args:
        style: Style sheet. Defaults to 'ggplot_classic'.
    """
    curr_dir = Path(__file__).parent
    if style == "ggplot_classic":
        stylesheet = curr_dir / "ggplot_classic.mplstyle"
    elif style == "ggplot_bw":
        stylesheet = curr_dir / "ggplot_bw.mplstyle"
    else:
        stylesheet = style

    plt.style.use(stylesheet)
