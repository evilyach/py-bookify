from bs4 import BeautifulSoup

from bookify.article.custom_types import Markdown
from bookify.article.models import Article
from bookify.parse.custom_types import ParseConfig, WebsiteConfig
from bookify.parse.exceptions import InvalidHTMLException
from bookify.parse.helpers import get_filename


class MarkdownParser:
    def __init__(
        self,
        article: Article,
        parse_config: ParseConfig,
        website_config: WebsiteConfig,
    ) -> None:
        self.article = article
        self.parse_config = parse_config
        self.website_config = website_config

        self.soup = BeautifulSoup(self.article.html, self.parse_config.parser)

        self.convert_handler = self.website_config.convert_handler
        self.get_author_handler = self.website_config.get_author_handler

        self.html = self.article.html
        self.markdown = self.article.markdown

    def get_title(self) -> str:
        try:
            return self.soup.title.string  # type: ignore
        except TypeError as error:
            raise InvalidHTMLException("Can't parse title.") from error

    def convert(self) -> Markdown:
        self.parse_config.temp_files_dir.mkdir(exist_ok=True)

        if not self.markdown:
            self.markdown = self.convert_handler(self)
            self.article.update_markdown(self.markdown)

        if self.parse_config.use_temp_files:
            self.write_to_temp_files()

        return self.markdown

    def write_to_temp_files(self) -> None:
        path = self.parse_config.temp_files_dir / get_filename(
            self.website_config.count, self.website_config.name, self.get_title()
        )

        with open(path, "w", encoding="utf-8") as file:
            file.write(str(self.article.markdown))
