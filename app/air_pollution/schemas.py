from pydantic import BaseModel, UUID4


class AirPollutionBase(BaseModel):
    """
    Base schema for Air Pollution data schemas.
    """

    country: str


class AirPollution(AirPollutionBase):
    """ "
    Schema for reading air pollution data from the database.
    """

    country: str
    year: str

    class Config:
        from_attributes = True