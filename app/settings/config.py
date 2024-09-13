import os

DEBUG = bool(os.getenv("DEBUG", False))
TESTING = bool(os.getenv("TESTING", False))

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
