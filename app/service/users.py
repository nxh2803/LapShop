from sqlalchemy.future import select
from app.model import User, Person
from app.config import db
from sqlalchemy.orm import Session
from app.schema.schema import RegisterSchema, UserSchema
from sqlalchemy import update
from uuid import UUID


class UserService:
    @staticmethod
    async def get_user_profile(username: str):
        query = (
            select(
                User.id,
                User.username,
                User.email,
                Person.name,
                Person.birth,
                Person.sex,
                Person.phone_number,
            )
            .join_from(User, Person)
            .where(User.username == username)
        )
        return (await db.execute(query)).mappings().one()

    @staticmethod
    async def get_all_users():
        query = select(
            User.id,
            User.username,
            User.email,
            Person.name,
            Person.birth,
            Person.sex,
            Person.phone_number,
        ).join_from(User, Person)
        return (await db.execute(query)).mappings().all()

    @staticmethod
    async def get_user_by_user_id(user_id: str):
        query = (
            select(
                User.id,
                User.username,
                User.email,
                User.created_at,
                User.modified_at,
                User.role,
                Person.name,
                Person.phone_number
            )
            .join_from(User, Person)
            .where(User.id == user_id)
        )
        return (await db.execute(query)).mappings().one()
