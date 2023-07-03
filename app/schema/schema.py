from fastapi import HTTPException
import logging
import re
from typing import TypeVar, Optional

from pydantic import BaseModel, validator
from sqlalchemy import false
from app.model.person import Sex


T = TypeVar("T")

# get root logger
logger = logging.getLogger(__name__)


class RegisterSchema(BaseModel):
    username: str
    email: str
    password: str
    name: str
    birth: str
    sex: Sex
    phone_number: str
    # phone number validation

    # @validator("phone_number")
    # def phone_validation(cls, v):
    #     logger.debug(f"phone in 2 validatior: {v}")

    #     # regex phone number
    #     regex = r"^(?:\+84|0)(?:\d{9}|(?:\d{2}-){3}\d{3})$"
    #     if v and not re.search(regex, v, re.I):
    #         raise HTTPException(status_code=400, detail="Invalid input phone number!")
    #     return v

    # Sex validation
    @validator("sex")
    def sex_validation(cls, v):
        if hasattr(Sex, v) is False:
            raise HTTPException(status_code=400, detail="Invalid input sex")
        return v


class UserSchema(BaseModel):
    email: str
    password: str
    name: str
    birth: str
    sex: Sex
    phone_number: str


class UserRegisterSchema(BaseModel):
    username: str
    email: str
    password: str
    role: str


class LoginSchema(BaseModel):
    id: Optional[str] = None
    username: str
    password: str
    role: Optional[str] = None


class ForgotPasswordSchema(BaseModel):
    email: str
    new_password: str


class DetailSchemas(BaseModel):
    status: str
    message: str
    result: Optional[T] = None


class ResponseSchema(BaseModel):
    detail: str
    result: Optional[T] = None
