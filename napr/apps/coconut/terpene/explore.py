"""Exploratory data analysis of terpenes."""

import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import seaborn as sns

from napr.plotting import label_subplot

SUBCLASS_NAME = {
    'Monoterpenoids': 'Monoterpenes',
    'Sesquiterpenoids': 'Sesquiterpenes',
    'Diterpenoids': 'Diterpenes',
    'Triterpenoids': 'Triterpenes',
    'Terpene glycosides': 'Glycosides',
    'Terpene lactones': 'Lactones',
    'Sesterterpenoids': 'Sesterterpenes',
    'Sesquaterpenoids': 'Sesquaterpenes',
    'Polyterpenoids': 'Polyterpenes',
    'other': 'Other'
}


def _filter_subclasses(data: pd.DataFrame) -> pd.DataFrame:
    """Filter our sublasses of interest."""
    return data[data['chemicalSubClass'].isin(SUBCLASS_NAME.keys())]


def plot_dist_subclass_mw_logp_nplscore(
        data: pd.DataFrame,
        figsize: tuple[float, float] = (9, 8)
) -> tuple[mpl.figure.Figure, mpl.axes.Axes]:
    """Plot the distribution of subclasses, molecular weight, logP, and
    NPL-score.

    Args:
        data (pd.DataFrame): Data to plot.
        figsize (tuple[float, float], optional): (Width, height) in inches.
            Defaults to (9, 8).

    Returns:
        tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]: Figure and Axes.
    """
    mosaic = """
    AAABBB
    AAABBB
    AAABBB
    CCDDEE
    CCDDEE"""
    fig, ax_dict = plt.subplot_mosaic(mosaic=mosaic, figsize=figsize)
    ax = list(ax_dict.values())

    # Filter our subclasses of interest
    data = _filter_subclasses(data)

    # Subplot a
    def _get_pies_data(data):
        data_pie = data['chemicalSubClass'].value_counts()
        threshold = 2000
        # Small pie
        data_smallpie = data_pie[data_pie.values <= threshold]
        data_smallpie.sort_values(inplace=True)
        # Large pie
        data_largepie = pd.concat(
            [data_pie, pd.Series({'other': data_smallpie.sum()})])
        data_largepie.drop(list(data_smallpie.index), inplace=True)
        data_largepie.sort_values(inplace=True)
        return data_largepie, data_smallpie

    def _get_labels(data):
        return [f"{SUBCLASS_NAME[key]}\n({val})" for key, val in data.items()]

    def _plot_connect_pies(ax_a, ax_b, theta_b=250):
        """theta_b is the angle of the bottom connecting point of pie b."""
        # Pie a
        center_a, r_a = ax_a.patches[0].center, ax_a.patches[0].r
        theta1_a, theta2_a = ax_a.patches[0].theta1, ax_a.patches[0].theta2
        # Pie b
        center_b, r_b = ax_b.patches[0].center, ax_b.patches[0].r
        theta1_b, theta2_b = theta_b, -theta_b
        # Connecting line
        for th_a, th_b in [(theta1_a, theta1_b), (theta2_a, theta2_b)]:
            x_a = center_a[0] + r_a * np.cos(np.pi/180 * th_a)
            y_a = center_a[1] + r_a * np.sin(np.pi/180 * th_a)
            x_b = center_b[0] + r_b * np.cos(np.pi/180 * th_b)
            y_b = center_b[1] + r_b * np.sin(np.pi/180 * th_b)
            con = ConnectionPatch(
                xyA=(x_a, y_a), xyB=(x_b, y_b), coordsA='data', coordsB='data',
                axesA=ax_a, axesB=ax_b, linewidth=0.7)
            ax_b.add_artist(con)

    # Data
    data_largepie, data_smallpie = _get_pies_data(data)
    # Large pie chart
    ax[0].pie(
        data_largepie.values, labels=_get_labels(data_largepie),
        startangle=-1./360*data_largepie.values[0], autopct='%.0f%%',
        explode=[0.1]+[0]*(len(data_largepie)-1),
        colors=sns.color_palette('Set2', n_colors=len(data_largepie)))
    # Small pie chart
    ax[1].pie(
        data_smallpie.values, labels=_get_labels(data_smallpie),
        startangle=-25, autopct='%.0f%%', radius=0.55,
        textprops={'size': 'smaller'},
        colors=sns.color_palette('light:#66c2a5', n_colors=len(data_smallpie)))
    # Connect pie charts
    _plot_connect_pies(ax_a=ax[0], ax_b=ax[1])

    # Subplot b
    def _plot_hist(data, xlim, xlabel, ylabel, ax):
        num_bins = 30
        binwidth = (xlim[1]-xlim[0])/num_bins if xlim else None
        sns.histplot(
            data=data, ax=ax, binwidth=binwidth, edgecolor='#40a0ff',
            color='#40a0ff', alpha=0.5, kde=False, linewidth=1)
        ax.set(xlim=xlim, xlabel=xlabel, ylabel=ylabel)

    def _plot_table(data, bbox, ax):
        table = ax.table(
            cellText=[(i, f"{v:.1f}") for i, v in data.items()], bbox=bbox)
        # Format
        table.auto_set_font_size(False)
        table.set_fontsize(8.5)
        for (row, col), cell in table.get_celld().items():
            cell.set_edgecolor('#ffc17a')
            if row == 0 or col < 0:
                cell.set_facecolor('#fff5e8')
            else:
                row_colors = ['#fff5e8', 'white']
                cell.set_facecolor(row_colors[row % len(row_colors)])
            if col == 0:
                cell.set_text_props(ha='left')

    def _plot_hist_table(
            data, ax, xlim=None, xlabel=None, ylabel=None, bbox=None):
        _plot_hist(data=data, ax=ax, xlim=xlim, xlabel=xlabel, ylabel=ylabel)
        _plot_table(data=data.describe()[1:], ax=ax, bbox=bbox)

    # Molecular weight
    _plot_hist_table(
        data=data['molecular_weight'], ax=ax[2], xlim=(0, 2000),
        xlabel='Molecular weight', ylabel='Count',
        bbox=(0.47, 0.54, 0.5, 0.46))
    # logP
    _plot_hist_table(
        data=data['alogp'], ax=ax[3], xlim=(-12, 20), xlabel='logP',
        ylabel='', bbox=(0.6, 0.54, 0.4, 0.46))
    # Natural product-likeness score
    _plot_hist_table(
        data=data['npl_score'], ax=ax[4], xlim=(-1, 4),
        xlabel='Natural product-likeness score', ylabel='',
        bbox=(0.08, 0.54, 0.4, 0.46))

    # Label and adjust subplots
    label_subplot(fig=fig, ax=ax[0], label='a', translate=(-0.6, -0.3))
    label_subplot(fig=fig, ax=ax[2], label='b', translate=(-0.6, -0.1))
    fig.subplots_adjust(wspace=1, hspace=-0.05)

    return fig, ax


