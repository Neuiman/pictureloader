from typing import Protocol, Annotated

from fastapi.params import Depends

from src.auth.schemas import UserRegisterSchema
from src.auth.repository import UserRepositoryProtocol, get_user_repository
from src.auth.schemas import UserLoginSchema
from src.auth.utils import check_user, create_user_register_hash_schema


class UserServiceProtocol(Protocol):

    async def add_new_user(self, user: UserRegisterSchema):
        ...

    async def verify_user(self, user: UserLoginSchema):
        ...


class UserServiceImp:
    def __init__(self, user_repository: UserRepositoryProtocol):
        self.user_repository = user_repository

    async def add_new_user(self, user: UserRegisterSchema):
        user = await create_user_register_hash_schema(user)
        user_dict = user.model_dump()
        new_user = await self.user_repository.add_user(user_dict)

        return new_user

    async def verify_user(self, user: UserLoginSchema) -> bool | dict:
        try:
            user_from_db = await self.user_repository.get_user_by_email(user.email)
            is_user_verified = await check_user(user, user_from_db[0])

            return is_user_verified
        except:
            return False


async def get_user_service(user_repository: UserRepositoryProtocol = Depends(get_user_repository)):
    return UserServiceImp(user_repository)


UserService = Annotated[UserServiceProtocol, Depends(get_user_service)]

