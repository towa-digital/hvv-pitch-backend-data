import uuid

from sqlalchemy import Boolean, Column, String, Date, UUID, text

from settings.database import Base


class User(Base):
    __tablename__ = "api_auth"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("UUID_STRING()")
    )
    created_at = Column(Date, server_default=text("CURRENT_DATE"))
    is_active = Column(Boolean, default=True)

    username = Column(String, unique=True)
    password = Column(String)
    otp_secret = Column(String, nullable=True)
    otp_verified = Column(Boolean, default=False)

    def __init__(self, **kwargs):
        if "id" not in kwargs:
            kwargs["id"] = uuid.uuid4()
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<User {self.username}>"

    @property
    def is_2fa_enabled(self):
        return self.otp_secret is not None and self.otp_verified