def plot_violin_mw_logp_nplscore(
    data: pd.DataFrame,
    figsize: tuple[float, float] = (8.5, 3.5)
) -> tuple[mpl.figure.Figure, mpl.axes.Axes]:
    """Plot the distribution of molecular weight, logP and NPL-score for each
    terpene subclass.

    Args:
        data (pd.DataFrame): Data to plot.
        figsize (tuple[float, float], optional): (Width, height) in inches.
            Defaults to (8.5, 3.5).

    Returns:
        tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]: Figure and Axes.
    """
    fig, ax = plt.subplots(1, 3, figsize=figsize, sharey=True)

    # Filter our subclasses of interest
    data = _filter_subclasses(data)

    # Data
    feat_subclass = 'chemicalSubClass'
    top_subclasses = data[feat_subclass].value_counts()[:6].index
    data_filtered = data[data[feat_subclass].isin(top_subclasses)]

    # Plot
    def _plot_violin(
            data, x, y, ax, xlim, xlabel, ylabel, order,
            yticklabels=[SUBCLASS_NAME[i] for i in top_subclasses]):
        # Violin
        sns.violinplot(
            data=data, x=x, y=y, ax=ax, order=order, scale='width', inner=None,
            palette=sns.color_palette('Dark2'), linewidth=1.2)
        # Mean
        mean = data.groupby(y)[x].mean()
        sns.stripplot(
            x=mean, y=mean.index, ax=ax, order=order, jitter=False,
            color='white', marker='o', size=4)
        # Axes
        ax.set(
            xlim=xlim, xlabel=xlabel, ylabel=ylabel, yticklabels=yticklabels)

    order = list(top_subclasses)
    # Molecular weight
    _plot_violin(
        data=data_filtered, x='molecular_weight', y=feat_subclass, ax=ax[0],
        xlim=(0, 2000), xlabel='Molecular weight', ylabel='Terpene subclass',
        order=order)
    # logP
    _plot_violin(
        data=data_filtered, x='alogp', y=feat_subclass, ax=ax[1],
        xlim=(-12, 20), xlabel='logP', ylabel='', order=order)
    # Natural product-likeness score
    _plot_violin(
        data=data_filtered, x='npl_score', y=feat_subclass, ax=ax[2],
        xlim=(-1, 4), xlabel='Natural product-likeness score', ylabel='',
        order=order)

    # Label and adjust subplots
    label_subplot(fig=fig, ax=ax[0], label='a', translate=(-1.05, 0))
    label_subplot(fig=fig, ax=ax[1], label='b', translate=(-0.25, 0))
    label_subplot(fig=fig, ax=ax[2], label='c', translate=(-0.25, 0))
    fig.tight_layout()

    return fig, ax


