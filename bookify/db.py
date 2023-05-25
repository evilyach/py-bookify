from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase


def init_engine() -> Engine:
    # pylint: disable=unused-import, import-outside-toplevel
    from bookify.article import models

    return create_engine("sqlite:///py-bookify.db")


class Base(DeclarativeBase):
    pass


engine = init_engine()
