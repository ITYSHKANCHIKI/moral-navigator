# -*- coding: utf-8 -*-
from typing import List, Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ────────── Users ─────────────────────────────────────────
class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> Optional[models.User]:
        return (
            self.db.query(models.User)
            .filter(models.User.username == username)
            .first()
        )

    def create(self, user_in: schemas.UserCreate) -> models.User:
        db_user = models.User(
            username=user_in.username,
            password_hash=pwd_context.hash(user_in.password),
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user


# ────────── Tests / Dilemmas ─────────────────────────────
class TestRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> List[models.Test]:
        return self.db.query(models.Test).all()

    def get(self, test_id: int) -> Optional[models.Test]:
        return self.db.query(models.Test).get(test_id)


class DilemmaRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_for_test(self, test_id: int) -> List[models.Dilemma]:
        return (
            self.db.query(models.Dilemma)
            .filter(models.Dilemma.test_id == test_id)
            .all()
        )


# ────────── History ──────────────────────────────────────
class HistoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        user_id: int,
        test_id: int,
        answers: List[schemas.AnswerCreate],
    ) -> models.History:
        # преобразуем объекты схемы → dict, чтобы записать в JSON
        answers_json = [
            {"dilemma_id": a.dilemma_id, "option_id": a.option_id}
            for a in answers
        ]

        db_history = models.History(
            user_id=user_id,
            test_id=test_id,
            answers=answers_json,
        )
        self.db.add(db_history)
        self.db.commit()
        self.db.refresh(db_history)
        return db_history

    def get_by_test(self, test_id: int, user_id: int) -> List[models.History]:
        """Вернуть все записи по конкретному тесту для данного пользователя."""
        return (
            self.db.query(models.History)
            .filter(
                models.History.test_id == test_id,
                models.History.user_id == user_id,
            )
            .order_by(models.History.id.desc())
            .all()
        )

    def list_by_user(self, user_id: int) -> List[models.History]:
        """Вернуть всю историю данного пользователя."""
        return (
            self.db.query(models.History)
            .filter(models.History.user_id == user_id)
            .order_by(models.History.id.desc())
            .all()
        )

    def get(self, history_id: int, user_id: int) -> Optional[models.History]:
        """Вернуть один шаг истории по его ID (с проверкой, что он принадлежит юзеру)."""
        return (
            self.db.query(models.History)
            .filter(
                models.History.id == history_id,
                models.History.user_id == user_id,
            )
            .first()
        )