def plot_lipinsky(
    data: pd.DataFrame,
    figsize: tuple[float, float] = (6, 8)
) -> tuple[mpl.figure.Figure, mpl.axes.Axes]:
    """Plot the Lipinsky's rule of five violations

    Args:
        data (pd.DataFrame): Data to plot.
        figsize (tuple[float, float], optional): (Width, height) in inches.
            Defaults to (6, 8).

    Returns:
        tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]: Figure and Axes.
    """
    fig = plt.figure(figsize=figsize)
    nrow, ncol = 3, 3

    # Filter our subclasses of interest
    data = _filter_subclasses(data)

    feat_subclass = 'chemicalSubClass'
    top_subclasses = data[feat_subclass].value_counts()[:6].index
    data_filtered = data[data[feat_subclass].isin(top_subclasses)]

    # Subplot a
    # Axes
    ax = [plt.subplot2grid(shape=(nrow, ncol), loc=(0, 0), colspan=3)]
    b_left, b_bottom, b_width, b_height = ax[-1].get_position().bounds
    ax[-1].set_position([
        b_left+b_width/10, b_bottom+b_height/5, 0.9*b_width, b_height])
    # Data
    feat_lipinsky = 'lipinskiRuleOf5Failures'
    counts_lipinsky = data_filtered[feat_lipinsky].value_counts()
    # Plot
    sns.countplot(
        data=data_filtered, x=feat_lipinsky, order=counts_lipinsky.index,
        edgecolor='black', palette=sns.color_palette('blend:white,darkred'),
        ax=ax[-1])
    ax[-1].set(xlabel='', ylabel='Count')
    ax[-1].set_title(
        'Number of Lipinski\'s rule of five violations', loc='center')
    ax[-1].bar_label(
        container=ax[-1].containers[0],
        labels=[f"{100 * val/len(data_filtered):.0f}%"
                for val in counts_lipinsky.values])

    # Subplot b
    def _plot_spider(data, ax, xticklabels, title, color):
        # Angles of starting points of sectors
        N = len(xticklabels)
        angles = [2 * np.pi * n/float(N) for n in range(N)]
        angles += angles[:1]
        # The first sector starts from the top (pi/2)
        ax.set_theta_offset(np.pi / 2)
        # Sectors direction is clockwise
        ax.set_theta_direction(-1)
        # xticks. Number of violations
        plt.xticks(
            ticks=angles[:-1], labels=xticklabels, size=9, position=(0.1, 0.1))
        # yticks. Values for smaller circles
        ax.set_rlabel_position(-90)
        yticklabels = np.arange(20, 100, step=20)
        plt.yticks(
            ticks=[t-1 for t in yticklabels],
            labels=[str(l) for l in yticklabels],
            color='#404040', size=7.5)
        plt.ylim(0, 80)
        # Main plot
        ax.plot(angles, data, color=color, linewidth=1.5, linestyle='solid')
        ax.fill(angles, data, color=color, alpha=0.7)
        # Title
        plt.title(title, y=1.1, color='black', size=11, loc='center')

    # Data
    df = 100 * pd.crosstab(
        data_filtered[feat_subclass], data_filtered[feat_lipinsky],
        normalize='index')
    df = df.reindex(list(top_subclasses)).reset_index()
    df[feat_subclass] = df[feat_subclass].map(SUBCLASS_NAME)
    # Plot
    colormap = plt.cm.get_cmap('Dark2', len(df))
    for i in range(len(df)):
        # Axes
        ax.append(fig.add_subplot(nrow, ncol, i+4, polar=True))
        # Data
        values = df.loc[i].drop(feat_subclass).values.flatten().tolist()
        values += values[:1]
        # Plot
        _plot_spider(
            data=values, ax=ax[-1], xticklabels=list(df)[1:],
            title=df[feat_subclass][i], color=colormap(i))

    # Label subplots
    label_subplot(fig=fig, ax=ax[0], label='a', translate=(-0.6, 0.15))
    label_subplot(fig=fig, ax=ax[1], label='b', translate=(-0.1, 0.27))

    return fig, ax


