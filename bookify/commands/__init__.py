import typer
from typing_extensions import Annotated, Never

from bookify.article.models import Article
from bookify.db import Base, engine
from bookify.download import download_html_from_url
from bookify.logger import log
from bookify.parse import ParseHTML


def convert_command(
    urls: Annotated[
        list[str],
        typer.Argument(help="Provide list of URLs or path to file"),
    ],
    name: Annotated[
        str,
        typer.Option("--name", help="Name of the book"),
    ],
) -> None | Never:
    Base.metadata.create_all(engine)

    for count, url in enumerate(urls):
        article = Article.get_by_url(url)

        if article:
            parser = ParseHTML(article.html)
        else:
            html = download_html_from_url(url)
            parser = ParseHTML(html, name=name, count=count)
            article = Article.create(url=url, html=html, title=parser.get_title())

            log.info(f"Uploaded {url} to the database")

        parser.convert_to_markdown()
