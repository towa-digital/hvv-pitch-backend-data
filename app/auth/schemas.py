from pydantic import BaseModel, UUID4


class UserBase(BaseModel):
    """
    Base schema for all User schemas.
    """

    username: str


class UserCreate(UserBase):
    """
    Schema used for creating a new user (aka registration).
    """

    password: str


class User(UserBase):
    """ "
    Schema for reading a user
    """

    id: UUID4
    is_active: bool
    is_2fa_enabled: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    """
    Schema for the token returned by the login endpoint.
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema for the data we extract from a token, used for loading the current user.
    """

    username: str | None = None


class TOTPVerify(BaseModel):
    """
    Schema for verifying a TOTP token.
    """

    token: str


class TOTPVerified(BaseModel):
    """
    Schema for verifying a TOTP token.
    """

    verified: bool
