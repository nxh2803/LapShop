from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session
from app.schema.schema import (
    ResponseSchema,
    RegisterSchema,
    LoginSchema,
    ForgotPasswordSchema,
    UserSchema,
    UserRegisterSchema,
)
from app.repository.auth_repo import JWTBearer, JWTRepo
from fastapi.security import HTTPAuthorizationCredentials
from app.service.users import UserService
from app.config import db, commit_rollback
from app.model.user import User
from sqlalchemy.future import select

router = APIRouter(
    prefix="",
    tags=["User"],
    # dependencies=[Depends(JWTBearer())]
)

# @router.get("/", response_model=ResponseSchema, response_model_exclude_none=True)
# async def get_user_profile(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
#     token = JWTRepo.extract_token(credentials)
#     result = await UserService.get_user_profile(token['username'])
#     return ResponseSchema(detail="Successfully fetch data!", result=result)


@router.get("/user", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_user_profile(username: str):
    result = await UserService.get_user_profile(username)
    return ResponseSchema(detail="Successfully fetch data!", result=result)


@router.get("/users", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all_users():
    users = await UserService.get_all_users()
    return ResponseSchema(detail="Successfully fetched all users!", result=users)


@router.get(
    "/user/{user_id}", response_model=ResponseSchema, response_model_exclude_none=True
)
async def get_user_by_id(user_id: str):
    user = await UserService.get_user_by_user_id(user_id)
    return ResponseSchema(detail="Successfully fetch data!", result=user)


@router.put("/user/{id}", response_model=ResponseSchema)
async def update_user(id: str, user_data: UserRegisterSchema):
    query = select(User).where(User.id == id)
    result = await db.session.execute(query)
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.username = user_data.username
    user.email = user_data.email
    user.password = user_data.password
    user.role = user_data.role

    await commit_rollback()
    return ResponseSchema(detail="User updated successfully!")


@router.delete("/{id}", response_model=ResponseSchema)
async def delete_user(id: str):
    query = select(User).where(User.id == id)
    result = await db.session.execute(query)
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.session.delete(user)
    await commit_rollback()
    return ResponseSchema(detail="User deleted successfully!")
