import sqlalchemy


def create_db_engine(uri):
    if uri.startswith('postgres'):
        return sqlalchemy.create_engine(uri, client_encoding='utf8')

    return sqlalchemy.create_engine(uri)


def execute_query(connection, query, params=None):
    with connection.connect() as conn:
        result = conn.execute(sqlalchemy.text(query), params or {})
    return result
