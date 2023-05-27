from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Callable

from bookify.article.custom_types import Markdown

if TYPE_CHECKING:
    from bookify.parse import MarkdownParser


@dataclass
class WebsiteConfig:
    count: int
    name: str

    convert_handler: Callable[["MarkdownParser"], Markdown]
    get_author_handler: Callable[["MarkdownParser"], str]


@dataclass
class ParseConfig:
    parser: str = field(default="html.parser")
    use_temp_files: bool = field(default=True)
    temp_files_dir: Path = field(default_factory=lambda: Path("output"))
