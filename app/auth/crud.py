from datetime import datetime
from typing import Type

from sqlalchemy.orm import Session

from . import models, schemas
from .models import User
from .utils import get_password_hash, get_user_otp_secret

def get_user_by_username(db: Session, username: str) -> models.User or None:
    """
    Load a user by username.
    """
    return db.query(models.User).filter(models.User.username == username).first()


def update_user(db: Session, user: models.User, data: dict) -> models.User:
    """
    Update a user with the given data.
    """
    for field, value in data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[Type[User]]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Create a new user from a UserCreate schema.
    """
    db_user = models.User(
        username=user.username,
        password=get_password_hash(user.password),
        created_at=datetime.now(),
        is_active=True,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def enable_user_2fa(db: Session, user: models.User) -> models.User:
    """
    Enable 2FA for a user.
    """
    user.otp_secret = get_user_otp_secret()
    db.commit()
    db.refresh(user)
    return user
