from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from jose import JWTError

from src.api.rest.user.decorators import check_permissions_decorator
from src.api.rest.user.models import CurrentUser
from src.api.rest.user.models import UserCreate, UserLogin
from src.api.rest.user.decorators import handle_user_errors
from src.core.user.services import user_service, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, \
    TokenIsNotValidError
from src.dependencies import get_current_user

users_router = APIRouter(prefix="/users", tags=['users'])

@users_router.post("/register")
@handle_user_errors
async def register(user: UserCreate):
    await user_service.create(username=user.username, password=user.password, email=user.email)
    return {"created": user.username}

@users_router.get("")
@check_permissions_decorator([])
async def get_all(current_user=Depends(get_current_user)):
    return await user_service.get_all()


@users_router.patch("/{user_id}")
@check_permissions_decorator([])
async def patch_user(user_id: int, user: PatchUser, current_user = Depends(get_current_user)):
    await user_service.patch(user_id, user)
    return user


@users_router.post("/login")
async def login(user: UserLogin):
    user = await user_service.authenticate_user(user.email, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = await user_service.create_token(data={"sub": user.email, "type": "access"}, expires_delta=access_token_expires)
    refresh_token = await user_service.create_token(data={"sub": user.email, "type": "refresh"}, expires_delta=refresh_token_expires)

    return {
        "acc_tok": access_token,
        "ref_tok": refresh_token
    }

@users_router.post("/refresh")
def refresh_access_token(token: str):
    try:
        username = user_service.verify_token(token, "refresh")
    except (JWTError, TokenIsNotValidError) as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error))
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = user_service.create_token(
        data={"sub": username, "type": "access"},
        expires_delta=access_token_expires
    )
    return {"acc_tok": access_token}

@users_router.get("/me")
async def me(current_user=Depends(get_current_user)):
    return CurrentUser.model_validate(current_user).model_dump()