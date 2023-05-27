import requests

from bookify.article.custom_types import HTML
from bookify.exceptions import DownloadFailedException


def download_html_from_url(url: str, *, timeout: int = 10) -> HTML:
    response = requests.get(url, timeout=timeout)

    if response.status_code != 200:
        raise DownloadFailedException(f"Could not download data from '{url}'")

    return HTML(response.text)
