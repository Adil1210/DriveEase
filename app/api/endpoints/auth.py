from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.api.models.auth import UserInDB, Token, User
from app.core.config import get_settings
from passlib.context import CryptContext

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
settings = get_settings()

fake_users_db = []

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db, username: str):
    for user in db:
        if user["username"] == username:
            return user


def create_user(db, user: UserInDB):
    db.append(user.dict())
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordBearer = Depends(oauth2_scheme)):
    user = get_user(fake_users_db, form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Here, you would normally generate a JWT token
    # For simplicity, we are returning the username as the access token
    return {"access_token": form_data.username, "token_type": "bearer"}


@router.post("/register", response_model=User)
async def register(user: User):
    hashed_password = pwd_context.hash(user.password)
    user_db = UserInDB(**user.dict(), hashed_password=hashed_password)
    create_user(fake_users_db, user_db)
    return user
