"""Tools for COCONUT data."""

from pathlib import Path

import pandas as pd
from pandas.core.frame import DataFrame

from napr import network


def load_terpene(
    download: bool = False, path: Path = network.CURR_DIR, version: str = "21.3"
) -> pd.DataFrame:
    """Loading the terpene dataset.

    If download=True, the data will be downloaded first.

    Args:
        download: If the data should be downloaded or loaded from local machine.
            Defaults to False.
        path: The path to save/load the data. Defaults to current directory.
        version: Version of the data. Defaults to "21.3".

    Raises:
        ValueError: if version is not in ["21.3"].
        FileNotFoundError: if download=False and the data in path is not found.

    Returns:
        The terpene data
    """
    if version not in ["21.3"]:
        raise ValueError(f"Version {version} not supported.")

    path = Path(path)

    if path.is_dir():
        path = path / f"terpene-{version}.bz2"

    if download:
        if version == "21.3":
            url = "https://drive.google.com/u/0/uc?id=1HFjVme274zL1r7Cr_0q-RrMoZebbGekJ&export=download"
        network.download(url=url, path=path)
    else:
        if not path.exists():
            raise FileNotFoundError(f"File {path} not found.")

    data: DataFrame = pd.read_csv(
        path,
        index_col=0,
        low_memory=False,
        compression="infer",
    )
    return data
