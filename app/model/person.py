from typing import Optional
from sqlalchemy import Enum, table
from sqlmodel import SQLModel, Field, Relationship
from app.model.mixins import TimeMixin


class Sex(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"

class Person(SQLModel, TimeMixin, table=True):
    __tablename__ = "person"

    id: Optional[str] = Field(None, primary_key=True, nullable=False)
    name: str
    birth: str
    sex: Sex
    phone_number: str

    user: Optional["User"] = Relationship(
        sa_relationship_kwargs={'uselist': False}, back_populates="person")
