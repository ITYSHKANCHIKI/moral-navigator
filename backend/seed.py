# backend/seed.py
from app.db     import SessionLocal, engine, Base
from app.models import User, Test, Dilemma, Option, History
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed():
    # 1) создаём таблицы
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # 2) Пользователь
        if not db.query(User).filter_by(username="ityshkanchiki").first():
            u = User(
                username="ityshkanchiki",
                password_hash=pwd_context.hash("12345678")
            )
            db.add(u)
            db.commit()

        # 3) Первый тест
        if not db.query(Test).filter_by(title="Первый тест").first():
            test = Test(title="Первый тест")
            db.add(test)
            db.flush()

            # Дилеммы
            d1 = Dilemma(
                text="Ты видишь, как кто-то плачет в метро. Подойдёшь ли ты помочь?",
                test_id=test.id
            )
            d2 = Dilemma(
                text="Твой друг просит списать ему работу. Согласишься?",
                test_id=test.id
            )
            db.add_all([d1, d2])
            db.flush()

            # Варианты для d1
            o1 = Option(
                text="Да, обязательно спрошу, что случилось",
                logic=0, empathy=2, fear=0, ambition=0,
                dilemma_id=d1.id
            )
            o2 = Option(
                text="Просто пройду мимо",
                logic=1, empathy=0, fear=0, ambition=0,
                dilemma_id=d1.id
            )
            # Варианты для d2
            o3 = Option(
                text="Дам списать",
                logic=0, empathy=1, fear=0, ambition=0,
                dilemma_id=d2.id
            )
            o4 = Option(
                text="Откажу",
                logic=1, empathy=0, fear=0, ambition=1,
                dilemma_id=d2.id
            )
            db.add_all([o1,o2,o3,o4])
            db.commit()

        # 4) Тест Хайнца
        if not db.query(Test).filter_by(title="Дилема Хайнца").first():
            heinz = Test(title="Дилема Хайнца", evaluation="simple-score")
            db.add(heinz)
            db.flush()

            dilemma = Dilemma(
                text=(
                    "Жена Хайнца смертельно больна... Что ему следует сделать?"
                ),
                test_id=heinz.id
            )
            db.add(dilemma)
            db.flush()

            opt1 = Option(
                text="Украсть лекарство, чтобы спасти жену",
                score=1,
                dilemma_id=dilemma.id
            )
            opt2 = Option(
                text="Не нарушать закон и не красть лекарство",
                score=0,
                dilemma_id=dilemma.id
            )
            db.add_all([opt1, opt2])
            db.commit()

        print("✅ Данные успешно засеяны")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
