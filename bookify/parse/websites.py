from urllib.parse import urlsplit

import mdformat
from markdownify import MarkdownConverter

from bookify.article.custom_types import Markdown
from bookify.parse import MarkdownParser
from bookify.parse.custom_types import WebsiteConfig
from bookify.parse.exceptions import InvalidHTMLException


class DefaultHandler:
    @staticmethod
    def convert_handler(parser_obj: MarkdownParser) -> Markdown:
        content = parser_obj.soup.get_text()

        unformatted_markdown = MarkdownConverter(
            strip="footer",
            escape_asterisks=False,
            escape_underscores=False,
        ).convert(str(content))

        formatted_markdown = mdformat.text(
            unformatted_markdown,
            codeformatters=("bash", "sh", "python", "json", "toml", "yaml"),
        )

        return Markdown(formatted_markdown)

    @staticmethod
    def get_author_handler(_: MarkdownParser) -> str:
        raise NotImplementedError()


class TenThousandMetersHandler:
    @staticmethod
    def convert_handler(parser_obj: MarkdownParser) -> Markdown:
        if not (body := parser_obj.soup.body):
            raise InvalidHTMLException("Body is invalid")

        if not (content := body.find("div", {"class": "entry-content"})):
            raise InvalidHTMLException("Can't find content")

        unformatted_markdown = MarkdownConverter(
            strip="footer",
            escape_asterisks=False,
            escape_underscores=False,
        ).convert(str(content))

        formatted_markdown = mdformat.text(
            unformatted_markdown,
            codeformatters=("bash", "sh", "python", "json", "toml", "yaml"),
        )

        return Markdown(formatted_markdown)

    @staticmethod
    def get_author_handler(_: MarkdownParser) -> str:
        raise NotImplementedError()


def get_website_config(url: str, *, count: int, name: str) -> WebsiteConfig:
    normalized_url = urlsplit(url).netloc

    website_to_config = {
        "tenthousandmeters.com": TenThousandMetersHandler,
    }

    config = website_to_config.get(normalized_url, DefaultHandler)

    return WebsiteConfig(
        count=count,
        name=name,
        convert_handler=config.convert_handler,
        get_author_handler=config.get_author_handler,
    )
