from datetime import timedelta
from fastapi import APIRouter, Response, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import *
from fastapi.encoders import jsonable_encoder
import app.auth_utils as auth_utils

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_utils.authenticate_user(form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_utils.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signup")
async def signup( request: Request, response: Response, data: UserData ):
    user = jsonable_encoder(data)
    res = await auth_utils.create_user(user)
    if res:
        return res
    raise HTTPException(
        status_code = 404, detail="Create User failed"
    )

@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(auth_utils.get_current_active_user)):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(auth_utils.get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
