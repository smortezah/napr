"""Utility functions for working with data."""

import os
import re
from tqdm import tqdm
import requests

CURR_DIR = os.getcwd()


def download(url: str, path: str = CURR_DIR, chunk_size: int = 1024) -> None:
    """Download a file from a URL."""
    try:
        responce = requests.get(url, stream=True)
        responce.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise SystemExit(exc) from exc

    # fmt: off
    if 'content-disposition' in responce.headers:
        dispos = responce.headers['content-disposition']
        file_name = re.findall("filename=\"(.+)\"", dispos)[0]

    # fmt: on
    if os.path.isdir(path):
        file_name = "tmp"
        file_path = os.path.join(path, file_name)
    else:
        file_name = os.path.basename(path)
        file_path = path

    file_size = int(responce.headers.get("content-length", 0))
    progress_bar = tqdm(
        desc=f"Downloading {file_name}",
        total=file_size,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    )

    with progress_bar, open(file_path, "wb") as file:
        for data in responce.iter_content(chunk_size=chunk_size):
            size = file.write(data)
            progress_bar.update(size)
