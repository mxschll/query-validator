import sqlalchemy


def create_db_engine(uri):
    return sqlalchemy.create_engine(uri)


def execute_query(connection, query, params=None):
    with connection.connect() as conn:
        result = conn.execute(sqlalchemy.text(query), params or {})
    return result
