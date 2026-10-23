from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional
from app.schemas.auth import UserRegister, UserLogin, Token, UserResponse
from app.db.models import User
from app.utils.security import hash_password, verify_password, create_access_token
from app.repositories.user_repository import UserRepository
from app.routers.deps import get_user_repo, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserRegister, user_repo: UserRepository = Depends(get_user_repo)):
    existing = user_repo.get_by_email(user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists."
        )

    user = User(
        name=user_in.name,
        email=user_in.email.lower().strip(),
        phone_no=user_in.phone_no,
        password_hash=hash_password(user_in.password),
        role=user_in.role or "EV_OWNER"
    )
    saved_user = user_repo.create(user)

    if saved_user.role == "ADMIN":
        user_repo.create_admin_profile(saved_user.id, saved_user.name, saved_user.email)

    return saved_user


@router.post("/login", response_model=Token)
def login(login_data: UserLogin, user_repo: UserRepository = Depends(get_user_repo)):
    user = user_repo.get_by_email(login_data.email.lower().strip())
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.email, "role": user.role, "user_id": user.id}
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        role=user.role,
        user_id=user.id,
        name=user.name,
        email=user.email
    )


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
