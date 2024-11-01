from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.auth.heandlers import sign_jwt
from src.auth.schemas import UserLoginSchema, UserRegisterSchema
from src.auth.service import UserService


router = APIRouter()

@router.post("/login")
async def user_login(user: UserLoginSchema, user_service: UserService):
    if await user_service.verify_user(user):
        access_token = sign_jwt(user.email)
        response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return response

    return {"error": "Wrong login details or user is not found!"}


@router.post("/register")
async def user_register(user: UserRegisterSchema, user_service: UserService):
    new_user = await user_service.add_new_user(user)
    return new_user
