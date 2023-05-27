from pathlib import Path

import typer
from typing_extensions import Annotated

from bookify.article.models import Article
from bookify.db import Base, engine
from bookify.download import download_html_from_url
from bookify.logger import log
from bookify.parse import MarkdownParser
from bookify.parse.custom_types import ParseConfig, WebsiteConfig
from bookify.parse.websites import get_website_config


def convert_command(
    urls: Annotated[
        list[str],
        typer.Argument(
            help="Provide list of URLs or path to file",
        ),
    ],
    name: Annotated[
        str,
        typer.Option(
            "--name",
            help="Name of the book",
        ),
    ],
    use_temp_files: Annotated[
        bool,
        typer.Option(
            "--use-temp-files",
            help="Check if you want to save temporary files",
        ),
    ] = True,
    temp_files_dir: Annotated[
        str,
        typer.Option(
            "--temp-file-dir",
            help="Path to the directory where you want to save temporary files",
        ),
    ] = "output",
) -> None:
    Base.metadata.create_all(engine)

    parse_config = ParseConfig(
        use_temp_files=use_temp_files, temp_files_dir=Path(temp_files_dir)
    )

    for count, url in enumerate(urls):
        website_config = get_website_config(url, count=count, name=name)
        article = Article.get_by_url(url)

        if article:
            parser = MarkdownParser(article, parse_config, website_config)
        else:
            html = download_html_from_url(url)
            article = Article.create(url=url, html=html)

            parser = MarkdownParser(article, parse_config, website_config)
            log.info(f"Uploaded {url} to the database")

        parser.convert()
