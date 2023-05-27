from pathlib import Path

import mdformat
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

from bookify.article.custom_types import HTML, Markdown
from bookify.article.exceptions import BadArticleException
from bookify.article.models import Article
from bookify.parse.exceptions import InvalidHTMLException


class ParseHTML:
    def __init__(
        self,
        article: Article,
        *,
        name: str = "",
        write_to_temp_files: bool = True,
        temp_files_dir: Path | None = None,
        count: int | None = None,
    ) -> None:
        self.article = article
        self.soup = BeautifulSoup(self.article.html, "html.parser")
        self.title = self.get_title()
        self.name = name
        self.write_to_temp_files = write_to_temp_files
        self.temp_files_dir = temp_files_dir or Path("output")
        self.count = count

        self.temp_files_dir.mkdir(parents=True, exist_ok=True)

    def get_title(self) -> str:
        if not (title_tag := self.soup.title):
            raise InvalidHTMLException("Title is invalid.")
        if not (title := title_tag.string):
            raise InvalidHTMLException("Can't parse title.")
        return title

    def get_content(self) -> HTML:
        if not (body := self.soup.body):
            raise InvalidHTMLException("Body is invalid")
        if not (content := body.find("div", {"class": "entry-content"})):
            raise InvalidHTMLException("Can't find content")

        return HTML(content)

    def get_filename(self) -> str:
        result = ""

        if self.count:
            result = f"{self.count}"

        if self.name:
            table = str.maketrans({" ": "-"})
            formatted_name = self.name.lower().translate(table)

            result = f"{result}-{formatted_name}"

        result = f"{result}-{self.title}" if result == "" else self.title

        return result

    def convert_to_markdown(self) -> Markdown:
        content = self.get_content()

        if not self.article.markdown:
            unformatted_markdown = MarkdownConverter(
                strip="footer",
                escape_asterisks=False,
                escape_underscores=False,
            ).convert(content)
            formatted_markdown = Markdown(
                mdformat.text(
                    unformatted_markdown,
                    codeformatters=("bash", "sh", "python", "json", "toml", "yaml"),
                )
            )

            self.article.update_markdown(formatted_markdown)

        if not self.article.markdown:
            raise BadArticleException("Wasn't able to get markdown from Article")

        if self.write_to_temp_files:
            filename = self.get_filename()

            with open(self.temp_files_dir / filename, "w", encoding="utf-8") as file:
                file.write(str(self.article.markdown))

        return self.article.markdown
