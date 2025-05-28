from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class AdminID(Base):
    __tablename__ = 'admin list'

    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    username: Mapped[str] = mapped_column(String(150), nullable=False)


class FAQ(Base):
    __tablename__ = 'FAQ'

    id: Mapped[int] = mapped_column(primary_key=True)
    contents: Mapped[str] = mapped_column(String(100), nullable=False) 
    problem: Mapped[str] = mapped_column(String(100), nullable=False)
    answer: Mapped[str] = mapped_column(String(355), nullable=False)