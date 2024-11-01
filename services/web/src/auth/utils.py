from fastapi import HTTPException, status
from fastapi import Request
from src.auth.heandlers import decode_jwt
from src.auth.schemas import UserLoginSchema, UserSchema, UserRegisterSchema, UserRegisterHashedSchema
from passlib.context import CryptContext

async def check_user(current_user: UserLoginSchema, user_from_db: UserSchema) -> bool:
    if current_user.email == user_from_db.email and await verify_password(current_user.password, user_from_db.hashed_password):
        return True
    else:
        return False


async def create_user_register_hash_schema(reg_user: UserRegisterSchema):
    return UserRegisterHashedSchema(
        name = reg_user.name,
        email = reg_user.email,
        hashed_password = await hash_password(reg_user.password)
    )

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def get_current_user(request: Request):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = request.cookies.get("access_token")
    if token is None:
        raise credentials_exception
    try:
        payload = decode_jwt(token)
        email: str = payload.get("user_email")
        if email is None:
            raise credentials_exception
    except:
        raise credentials_exception
    return email
