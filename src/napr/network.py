"""Network utility functions."""

import re
from pathlib import Path

import requests
from tqdm import tqdm

CURR_DIR = Path.cwd()


def download(url: str, path: Path = CURR_DIR, chunk_size: int = 1024) -> None:
    """Download a file from a URL."""
    if not url:
        raise ValueError("url must not be empty.")

    try:
        responce = requests.get(url, stream=True)
        responce.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise SystemExit(exc) from exc

    cd_file_name = None
    if "content-disposition" in responce.headers:
        dispos = responce.headers["content-disposition"]
        matches = re.findall('filename="(.+)"', dispos)
        if matches:
            cd_file_name = matches[0]

    if path.is_dir():
        file_name = cd_file_name or "tmp"
        file_path = path / file_name
    else:
        file_name = path.name
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
