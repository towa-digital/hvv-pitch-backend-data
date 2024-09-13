from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Response, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from settings.database import get_db
from settings.config import ACCESS_TOKEN_EXPIRE_MINUTES

from .crud import get_user_by_username, create_user, enable_user_2fa, update_user
from .dependencies import get_current_user
from .models import User
from .schemas import Token, User as UserSchema, UserCreate, TOTPVerify, TOTPVerified
from .utils import (
    authenticate_user,
    create_access_token,
    generate_user_2fa_qr_code,
    verify_user_2fa_token,
)

app = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)

Database = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]



@app.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Database,
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/me")
async def read_users_me(
    current_user: CurrentUser,
):
    return UserSchema.model_validate(current_user)


@app.post("/register")
async def register(
    form_data: Annotated[UserCreate, Depends()],
    db: Database,
) -> UserSchema:
    user = get_user_by_username(db, username=form_data.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    new_user = create_user(db, form_data)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register user",
        )

    return UserSchema.model_validate(new_user)


@app.post("/2fa/enable")
async def enable_2fa(
    current_user: CurrentUser,
    db: Database,
) -> Response:
    """
    Enable 2FA for the current user and return a QR code image.
    """
    if current_user.otp_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA already enabled",
        )

    current_user = enable_user_2fa(db, current_user)
    img_byte_arr = generate_user_2fa_qr_code(current_user)
    return Response(content=img_byte_arr, media_type="image/png")


@app.post("/2fa/verify")
async def verify_2fa(
    token_data: Annotated[TOTPVerify, Form()],
    current_user: CurrentUser,
    db: Database,
) -> TOTPVerified:
    """
    Verify a 2FA token for the current user.
    """
    if not verify_user_2fa_token(token_data.token, current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid 2FA token",
        )

    update_user(db, current_user, {"otp_verified": True})
    return TOTPVerified(verified=True)
