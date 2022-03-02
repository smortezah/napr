"""Utility functions for working with data."""

import os
import re
from tqdm import tqdm
import requests

import pandas as pd

CURR_DIR = os.getcwd()


def _download(url: str, path: str = CURR_DIR, chunk_size: int = 1024) -> None:
    """Download a file from a URL."""
    try:
        responce = requests.get(url, stream=True)
        responce.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise SystemExit(exc) from exc

    file_size = int(responce.headers.get('content-length', 0))
    dispos = responce.headers['content-disposition']
    file_name = re.findall("filename=\"(.+)\"", dispos)[0]
    progress_bar = tqdm(
        desc=f"Downloading {file_name}", total=file_size, unit='iB',
        unit_scale=True, unit_divisor=1024)
    if os.path.isdir(path):
        file_path = os.path.join(path, file_name)
    else:
        file_path = path

    with progress_bar, open(file_path, 'wb') as file:
        for data in responce.iter_content(chunk_size=chunk_size):
            size = file.write(data)
            progress_bar.update(size)


def load_terpene(
        download: bool = False,
        path: str = CURR_DIR,
        version: str = '21.3') -> pd.DataFrame:
    """Loading the terpene dataset.

    If download=True, the data will be downloaded first.

    Args:
        download (bool, optional): If the data should be downloaded or loaded
            from local machine. Defaults to False.
        path (str, optional): The path to save/load the data. Defaults to
            current directory.
        version (str, optional): Version of the data. Defaults to "21.3".

    Raises:
        ValueError: if version is not in ["21.3"].
        FileNotFoundError: if download=False and the data in path
            is not found.

    Returns:
        pandas.DataFrame: The terpene data
    """
    if version not in ['21.3']:
        raise ValueError(f"Version {version} not supported.")

    if os.path.isdir(path):
        path = os.path.join(path, f"terpene-{version}.bz2")

    if not download:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File {path} not found.")
    else:
        if version == '21.3':
            url = 'https://drive.google.com/uc?id=1naoIB6yWvba-JY2UAvJln9t3Xh_f6C8p&export=download'
            _download(url=url, path=path)

    data = pd.read_csv(
        path, index_col=0, low_memory=False, compression='infer')
    return data
