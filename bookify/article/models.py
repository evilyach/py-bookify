from sqlalchemy import String, Text, select
from sqlalchemy.orm import Mapped, Session, mapped_column

from bookify.db import Base, engine


class Article(Base):
    __tablename__ = "article"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String)
    html: Mapped[str] = mapped_column(Text)

    def __repr__(self) -> str:
        return f"Article(id={self.id!r}, title={self.title!r})"

    @staticmethod
    def get_by_id(_id: str) -> "Article" | None:
        with Session(engine) as session:
            return session.scalar(select(Article).where(Article.id == _id))

    @staticmethod
    def get_by_url(_url: str) -> "Article" | None:
        with Session(engine) as session:
            return session.scalar(select(Article).where(Article.url == _url))
