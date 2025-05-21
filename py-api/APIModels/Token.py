from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
import jwt
import APIModels.User

from APIModels.User import UserOut,from_account_name


SECRET_KEY: str
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: timedelta | None = None) -> 'Token':
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return Token(access_token=encoded_jwt, token_type="bearer")

    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            print(payload)
            username = payload.get("sub")
            print(username)
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except Token.InvalidTokenError as e:
            print(e)
            raise credentials_exception
        user = from_account_name(token_data.username)
        if user is None:
            raise credentials_exception
        return user


async def get_current_active_user(
            current_user: Annotated[UserOut, Depends(Token.get_current_user)],
    ):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user


class TokenData(BaseModel):
    username: str | None = None