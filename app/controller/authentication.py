from fastapi import APIRouter

from app.schema.schema import ResponseSchema, RegisterSchema, LoginSchema, ForgotPasswordSchema
from app.service.auth_service import AuthService
from app.service.users import UserService

router = APIRouter(prefix="/auth", tags=['Authentication'])

@router.post("/register", response_model=ResponseSchema, response_model_exclude_none=True)
async def register(request_body: RegisterSchema):
    await AuthService.register_service(request_body)
    return ResponseSchema(detail="Successfully save data!")

@router.post("/login", response_model=ResponseSchema)
async def login(request_body: LoginSchema):
    token = await AuthService.logins_service(request_body)
    user = await AuthService.get_user_by_credentials(request_body.id, request_body.username, request_body.password, request_body.role)
    return ResponseSchema(detail="Successfully login", result={"token_type": "Bearer", "access_token": token, "id": user.id, "username": user.username, "email": user.email, "role": user.role})

@router.post("/forgot-password", response_model=ResponseSchema, response_model_exclude_none=True)
async def forgot_password(request_body: ForgotPasswordSchema):
    await AuthService.forgot_password_service(request_body)
    return ResponseSchema(detail="Successfully update data!")
