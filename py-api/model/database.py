from sqlalchemy import create_engine, Engine
from sqlalchemy_utils import database_exists

class DBContext:
    engine: Engine
    def __init__(self, config: dict) -> None:
        self.engine = create_engine(
            f"postgresql+psycopg://{config.dbuser}:{config.dbpassword}@{config.dbhost}:{config.dbport}/{config.dbname}",
            echo=True)
        if not database_exists(self.engine.url):
            raise IOError("Database does not exist.  Please run manage.py to create.")


dbcontext: DBContext


def setup_db(config):
    global dbcontext
    dbcontext =  DBContext(config)


