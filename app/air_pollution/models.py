import uuid

from sqlalchemy import Boolean, Column, String, Date, UUID, text, INT, REAL, Float

from settings.database import Base


class AirPollution(Base):
    __tablename__ = "aggregated_air_pollution"

    Id = Column(INT, primary_key=True)
    Country = Column(String)
    Year = Column(INT)
    Mean = Column(REAL)
    Standarddeviation = Column(REAL)
    Median = Column(REAL)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<AirPollution {self.Id}>"