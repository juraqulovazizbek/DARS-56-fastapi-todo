from enum import Enum
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Enum as SqlEnum,
    DateTime
)

from ..core.database import Base


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True , autoincrement=True)
    username = Column(String(length=64), unique=True , nullable=False)
    password = Column(String(length=128), nullable=False)
    role = Column(SqlEnum(Role),default=Role.USER, nullable=False)

    created_at = Column(DateTime , default=datetime.now)
    updated_at = Column(DateTime , default=datetime.now, onupdate=datetime.now)
    
    def __str__(self):
        return self.username