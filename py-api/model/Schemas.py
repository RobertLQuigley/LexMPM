from sqlalchemy import inspect
from sqlalchemy.schema import CreateSchema

schemas = ('users','security','pm')

def create_schemas(connection):
    for schema in schemas:
        if not inspect(connection).has_schema(schema):
            connection.execute(CreateSchema(schema))
            connection.commit()
