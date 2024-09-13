import io
from datetime import timedelta, datetime, timezone

import jwt
import pyotp
import qrcode
from passlib.context import CryptContext
from qrcode.image.pure import PyPNGImage

from settings.config import SECRET_KEY, ALGORITHM

from .models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hashed password from the database
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password for storing in the database
    """
    return pwd_context.hash(password)


def authenticate_user(db, username: str, password: str) -> User | bool:
    """
    Returns the user if the username and password match a user, otherwise False
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> bytes:
    """
    Create a new access token with the given data and expiration time
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_otp_secret() -> str:
    """
    Generate a random base32 secret for a user

    https://pyauth.github.io/pyotp/#generating-a-secret-key
    """
    return pyotp.random_base32()


def generate_user_2fa_qr_code(user: User) -> bytes:
    """
    Generate a QR code PNG for a user's 2FA secret
    """
    totp = pyotp.TOTP(user.otp_secret)
    qr_code = qrcode.make(
        totp.provisioning_uri(name=user.username, issuer_name="HVV Air Quality"),
        image_factory=PyPNGImage,
    )
    byte_array = io.BytesIO()
    qr_code.save(byte_array)
    return byte_array.getvalue()


def verify_user_2fa_token(token: str, user: User) -> bool:
    """
    Verify a TOTP token for a user
    """
    totp = pyotp.TOTP(user.otp_secret)
    return totp.verify(token)
