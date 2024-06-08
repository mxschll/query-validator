from sqlalchemy import create_engine, text


def create_db_engine(uri):
    return create_engine(uri)


def execute_query(connection, query, params=None):
    with connection.connect() as conn:
        result = conn.execute(text(query), params or {})
    return result
