from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import TIMESTAMP


class Base(DeclarativeBase):
    pass


class Domain(Base):
    __tablename__ = "domain"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class LinkView(Base):
    __tablename__ = "linkview"

    id: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[str]
    domain_id: Mapped[int] = mapped_column(ForeignKey("domain.id"))
    viewed_at: Mapped[datetime] = mapped_column(TIMESTAMP())
