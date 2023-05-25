import requests

from bookify.exceptions import DownloadFailedException


def download_html_from_url(url: str, *, timeout: int = 10) -> str:
    response = requests.get(url, timeout=timeout)

    if response.status_code != 200:
        raise DownloadFailedException(f"Could not download data from '{url}'")

    return response.text
