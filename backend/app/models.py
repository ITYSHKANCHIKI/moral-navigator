# backend/app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    username      = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    histories = relationship("History", back_populates="user")

    def __repr__(self) -> str:
        return f"<User #{self.id} {self.username!r}>"


class Test(Base):
    __tablename__ = "tests"

    id         = Column(Integer, primary_key=True, index=True)
    title      = Column(String, nullable=False)
    evaluation = Column(String, default="simple-score", nullable=False)

    dilemmas = relationship(
        "Dilemma", back_populates="test", cascade="all, delete-orphan"
    )


class Dilemma(Base):
    __tablename__ = "dilemmas"

    id      = Column(Integer, primary_key=True, index=True)
    text    = Column(String, nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)

    test    = relationship("Test", back_populates="dilemmas")
    options = relationship(
        "Option", back_populates="dilemma", cascade="all, delete-orphan"
    )


class Option(Base):
    __tablename__ = "options"

    id         = Column(Integer, primary_key=True, index=True)
    text       = Column(String, nullable=False)
    logic      = Column(Integer, default=0)
    empathy    = Column(Integer, default=0)
    fear       = Column(Integer, default=0)
    ambition   = Column(Integer, default=0)
    score      = Column(Integer, default=0)
    dilemma_id = Column(Integer, ForeignKey("dilemmas.id"), nullable=False)

    dilemma = relationship("Dilemma", back_populates="options")

    @hybrid_property
    def impact(self) -> int:
        return self.logic + self.empathy + self.fear + self.ambition


class History(Base):
    __tablename__ = "histories"

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    test_id     = Column(Integer, ForeignKey("tests.id"), nullable=False)
    answers     = Column(JSON, nullable=False)    # универсальный JSON
    result_text = Column(String, nullable=True)

    user = relationship("User", back_populates="histories")
