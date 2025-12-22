
from enum import Enum
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Enum as SqlEnum,
    DateTime, 
    ForeignKey
)

from ..core.database import Base


class Category(Base):
    __tablename__ = "categories"
    category_id = Column( 'id', Integer, primary_key=True , autoincrement=True)
    name = Column(String(length=64), nullable=False, unique=True)
    icon = Column(String(length=255), nullable=False, default='media/category-icons/default-icon.svg')
    color = Column(String(length=20), nullable=False, default='#ede7dc')

    created_at = Column(DateTime , default=datetime.now)
    updated_at = Column(DateTime , default=datetime.now, onupdate=datetime.now)

    def __str__(self):
        return self.name

class Task(Base):
    __tablename__ = "tasks"

    task_id = Column( 'id', Integer, primary_key=True , autoincrement=True)
    name = Column(String(length=64), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id' , ondelete='CASCADE'))
    description = Column(String(length=255), nullable=True)
    due_date = Column(DateTime , nullable=True)
    

    created_at = Column(DateTime , default=datetime.now)
    updated_at = Column(DateTime , default=datetime.now, onupdate=datetime.now)

class subtask(Base):
    __tablename__ = "subtasks"

    created_at = Column(DateTime , default=datetime.now)
    updated_at = Column(DateTime , default=datetime.now, onupdate=datetime.now)


class attachment(Base):
    __tablename__ = "attachments"

    created_at = Column(DateTime , default=datetime.now)
    updated_at = Column(DateTime , default=datetime.now, onupdate=datetime.now)
