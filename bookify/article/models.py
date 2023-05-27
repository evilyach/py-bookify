from __future__ import annotations

from sqlalchemy import String, Text, select
from sqlalchemy.orm import Mapped, Session, mapped_column
from typing_extensions import Self, Type

from bookify.article.custom_types import HTML, Markdown
from bookify.db import Base, engine


class Article(Base):
    __tablename__ = "article"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String)
    author: Mapped[str | None] = mapped_column(String, nullable=True)
    title: Mapped[str | None] = mapped_column(String, nullable=True)
    html: Mapped[HTML | None] = mapped_column(Text, nullable=True)
    markdown: Mapped[Markdown | None] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"Article(id={self.id!r}, title={self.title!r})"

    @classmethod
    def create(cls: Type[Self], **kwargs) -> Self:
        with Session(engine) as session:
            session.add(article := Article(**kwargs))
            session.commit()

        return article

    @staticmethod
    def get_by_id(_id: str) -> Article | None:
        with Session(engine) as session:
            return session.scalar(select(Article).where(Article.id == _id))

    @staticmethod
    def get_by_url(url: str) -> Article | None:
        with Session(engine) as session:
            return session.scalar(select(Article).where(Article.url == url))

    @staticmethod
    def get_markdown_by_url(url: str) -> Markdown | None:
        with Session(engine) as session:
            return session.scalar(select(Article.markdown).where(Article.url == url))

    def update_markdown(self: Article, markdown: Markdown) -> None:
        with Session(engine) as session:
            self.markdown = markdown

            session.merge(self)
            session.commit()
