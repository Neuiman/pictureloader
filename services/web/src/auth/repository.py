from typing import Protocol

from sqlalchemy import insert, select

from src.auth.models import User
from src.auth.schemas import UserSchema
from src.database import session_maker


class UserRepositoryProtocol(Protocol):

    async def add_user(self, data: dict) -> UserSchema:
        ...

    async def get_user_by_email(self, email: str) -> UserSchema:
        ...


class UserRepositoryImp:
    async def add_user(self, data: dict) :
        async with session_maker() as session:
            stmt = insert(User).values(**data).returning(User)
            result = await session.execute(stmt)
            new_user = [row[0].to_read_model() for row in result.all()]
            await session.commit()
            return new_user

    async def get_user_by_email(self, email: str):
        async with session_maker() as session:
            stmt = select(User).where(User.email == email)
            result = await session.execute(stmt)
            result = [row[0] for row in result.all()]
            return result


async def get_user_repository() -> UserRepositoryProtocol:
    return UserRepositoryImp()
