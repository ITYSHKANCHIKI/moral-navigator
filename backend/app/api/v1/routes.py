# -*- coding: utf-8 -*-
from typing      import List
from fastapi     import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm   import Session

from app import crud, schemas
from app.db import get_db
from app.auth import authenticate_user, create_access_token, get_current_user

router = APIRouter()

# ────────── AUTH ──────────────────────────────────────────
@router.post(
    "/auth/login-json",
    response_model=schemas.Token,
    tags=["auth"],
)
def login_json(
    creds:   schemas.Login   = Body(...),
    db_sess: Session         = Depends(get_db),
):
    user = crud.UserRepository(db_sess).get_by_username(creds.username)
    if not user or not authenticate_user(creds.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": user.username})
    return {
        "access_token": token,
        "token_type":   "bearer",
    }

@router.post(
    "/auth/login",
    response_model=schemas.Token,
    tags=["auth"],
)
def login_form(
    form:     OAuth2PasswordRequestForm = Depends(),
    db_sess:  Session               = Depends(get_db),
):
    user = crud.UserRepository(db_sess).get_by_username(form.username)
    if not user or not authenticate_user(form.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": user.username})
    return {
        "access_token": token,
        "token_type":   "bearer",
    }

@router.get(
    "/auth/me",
    response_model=schemas.UserOut,
    tags=["auth"],
)
def read_me(current_user: schemas.UserOut = Depends(get_current_user)):
    return current_user


# ────────── TESTS ─────────────────────────────────────────
@router.get(
    "/tests",
    response_model=List[schemas.TestSummary],
    tags=["tests"],
)
def list_tests(
    db_sess: Session            = Depends(get_db),
    _:       schemas.UserOut    = Depends(get_current_user),
):
    return crud.TestRepository(db_sess).list_all()

@router.get(
    "/tests/{test_id}/dilemmas",
    response_model=List[schemas.DilemmaOut],
    tags=["tests"],
)
def list_dilemmas(
    test_id: int,
    db_sess: Session           = Depends(get_db),
    _:       schemas.UserOut   = Depends(get_current_user),
):
    if not crud.TestRepository(db_sess).get(test_id):
        raise HTTPException(404, "Тест не найден")
    return crud.DilemmaRepository(db_sess).list_for_test(test_id)


# ────────── HISTORY ──────────────────────────────────────
@router.post(
    "/history",
    response_model=schemas.HistoryOut,
    status_code=status.HTTP_201_CREATED,
    tags=["history"],
)
def record_history(
    payload:  schemas.HistoryCreate,
    db_sess:  Session          = Depends(get_db),
    user:     schemas.UserOut   = Depends(get_current_user),
):
    if not crud.TestRepository(db_sess).get(payload.test_id):
        raise HTTPException(400, "Тест не найден")
    return crud.HistoryRepository(db_sess).create(
        user_id=user.id,
        test_id=payload.test_id,
        answers=payload.answers,
    )

# новый маршрут: просто GET /history
@router.get(
    "/history",
    response_model=List[schemas.HistoryOut],
    tags=["history"],
)
def list_history(
    db_sess: Session          = Depends(get_db),
    user:    schemas.UserOut  = Depends(get_current_user),
):
    return crud.HistoryRepository(db_sess).list_by_user(user.id)

@router.get(
    "/history/{test_id}",
    response_model=List[schemas.HistoryOut],
    tags=["history"],
)
def get_history(
    test_id: int,
    db_sess:  Session         = Depends(get_db),
    user:     schemas.UserOut  = Depends(get_current_user),
):
    if not crud.TestRepository(db_sess).get(test_id):
        raise HTTPException(404, "Тест не найден")
    return crud.HistoryRepository(db_sess).get_by_test(test_id, user.id)
