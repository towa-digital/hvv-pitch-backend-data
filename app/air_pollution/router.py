import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from datetime import timedelta
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Response, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from settings.database import get_db
from settings.config import ACCESS_TOKEN_EXPIRE_MINUTES

from auth.dependencies import get_current_user
from auth.models import User
from auth.router import read_users_me

from .crud import get_data
from .models import AirPollution
from .schemas import AirPollution as AirPollutionSchema

app = APIRouter(
    prefix="/pollution_data",
    tags=["Air Pollution"],
    responses={404: {"description": "Not found"}},
)

Database = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]

@app.get("/get")
async def fetch_pollution_data(
    db: Database,
    current_user: CurrentUser,
    country: str = Query(None, description="The country the air pollution data should be fetched for."),
    year: str = Query(None, description="The year the data should be fetched for."),
):
    result = get_data(db, country, year)
    if result is None:
        raise HTTPException(status_code=404, detail="No data found for the given country and year.")

    return get_data(db, country, year)
