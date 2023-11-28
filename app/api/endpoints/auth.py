import jwt

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app.api.models.auth import UserInDB, Token, User
from app.core.config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = []

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db, username: str):
    for user in db:
        if user["username"] == username:
            return user


def create_user(db, user: UserInDB):
    db.append(user.model_dump())
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(fake_users_db, form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {"sub": form_data.username}
    access_token = jwt.encode(token_data, settings.secret_key, algorithm="HS256")

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=User)
async def register(user: User):
    hashed_password = pwd_context.hash(user.password)
    user_db = UserInDB(**user.model_dump(), hashed_password=hashed_password)
    create_user(fake_users_db, user_db)
    return user
