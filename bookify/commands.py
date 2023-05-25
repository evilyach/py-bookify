import typer
from sqlalchemy.orm import Session
from typing_extensions import Annotated, Never

from bookify.article.models import Article
from bookify.db import Base, engine
from bookify.download import download_html_from_url
from bookify.logger import log


def convert_command(
    urls: Annotated[
        list[str],
        typer.Argument(help="Provide list of URLs or path to file"),
    ],
) -> None | Never:
    if not urls:
        log.error("You provided no URLs...")

        raise typer.Exit(-1)

    Base.metadata.create_all(engine)

    for url in urls:
        article = Article.get_by_url(url)

        if not article:
            html = download_html_from_url(url)

            with Session(engine) as session:
                session.add(Article(url=url, html=html))
                session.commit()

            log.info(f"Uploaded {url} to the database")
