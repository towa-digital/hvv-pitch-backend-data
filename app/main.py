from typing import Annotated
from fastapi import FastAPI, Depends

from auth.dependencies import oauth2_scheme
from auth.router import app as auth_router
from air_pollution.router import app as air_pollution_router
from settings.config import DEBUG

app = FastAPI(debug=DEBUG)
app.include_router(auth_router)
app.include_router(air_pollution_router)
