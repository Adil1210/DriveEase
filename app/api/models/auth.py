from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class User(BaseModel):
    username: str
    email: str
    password: str


class UserInDB(User):
    hashed_password: str