def plot_hbond(
    data: pd.DataFrame,
    figsize: tuple[float, float] = (7, 10)
) -> tuple[mpl.figure.Figure, mpl.axes.Axes]:
    """Plot the distribution of hydrogen bond acceptors and donors.

    Args:
        data (pd.DataFrame): Data to plot.
        figsize (tuple[float, float], optional): (Width, height) in inches.
            Defaults to (7, 10).

    Returns:
        tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]: Figure and Axes.
    """
    fig, ax = plt.subplots(
        7, 2, figsize=figsize, gridspec_kw={
            'width_ratios': [1.5, 1],
            'height_ratios': [1.5, 1, 1, 1, 1, 1, 1]})
    ax = ax.flatten()

    # Data
    # Filter our subclasses of interest
    data = _filter_subclasses(data)

    feat_subclass = 'chemicalSubClass'
    top_subclasses = data[feat_subclass].value_counts()[:6].index
    data_filtered = data[data[feat_subclass].isin(top_subclasses)]

    # Plot
    def _bar_label(ax, full_data):
        # Write 0% when there is no bar
        np.nan_to_num(ax.containers[0].datavalues, copy=False)
        ax.bar_label(
            container=ax.containers[0], fontsize=8.5, padding=1,
            labels=[f"{100 * val/len(full_data):.0f}%"
                    for val in ax.containers[0].datavalues])

    def _plot(data, feature, upper, color, title, ylabel, ax):
        # Data
        data_filtered = data[data[feature] <= upper]
        counts = data_filtered[feature].value_counts(sort=False)
        for i in range(upper+1):
            if i not in counts.index:
                counts.loc[i] = 0
        counts = counts.sort_index()
        # Plot
        sns.countplot(
            data=data_filtered, x=feature, order=counts.index, ax=ax,
            color=color, edgecolor='black', linewidth=1)
        ax.set(xlabel='', ylabel=ylabel)
        ax.set_title(title, loc='center', fontsize=10.5)
        _bar_label(ax=ax, full_data=data)

    color = sns.color_palette('Dark2', n_colors=8)
    for i, (feature, upper) in enumerate(
            zip(['hBondAcceptorCount', 'hBondDonorCount'], [10, 5])):
        # Subplots a, b
        _plot(
            data=data_filtered, feature=feature, upper=upper,
            color=color[-1-i], title='Terpenes', ylabel='' if i else 'Count',
            ax=ax[i])
        # Subplots c, d
        for j, subclass in enumerate(top_subclasses):
            _plot(
                data=data_filtered[data_filtered[feat_subclass] == subclass],
                feature=feature, upper=upper, color=color[j],
                title=SUBCLASS_NAME[subclass], ylabel='' if i else 'Count',
                ax=ax[2+i+2*j])
    ax[12].set_xlabel('Hydrogen bond acceptor')
    ax[13].set_xlabel('Hydrogen bond donor')

    # Labels and layout
    label_subplot(fig=fig, ax=ax[0], label='a', translate=(-0.55, 0.15))
    label_subplot(fig=fig, ax=ax[1], label='b', translate=(-0.35, 0.15))
    label_subplot(fig=fig, ax=ax[2], label='c', translate=(-0.55, 0.15))
    label_subplot(fig=fig, ax=ax[3], label='d', translate=(-0.35, 0.15))
    fig.tight_layout()

    return fig, ax
