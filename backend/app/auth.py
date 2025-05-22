# backend/app/auth.py
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError

from sqlalchemy.orm import Session
from app import crud, schemas
from app.db import get_db

# Секрет и алгоритмы — оставляем ваши
SECRET_KEY = "…ваш секретный ключ…"
ALGORITHM  = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # теперь токен живёт час

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login-json")


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(plain_password: str, password_hash: str) -> bool:
    # ваш код проверки через passlib
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, password_hash)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> schemas.UserOut:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # декодируем токен
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

    except ExpiredSignatureError:
        # отсюда теперь будет понятно фронту, что токен просрочен
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        # все остальные ошибки декодирования
        raise credentials_exception

    # подтягиваем пользователя из базы
    user = crud.UserRepository(db).get_by_username(username)
    if not user:
        raise credentials_exception

    # конвертим в выходную Pydantic-модель
    return schemas.UserOut.from_orm(user)
