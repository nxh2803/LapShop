
import email
from multiprocessing import synchronize
from sqlalchemy import update as sql_update
from sqlalchemy.future import select


from app.config import db, commit_rollback
from app.model.user import User
from app.repository.base_repo import BaseRepo


class UsersRepository(BaseRepo):
    model = User

    @staticmethod
    async def find_by_username(username: str):
        query = select(User).where(User.username == username)
        return (await db.execute(query)).scalar_one_or_none()

    @staticmethod
    async def find_by_email(email: str):
        query = select(User).where(User.email == email)
        return (await db.execute(query)).scalar_one_or_none()

    @staticmethod
    async def update_password(email: str, password: str):
        query = sql_update(User).where(User.email == email).values(
            password=password).execution_options(synchronize_session="fetch")
        await db.execute(query)
        await commit_rollback()

