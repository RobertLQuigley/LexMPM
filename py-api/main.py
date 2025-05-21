from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from sqlalchemy.orm import Session

import APIModels.Token
from APIModels.User import UserOut
import model.database
from configuration.Configuration import Configuration
from configuration.Security import pwd_context, pwd_config
from APIModels import User
from APIModels.Token import Token, get_current_active_user
import jwt

app = FastAPI()

try:
    config = Configuration.from_file("lexmpmapi.json")
except IOError:
    config = Configuration.default()
    config.write()

APIModels.Token.SECRET_KEY = config.secret_key
APIModels.Token.ACCESS_TOKEN_EXPIRE_MINUTES = config.access_token_expires
APIModels.Token.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

model.database.setup_db(config)

pwd_context.load(pwd_config)




@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], ) -> Token:
    session = Session(model.database.dbcontext.engine)
    user = User.authenticate(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token.create_access_token(
        data={"sub": user.username}
    )


@app.get("/user/me", response_model=UserOut)
async def read_users_me(current_user: Annotated[UserOut, Depends(get_current_active_user)]):
    return current_user
