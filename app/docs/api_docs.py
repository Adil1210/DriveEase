"""
FastAPI Authentication and Authorization Example

This module provides a simple FastAPI implementation with user authentication and token-based authorization.

Endpoints:
- POST /token: Authenticate user and generate an access token.
- POST /register: Register a new user.

Dependencies:
- jwt: JSON Web Token encoding and decoding library.
- fastapi: A modern, fast (high-performance), web framework for building APIs.
- passlib: Password hashing library for secure password storage.
- app.api.models.auth: Module containing data models for authentication.
- app.core.config.settings: Module containing application settings.

Usage:
1. Import the necessary libraries and modules.
2. Configure the FastAPI router and security settings.
3. Define utility functions for password verification and user operations.
4. Implement the /token endpoint for user authentication and token generation.
5. Implement the /register endpoint for user registration.

Note: This code is a basic example and may need enhancements for production use, such as database integration.
"""

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app.api.models.auth import UserInDB, Token, User
from app.core.config import settings

# Initialize FastAPI router
router = APIRouter()

# Configure OAuth2 password bearer for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# In-memory database for demonstration purposes
fake_users_db = []

# Initialize passlib context for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """Verify the provided plain password against the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db, username: str):
    """Get a user from the database by username."""
    for user in db:
        if user["username"] == username:
            return user


def create_user(db, user: UserInDB):
    """Create a new user in the database."""
    db.append(user.model_dump())
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint to authenticate a user and generate an access token.

    Args:
    - form_data: OAuth2PasswordRequestForm containing username and password.

    Returns:
    - Token: Response model containing the generated access token.
    """
    user = get_user(fake_users_db, form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {"sub": form_data.username}
    access_token = jwt.encode(token_data, settings.secret_key, algorithm="HS256")

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=User)
async def register(user: User):
    """
    Endpoint to register a new user.

    Args:
    - user: User model containing user details.

    Returns:
    - User: Response model containing the registered user details.
    """
    hashed_password = pwd_context.hash(user.password)
    user_db = UserInDB(**user.model_dump(), hashed_password=hashed_password)
    create_user(fake_users_db, user_db)
    return user
