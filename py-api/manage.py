
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

from model.Base import Base

import APIModels.Token
from model.Roles import Role
from model.Schemas import create_schemas
from configuration.Configuration import Configuration
from configuration.Security import pwd_context, pwd_config
from model.Users import UserAccount


try:
    config = Configuration.from_file("lexmpmapi.json")
except IOError:
    config = Configuration.default()
    config.write()
    print("Configuration file created, please update connection info and run again.")


APIModels.Token.SECRET_KEY = config.secret_key
APIModels.Token.ACCESS_TOKEN_EXPIRE_MINUTES = config.access_token_expires

pwd_context.load(pwd_config)

engine = create_engine(
    f"postgresql+psycopg://{config.dbuser}:{config.dbpassword}@{config.dbhost}:{config.dbport}/{config.dbname}", echo=True)
if not database_exists(engine.url):
    create_database(engine.url)
    engine = create_engine(
        f"postgresql+psycopg://{config.dbuser}:{config.dbpassword}@{config.dbhost}:{config.dbport}/{config.dbname}", echo=True)

with engine.connect() as conn:
    create_schemas(conn)

Base.metadata.create_all(engine)


with Session(engine) as session:
    if session.query(Role).count() == 0 or (session.scalars(select(Role).where(Role.id==1))).first() is None:
        role = Role(name="admin")
        session.add(role)
        session.commit()

    for role in session.scalars(select(Role).where(Role.name == "admin")):
        print(role.name)

    if session.query(UserAccount).count() == 0 or (session.scalars(select(UserAccount).where(UserAccount.id == 1))).first() is None:
        user = UserAccount(account_name="admin",
                           display_name="Administration",
                           password=UserAccount.hash_password("admin"))
        session.add(user)
        session.commit()