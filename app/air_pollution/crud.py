from datetime import datetime
from typing import Type, Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

from . import models, schemas
from .models import AirPollution


def get_data(db: Session, country: str, year:  int) -> models.AirPollution or None:
    """
    Load air pollution data by country and year.
    """
    query = db.query(
        models.AirPollution
    ).filter(
        models.AirPollution.Country == country
    ).filter(
        models.AirPollution.Year == year
    ).first()
    return query
